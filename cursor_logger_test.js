export function cursorLog(message) {
    const logEntry = {
        agent: "cursor",
        message: message,
        createdAt: new Date().toISOString()
    };

    console.log("[CURSOR TEST LOG]", logEntry);
    return logEntry;
}

export function cursorPing() {
    return "cursor_ping_ok";
}
