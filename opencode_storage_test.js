export function opencodeStore(key, value) {
    return {
        agent: "opencode",
        key: key,
        value: value,
        storedAt: new Date().toISOString()
    };
}

export function opencodeKeyPrefix(name) {
    return `opencode_${name}`;
}
