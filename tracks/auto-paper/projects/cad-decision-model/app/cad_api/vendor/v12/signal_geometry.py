"""Raw-image supported outside signal elbows and short symbol port gaps.

These are proposals for the existing line/endpoint judges, never semantic
connections. A dashed elbow must have a repeated straight dash chain, a
perpendicular arm that continues to other ink or a symbol, and original gray
ink supporting both arms. All paths stay outside erased boxes and equipment.
"""
from __future__ import annotations

import math
import hashlib

import cv2
import numpy as np

import page_cv as CV


def _signal_port_symbol(symbol, text_h):
    """Existing model classes may expose a small signal port, never a verdict."""
    if str(symbol.get('class', '')).startswith('instrument/'):
        return True
    box = symbol.get('bbox')
    confidence = symbol.get('class_confidence')
    return (symbol.get('class') in {'hand_switch', 'controller'} and box is not None
            and max(box[2]-box[0]+1, box[3]-box[1]+1) <= 6*text_h
            and type(confidence) in (int, float) and math.isfinite(confidence)
            and .60 <= confidence <= 1)


def _blocked(shape, symbols, erase, obstacles=None, exclude=()):
    blocked = np.zeros(shape, np.uint8)
    for symbol in symbols:
        x0, y0, x1, y1 = symbol['bbox']
        blocked[max(0, y0-erase):min(shape[0], y1+erase+1),
                max(0, x0-erase):min(shape[1], x1+erase+1)] = 1
    for x0, y0, x1, y1 in exclude:
        blocked[max(0,y0):min(shape[0],y1+1),max(0,x0):min(shape[1],x1+1)]=1
    if obstacles is not None:
        blocked |= (obstacles != 0).astype(np.uint8)
    return blocked


def _path_pixels(path):
    pixels = []
    for a, b in zip(path, path[1:]):
        steps = max(abs(a[0]-b[0]), abs(a[1]-b[1]))
        pixels += [(round(a[0]+(b[0]-a[0])*k/max(1,steps)),
                    round(a[1]+(b[1]-a[1])*k/max(1,steps))) for k in range(steps+1)]
    return list(dict.fromkeys(pixels))


def _raw_support(gray, path, min_share=.40):
    if len(path) < 2:
        return False
    H,W=gray.shape
    # A one-pixel raster displacement is allowed; gray halos next to dark ink
    # do not establish a new direction because straight arm evidence is also
    # required from the already traced wire mask.
    raw=(gray<200).astype(np.uint8)
    for a,b in zip(path,path[1:]):
        pixels=_path_pixels([a,b])
        values=[]
        for x,y in pixels:
            if not 0<=x<W or not 0<=y<H:
                return False
            values.append(bool(raw[max(0,y-1):min(H,y+2),max(0,x-1):min(W,x+2)].any()))
        if len(values)>2 and sum(values)/len(values)<min_share:
            return False
    return True


def _metadata(path, reason, shape, **extra):
    xs,ys=zip(*path)
    return {'path':path,'bbox':[max(0,min(xs)-18),max(0,min(ys)-18),
                               min(shape[1]-1,max(xs)+18),min(shape[0]-1,max(ys)+18)],
            'gap_points':[path[0],path[-1]],'reason':reason,
            'requires_original_ink_check':True, **extra}


