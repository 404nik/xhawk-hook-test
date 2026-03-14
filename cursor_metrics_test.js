export function cursorMetrics() {
    return {
        agent: "cursor",
        metric: "hook_test",
        value: Math.floor(Math.random() * 100),
        createdAt: new Date().toISOString()
    };
}

export function cursorAdd(a, b) {
    return a + b;
}
