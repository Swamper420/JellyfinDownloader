"""Utility functions for JellyfinDownloader."""

import re
from pathlib import Path

def sanitize_filename(s: str) -> str:
    """Remove invalid characters from filename."""
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s.rstrip(" .")

def episode_filename(item: dict, default_ext: str = ".mp4") -> str:
    """Generate filename for episode."""
    series = item.get("SeriesName") or "Unknown Series"
    season = item.get("ParentIndexNumber")
    epnum = item.get("IndexNumber")
    title = item.get("Name") or "Untitled"

    if isinstance(season, int) and isinstance(epnum, int):
        base = f"{series} - S{season:02d}E{epnum:02d} - {title}"
    else:
        base = f"{series} - {title}"

    return sanitize_filename(base) + default_ext

def media_extension(item: dict, default_ext: str) -> str:
    """Determine a reasonable file extension from the media source."""
    ms = item.get("MediaSources") or []
    if ms and isinstance(ms, list) and isinstance(ms[0], dict):
        path = ms[0].get("Path")
        if path:
            suffix = Path(path).suffix
            if suffix:
                return suffix

        container = (ms[0].get("Container") or "").split(",")[0].strip(" .")
        if container:
            return f".{container.lower()}"

    return default_ext

def music_filename(item: dict, default_ext: str = ".mp3") -> str:
    """Generate filename for a music track."""
    artists = item.get("Artists") or []
    artist = item.get("AlbumArtist") or (artists[0] if artists else None) or "Unknown Artist"
    album = item.get("Album") or "Unknown Album"
    track = safe_int(item.get("IndexNumber"))
    title = item.get("Name") or "Untitled"

    if track is not None:
        base = f"{artist} - {album} - {track:02d} - {title}"
    else:
        base = f"{artist} - {album} - {title}"

    return sanitize_filename(base) + media_extension(item, default_ext)

def safe_int(x):
    """Safely convert to int, returning None on failure."""
    try:
        return int(x)
    except Exception:
        return None

def format_episode_label(item):
    """Format episode label for display."""
    s = safe_int(item.get("ParentIndexNumber"))
    e = safe_int(item.get("IndexNumber"))
    name = item.get("Name") or "Untitled"
    if s is not None and e is not None:
        return f"S{s:02d}E{e:02d} - {name}"
    return name

def format_music_label(item):
    """Format music track label for display."""
    artists = item.get("Artists") or []
    artist = item.get("AlbumArtist") or (artists[0] if artists else None) or "Unknown Artist"
    album = item.get("Album") or "Unknown Album"
    track = safe_int(item.get("IndexNumber"))
    name = item.get("Name") or "Untitled"

    prefix = f"{track:02d} - " if track is not None else ""
    return f"{artist} / {album} / {prefix}{name}"
