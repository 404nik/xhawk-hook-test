export function cursorParseEvent(event) {
    if (!event) {
        return { agent: "cursor", status: "empty_event" };
    }

    return {
        agent: "cursor",
        type: event.type || "unknown",
        payload: event.payload || {},
        parsedAt: new Date().toISOString()
    };
}

export function cursorEventSummary(eventName) {
    return `cursor_event_${eventName}`;
}
