#!/usr/bin/env python3
"""Render and verify a silent infographic Reel from an explicit account brief."""
from __future__ import annotations

import argparse
from datetime import date, datetime
from fractions import Fraction
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

import render_carousel as common
import run_carousel as carousel
from render_reel import Renderer, MediaFrames, encode_scene

require = common.require
LAYOUTS = {'media', 'flow', 'steps', 'occlusion', 'cards', 'metric'}


def number(value, label, minimum=0):
    require(type(value) in (int,float) and math.isfinite(value) and value >= minimum,
            f'{label} must be a finite number >= {minimum}.')
    return value


def integer(value, label, minimum=1):
    require(type(value) is int and value >= minimum, f'{label} must be an integer >= {minimum}.')
    return value


def string(value, label, empty=False):
    require(isinstance(value,str) and (empty or bool(value.strip())), f'{label} must be a string{ "" if empty else " with content"}.')
    return value


def timestamp(value):
    parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
    require(parsed.utcoffset() is not None, 'Timestamps need an explicit timezone offset.')
    return parsed


def probe(path, ffprobe):
    result=subprocess.run([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(path)],capture_output=True,text=True)
    require(result.returncode==0, f'Cannot inspect media: {path.name}: {result.stderr[-500:]}')
    return json.loads(result.stdout)


