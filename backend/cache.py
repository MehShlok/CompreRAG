from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def get_embedding_cache(text: str):
    # This is a placeholder. In a real scenario, you might want to cache the actual embedding vector.
    # Since we can't cache the vector directly in memory across restarts easily without Redis,
    # we'll use this for in-memory caching of frequent queries within the same instance.
    return None

def generate_cache_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()
