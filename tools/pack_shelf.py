"""
Pack the slide archive ("shelf") into a tarball for GitHub Pages.

The old server listed folders with Apache's autoindex. GitHub Pages has no
such thing, so every folder without its own ``index.html`` gets a generated
listing that looks like Apache's default one.

Usage::

    python tools/pack_shelf.py shelf shelf.tar.gz --exclude git-2022/git-2022.zip
"""

import argparse
import io
import tarfile
import time
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

URL_PREFIX = "/shelf"

PAGE = """\
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of {path}</title>
 </head>
 <body>
<h1>Index of {path}</h1>
  <table>
   <tr><th valign="top">&nbsp;</th><th>Name</th><th>Last modified</th><th>Size</th><th>Description</th></tr>
   <tr><th colspan="5"><hr></th></tr>
{rows}
   <tr><th colspan="5"><hr></th></tr>
</table>
</body></html>
"""

ROW = (
    '<tr><td valign="top">{icon}</td><td><a href="{href}">{name}</a></td>'
    '<td align="right">{mtime}  </td><td align="right">{size}</td>'
    "<td>&nbsp;</td></tr>"
)


def human_size(size: int) -> str:
    """Format a size the way Apache does: 512, 12K, 5.4M."""
    value = float(size)
    for unit in ("", "K", "M", "G"):
        if value < 1024 or unit == "G":
            break
        value /= 1024
    if not unit:
        return str(size)
    return f"{value:.1f}{unit}" if value < 10 else f"{value:.0f}{unit}"


def listing(folder: Path, root: Path, excluded: set[Path]) -> bytes:
    rel = folder.relative_to(root)
    url_path = f"{URL_PREFIX}/{rel.as_posix()}/" if rel.parts else f"{URL_PREFIX}/"
    entries = [
        child
        for child in folder.iterdir()
        if child.relative_to(root) not in excluded
    ]
    entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    rows = [
        ROW.format(
            icon="[PARENTDIR]",
            href="../",
            name="Parent Directory",
            mtime="&nbsp;",
            size="  - ",
        )
    ]
    for child in entries:
        stat = child.stat()
        name = child.name + ("/" if child.is_dir() else "")
        rows.append(
            ROW.format(
                icon="[DIR]" if child.is_dir() else "[&nbsp;&nbsp;&nbsp;]",
                href=quote(name),
                name=escape(name),
                mtime=datetime.fromtimestamp(stat.st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                ),
                size="  - " if child.is_dir() else human_size(stat.st_size),
            )
        )
    return PAGE.format(path=escape(url_path), rows="\n".join(rows)).encode()


def pack(root: Path, out: Path, excluded: set[Path]) -> None:
    def keep(info: tarfile.TarInfo) -> tarfile.TarInfo | None:
        return None if Path(info.name) in excluded else info

    with tarfile.open(out, "w:gz") as tar:
        for path in sorted(root.iterdir()):
            tar.add(path, arcname=path.name, filter=keep)
        for folder in sorted([root, *(p for p in root.rglob("*") if p.is_dir())]):
            rel = folder.relative_to(root)
            if rel in excluded or (folder / "index.html").exists():
                continue
            if any(parent in excluded for parent in rel.parents):
                continue
            data = listing(folder, root, excluded)
            info = tarfile.TarInfo((rel / "index.html").as_posix())
            info.size = len(data)
            info.mtime = int(time.time())
            tar.addfile(info, io.BytesIO(data))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("root", type=Path, help="The local shelf folder")
    parser.add_argument("out", type=Path, help="The tarball to write")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Path relative to the shelf folder to leave out (repeatable)",
    )
    args = parser.parse_args()
    excluded = {Path(p) for p in args.exclude}
    missing = [p for p in excluded if not (args.root / p).exists()]
    if missing:
        parser.error(f"excluded paths do not exist: {missing}")
    pack(args.root, args.out, excluded)


if __name__ == "__main__":
    main()
