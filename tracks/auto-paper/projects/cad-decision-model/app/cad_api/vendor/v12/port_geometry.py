"""Outside-only outlet tee proposals; do not accept without a raw-image Jev check.

A valve outlet branch may end at the valve corner, so body erasure cuts its tee.
Only perpendicular arms on the same valve outlet side may be bridged. Opposite
ports, central actuator stems, and any route through an erased box are excluded.
"""
from __future__ import annotations
import cv2
import numpy as np


def _crossing_diagonals(raw, box):
    """Distinguish a bow-tie valve from a rectangle with one slash.

    Both internal diagonals need drawn ink; bbox edges and an actuator stem
    alone cannot supply this evidence. This intentionally limits recall.
    """
    x0,y0,x1,y1=map(int,box)
    crop=(raw[y0:y1+1,x0:x1+1]!=0).astype(np.uint8)
    h,w=crop.shape
    if min(h,w)<7:
        return False
    support=cv2.dilate(crop,np.ones((3,3),np.uint8))
    xs=np.arange(2,w-2)
    if len(xs)<3:
        return False
    ys=np.rint((h-1)*xs/(w-1)).astype(int)
    return min(support[ys,xs].mean(),support[h-1-ys,xs].mean()) >= .75


def outlet_tee_bridges(mask, symbols, erase=2, text_h=9, raw=None):
    """Return L paths around a valve corner, wholly outside all erased boxes.

    ``mask`` is binary wire ink after symbol erasure. Result paths are inference
    candidates; model views must always use the original image, never inserted ink.
    """
    if raw is None:
        return []  # erased wire ink cannot establish the valve body topology
    mask = (np.asarray(mask) != 0).astype(np.uint8)
    H, W = mask.shape
    arm, gap = max(5, round(text_h * .65)), max(5, round(text_h * 1.2))
    arm += 1 - (arm % 2)  # odd kernels preserve segment endpoints instead of shifting them
    horizontal = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (arm, 1)))
    vertical = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, arm)))
    blocked = np.zeros_like(mask)
    for s in symbols:
        x0, y0, x1, y1 = s['bbox']
        blocked[max(0,y0-erase):min(H,y1+erase+1),max(0,x0-erase):min(W,x1+erase+1)] = 1
    _,labels=cv2.connectedComponents(mask,connectivity=8)
    proposals, seen = [], set()
    for s in symbols:
        if not str(s.get('class','')).startswith('valve/') or not _crossing_diagonals(raw,s['bbox']):
            continue
        x0,y0,x1,y1=map(int,s['bbox'])
        transpose = (y1-y0) > (x1-x0)
        if transpose:
            hm,vm,block,lab=vertical.T,horizontal.T,blocked.T,labels.T
            x0,y0,x1,y1=y0,x0,y1,x1
        else:
            hm,vm,block,lab=horizontal,vertical,blocked,labels
        HH,WW=hm.shape
        for side,edge,sign in [('left',x0,-1),('right',x1,1)]:
            outside=edge+sign*(erase+1)
            xlo,xhi=sorted((outside,outside+sign*(arm-1)))
            if xlo<0 or xhi>=WW:
                continue
            rows=[y for y in range(max(0,y0),min(HH,y1+1)) if hm[y,xlo:xhi+1].all()]
            for y in rows:
                for end in ('top','bottom'):
                    by=y0-erase-1 if end=='top' else y1+erase+1
                    if not 0<=by<HH:
                        continue
                    # Columns remain at the physical outlet edge; the central
                    # actuator attachment is deliberately not a candidate.
                    for x in range(max(0,edge-2),min(WW,edge+3)):
                        yy=range(max(0,by-gap),by+1) if end=='top' else range(by,min(HH,by+gap+1))
                        candidates=[q for q in yy if vm[q,x]]
                        if not candidates:
                            continue
                        b=max(candidates) if end=='top' else min(candidates)
                        if abs(y-b)>gap:
                            continue
                        if not lab[b,x] or not lab[y,outside] or lab[b,x]==lab[y,outside]:
                            continue
                        pts=[[x,b],[outside,b],[outside,y]]
                        bx0,bx1=sorted((x,outside))
                        by0,by1=sorted((b,y))
                        if block[b,bx0:bx1+1].any() or block[by0:by1+1,outside].any():
                            continue
                        if transpose:
                            pts=[[q[1],q[0]] for q in pts]
                        key=(s.get("id"),side,end)
                        if key in seen:
                            continue
                        seen.add(key)
                        xs,ys=zip(*pts)
                        proposals.append({'symbol':s.get('id'),'side':side if not transpose else {'left':'top','right':'bottom'}[side],
                                          'path':pts,'bbox':[max(0,min(xs)-18),max(0,min(ys)-18),min(W-1,max(xs)+18),min(H-1,max(ys)+18)],
                                          'reason':'outside_outlet_tee_gap',
                                          'gap_points':[pts[0],pts[-1]],'requires_original_ink_check':True})
    return proposals


