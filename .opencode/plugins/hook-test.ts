// OpenCode test plugin — logs ALL events to verify which ones fire.
// Logs to: /tmp/opencode-hooks.log
import type { Plugin } from "@opencode-ai/plugin"
import { appendFileSync } from "fs"

const LOG_FILE = "/tmp/opencode-hooks.log"

function log(eventType: string, data: unknown) {
  const ts = new Date().toISOString()
  const line = `${ts} | ${eventType} | ${JSON.stringify(data)}\n`
  try {
    appendFileSync(LOG_FILE, line)
  } catch {}
}

export const HookTest: Plugin = async ({ directory, worktree }) => {
  log("plugin.loaded", { directory, worktree })

  return {
    event: async ({ event }) => {
      log(event.type, (event as any).properties || {})
    },
  }
}
