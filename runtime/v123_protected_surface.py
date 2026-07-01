#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path
import stat


def file_digest(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_digest(root: Path):
    if not root.exists() or root.is_symlink():
        return ()
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        mode = os.lstat(path).st_mode
        if stat.S_ISLNK(mode):
            rows.append((str(relative), "symlink", os.readlink(path)))
        elif stat.S_ISDIR(mode):
            rows.append((str(relative), "dir", stat.S_IMODE(mode)))
        elif stat.S_ISREG(mode):
            rows.append((str(relative), "file", stat.S_IMODE(mode), file_digest(path)))
        else:
            rows.append((str(relative), "other", stat.S_IFMT(mode)))
    return tuple(rows)


def protected_git_snapshot(git_dir: Path) -> dict:
    return {
        "objects": tree_digest(git_dir / "objects"),
        "references": (
            tree_digest(git_dir / "refs"),
            file_digest(git_dir / "HEAD"),
            file_digest(git_dir / "packed-refs"),
        ),
        "reflogs": tree_digest(git_dir / "logs"),
    }
