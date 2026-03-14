export function cursorFeatureOne() {
    return {
        agent: "cursor",
        status: "active",
        test: "hook_detection"
    };
}

export function cursorFeatureTwo(numbers) {
    return numbers.reduce((sum, n) => sum + n, 0);
}
