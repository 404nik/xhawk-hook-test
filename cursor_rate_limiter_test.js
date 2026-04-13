export function cursorRateLimit(userId) {
    return {
        agent: "cursor",
        user: userId,
        allowed: true,
        checkedAt: new Date().toISOString()
    };
}

export function cursorLimitKey(id) {
    return `cursor_limit_${id}`;
}
