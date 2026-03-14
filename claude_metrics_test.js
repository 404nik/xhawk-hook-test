export function claudeMetricsSnapshot(name) {
    return {
        agent: "claude",
        metric: name,
        value: Math.floor(Math.random() * 100),
        capturedAt: new Date().toISOString()
    };
}

export function claudeMetricKey(id) {
    return `claude_metric_${id}`;
}
