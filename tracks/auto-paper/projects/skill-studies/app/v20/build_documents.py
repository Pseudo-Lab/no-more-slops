"""Verify or re-typeset the week-02 document package; no scientific experiments."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

PACKAGE = Path(__file__).resolve().parents[2] / 'outputs/week-02/v20'
ACK = 'This work was created as part of the No-More-Slops group activities at Pseudo Lab.'
STEMS = {'skillmerge': 'SkillMerge', 'second-chance': 'SecondChance', 'probeflow': 'ProbeFlow'}
DOCUMENTS = [f'build/{key}/{stem}{suffix}_v20' for key, stem in STEMS.items()
             for suffix in ['', '_SUPPLEMENT', '_EXPLAINER_KO']]
MAX_PDF_BYTES = 6_000_000


def require(condition, message):
    if not condition:
        raise ValueError(message)


def no_link(path):
    info = path.lstat()
    require(not path.is_symlink() and not getattr(info, 'st_file_attributes', 0) & 0x400,
            'symlink/reparse point refused: ' + str(path))


def file_at(root, relative):
    require(isinstance(relative, str) and relative and '\\' not in relative and ':' not in relative,
            'unsafe asset path')
    parts = relative.split('/')
    require(all(p not in ['', '.', '..'] for p in parts) and not PurePosixPath(relative).is_absolute(),
            'unsafe asset path: ' + relative)
    no_link(root)
    path = root
    for part in parts:
        path = path / part
        no_link(path)
    require(path.resolve().is_relative_to(root.resolve()) and path.is_file(), 'asset is not a regular file')
    return path


def files(root):
    no_link(root)
    result = set()
    for path in root.rglob('*'):
        no_link(path)
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
    return result


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_pdf(path):
    try:
        import fitz
    except ImportError as error:
        raise RuntimeError('PDF checks require an already installed PyMuPDF (fitz). No installation is attempted.') from error
    with fitz.open(path) as document:
        return len(document), '\n'.join(page.get_text() for page in document)


def inspect_pdf(path, expected_pages=None):
    require(0 < path.stat().st_size <= MAX_PDF_BYTES, 'PDF byte limit: ' + str(path))
    pages, text = read_pdf(path)
    require(0 < pages <= 80 and (expected_pages is None or pages == expected_pages),
            'PDF page count mismatch/limit: ' + str(path))
    require(ACK in re.sub(r'\s+', ' ', text), 'Acknowledgement missing: ' + str(path))
    return dict(pages=pages, bytes=path.stat().st_size, sha256=sha(path)), text


def verify(package):
    package = Path(package).absolute()
    manifest = json.loads(file_at(package, 'MANIFEST.json').read_text(encoding='utf-8'))
    require(manifest['schema'] == 'nms_week02_document_package_v1' and manifest['version'] == 'v20-20261019',
            'unsupported manifest')
    inventory = files(package) - {'MANIFEST.json'}
    records = manifest['assets']
    require(len({item['path'] for item in records}) == len(records), 'duplicate manifest path')
    require({item['path'] for item in records} == inventory, 'manifest must match the exact package inventory')
    pdfs = []
    for item in records:
        path = file_at(package, item['path'])
        require(path.stat().st_size == item['bytes'] and sha(path) == item['sha256'], 'changed asset: ' + item['path'])
        if path.suffix.lower() == '.pdf':
            require(type(item.get('pages')) is int, 'PDF pages missing from manifest')
            record, _ = inspect_pdf(path, item['pages'])
            pdfs.append(dict(path=item['path'], **record))
    require({p['path'] for p in pdfs} == {name + '.pdf' for name in DOCUMENTS}, 'expected exactly nine document PDFs')
    return dict(ok=True, assets=len(records), pdfs=pdfs, scope='Document integrity and typesetting only; no scientific experiment reproduced.')


def font_paths():
    paths = [Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts']
    spec = importlib.util.find_spec('matplotlib')
    if spec and spec.submodule_search_locations:
        paths.append(Path(next(iter(spec.submodule_search_locations))) / 'mpl-data/fonts/ttf')
    return [p for p in paths if p.is_dir()]


def rebuild(package, out):
    package = Path(package).absolute()
    out = Path(out)
    require(out.is_absolute(), '--out must be an absolute fresh directory')
    require(not out.exists() and not out.is_symlink(), 'existing output refused')
    require(not out.resolve().is_relative_to(package.resolve()), 'output must be outside the package')
    for parent in out.parents:
        if parent.exists():
            no_link(parent)
    build = package / 'build'
    source_names = sorted(name for name in files(build) if Path(name).suffix.lower() in {'.typ', '.svg'})
    require(source_names, 'no Typst/SVG sources')
    for name in DOCUMENTS:
        file_at(package, name + '.typ')
    executable = shutil.which('typst')
    require(executable, 'an already installed typst executable is required; no installation is attempted')
    fonts = font_paths()
    out.mkdir(parents=True)
    for name in source_names:
        source = file_at(build, name)
        target = out / 'build' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    records = []
    for name in DOCUMENTS:
        source = out / (name + '.typ')
        pdf = out / (name + '.pdf')
        command = [executable, 'compile', '--root', str(out), '--ignore-system-fonts']
        for folder in fonts:
            command.extend(['--font-path', str(folder)])
        command.extend([str(source), str(pdf)])
        result = subprocess.run(command, cwd=source.parent, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
        source.with_suffix('.log').write_text(result.stdout + result.stderr, encoding='utf-8')
        require(result.returncode == 0, 'Typst failed; partial output preserved: ' + str(source.with_suffix('.log')))
        record, text = inspect_pdf(pdf)
        source.with_suffix('.txt').write_text(text, encoding='utf-8')
        records.append(dict(path=name + '.pdf', **record))
    result = dict(ok=True, pdfs=records, font_paths=[str(p) for p in fonts],
                  scope='Fresh document typesetting only; no scientific experiments, new samples or model calls.')
    (out / 'rebuild_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['verify', 'rebuild'])
    parser.add_argument('--package', type=Path, default=PACKAGE)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if args.mode == 'rebuild' and args.out is None:
        parser.error('rebuild requires --out pointing to a fresh absolute directory')
    result = verify(args.package) if args.mode == 'verify' else rebuild(args.package, args.out)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
