// OpenCode test plugin — logs ALL events to verify reliability.
// Logs to: /tmp/opencode-hooks.log
import { appendFileSync } from "fs";

const LOG_FILE = "/tmp/opencode-hooks.log";

function log(eventType, data) {
  const ts = new Date().toISOString();
  const line = `${ts} | ${eventType} | ${JSON.stringify(data)}\n`;
  try {
    appendFileSync(LOG_FILE, line);
  } catch {}
}

// Module-level marker — confirms the file was loaded by Bun
try {
  appendFileSync(LOG_FILE, `${new Date().toISOString()} | PLUGIN_FILE_EVALUATED\n`);
} catch {}

export const OpenCodeHookTest = async ({ project, client, $, directory, worktree }) => {
  log("plugin.loaded", { directory, worktree });

  return {
    // Log ALL events — no filtering, so we can see exactly what fires
    event: async ({ event }) => {
      log(event.type, event.properties || {});
    },
  };
};