def elbow_bridges(gray, mask, symbols=(), erase=2, text_h=9, obstacles=None, exclude=()):
    """Recover short missing right-angle turns between observed dash arms."""
    mask=(np.asarray(mask)!=0).astype(np.uint8)
    blocked=_blocked(mask.shape,symbols,erase,obstacles,exclude)
    n,lab,stats,_=cv2.connectedComponentsWithStats(mask,connectivity=8)
    dash=CV._dash_components(stats,max(10,round(3.3*text_h)),3)
    # Generic dash joining also admits pieces of glyphs. For an elbow's prior
    # evidence use only truly thin, uniform, repeated collinear components.
    strict={label:segment for label,segment in dash.items()
            if min(stats[label][2],stats[label][3])<=2
            and .55*text_h<=max(stats[label][2],stats[label][3])<=2.2*text_h
            and stats[label][4]>=.75*stats[label][2]*stats[label][3]}
    parent=CV._DSU(n)
    for label,a in strict.items():
        for other,b in strict.items():
            if label>=other or a[0]!=b[0]:
                continue
            crossa=(a[2]+a[4])/2 if a[0]=='h' else (a[1]+a[3])/2
            crossb=(b[2]+b[4])/2 if b[0]=='h' else (b[1]+b[3])/2
            aa=(a[1],a[3]) if a[0]=='h' else (a[2],a[4])
            bb=(b[1],b[3]) if b[0]=='h' else (b[2],b[4])
            gap_between=max(bb[0]-aa[1],aa[0]-bb[1])-1
            if abs(crossa-crossb)<=1 and 2<=gap_between<=.8*text_h:
                parent.union(label,other)
    groups={}
    for label in strict:
        groups.setdefault(parent.find(label),[]).append(label)
    repeated_labels=set()
    limits={}
    for labels in groups.values():
        if len(labels)<3:
            continue
        orient=strict[labels[0]][0]
        intervals=sorted((strict[k][1],strict[k][3]) if orient=='h' else (strict[k][2],strict[k][4]) for k in labels)
        lengths=np.array([b-a+1 for a,b in intervals]);gaps=np.array([b[0]-a[1]-1 for a,b in zip(intervals,intervals[1:])])
        core=lengths[1:-1] if len(lengths)>=4 else lengths
        if np.ptp(core)>max(2,.35*np.median(core)) or np.ptp(gaps)>max(2,.4*np.median(gaps)):
            continue
        repeated_labels.update(labels)
        for label in labels:
            limits[label]=(intervals[0][0],intervals[-1][1])
    segments=CV._segments(mask,min_len=max(4,round(.5*text_h))|1)
    arms=[]
    for orientation,x0,y0,x1,y1 in segments:
        cx,cy=(x0+x1)//2,(y0+y1)//2
        label=int(lab[cy,cx])
        if not label:
            continue
        # Every candidate turn has at least one proven repeated dash arm. The
        # other arm can be a junction-dot component or a short terminal dash.
        repeated=label in repeated_labels
        arms.append((orientation,x0,y0,x1,y1,label,repeated))
    gap=max(5,round(1.1*text_h))
    result,seen=[],set()
    for h in [s for s in arms if s[0]=='h']:
        _,hx0,hy0,hx1,hy1,hl,hr=h;hy=(hy0+hy1)//2
        for v in [s for s in arms if s[0]=='v']:
            _,vx0,vy0,vx1,vy1,vl,vr=v;vx=(vx0+vx1)//2
            if hl==vl or not (hr or vr):
                continue
            if hx0<vx<hx1 or vy0<hy<vy1:
                # An existing intersection or a pass-by crossing is not a
                # missing endpoint turn, so do not create a new branch there.
                continue
            hx=min((hx0,hx1),key=lambda x:abs(vx-x))
            vy=min((vy0,vy1),key=lambda y:abs(hy-y))
            if hr and hx not in limits[hl] or vr and vy not in limits[vl]:
                continue
            if (max(abs(vx-hx),abs(hy-vy))>gap
                    or abs(vx-hx)+abs(hy-vy)<1):
                continue
            path=[list(p) for p in dict.fromkeys([(hx,hy),(vx,hy),(vx,vy)])]
            pixels=_path_pixels(path)
            if any(blocked[y,x] for x,y in pixels) or not _raw_support(gray,path,.4):
                continue
            # Unrepeated short arms need original ink continuing toward a real
            # symbol, or a second aligned dash. Font L strokes are insufficient.
            other=h if vr else v
            if not other[6]:
                orient,a0,b0,a1,b1,label,_=other
                if min(stats[label][2],stats[label][3])>2:
                    # A compact junction dot with a dash is useful only when
                    # its straight segment spans outside the dot both ways.
                    if max(stats[label][2],stats[label][3])>2.6*text_h or stats[label][4]>.30*stats[label][2]*stats[label][3]:
                        continue
                continuing=False
                for segment in arms:
                    if segment is other or segment[0]!=orient:
                        continue
                    if orient=='h':
                        aligned=abs((segment[2]+segment[4])/2-(b0+b1)/2)<=1
                        distance=max(0,segment[1]-a1,a0-segment[3])
                    else:
                        aligned=abs((segment[1]+segment[3])/2-(a0+a1)/2)<=1
                        distance=max(0,segment[2]-b1,b0-segment[4])
                    if aligned and distance<=1.8*text_h:
                        continuing=True;break
                if not continuing:
                    for symbol in symbols:
                        x0,y0,x1,y1=symbol['bbox']
                        if orient=='h' and y0+3<=(b0+b1)/2<=y1-3:
                            distance=min(abs(a0-x1),abs(a1-x0))
                            continuing|=distance<=1.8*text_h
                        if orient=='v' and x0+3<=(a0+a1)/2<=x1-3:
                            distance=min(abs(b0-y1),abs(b1-y0))
                            continuing|=distance<=1.8*text_h
                if not continuing:
                    continue
            key=tuple(tuple(p) for p in path)
            if key in seen:
                continue
            seen.add(key)
            result.append(_metadata(path,'raw_supported_dashed_elbow',mask.shape,
                                    dash_arm_labels=[hl,vl],raw_support_threshold=.4,
                                    arm_directions=[[-1 if hx==hx1 else 1,0],
                                                    [0,1 if vy==vy0 else -1]]))
    # A terminal arm may contain only one/two short dashes and be omitted from
    # normal nets. Follow its observed collinear fragments toward the next real
    # ink, adding only regular tiny dash gaps, never across a symbol or crossing.
    seed_labels={label for p in result for label in p['dash_arm_labels']}
    known=set(seed_labels)
    for _ in range(3):
        changed=False
        for first,a in dash.items():
            for second,b in dash.items():
                if first>=second or not ({first,second}&known) or a[0]!=b[0]:
                    continue
                if min(stats[first][2],stats[first][3],stats[second][2],stats[second][3])>2:
                    continue
                if a[0]=='h':
                    if abs((a[2]+a[4])-(b[2]+b[4]))>2:continue
                    left,right=(a,b) if a[1]<b[1] else (b,a)
                    separation=right[1]-left[3]-1
                    path=[[left[3],(left[2]+left[4])//2],[right[1],(right[2]+right[4])//2]]
                else:
                    if abs((a[1]+a[3])-(b[1]+b[3]))>2:continue
                    top,bottom=(a,b) if a[2]<b[2] else (b,a)
                    separation=bottom[2]-top[4]-1
                    path=[[(top[1]+top[3])//2,top[4]],[(bottom[1]+bottom[3])//2,bottom[2]]]
                if not 2<=separation<=.8*text_h or any(blocked[y,x]for x,y in _path_pixels(path)):
                    continue
                key=tuple(tuple(p)for p in path)
                if key not in seen:
                    seen.add(key);changed=True
                    result.append(_metadata(path,'terminal_dashed_arm_gap',mask.shape,
                                            dash_arm_labels=[first,second]))
                known.update((first,second))
        if not changed:break
    # Continue the last tiny terminal dash to a compact junction component or
    # longer solid arm straight ahead. It must carry a real horizontal/vertical
    # stroke; arbitrary glyphs directly ahead do not count as continuation.
    for label in list(known):
        if label not in dash:continue
        orient,x0,y0,x1,y1=dash[label]
        if orient=='h':
            yc=(y0+y1)//2;probes=[((x0,yc),(-1,0)),((x1,yc),(1,0))]
        else:
            xc=(x0+x1)//2;probes=[((xc,y0),(0,-1)),((xc,y1),(0,1))]
        for point,(dx,dy) in probes:
            for step in range(1,round(.8*text_h)+2):
                x,y=point[0]+dx*step,point[1]+dy*step
                if not 0<=x<mask.shape[1] or not 0<=y<mask.shape[0] or blocked[y,x]:break
                hit=int(lab[y,x])
                if not hit:continue
                if hit==label:break
                if hit in dash:break
                xh,yh,wh,hh,area=map(int,stats[hit])
                patch=mask[yh:yh+hh,xh:xh+wh]
                # Compact dot + thin arm, such as the UA signal branch. Its
                # width runs along the dash, with the dot only a few pixels tall.
                along=(patch[max(0,y-yh-1):min(hh,y-yh+2)].any(axis=0).sum() if dx
                       else patch[:,max(0,x-xh-1):min(wh,x-xh+2)].any(axis=1).sum())
                across=hh if dx else wh
                if along<.8*text_h or across>text_h:break
                path=[list(point),[x,y]];key=tuple(tuple(p)for p in path)
                if key not in seen:
                    seen.add(key);result.append(_metadata(path,'terminal_dash_to_junction',mask.shape,
                                                         dash_arm_labels=[label,hit]))
                break
    # An erased circle's right/left port may leave only a short terminal dash.
    # It is a valid endpoint hypothesis only when raw gray ink continues along
    # the central port band to the actual outline, not merely near its corner.
    port_obstacles={}
    for label in list(known):
        if label not in dash:continue
        orient,x0,y0,x1,y1=dash[label]
        for symbol in symbols:
            bx0,by0,bx1,by1=map(int,symbol['bbox'])
            if not _signal_port_symbol(symbol, text_h):
                continue
            if orient=='h':
                y=(y0+y1)//2
                if not by0+.3*(by1-by0)<=y<=by1-.3*(by1-by0):continue
                candidates=[('right',[x0,y],[bx1,y]) if x0>bx1 else ('left',[x1,y],[bx0,y])]
            else:
                x=(x0+x1)//2
                if not bx0+.3*(bx1-bx0)<=x<=bx1-.3*(bx1-bx0):continue
                candidates=[('bottom',[x,y0],[x,by1]) if y0>by1 else ('top',[x,y1],[x,by0])]
            for side,anchor,contact in candidates:
                reach = 1.6*text_h if str(symbol.get('class','')).startswith('instrument/') else 2*text_h
                if math.dist(anchor,contact)>reach or math.dist(anchor,contact)<erase+1:
                    continue
                if not str(symbol.get('class','')).startswith('instrument/'):
                    key=id(symbol)
                    if key not in port_obstacles:
                        port_obstacles[key]=_blocked(mask.shape, [s for s in symbols if s is not symbol],
                                                     0, obstacles, exclude)
                    other=port_obstacles[key]
                    if any(other[y,x] for x,y in _path_pixels([anchor,contact])):
                        continue
                if not _raw_support(gray,[anchor,contact],.65):continue
                result.append(_metadata([anchor,contact],'instrument_terminal_port',mask.shape,
                                        symbol=symbol.get('id'),side=side,body_contact=contact,
                                        dash_arm_labels=[label],requires_endpoint_check=True))
    return result


def apply_bridges(mask, proposals):
    out=(np.asarray(mask)!=0).astype(np.uint8)
    for proposal in proposals:
        cv2.polylines(out,[np.asarray(proposal['path'],np.int32)],False,1,1)
    return out


def augment_nets(nets, labels, proposals, symbols, gray=None):
    """Append hypothesis nets without altering original labels, routes or nets.

    Repainting an elbow turns its terminal dash into an L-shaped component and
    can defeat the original straight-only dash linking. Merge already traced
    net records instead, preserving every original dash/crossing bridge. An
    inferred elbow is represented by its two outside anchors; its raw L path is
    retained in metadata for mandatory original-image judgment.
    """
    import copy
    owner={label:i for i,net in enumerate(nets) for label in net['labels']}
    all_nets=copy.deepcopy(nets)
    # Tiny terminal dashes are real label components even when wire_nets omits
    # them for having no port/extent. Keep them only inside a judged hypothesis.
    needed={int(labels[p[1],p[0]]) for proposal in proposals for p in proposal['gap_points']}
    for label in needed-set(owner)-{0}:
        ys,xs=np.nonzero(labels==label)
        if not len(xs):continue
        owner[label]=len(all_nets)
        all_nets.append({'id':len(all_nets),'bbox':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
                         'labels':[label],'ports':[],'bridges':[],'dashed':True})
    parents=CV._DSU(len(all_nets))
    accepted=[]
    object_index={symbol.get('id'):i for i,symbol in enumerate(symbols)}
    for proposal in proposals:
        a,b=proposal['gap_points']
        la=int(labels[a[1],a[0]]);lb=int(labels[b[1],b[0]])
        if proposal['reason'] in {'inline_equipment_port_flange_gap','instrument_terminal_port'}:
            anchor=proposal['gap_points'][-1] if proposal['reason']=='inline_equipment_port_flange_gap' else proposal['gap_points'][0]
            label=int(labels[anchor[1],anchor[0]])
            if label not in owner or proposal.get('symbol') not in object_index:
                continue
            accepted.append((proposal,owner[label],None))
        elif la in owner and lb in owner and owner[la]!=owner[lb]:
            parents.union(owner[la],owner[lb])
            accepted.append((proposal,owner[la],owner[lb]))
    groups={}
    for proposal,a,b in accepted:
        groups.setdefault(parents.find(a),[]).append((proposal,a,b))
    appended=[]
    for root,items in groups.items():
        indices={i for i in range(len(all_nets)) if parents.find(i)==root}
        source=[all_nets[i] for i in sorted(indices)]
        parts=[net['bbox'] for net in source]
        bbox=[min(p[0]for p in parts),min(p[1]for p in parts),max(p[2]for p in parts),max(p[3]for p in parts)]
        net={'id':len(nets)+len(appended),'bbox':bbox,
             'labels':sorted({label for old in source for label in old['labels']}),
             'ports':copy.deepcopy([p for old in source for p in old['ports']]),
             'bridges':copy.deepcopy([p for old in source for p in old['bridges']]),
             'bridge_paths':[],
             'dashed':any(old.get('dashed')for old in source),'signal_gap_proposals':[]}
        for proposal,a,b in items:
            net['signal_gap_proposals'].append(proposal)
            if b is not None:
                net['bridges'].append(copy.deepcopy(proposal['gap_points']))
                net['bridge_paths'].append({'endpoints':copy.deepcopy(proposal['gap_points']),
                                            'path':copy.deepcopy(proposal['path'])})
            else:
                point=(proposal['gap_points'][-1] if proposal['reason']=='inline_equipment_port_flange_gap'
                       else proposal['gap_points'][0])
                net['ports'].append({'obj':object_index[proposal['symbol']],'side':proposal['side'],
                                     'point':point,'anchor':point,'contact':2,
                                     'inferred_port_gap':proposal})
        # A short branch attached to a dot can end just outside an instrument.
        # Require a compact actual original component and a central-side
        # attachment; this is an endpoint hypothesis, never a class/tag rule.
        for label in net['labels']:
            ys,xs=np.nonzero(labels==label)
            if not len(xs) or max(xs.max()-xs.min()+1,ys.max()-ys.min()+1)>3*CV.SC.text_h:
                continue
            for index,symbol in enumerate(symbols):
                if not str(symbol.get('class','')).startswith('instrument/'):
                    continue
                if any(p['obj']==index for p in net['ports']):continue
                x0,y0,x1,y1=symbol['bbox'];cx=(x0+x1)/2
                near=np.flatnonzero((abs(xs-cx)<=.25*(x1-x0)) & (ys<y0) & (ys>=y0-1.3*CV.SC.text_h))
                if not len(near) or gray is None:continue
                k=near[np.argmax(ys[near])];point=[int(xs[k]),int(ys[k])]
                contact=[point[0],int(y0)]
                if not _raw_support(gray,[point,contact],.65):continue
                net['ports'].append({'obj':index,'side':'top','point':point,'anchor':point,'contact':2,
                                     'inferred_port_gap':{'reason':'compact_signal_branch_endpoint',
                                                          'symbol':symbol.get('id'),'body_contact':contact,
                                                          'requires_original_ink_check':True,
                                                          'raw_contact_path':[point,contact]}})
        net['ports'].sort(key=lambda p:(p['obj'],p['side']))
        appended.append(net)
    return appended


def propose(gray, mask, symbols, erase=2, text_h=9, obstacles=None, exclude=()):
    """Outside gap hypotheses for ``augment_nets`` and raw-image judges."""
    return (elbow_bridges(gray,mask,symbols,erase,text_h,obstacles,exclude)
            + port_gap_proposals(gray,mask,symbols,erase,text_h,obstacles,exclude))


def route_used_gap(gap, path, raw_mask):
    """Review only the supported proposal arms that this route actually uses.

    A vertical route through a dot can use one arm of a proposed L bridge
    without visiting its horizontal arm. Preserve the full proposal as
    evidence, and require a normal raw-image check of the used gap. This
    neither drops a used gap nor changes the route or endpoint judgments.
    """
    import copy
    import connection_geometry as CG
    original = gap.get('path', [])
    if gap.get('reason') != 'raw_supported_dashed_elbow' or len(original) != 3:
        return gap
    def parallel_used(a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]
        length=math.hypot(dx,dy)
        if not length:return False
        for c,d in zip(path or (), (path or ())[1:]):
            vx,vy=d[0]-c[0],d[1]-c[1]
            other=math.hypot(vx,vy)
            if other and abs(dx*vx+dy*vy)/(length*other)>=.94 \
                    and CG.uses_bridge([c,d],[a,b],raw_mask):
                return True
        return False
    used = [i for i, (a,b) in enumerate(zip(original, original[1:])) if parallel_used(a,b)]
    if len(used) != 1:
        return gap
    selected = copy.deepcopy(gap)
    selected['original_proposal_path'] = copy.deepcopy(original)
    selected['route_used_arms'] = used
    selected['path'] = copy.deepcopy(original[used[0]:used[0]+2])
    selected['gap_points'] = [selected['path'][0], selected['path'][-1]]
    selected['arm_directions'] = [None, None]
    return selected


def review_detail(gray, gap, text_h=9, symbols=()):
    """Move close gap markers onto their observed outside arms for raw review.

    No pixels or route topology are changed. Each anchor walks away from the
    proposed gap to an actual black/gray pixel; crops show several full dash
    periods and the unpainted short gap. Port attachment is judged by K6, so its
    K5 detail begins on the outside line and shows the nearby body as context.
    """
    path=[list(p)for p in gap.get('raw_contact_path',gap['path'])]
    if len(path)<2:return None
    H,W=gray.shape
    raw=gray<200
    def walk(point, neighbour, direction=None):
        dx,dy=direction if direction is not None else (point[0]-neighbour[0],point[1]-neighbour[1])
        length=max(abs(dx),abs(dy),1)
        dx,dy=dx/length,dy/length
        candidates=[]
        for step in range(max(4,round(.8*text_h)),round(2.2*text_h)+1):
            x,y=round(point[0]+dx*step),round(point[1]+dy*step)
            if not 0<=x<W or not 0<=y<H:break
            if any(s['bbox'][0]<=x<=s['bbox'][2] and s['bbox'][1]<=y<=s['bbox'][3] for s in symbols):break
            if raw[max(0,y-1):min(H,y+2),max(0,x-1):min(W,x+2)].any():
                candidates.append([x,y])
        return candidates[len(candidates)//2] if candidates else list(point)
    arms=gap.get('arm_directions',[None,None])
    first,last=walk(path[0],path[1],arms[0]),walk(path[-1],path[-2],arms[1])
    if gap.get('reason') in {'instrument_terminal_port','inline_equipment_port_flange_gap'}:
        # Never move one marker into a symbol interior. Both K5 marks remain on
        # the outside arm; K6 uses the finite original body_contact separately.
        contact=gap.get('body_contact',path[-1])
        anchor=path[0]if gap['reason']=='instrument_terminal_port'else path[-1]
        far=walk(anchor,contact)
        first,last=anchor,far
        reviewed=[first,last]
    else:
        reviewed=[first]+path+[last]
    pad=max(18,round(3.5*text_h))
    xs,ys=zip(*reviewed+path)
    return {'path':reviewed,'a':first,'b':last,
            'bbox':[max(0,min(xs)-pad),max(0,min(ys)-pad),min(W-1,max(xs)+pad),min(H-1,max(ys)+pad)],
            'kind':'signal_gap','reason':gap['reason'],'original_gap_path':path,
            'markers_moved_to_observed_arms':True}


def junction_gap_detail(gray, item, gaps, text_h=9, symbols=()):
    """Use the exact raw gap's view for a duplicate junction on the same arms."""
    if item.get('kind')!='junction' or len(item.get('path',[]))!=3:return None
    a,c,b=item['path']
    def aligned(p,q):
        u=[p[0]-c[0],p[1]-c[1]];v=[q[0]-c[0],q[1]-c[1]]
        length=math.hypot(*u)*math.hypot(*v)
        return length and sum(x*y for x,y in zip(u,v))/length>=.94
    for gap in gaps:
        path=gap.get('path',[])
        if gap.get('reason')!='raw_supported_dashed_elbow' or len(path)!=3 \
                or math.dist(c,path[1])>1:continue
        if not ((aligned(a,path[0]) and aligned(b,path[-1]))
                or (aligned(b,path[0]) and aligned(a,path[-1]))):continue
        fresh=review_detail(gray,gap,text_h,symbols)
        old=item['bbox'];box=fresh['bbox']
        fresh['bbox']=[min(old[0],box[0]),min(old[1],box[1]),max(old[2],box[2]),max(old[3],box[3])]
        fresh['original_junction_checkpoint']=item
        fresh['same_original_gap_arms']=True
        fresh['marker_style']='legacy_markers_keep_original_ink'
        return fresh
    return None


def endpoint_contact(gray, box, point, text_h=9):
    """Finite own-box attachment proposal for a new paired K6 examination.

    A point just outside a central port may lie beyond a one-pixel gray raster
    break. Walk to the actual nearby outline, require raw support along that
    short segment, and put the marker one pixel outside the body. This does not
    accept a connection or change the box, route, or existing model response.
    """
    x0,y0,x1,y1=map(int,box);px,py=map(int,point)
    choices=[]
    if x0+.3*(x1-x0)<=px<=x1-.3*(x1-x0):
        choices += [('top',[px,y0])if py<y0 else ('bottom',[px,y1])if py>y1 else None]
    if y0+.3*(y1-y0)<=py<=y1-.3*(y1-y0):
        choices += [('left',[x0,py])if px<x0 else ('right',[x1,py])if px>x1 else None]
    choices=[p for p in choices if p]
    if not choices:return None
    side,contact=min(choices,key=lambda item:math.dist(point,item[1]))
    if not 2<=math.dist(point,contact)<=1.4*text_h:return None
    if not _raw_support(gray,[list(point),contact],.65):return None
    if gray[contact[1],contact[0]]>=200:return None
    dx=(px-contact[0]);dy=(py-contact[1]);length=max(abs(dx),abs(dy),1)
    marker=[round(contact[0]+dx/length),round(contact[1]+dy/length)]
    return {'bbox':list(box),'point':marker,'body_contact':contact,'side':side,
            'original_point':list(point),'raw_contact_path':[contact,list(point)],
            'reason':'finite_central_port_contact_recheck','requires_new_paired_endpoint_check':True}


def contact_markers(gray, detail):
    """Place body and contact brackets only on blank original raster pixels."""
    H,W=gray.shape
    protected=cv2.dilate((gray<255).astype(np.uint8),np.ones((3,3),np.uint8))
    def clear(segments):
        return all(0<=x<W and 0<=y<H and not protected[y,x]
                   for segment in segments for x,y in _path_pixels(segment))
    x0,y0,x1,y1=detail['bbox'];px,py=detail['point']
    body=[]
    for x,y,sx,sy in [(x0,y0,-1,-1),(x1,y0,1,-1),(x0,y1,-1,1),(x1,y1,1,1)]:
        placed=None
        for margin in range(3,10):
            a=[x+sx*margin,y+sy*margin]
            segments=[[a,[a[0]+sx*2,a[1]]],[a,[a[0],a[1]+sy*2]]]
            if clear(segments):
                placed=segments;break
        if placed is not None:body.extend(placed)
    # Larger instrument frames can have a thick lower edge. Keep the centre
    # fixed, but search farther on blank pixels without leaving the context.
    vertical_limit=max(4,min(16,round(.2*min(x1-x0+1,y1-y0+1))+3))
    for dy in range(1,vertical_limit+1):
        for dx in range(3,10):
            point=[]
            for sx in (-1,1):
                for sy in (-1,1):
                    point.append([[px+sx*dx,py+sy*dy],[px+sx*(dx+2),py+sy*dy]])
            if clear(point):return {'body':body,'point':point,'marker_style':'blank_body_and_contact_brackets'}
    return None


def port_gap_proposals(gray, mask, symbols, erase=2, text_h=9, obstacles=None, exclude=()):
    """Short straight blank port gaps ending at observed flange or dash ink.

    A proposal joins an outside wire anchor to a point just outside the target
    body. The actual body remains erased and every original-image endpoint must
    still be judged. No two opposite ports are connected through an equipment.
    """
    mask=(np.asarray(mask)!=0).astype(np.uint8)
    blocked=_blocked(mask.shape,symbols,erase,obstacles,exclude)
    H,W=mask.shape
    gap=max(5,round(1.1*text_h))
    result=[]
    for symbol in symbols:
        box=tuple(symbol['bbox']);x0,y0,x1,y1=box
        # A small closed inline equipment rectangle can have a flange drawn a
        # short distance outside it. Big vessels use their verified silhouette.
        if symbol.get('class')!='equipment' or max(x1-x0,y1-y0)>5*text_h:
            continue
        for side,centre,direction in [('top',((x0+x1)//2,y0-erase-1),(0,-1)),
                                      ('bottom',((x0+x1)//2,y1+erase+1),(0,1)),
                                      ('left',(x0-erase-1,(y0+y1)//2),(-1,0)),
                                      ('right',(x1+erase+1,(y0+y1)//2),(1,0))]:
            ex,ey=centre;dx,dy=direction
            if not 0<=ex<W or not 0<=ey<H or mask[ey,ex]:
                continue
            hit=None
            for step in range(1,gap+1):
                px,py=ex+dx*step,ey+dy*step
                if not 0<=px<W or not 0<=py<H or blocked[py,px]:
                    break
                if mask[py,px]:
                    hit=(px,py);break
            if hit is None:
                continue
            # The first ink must be a perpendicular flange with a continuing
            # shaft away from the symbol; arbitrary nearby glyph ink is rejected.
            px,py=hit
            if dx==0:
                cross=mask[max(0,py-1):min(H,py+2),max(0,px-4):min(W,px+5)].any(axis=0).sum()
                along=sum(mask[py+dy*k,px] for k in range(1,7) if 0<=py+dy*k<H)
            else:
                cross=mask[max(0,py-4):min(H,py+5),max(0,px-1):min(W,px+2)].any(axis=1).sum()
                along=sum(mask[py,px+dx*k] for k in range(1,7) if 0<=px+dx*k<W)
            if cross<5 or along<4:
                continue
            target=(ex-dx*(erase+1),ey-dy*(erase+1))
            raw_path=[list(target),list(hit)]
            # Flange gaps themselves can be white, but both actual endpoints
            # and the shaft must exist in the original image.
            if gray[target[1],target[0]]>=200 or gray[py,px]>=200:
                continue
            path=[list(centre),list(hit)]
            result.append(_metadata(path,'inline_equipment_port_flange_gap',mask.shape,
                                    symbol=symbol.get('id'),side=side,body_contact=list(target),
                                    raw_contact_path=raw_path,requires_endpoint_check=True))
    return result
