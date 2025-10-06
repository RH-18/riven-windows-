"""Updater module"""
from pathlib import PurePath
from typing import Generator, Iterable

from loguru import logger

from program.media.item import MediaItem
from program.services.updaters.emby import EmbyUpdater
from program.services.updaters.jellyfin import JellyfinUpdater
from program.services.updaters.plex import PlexUpdater
from program.settings.manager import settings_manager
from program.utils.platform_paths import (
    as_os_path_string,
    combine_library_path,
    normalize_path,
)


class Updater:
    """
    Main updater service that coordinates multiple media server updaters.

    This service manages multiple updater implementations (Plex, Emby, Jellyfin)
    and triggers media server refreshes for items.
    """

    def __init__(self):
        self.key = "updater"
        self.library_path = settings_manager.settings.updaters.library_path
        self.services = {
            PlexUpdater: PlexUpdater(),
            JellyfinUpdater: JellyfinUpdater(),
            EmbyUpdater: EmbyUpdater(),
        }
        self.initialized = self.validate()

    def validate(self) -> bool:
        """Validate that at least one updater service is initialized."""
        initialized_services = [service for service in self.services.values() if service.initialized]
        return len(initialized_services) > 0

    def run(self, item: MediaItem) -> Generator[MediaItem, None, None]:
        """
        Update media servers for the given item.

        Extracts the filesystem path from the item and triggers a refresh
        in all initialized media servers.

        For movies: refreshes parent directory (e.g., /movies/Movie Name (2020)/)
        For shows: refreshes parent's parent directory (e.g., /shows/Show Name/)

        Args:
            item: MediaItem to update

        Yields:
            MediaItem: The item after processing
        """
        logger.debug(f"Starting update process for {item.log_string}")

        if not self.initialized:
            logger.debug("Updater service is not initialized; skipping refresh")
            yield item
            return

        items = self.get_items_to_update(item)
        last_path = None

        for _item in items:
            filesystem_entry = getattr(_item, "filesystem_entry", None)
            fe_path = getattr(filesystem_entry, "path", None)
            if not fe_path:
                logger.debug(f"Skipping {_item.log_string}: no filesystem entry path present")
                continue

            logger.debug(f"Updating {_item.log_string} at {fe_path}")

            refresh_path = self._derive_refresh_path(fe_path, getattr(_item, "type", ""))
            if refresh_path is None:
                logger.debug(
                    f"Skipping {_item.log_string}: could not derive refresh path from {fe_path}"
                )
                continue

            if last_path is None or refresh_path != last_path:
                refresh_str = as_os_path_string(refresh_path)
                self.refresh_path(refresh_str)
                last_path = refresh_path

            _item.updated = True
            logger.debug(f"Updated {_item.log_string}")

        logger.info(f"Updated {item.log_string}")
        yield item

    def _derive_refresh_path(self, filesystem_path: str, item_type: str) -> PurePath | None:
        """Return the directory that should be refreshed for ``filesystem_path``."""

        if not filesystem_path:
            return None

        try:
            absolute_path = combine_library_path(self.library_path, filesystem_path)
        except Exception as error:  # pragma: no cover - defensive, log for diagnostics
            logger.debug(f"Failed to combine library path for {filesystem_path}: {error}")
            return None

        refresh_path = normalize_path(absolute_path).parent
        if item_type in {"episode", "show"}:
            refresh_path = refresh_path.parent

        return refresh_path

    def refresh_path(self, path: str) -> bool:
        """
        Refresh a specific path in all initialized media servers.

        This triggers each media server to scan/refresh the given path,
        which will add/remove/update items as needed.

        Args:
            path: Absolute path to refresh in the media servers

        Returns:
            bool: True if at least one service refreshed successfully, False otherwise
        """
        success = False
        for service in self.services.values():
            if service.initialized:
                try:
                    if service.refresh_path(path):
                        logger.debug(f"Refreshed path: {path}")
                        success = True
                except Exception as e:
                    logger.error(f"Failed to refresh path {path}: {e}")

        if not success:
            logger.debug(f"No updater service successfully refreshed path {path}")

        return success
    
    def get_items_to_update(self, item: MediaItem) -> list[MediaItem]:
        """Get the list of files to update for the given item."""
        if item.type in ["movie", "episode"]:
            return [item]
        if item.type == "show":
            seasons_candidate = getattr(item, "seasons", []) or []
            try:
                seasons: Iterable = list(seasons_candidate)
            except TypeError:
                seasons = []
            collected = []
            for season in seasons:
                episodes: Iterable = getattr(season, "episodes", []) or []
                for episode in episodes:
                    if getattr(episode, "available_in_vfs", False):
                        collected.append(episode)
            return collected or [item]
        if item.type == "season":
            episodes: Iterable = getattr(item, "episodes", []) or []
            return [
                e for e in episodes
                if getattr(e, "available_in_vfs", False)
            ]
        return []
