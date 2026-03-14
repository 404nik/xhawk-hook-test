function server_claude() {
    return "claude_test";
}

function server_opencode() {
    return "opencode_test";
}

function server_cursor() {
    return "cursor_test";
}

function server_gemini() {
    return "gemini_test";
}

function cursorAnalyticsEvent(eventName) {
    const event = {
        agent: "cursor",
        event: eventName,
        createdAt: new Date().toISOString()
    };
    return event;
}