def add_outlet_tees(mask,symbols,erase=2,text_h=9,raw=None):
    """Return (candidate mask, proposals), preserving the original input array."""
    out=(np.asarray(mask)!=0).astype(np.uint8)
    bridges=outlet_tee_bridges(out,symbols,erase,text_h,raw)
    for b in bridges:
        cv2.polylines(out,[np.asarray(b['path'],np.int32)],False,1,1)
    return out,bridges


def outlet_tee_wire_mask(bw, boxes, regions, symbols, erase=2, exclude=(), text_h=9):
    """Return CV's erased wire mask plus candidate outside-corner tee proposals.

    ``symbols`` and ``boxes`` have the same order; boxes are the actual erasure
    geometry. No drawing API is called, and the input is unchanged. The caller
    must attach ``gap_points`` to every new net/relation using inserted pixels
    and require Jev's original-image line/endpoint checks regardless of K3.
    """
    import page_cv as CV
    mask=CV.wire_mask(bw,boxes,regions,erase,exclude)
    objects=[{**s,"bbox":list(b)} for s,b in zip(symbols,boxes)]
    candidate,proposals=add_outlet_tees(mask,objects,erase,text_h,raw=bw)
    allowed=np.zeros_like(mask)
    for x0,y0,x1,y1 in regions:
        allowed[y0:y1+1,x0:x1+1]=1
    for x0,y0,x1,y1 in exclude:
        allowed[y0:y1+1,x0:x1+1]=0
    kept=[]
    for proposal in proposals:
        path=np.zeros_like(mask)
        cv2.polylines(path,[np.asarray(proposal["path"],np.int32)],False,1,1)
        if not (path&(1-allowed)).any():
            kept.append(proposal)
    out=mask.copy()
    for proposal in kept:
        cv2.polylines(out,[np.asarray(proposal["path"],np.int32)],False,1,1)
    return out,kept


def outlet_tee_input(bw, boxes, regions, symbols, erase=2, exclude=(), text_h=9):
    """Return a copy of original ink plus tee candidate ink, and audit metadata.

    Pass this copy to ``CV.wire_nets`` normally; preserve original ``bw`` and page
    for every model view. Subsequent symbol erasure leaves the outside paths.
    """
    candidate,proposals=outlet_tee_wire_mask(bw,boxes,regions,symbols,erase,exclude,text_h)
    out=np.asarray(bw).copy()
    for proposal in proposals:
        cv2.polylines(out,[np.asarray(proposal["path"],np.int32)],False,1,1)
    return out,proposals


def prune_redundant_tees(proposals, labels, nets):
    """Keep hypotheses that join distinct existing CV nets, including dash unions.

    Same raw component is already excluded during proposal generation. CV also
    joins dash/flange/crossing fragments in a DSU, so adding pixels between those
    fragments brings no new relation benefit and can needlessly reroute a header.
    Return ``(needed, redundant)`` without altering inputs; removed entries retain
    their original metadata and add ``prune_reason``.
    """
    owner={int(label):net['id'] for net in nets for label in net['labels']}
    needed, redundant = [], []
    h,w=labels.shape
    for proposal in proposals:
        components=[]
        for x,y in proposal['gap_points']:
            components.append(int(labels[y,x]) if 0<=x<w and 0<=y<h else 0)
        roots=[owner.get(label) for label in components]
        if 0 in components or None in roots:
            redundant.append({**proposal,'prune_reason':'endpoint_not_in_original_net'})
        elif roots[0]==roots[1]:
            redundant.append({**proposal,'prune_reason':'already_same_original_net'})
        else:
            needed.append(proposal)
    return needed,redundant


def apply_outlet_tees(mask, proposals):
    """Copy a CV wire mask and add only retained outside-tee candidate paths."""
    out=(np.asarray(mask)!=0).astype(np.uint8)
    for proposal in proposals:
        cv2.polylines(out,[np.asarray(proposal['path'],np.int32)],False,1,1)
    return out