def preflight(manifest, brief_path):
    post=json.loads(manifest.read_text(encoding='utf-8'))
    brief=json.loads(brief_path.read_text(encoding='utf-8'))
    require(isinstance(post,dict) and isinstance(brief,dict),'Manifest and brief must be objects.')
    require(post.get('schema_version')==1,'Use manifest schema_version: 1.')
    require(type(post.get('demo',False)) is bool,'demo must be a boolean.')
    require(post.get('content_type') in ('news','evergreen','promotion'),'Unknown content_type.')
    string(post.get('topic'),'topic')
    date.fromisoformat(string(post.get('edition_date'),'edition_date'))
    string(post.get('caption'),'caption')
    require('brand' not in post and 'account' not in post,'Keep account and brand only in the selected brief, not the episode manifest.')
    account=carousel.object_field(brief,'account')
    brand=carousel.object_field(brief,'brand')
    delivery=carousel.object_field(brief,'deliverable')
    policy=carousel.object_field(brief,'caption_policy')
    carousel.object_field(brief,'punctuation_policy')
    compression=brief.get('recompression_policy',{})
    require(isinstance(compression,dict),'recompression_policy must be an object.')
    for key in ('body_on_light_panel','require_review'):
        if key in compression:
            require(type(compression[key]) is bool,f'recompression_policy.{key} must be boolean.')
    for key in ('min_body_font_at_1080','min_graphic_font_at_1080','min_line_width_at_1080'):
        if key in compression:
            number(compression[key],f'recompression_policy.{key}',1)
    string(account.get('display_name'),'account.display_name')
    for key in ('background','text'):
        require(isinstance(brand.get(key),str) and re.fullmatch(r'#[0-9A-Fa-f]{6}',brand[key]),f'Invalid brand.{key}.')
    string(brief.get('acknowledgement',''),'acknowledgement',True)
    require(delivery.get('type')=='reel','This harness expects deliverable.type: reel.')
    require(delivery.get('audio')=='none','This harness supports audio: none; it does not add narration, music or silent audio tracks.')
    w=integer(delivery.get('width'),'width',180)
    h=integer(delivery.get('height'),'height',320)
    require(w%2==0 and h%2==0 and w*16==h*9,'Use even dimensions with an exact 9:16 aspect ratio.')
    fps=integer(delivery.get('fps'),'fps')
    require(fps<=60,'fps must be <= 60.')
    if 'min_short_side' in delivery:
        minimum=integer(delivery['min_short_side'],'min_short_side')
        require(min(w,h)>=minimum,'Resolution falls below the brief’s min_short_side.')
    duration=number(delivery.get('duration_seconds'),'duration_seconds',.1)
    margins=carousel.object_field(delivery,'safe_area')
    for key in ('left','top','right','bottom'):
        require(number(margins.get(key),f'safe_area.{key}')<1,'Safe-area insets must be fractions below 1.')
    require(margins['left']+margins['right']<=.5 and margins['top']+margins['bottom']<=.5,
            'These layouts need at least half of the canvas width and height inside the safe area.')
    for key in ('max_characters','hashtag_count','max_hashtags'):
        if key in policy:
            integer(policy[key],f'caption_policy.{key}',1 if key=='max_characters' else 0)
    sources=post.get('sources',[])
    require(isinstance(sources,list),'sources must be a list.')
    source_ids=set()
    for source in sources:
        require(isinstance(source,dict),'Each source must be an object.')
        for key in ('id','title','publisher','url','checked_at'):
            string(source.get(key),f'source.{key}')
        require(common.valid_url(source['url']),'Source URL must use http(s).')
        require(source['id'] not in source_ids,'Duplicate source id.')
        source_ids.add(source['id'])
    require(post.get('demo') or post['content_type']!='news' or sources,'A news item requires primary source records.')
    if freshness:=post.get('freshness'):
        require(isinstance(freshness,dict),'freshness must be an object.')
        reference=timestamp(string(freshness.get('reference_time'),'freshness.reference_time'))
        age=number(freshness.get('max_age_hours'),'freshness.max_age_hours',.01)
        recent=[]
        for source in sources:
            if source.get('published_at'):
                hours=(reference-timestamp(source['published_at'])).total_seconds()/3600
                require(hours>=0,'A source publication is later than the selected reference_time.')
                recent.append(hours<=age)
        require(any(recent),'No dated source falls within the requested freshness window.')
    scenes=post.get('scenes')
    require(isinstance(scenes,list) and 1<=len(scenes)<=30,'Use 1–30 scenes.')
    ids=set(); total=0
    min_scene=number(delivery.get('min_scene_seconds',0),'min_scene_seconds')
    for i,scene in enumerate(scenes):
        require(isinstance(scene,dict),'Each scene must be an object.')
        sid=string(scene.get('id'),'scene.id')
        require(sid not in ids,'Duplicate scene id.'); ids.add(sid)
        require(scene.get('layout') in LAYOUTS,f'{sid}: unsupported layout.')
        seconds=number(scene.get('duration'),f'{sid}.duration',max(.001,min_scene))
        frames=seconds*fps
        require(abs(frames-round(frames))<1e-6 and round(frames)>=1,f'{sid}: duration must align to whole frames.')
        scene['_frames'],scene['_start']=round(frames),total/fps
        total+=round(frames)
        for key in ('title','body'):
            scene[key]=common.lines(scene.get(key,[]))
            require(1<=len(scene[key])<=2 and all(v.strip() for v in scene[key]),f'{sid}: use one or two nonempty {key} lines.')
        string(scene.get('credit'),f'{sid}.credit')
        string(scene.get('kicker',''),f'{sid}.kicker',True)
        refs=scene.get('source_ids',[])
        require(isinstance(refs,list) and all(isinstance(ref,str) and ref in source_ids for ref in refs),f'{sid}: invalid source_ids.')
        needs=scene.get('requires_sources',post['content_type']=='news')
        require(type(needs) is bool,'requires_sources must be boolean.')
        require(post.get('demo') or not needs or refs,f'{sid}: connect claims to source_ids.')
        if needs and not post.get('demo'):
            string(scene.get('evidence_note'),f'{sid}.evidence_note')
        visual=scene.get('visual',{})
        require(isinstance(visual,dict),f'{sid}: visual must be an object.')
        layout=scene['layout']
        if layout in ('flow','steps','cards'):
            key='nodes' if layout=='flow' else 'items'
            items=visual.get(key)
            lower,upper=(2,5) if layout=='flow' else ((2,3) if layout=='steps' else (1,3))
            require(isinstance(items,list) and lower<=len(items)<=upper,f'{sid}: {key} needs {lower}–{upper} items.')
            for item in items:
                require(isinstance(item,dict),f'{sid}: each item must be an object.')
                for field in ('symbol','label')+(('detail',) if layout=='cards' else ()):
                    string(item.get(field),f'{sid}.{field}')
            if layout=='flow':
                visual['center']=common.lines(visual.get('center',[]))
                require(1<=len(visual['center'])<=2,f'{sid}: center needs 1–2 lines.')
        elif layout in ('occlusion','metric'):
            fields=('cover_label','memory_label') if layout=='occlusion' else ('value','label','note')
            for field in fields:
                string(visual.get(field),f'{sid}.{field}')
        elif layout=='media':
            media=scene.get('media')
            require(isinstance(media,dict),f'{sid}: media is required.')
            require(media.get('kind') in ('image','video'),f'{sid}: media.kind must be image or video.')
            string(media.get('path'),f'{sid}.media.path')
            require(not common.valid_url(media['path']), 'Supply local media, not a download URL.')
            string(media.get('credit'),f'{sid}.media.credit')
            string(media.get('usage_note'),f'{sid}.media.usage_note')
            path=Path(media['path']).expanduser()
            path=(manifest.parent/path).resolve() if not path.is_absolute() else path.resolve()
            require(path.is_file(),f'{sid}: media file is missing.')
            media['_path']=path
            number(media.get('start',0),f'{sid}.media.start')
            if 'duration' in media:
                number(media['duration'],f'{sid}.media.duration',.001)
            for key in ('source_url','license_url'):
                if key in media:
                    require(common.valid_url(media[key]),f'{sid}: {key} must be an http(s) URL.')
    require(abs(total/fps-duration)<1e-6,'Scene durations must equal the brief’s duration_seconds exactly.')
    caption=common.caption_text(post,{'acknowledgement':brief.get('acknowledgement','')})
    tags=carousel.hashtag_count(caption)
    require('max_characters' not in policy or len(caption)<=policy['max_characters'],f'Final caption has {len(caption)} characters; exceeds max_characters (including credits and newlines).')
    require('hashtag_count' not in policy or tags==policy['hashtag_count'],f'Final caption has {tags} hashtags; does not match hashtag_count.')
    require('max_hashtags' not in policy or tags<=policy['max_hashtags'],'Final caption exceeds max_hashtags.')
    findings=carousel.punctuation_findings({'caption':caption,'slides':[dict(s,rows=[]) for s in scenes]},brief.get('punctuation_policy',{}))
    # Metric and diagram labels are display copy, too; findings never rewrite input.
    if brief.get('punctuation_policy',{}).get('large_display_copy')=='omit_terminal_period':
        def inspect(value,field):
            if isinstance(value,dict):
                for key,item in value.items(): inspect(item,f'{field}.{key}')
            elif isinstance(value,list):
                for j,item in enumerate(value): inspect(item,f'{field}[{j}]')
            elif isinstance(value,str) and value.rstrip().endswith(('.','。','．')):
                findings.append({'field':field,'text':value,'reason':'Review terminal display punctuation; preserve meaningful punctuation.'})
        for scene in scenes: inspect(scene.get('visual',{}),f'{scene["id"]}.visual')
    report={'schema_version':1,'dimensions':[w,h],'aspect_ratio':'9:16','duration_seconds':duration,'fps':fps,'frames':total,
            'caption_characters':len(caption),'character_count_method':'Unicode code points, including final newline','hashtags':tags,
            'punctuation_review':findings,'exports_verified':False,'manual_review':['Review claims, dates and media permissions against the original sources.','Watch the actual MP4 at phone size and inspect scene transitions, reading time and UI overlap.'],
            'safe_area_note':'Insets are task settings, not a universal Instagram UI guarantee.'}
    if compression.get('require_review'):
        report['recompression_review']={'status':'pending','actual_instagram_result_verified':False}
        report['manual_review'].append('Run preview_recompression.py on the final master and inspect both review-only videos at phone size. Record legibility and motion findings separately; exports_verified does not pass this review.')
    return post,brief,caption,report


