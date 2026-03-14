export function claudeQueueTask(taskName) {
    return {
        agent: "claude",
        task: taskName,
        queuedAt: new Date().toISOString()
    };
}

export function claudeQueueSize(items) {
    return Array.isArray(items) ? items.length : 0;
}
