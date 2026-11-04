#!/bin/sh
set -eu
python3 - <<'PY'
from pathlib import Path, PurePosixPath
from zipfile import ZipFile
import shutil
out = Path('dist')
if out.exists():
    shutil.rmtree(out)
out.mkdir()
with ZipFile('BHS-Fitchburg-Professional-Website.zip') as archive:
    for entry in archive.infolist():
        parts = PurePosixPath(entry.filename).parts
        if entry.is_dir() or 'public' not in parts:
            continue
        relative = PurePosixPath(*parts[parts.index('public') + 1:])
        if not relative.parts or relative.is_absolute() or '..' in relative.parts:
            raise ValueError('Unsafe archive path')
        target = out.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(entry))
if not (out / 'index.html').is_file():
    raise RuntimeError('Missing homepage')
PY
python3 redesign.py
