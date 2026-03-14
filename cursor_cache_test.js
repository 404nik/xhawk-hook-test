export function cursorCacheSet(key, value) {
    const cacheEntry = {
        key: key,
        value: value,
        agent: "cursor",
        createdAt: new Date().toISOString()
    };
    return cacheEntry;
}

export function cursorCacheGet(key) {
    return `cursor_cache_lookup_${key}`;
}
