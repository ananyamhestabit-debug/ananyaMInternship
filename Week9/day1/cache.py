import json
import os

CACHE_FILE = "cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(data):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_cached_response(query):
    cache = load_cache()
    return cache.get(query.lower())


def set_cached_response(query, response):
    cache = load_cache()
    cache[query.lower()] = response
    save_cache(cache)