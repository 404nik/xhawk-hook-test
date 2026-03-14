export function geminiTransformData(data) {
    if (!data) {
        return {
            agent: "gemini",
            status: "no_data"
        };
    }

    return {
        agent: "gemini",
        transformed: true,
        payload: data,
    };
}
