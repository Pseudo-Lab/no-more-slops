"""Recompile the supplied reviewed Typst sources into a new directory."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    output = args.out.resolve()
    assert not output.exists(), 'Use a new output directory; existing files are preserved.'
    manifest = json.loads((source / 'PUBLIC_MANIFEST.json').read_text(encoding='utf8'))
    for name, item in manifest['files'].items():
        path = (source / name).resolve()
        assert path.is_relative_to(source) and path.is_file(), name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], name
    typst = shutil.which('typst')
    assert typst, 'An installed Typst executable is required; no dependency is downloaded.'
    spec = importlib.util.spec_from_file_location('existing_document_helper', source / 'source_tools/base_builder.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    output.mkdir(parents=True)
    for name in manifest['files']:
        if Path(name).suffix in ('.typ', '.svg') or name in ('DOCUMENT.json', 'source.DOCUMENT.json'):
            target = output / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
    data = json.loads((output / 'source.DOCUMENT.json').read_text(encoding='utf8'))
    assert (output / 'DOCUMENT.json').read_bytes() == (output / 'source.DOCUMENT.json').read_bytes()
    helper.validate(output, data)
    for kind in ('paper', 'supplement', 'explainer'):
        helper.compile_typst(typst, output / (kind + '.typ'), output / (kind + '.pdf'), output)
    print('Built three PDFs in ' + str(output))


if __name__ == '__main__':
    main()
