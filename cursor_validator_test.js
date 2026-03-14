export function cursorValidateInput(input) {
    if (!input) {
        return {
            agent: "cursor",
            valid: false,
            reason: "empty_input"
        };
    }

    return {
        agent: "cursor",
        valid: true,
        value: input,
        validatedAt: new Date().toISOString()
    };
}

export function cursorIsNumber(value) {
    return typeof value === "number";
}
