export function geminiCacheSet(key, value) {
    return {
        agent: "gemini",
        key: key,
        value: value,
        cachedAt: new Date().toISOString()
    };
}

export function geminiCacheGet(key) {
    return `gemini_cache_lookup_${key}`;
}
