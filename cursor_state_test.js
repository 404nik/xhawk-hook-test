export function cursorStateSnapshot(state) {
    return {
        agent: "cursor",
        snapshot: state || {},
        capturedAt: new Date().toISOString()
    };
}

export function cursorStateKey(name) {
    return `cursor_state_${name}`;
}
