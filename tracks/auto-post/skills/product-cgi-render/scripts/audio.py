#!/usr/bin/env python3
"""효과음 믹스: 설정의 "audio.sfx" 목록을 정해진 시각에 얹고, 음량을 맞춘다 (ffmpeg만 쓴다).

사용법:
  python3 audio.py --config project.json [--out audio/mix.wav] [--mux video.mp4 --mux-out final.mp4]
                   [--allow-unlicensed] [--report]

설정 예 ("audio"):
  {"duration": 19.0,            # 없으면 컷 길이 합계
   "normalize": "loudness",     # loudness(2패스 loudnorm) | peak | none
   "lufs": -14, "true_peak": -1.5,
   "loop_tail": true,           # 끝을 넘는 꼬리를 0초에 겹쳐 반복 재생 이음매에서 소리가 끊기지 않게
   "sfx": [{"file": "sfx/tap.wav", "at": 1.0, "gain_db": -3, "trim": [0.14, 0.42],
            "fade_in": 0.002, "fade_out": 0.015, "license": "CC0", "source": "https://…"}]}
권리: 각 효과음의 "license"는 CC0 또는 own(직접 녹음·합성)이어야 한다. 아니면 멈춘다 (--allow-unlicensed는 내부 시험용).
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cgi_config import Config  # noqa: E402

OK_LICENSES = {"cc0", "own", "public-domain"}
SR = 48000


def run(cmd, capture=False):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"실패: {' '.join(cmd[:8])} …\n{r.stderr[-1500:]}")
    return r.stderr if capture else None


def probe_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def build_mix(cfg, acfg, out_raw, allow_unlicensed=False):
    """정규화 전 믹스를 만든다. 돌려줌: (길이, 효과음 행 목록)."""
    dur = float(acfg.get("duration") or sum(float(c["duration"]) for c in cfg.cuts))
    sfx = acfg.get("sfx", [])
    rows, ins, chains = [], [], []
    tail_end = dur
    for i, s in enumerate(sfx):
        lic = str(s.get("license", "")).lower()
        if lic not in OK_LICENSES and not allow_unlicensed:
            raise SystemExit(f"효과음 {s.get('file')}: license '{s.get('license')}'. CC0 또는 own만 쓴다 (출처를 sources.md에)")
        path = cfg.resolve(s["file"])
        if not os.path.exists(path):
            raise SystemExit(f"효과음 파일이 없다: {path}")
        trim = s.get("trim") or [0]
        a, b = trim[0], (trim[1] if len(trim) > 1 else None)
        length = (b if b is not None else probe_duration(path)) - (a or 0)
        at = float(s["at"])
        tail_end = max(tail_end, at + length)
        f = [f"atrim=start={a or 0}" + (f":end={b}" if b is not None else ""), "asetpts=PTS-STARTPTS",
             f"aresample={SR}", "aformat=sample_fmts=fltp:channel_layouts=stereo"]
        if s.get("fade_in"):
            f.append(f"afade=t=in:d={s['fade_in']}")
        if s.get("fade_out"):
            f.append(f"afade=t=out:st={max(0.0, length - s['fade_out']):.4f}:d={s['fade_out']}")
        f.append(f"volume={float(s.get('gain_db', 0))}dB")
        ms = int(round(at * 1000))
        f.append(f"adelay={ms}|{ms}")
        ins += ["-i", path]
        chains.append(f"[{i + 1}:a]{','.join(f)}[s{i}]")
        rows.append({"file": s["file"], "at": at, "length": round(length, 3), "gain_db": s.get("gain_db", 0), "license": s.get("license")})
    long_len = max(tail_end, dur) + 0.05
    base = ["-f", "lavfi", "-t", f"{long_len:.3f}", "-i", f"anullsrc=r={SR}:cl=stereo"]
    labels = "".join(f"[s{i}]" for i in range(len(sfx)))
    fc = ";".join(chains + [f"[0:a]{labels}amix=inputs={len(sfx) + 1}:duration=first:normalize=0[long]"])
    if acfg.get("loop_tail", False) and tail_end > dur:
        # 끝을 넘는 꼬리 → 0초에 겹친다 (반복 재생 때 다음 바퀴 시작에서 이어 울림)
        fc += (f";[long]asplit=2[l1][l2];[l1]atrim=0:{dur:.4f}[main];[l2]atrim=start={dur:.4f},asetpts=PTS-STARTPTS[tail]"
               f";[main][tail]amix=inputs=2:duration=first:normalize=0[mix]")
    else:
        fc += f";[long]atrim=0:{dur:.4f}[mix]"
    run(["ffmpeg", "-y", "-v", "error", *base, *ins, "-filter_complex", fc, "-map", "[mix]", "-c:a", "pcm_s24le", "-ar", str(SR), out_raw])
    return dur, rows


def loudness(path):
    """통합 음량(LUFS)과 트루 피크(dBTP)를 잰다."""
    err = run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture=True)
    i = re.findall(r"I:\s+(-?[\d.]+|-inf) LUFS", err)
    tp = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", err)
    return (float(i[-1]) if i and i[-1] != "-inf" else float("-inf")), (float(tp[-1]) if tp and tp[-1] != "-inf" else float("-inf"))


def normalize(src, out, mode, lufs, tp):
    if mode == "none":
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-c:a", "pcm_s16le", out])
        return
    if mode == "peak":
        _, peak = loudness(src)
        gain = (tp - peak) if peak != float("-inf") else 0.0
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"volume={gain:.2f}dB", "-c:a", "pcm_s16le", out])
        return
    # 2패스 loudnorm: 1패스로 재고 2패스에서 선형 보정
    err = run(["ffmpeg", "-nostats", "-i", src, "-af", f"loudnorm=I={lufs}:TP={tp}:LRA=11:print_format=json", "-f", "null", "-"], capture=True)
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    if m["input_i"] in ("-inf", "inf"):
        raise SystemExit("믹스가 무음이다")
    af = (f"loudnorm=I={lufs}:TP={tp}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample={SR}")
    run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", af, "-c:a", "pcm_s16le", "-ar", str(SR), out])


def main(argv=None):
    p = argparse.ArgumentParser(description="CC0 효과음을 시각에 맞춰 믹스하고 음량을 맞춘다")
    p.add_argument("--config", required=True)
    p.add_argument("--out")
    p.add_argument("--mux", help="이 영상에 믹스를 입힌다")
    p.add_argument("--mux-out")
    p.add_argument("--allow-unlicensed", action="store_true")
    args = p.parse_args(argv)
    cfg = Config(args.config)
    acfg = cfg.data.get("audio", {})
    out = cfg.resolve(args.out or acfg.get("out", "audio/mix.wav"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    raw = os.path.splitext(out)[0] + ".raw.wav"
    dur, rows = build_mix(cfg, acfg, raw, args.allow_unlicensed)
    mode = acfg.get("normalize", "loudness")
    lufs, tp = float(acfg.get("lufs", -14)), float(acfg.get("true_peak", -1.5))
    normalize(raw, out, mode, lufs, tp)
    os.unlink(raw)
    i, peak = loudness(out)
    print("| 효과음 | 시각(초) | 길이 | 게인 dB | 라이선스 |\n|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['file']} | {r['at']:.3f} | {r['length']:.3f} | {r['gain_db']} | {r['license']} |")
    print(f"믹스 {dur:.2f}초, 정규화 {mode}: 통합 {i:.1f} LUFS (목표 {lufs:g}), 트루 피크 {peak:.1f} dBTP (상한 {tp:g}) → {out}")
    if args.mux:
        mo = cfg.resolve(args.mux_out or os.path.splitext(cfg.resolve(args.mux))[0] + "-sfx.mp4")
        run(["ffmpeg", "-y", "-v", "error", "-i", cfg.resolve(args.mux), "-i", out, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest", "-movflags", "+faststart", mo])
        print(f"→ {mo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
