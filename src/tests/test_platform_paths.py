"""Tests for cross-platform path helpers."""

from program.utils.platform_paths import (
    as_os_path_string,
    combine_library_path,
    normalize_path,
)


def test_combine_library_path_posix_relative():
    root = "/mnt/library"
    candidate = "movies/Test"
    result = combine_library_path(root, candidate)
    assert result.as_posix() == "/mnt/library/movies/Test"


def test_combine_library_path_posix_leading_slash():
    root = "/mnt/library"
    candidate = "/shows/Test"
    result = combine_library_path(root, candidate)
    assert result.as_posix() == "/mnt/library/shows/Test"


def test_combine_library_path_windows_relative_on_posix():
    root = "/mnt/library"
    candidate = "\\shows\\Test"
    result = combine_library_path(root, candidate)
    assert result.as_posix() == "/mnt/library/shows/Test"


def test_combine_library_path_windows_absolute():
    root = r"C:\Riven\Library"
    candidate = r"C:\Riven\Library\movies"
    result = combine_library_path(root, candidate)
    assert as_os_path_string(result) == candidate


def test_as_os_path_string_windows_conversion():
    path = r"C:\Riven\Library\movies"
    pure = normalize_path(path)
    assert as_os_path_string(pure) == path


def test_as_os_path_string_posix_conversion():
    path = "/mnt/library/shows"
    pure = normalize_path(path)
    assert as_os_path_string(pure) == path
