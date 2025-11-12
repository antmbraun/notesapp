# cache.py
import hashlib

# In-memory cache dictionary
_summary_cache: dict[str, str] = {}


def _get_cache_key(text: str) -> str:
    """Generate a cache key from text."""
    return hashlib.sha256(text.encode()).hexdigest()


def get_cached_summary(text: str) -> str | None:
    """Retrieve a cached summary if it exists."""
    key = _get_cache_key(text)
    return _summary_cache.get(key)


def cache_summary(text: str, summary: str) -> None:
    """Cache a summary for future use."""
    key = _get_cache_key(text)
    _summary_cache[key] = summary