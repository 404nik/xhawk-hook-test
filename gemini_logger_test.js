export function geminiLogEvent(eventName) {
    return {
        agent: "gemini",
        event: eventName,
        loggedAt: new Date().toISOString()
    };
}

export function geminiLowerCase(text) {
    return text ? text.toLowerCase() : "gemini_empty";
}
