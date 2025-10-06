"""Utilities for cross-platform path handling."""

from __future__ import annotations

import os
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import Iterable, Sequence, Union

PathLike = Union[str, Path, PurePath]


def default_mount_root() -> Path:
    """Return the default mount directory for the active platform.

    On Windows we place data beneath the user's documents folder to avoid
    requiring elevated privileges. On POSIX platforms we keep the historical
    location under ``~/riven`` to remain backwards compatible.
    """

    if os.name == "nt":
        return Path.home() / "Documents" / "Riven" / "mount"
    return Path.home() / "riven" / "mount"


def default_cache_root() -> Path:
    """Return the default cache directory for the active platform."""

    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "Riven" / "cache"
    return Path("/dev/shm/riven-cache")


def default_library_root() -> Path:
    """Return a sensible default library root path for the OS."""

    if os.name == "nt":
        return Path.home() / "Videos" / "RivenLibrary"
    return Path("/path/to/library/mount")


def normalize_path(path: PathLike) -> PurePath:
    """Normalize any path-like object for reliable comparisons.

    The helper converts to :class:`~pathlib.PurePath` while preserving Windows
    semantics when applicable.
    """

    if isinstance(path, PurePath):
        return path
    if isinstance(path, Path):
        return PurePath(path)
    raw = str(path)
    if os.name == "nt":
        return PureWindowsPath(raw)
    if ":" in raw or "\\" in raw:
        # Handle Windows-style paths even when running on POSIX
        return PureWindowsPath(raw)
    return PurePosixPath(raw)


def combine_library_path(library_root: PathLike, filesystem_path: PathLike) -> PurePath:
    """Return ``filesystem_path`` rooted beneath ``library_root`` when relative.

    The helper understands both POSIX and Windows style semantics. Absolute
    paths are preserved, while relative paths are appended to the provided
    ``library_root`` using the appropriate platform rules.
    """

    root = normalize_path(library_root)
    candidate = normalize_path(filesystem_path)

    if isinstance(candidate, PureWindowsPath):
        if candidate.is_absolute() or candidate.drive or candidate.anchor.startswith("\\\\"):
            return candidate
        parts: Sequence[str] = [part for part in candidate.parts if part not in {"\\", "/"}]
        return root.joinpath(*parts)

    if candidate.is_absolute():
        if path_is_within(candidate, [root]):
            return candidate
        parts = candidate.parts[1:]
        return root.joinpath(*parts)

    return root.joinpath(*candidate.parts)


def as_os_path_string(path: PathLike) -> str:
    """Convert any path-like object into an OS-friendly string representation."""

    pure = normalize_path(path)
    if isinstance(pure, PureWindowsPath):
        return str(pure)
    return pure.as_posix()


def paths_match(left: PathLike, right: PathLike) -> bool:
    """Return True when two filesystem paths refer to the same location.

    On Windows the comparison is case-insensitive to align with NTFS default
    behaviour.
    """

    lp = normalize_path(left)
    rp = normalize_path(right)

    if os.name == "nt":
        return lp.as_posix().casefold() == rp.as_posix().casefold()
    return lp == rp


def path_is_within(path: PathLike, candidates: Iterable[PathLike]) -> bool:
    """Return True if ``path`` resides under any directory in ``candidates``."""

    target = normalize_path(path)
    for candidate in candidates:
        candidate_path = normalize_path(candidate)
        if paths_match(target, candidate_path):
            return True
        try:
            target.relative_to(candidate_path)
            return True
        except ValueError:
            continue
    return False

