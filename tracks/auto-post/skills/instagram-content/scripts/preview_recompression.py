#!/usr/bin/env python3
"""Create local stress previews; never predict or certify Instagram's transcode."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw

from run_reel import encoded_frame, probe, require, verify_movie

PROFILES = ((1080, 1920, 26), (720, 1280, 30))
FILES = ('review-only-1080p.mp4', 'review-only-720p.mp4',
         'comparison.jpg', 'review-report.json', 'READ-ME.txt')
NOTICE = 'Local stress previews only; not Instagram captures or a reproduction of its encoding algorithm.'


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            result.update(chunk)
    return result.hexdigest()


def inspect_source(path, ffprobe):
    info = probe(path, ffprobe)
    streams = info['streams']
    require(len(streams) == 1 and streams[0]['codec_type'] == 'video',
            'Use a silent master with exactly one video stream and zero audio streams.')
    video = streams[0]
    width, height = video['width'], video['height']
    require(width >= 1080 and width*16 == height*9, 'Use a 9:16 master at least 1080 pixels wide; previews must not upscale it.')
    require(all(video.get(key) == 'bt709' for key in ('color_space','color_transfer','color_primaries')),
            'Use an SDR master explicitly tagged BT.709; normalize untagged/HDR sources separately.')
    require(video.get('sample_aspect_ratio', '1:1') == '1:1', 'Use square pixels.')
    require(not video.get('tags', {}).get('rotate') and not any(item.get('rotation') for item in video.get('side_data_list', [])),
            'Bake rotation into the master before making review previews.')
    fps = Fraction(video['avg_frame_rate'])
    require(fps.denominator == 1 and 1 <= fps <= 60 and Fraction(video['r_frame_rate']) == fps,
            'Use a constant whole-number frame rate from 1 to 60 fps.')
    frames = int(video.get('nb_frames', 0))
    duration = float(info['format']['duration'])
    require(frames > 0 and math.isfinite(duration) and abs(duration-frames/fps) <= .001,
            'Master duration must match its declared whole-frame count.')
    return {'width':width,'height':height,'fps':int(fps),'frames':frames,'duration_seconds':duration}


def make_comparison(paths, times, target, ffmpeg):
    cell_w, cell_h, label_h, heading_h = 360, 640, 30, 46
    sheet = Image.new('RGB', (cell_w*3, heading_h+(cell_h+label_h)*len(times)), 'white')
    draw = ImageDraw.Draw(sheet)
    draw.text((12, 14), 'LOCAL RECOMPRESSION TEST / NOT AN INSTAGRAM CAPTURE', fill='black')
    for row, at in enumerate(times):
        for column, (label, path) in enumerate(paths):
            x, y = column*cell_w, heading_h+row*(cell_h+label_h)
            draw.text((x+10, y+8), f'{label} / {at:g}s', fill='black')
            frame = encoded_frame(path, at, ffmpeg).resize((cell_w, cell_h), Image.Resampling.LANCZOS)
            sheet.paste(frame, (x, y+label_h))
    sheet.save(target, quality=95, subsampling=0)


def run(args):
    source, out = Path(args.video).resolve(), Path(args.out).resolve()
    require(source.is_file(), 'Master video does not exist.')
    require(out != source and not source.is_relative_to(out), 'Keep the master outside the review output directory.')
    require(not out.exists() or out.is_dir(), 'Review output must be a directory.')
    require(not out.exists() or args.overwrite or not any(out.iterdir()), 'Review output is not empty; choose a new directory or use --overwrite.')
    for name in FILES:
        target = out/name
        require(not target.is_symlink() and not target.is_dir(), f'Refusing a symlink/directory output: {name}')
        require(not target.exists() or not target.samefile(source), 'A review output must not alias the master.')
    for executable in (args.ffmpeg, args.ffprobe):
        require(shutil.which(executable) is not None, f'Executable not found: {executable}')
    metadata = inspect_source(source, args.ffprobe)
    latest = (metadata['frames']-1)/metadata['fps']
    times = args.at if args.at is not None else [round(latest*fraction, 4) for fraction in (.1,.5,.9)]
    require(1 <= len(times) <= 12 and all(math.isfinite(t) and 0 <= t <= latest for t in times),
            f'Choose 1–12 finite timestamps from 0 to {latest:g} seconds.')
    original_hash = digest(source)
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.recompression-', dir=out.parent) as temporary:
        stage = Path(temporary)
        previous = source
        variants = []
        for width, height, crf in PROFILES:
            name = f'review-only-{width}p.mp4'
            destination = stage/name
            command = [args.ffmpeg,'-v','error','-y','-i',str(previous),'-map','0:v:0','-an','-sn',
                       '-map_metadata','-1','-vf',f'scale={width}:{height}:flags=lanczos:out_range=tv,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709',
                       '-c:v','libx264','-preset','fast','-crf',str(crf),'-threads','2',
                       '-pix_fmt','yuv420p','-color_range','tv','-colorspace','bt709',
                       '-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(destination)]
            subprocess.run(command, check=True, capture_output=True)
            delivery = {**metadata, 'width':width, 'height':height}
            measured = verify_movie(destination, delivery, metadata['frames'], args.ffmpeg, args.ffprobe)
            variants.append({'file':name, 'input':previous.name, 'dimensions':[width,height],
                             'encoding':{'codec':'libx264','preset':'fast','crf':crf,'pixel_format':'yuv420p','scaler':'lanczos'},
                             'measured':measured})
            previous = destination
        make_comparison([('Master',source),('1080p / CRF 26',stage/FILES[0]),('720p / CRF 30',stage/FILES[1])],
                        times, stage/'comparison.jpg', args.ffmpeg)
        require(digest(source) == original_hash, 'Master changed during review; discard this run and retry with a stable source.')
        report = {'schema_version':1, 'purpose':'local_recompression_stress_review', 'notice':NOTICE,
                  'manual_visual_review':'pending', 'actual_instagram_result_verified':False,
                  'source':{'file':source.name,'sha256':original_hash,**metadata},
                  'source_preserved':True, 'sample_times_seconds':times, 'variants':variants,
                  'review':['Watch both complete previews at phone size; inspect text edges, thin lines, color bleed and UI margins.',
                            'Inspect the primary explanatory graphic throughout every scene and transition for the selected motion policy.',
                            'Record findings separately; a successful encode is not visual approval. Rework failed scenes and repeat.']}
        (stage/'review-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        (stage/'READ-ME.txt').write_text(NOTICE+'\n\nThese are review-only files. Keep the original master as the deliverable.\n'
                                        '720p is recompressed from the 1080p preview. These are chosen stress settings, not platform specifications.\n'
                                        'The contact sheet is sampled and resized; also watch both complete MP4s at phone size.\n'
                                        'Manual visual review remains pending in review-report.json.\n',encoding='utf-8')
        out.mkdir(exist_ok=True)
        for name in FILES:
            (stage/name).replace(out/name)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--at', type=float, nargs='+', help='Sample timestamps in seconds; default 10%%, 50%%, 90%% of the video.')
    parser.add_argument('--ffmpeg', default='ffmpeg')
    parser.add_argument('--ffprobe', default='ffprobe')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        report = run(args)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Recompression preview failed: {error}\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
