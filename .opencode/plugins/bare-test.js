const fs = require("fs")
const LOG = "/Users/nikhilunavekar/Illusion/xhawk/github/opencode-hooks.log"
fs.appendFileSync(LOG, "BARE_TEST_LOADED\n")

exports.BareTest = async () => {
  fs.appendFileSync(LOG, "BARE_TEST_INIT\n")
  return {
    event: async ({ event }) => {
      fs.appendFileSync(LOG, `${new Date().toISOString()} | ${event.type} | ${JSON.stringify(event.properties || {})}\n`)
    },
  }
}
