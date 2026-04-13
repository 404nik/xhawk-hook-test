export function geminiMetricsEvent(eventName) {
    return {
        agent: "gemini",
        event: eventName,
        metric: "hook_test",
        createdAt: new Date().toISOString()
    };
}

export function geminiAverage(numbers) {
    if (!Array.isArray(numbers) || numbers.length === 0) {
        return 0;
    }
    const sum = numbers.reduce((acc, n) => acc + n, 0);
    return sum / numbers.length;
}
