"""Utilities for parsing series names from episode titles."""
from __future__ import annotations

import re

_SUFFIX_PATTERN = re.compile(r"\s*第[一二三四五六七八九十百千万\d]+季\s*$")
_EPISODE_PATTERN = re.compile(r"\s*[_-]\s*\d+\s*$")
_TRAILING_BRACKET_PATTERN = re.compile(r"[（(][^（）()]*[）)]\s*$")


def parse_series_name(episode_title: str) -> str:
    """Extract base series name from a concrete episode title string."""
    if not episode_title or not episode_title.strip():
        return ""

    name = episode_title.strip()
    name = _EPISODE_PATTERN.sub("", name)
    name = _SUFFIX_PATTERN.sub("", name)
    name = _TRAILING_BRACKET_PATTERN.sub("", name)
    return name.strip()
