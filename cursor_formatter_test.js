export function cursorFormatResponse(data) {
    return {
        agent: "cursor",
        formatted: true,
        data: data,
        formattedAt: new Date().toISOString()
    };
}

export function cursorUpperCase(text) {
    if (!text) {
        return "CURSOR_EMPTY";
    }
    return text.toUpperCase();
}