def inspect_media(post, ffprobe):
    records=[]
    for scene in post['scenes']:
        if scene['layout']!='media': continue
        media=scene['media']
        if media['kind']=='video':
            info=probe(media['_path'],ffprobe)
            video=next((s for s in info['streams'] if s['codec_type']=='video'),None)
            require(video is not None,'Source has no video stream.')
            length=float(video.get('duration',info.get('format',{}).get('duration',0)))
            start=media.get('start',0)
            seconds=media.get('duration',min(scene['duration'],length-start))
            require(start<length and seconds>0 and start+seconds<=length+.02,'Selected source range exceeds its duration.')
            media['_seconds']=seconds
            dimensions=[video['width'],video['height']]
        else:
            with Image.open(media['_path']) as image:
                image.load(); dimensions=list(image.size)
        records.append({'scene':scene['id'],'kind':media['kind'],'source_dimensions':dimensions,'source_detail_limit_retained':True})
    return records


def encoded_frame(movie, at, ffmpeg):
    data=subprocess.check_output([ffmpeg,'-v','error','-ss',str(at),'-i',str(movie),'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    return Image.open(io.BytesIO(data)).convert('RGB')


def verify_movie(movie, delivery, expected_frames, ffmpeg, ffprobe):
    info=probe(movie,ffprobe)
    streams=info['streams']
    require(len(streams)==1 and streams[0]['codec_type']=='video','Expected one video stream and zero audio streams.')
    video=streams[0]
    require((video['width'],video['height'])==(delivery['width'],delivery['height']),'Encoded dimensions differ from the brief.')
    require(Fraction(video['avg_frame_rate'])==delivery['fps'],'Incorrect frame rate.')
    require(int(video['nb_frames'])==expected_frames,'Incorrect encoded frame count.')
    require(abs(float(info['format']['duration'])-delivery['duration_seconds'])<=.001,'Incorrect encoded duration.')
    require(video['codec_name']=='h264' and video['pix_fmt']=='yuv420p','Expected H.264 yuv420p.')
    require(all(video.get(k)=='bt709' for k in ('color_space','color_transfer','color_primaries')),'Missing BT.709 color metadata.')
    subprocess.run([ffmpeg,'-v','error','-i',str(movie),'-f','null','-'],check=True)
    return {'audio_streams':0,'decode_verified':True,'codec':'h264','pixel_format':'yuv420p','color_metadata':'BT.709','file_bytes':movie.stat().st_size}


def source_document(post):
    lines=[f'# {post["topic"]}',f'Edition date: {post["edition_date"]}','## Sources']
    for source in post.get('sources',[]):
        lines.append(f'- [{source["id"]}] {source["publisher"]}: {source["title"]}\n  {source["url"]}\n  Published: {source.get("published_at","undated")} / Checked: {source["checked_at"]}')
    lines.append('## Scene evidence and media')
    for scene in post['scenes']:
        lines.append(f'### {scene["id"]} ({scene["_start"]:g}–{scene["_start"]+scene["duration"]:g}s)\nReferences: {", ".join(scene.get("source_ids",[]))}\n{scene.get("evidence_note","")}')
        if media:=scene.get('media'):
            lines.append(f'Credit: {media["credit"]}\nFile: {Path(media["path"]).name}')
            for key in ('source_url','license','license_url','usage_note','start','duration'):
                if key in media: lines.append(f'{key}: {media[key]}')
    lines.append('## Production limits\nText and geometry are rendered at the requested resolution. Source media retain their original detail limit. Animated diagrams are explanations, not measurements or product interfaces. No source audio is included. UI insets are configurable and require visual review on the target view.')
    return '\n\n'.join(lines)+'\n'


def timecode(seconds):
    ms=round(seconds*1000)
    return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'


def write_previews(stage, post, renderer, movie, ffmpeg):
    frames=[encoded_frame(movie,s['_start']+min(s['duration']*.6,s['duration']-1/renderer.brief['deliverable']['fps']),ffmpeg) for s in post['scenes']]
    frames[0].save(stage/'cover.jpg',quality=95)
    columns=min(3,len(frames)); rows=math.ceil(len(frames)/columns)
    contact=Image.new('RGB',(columns*284,rows*502),(20,20,20))
    safe_contact=contact.copy()
    sl,st,sr,sb=renderer.safe
    for i,frame in enumerate(frames):
        thumbnail=frame.resize((270,480),Image.Resampling.LANCZOS)
        x,y=7+i%columns*284,7+i//columns*502
        contact.paste(thumbnail,(x,y))
        overlay=thumbnail.convert('RGBA')
        shade=Image.new('RGBA',overlay.size)
        draw=ImageDraw.Draw(shade)
        a,b,c,e=[round(v/4) for v in (sl,st,sr,sb)]
        for box in [(0,0,270,b),(0,e,270,480),(0,b,a,e),(c,b,270,e)]:
            draw.rectangle(box,fill=(0,0,0,145))
        draw.rectangle((a,b,c,e),outline=(255,255,255,255),width=1)
        safe_contact.paste(Image.alpha_composite(overlay,shade).convert('RGB'),(x,y))
    contact.save(stage/'preview.jpg',quality=94)
    safe_contact.save(stage/'safe-area-preview.jpg',quality=94)


def run(args):
    manifest,brief_path=args.manifest.resolve(),args.brief.resolve()
    post,brief,caption,report=preflight(manifest,brief_path)
    if args.validate_only:
        return report
    require(args.out is not None,'--out is required for rendering.')
    ffmpeg,ffprobe=shutil.which(args.ffmpeg),shutil.which(args.ffprobe)
    require(ffmpeg and ffprobe,'Install FFmpeg and ffprobe, or specify --ffmpeg and --ffprobe.')
    def visible_strings(value):
        if isinstance(value,str):
            return [value]
        if isinstance(value,dict):
            return [text for item in value.values() for text in visible_strings(item)]
        if isinstance(value,list):
            return [text for item in value for text in visible_strings(item)]
        return []
    font_post={'brand':brief['account'],'slides':[
        {'title':s['title'],'kicker':s.get('kicker',''),'body':s['body']+visible_strings(s.get('visual',{})),
         'image':{'credit':s['credit']},'rows':[]} for s in post['scenes']]}
    fonts=common.find_fonts(args,font_post)
    inputs=[manifest,brief_path,*[p.resolve() for p in fonts.values()]]
    inputs.extend(s['media']['_path'] for s in post['scenes'] if s.get('media'))
    out=args.out.resolve()
    common.output_guard(out,inputs,args.overwrite)
    report['media']=inspect_media(post,ffprobe)
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.reel-',dir=out.parent) as temporary:
        stage=Path(temporary); segments=stage/'segments'; segments.mkdir()
        renderer=Renderer(post,brief,fonts)
        for i,scene in enumerate(post['scenes']):
            media=MediaFrames(scene['media'],renderer.media_size(),brief['deliverable']['fps'],ffmpeg) if scene['layout']=='media' else None
            encode_scene(renderer,i,segments,ffmpeg,media)
            print(f'Rendered scene {i+1}/{len(post["scenes"])}',file=sys.stderr,flush=True)
        # Relative generated names avoid shell and concat-path quoting hazards.
        (stage/'concat.txt').write_text(''.join(f"file 'segments/{i:02d}.mp4'\n" for i in range(len(post['scenes']))))
        movie=stage/'reel.mp4'
        subprocess.run([ffmpeg,'-y','-v','error','-f','concat','-safe','1','-i',str(stage/'concat.txt'),'-map','0:v:0','-an','-c:v','copy',
                        '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1','-map_metadata','-1','-movflags','+faststart',str(movie)],check=True)
        report.update(verify_movie(movie,brief['deliverable'],report['frames'],ffmpeg,ffprobe))
        write_previews(stage,post,renderer,movie,ffmpeg)
        (stage/'caption.txt').write_text(caption,encoding='utf-8',newline='\n')
        (stage/'sources.md').write_text(source_document(post),encoding='utf-8')
        subs=[]
        for i,s in enumerate(post['scenes']):
            subs.append(f'{i+1}\n{timecode(s["_start"])} --> {timecode(s["_start"]+s["duration"])}\n'+ '\n'.join(s['body'])+'\n')
        (stage/'subtitles.srt').write_text('\n'.join(subs),encoding='utf-8')
        (stage/'brand-brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        # Layout bounds are collected across every rendered frame, not just keyframes.
        report.update({'exports_verified':True,'native_text_and_geometry':True,'safe_area_pixels':[round(v*renderer.scale) for v in renderer.safe],
                       'layout_bounds':[{'scene':key[0],'region':key[1],'pixels':[round(v*renderer.scale) for v in box]} for key,box in sorted(renderer.bounds.items())],
                       'motion':'Scene-specific moving signals, occlusion/reveal and transfers; body copy stays fixed for each full scene'})
        (stage/'production-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        require((stage/'caption.txt').read_bytes()==caption.encode('utf-8'),'Caption changed during export.')
        common.output_guard(out,inputs,args.overwrite)
        out.mkdir(parents=True,exist_ok=True)
        for name in ('reel.mp4','cover.jpg','preview.jpg','safe-area-preview.jpg','caption.txt','sources.md','subtitles.srt','brand-brief.json','production-report.json'):
            (stage/name).replace(out/name)
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest',type=Path)
    parser.add_argument('--brief',type=Path,required=True)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--validate-only',action='store_true')
    parser.add_argument('--overwrite',action='store_true')
    parser.add_argument('--font-regular'); parser.add_argument('--font-bold'); parser.add_argument('--font-dir')
    parser.add_argument('--ffmpeg',default='ffmpeg'); parser.add_argument('--ffprobe',default='ffprobe')
    args=parser.parse_args()
    try:
        print(json.dumps(run(args),ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        raise SystemExit(1)


if __name__=='__main__':
    main()
