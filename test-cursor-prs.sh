#!/usr/bin/env bash
# Test script: 5 PRs with 7-10 commits each, for Cursor session attribution testing.
set -euo pipefail

REPO_DIR="/Users/nikhilunavekar/Illusion/xhawk/github/xhawk-hook-test"
cd "$REPO_DIR"

BATCH=300
MAIN_BRANCH="main"

echo "=== Cursor PR Test (batch $BATCH) ==="

# --- PR 1: 8 commits ---
BRANCH="feat/cursor-batch-$((BATCH + 1))"
git checkout "$MAIN_BRANCH"
git checkout -b "$BRANCH"

echo "// Auth module v$((BATCH+1))" > "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): init auth module"

echo "export class AuthService {}" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add AuthService class"

echo "  login(user: string, pass: string) {}" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add login method"

echo "  logout() { this.token = null; }" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add logout method"

echo "  refreshToken() { return fetch('/refresh'); }" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add token refresh"

echo "  validateSession() { return !!this.token; }" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add session validation"

echo "  hashPassword(p: string) { return crypto.hash(p); }" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): add password hashing"

echo "export default new AuthService();" >> "cursor-auth-$((BATCH+1)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+1))): export singleton"

git push origin "$BRANCH"
gh pr create --title "Cursor PR $((BATCH+1)): Auth service" --body "Cursor test batch $BATCH" --base "$MAIN_BRANCH" --head "$BRANCH"
echo "--- PR 1 done (8 commits) ---"

# --- PR 2: 7 commits ---
BRANCH="feat/cursor-batch-$((BATCH + 2))"
git checkout "$MAIN_BRANCH"
git checkout -b "$BRANCH"

echo "// Database module v$((BATCH+2))" > "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): init database module"

echo "export class Database { pool: any; }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add Database class with pool"

echo "  connect(url: string) { this.pool = createPool(url); }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add connect method"

echo "  query(sql: string) { return this.pool.query(sql); }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add query method"

echo "  transaction(fn: Function) { return this.pool.tx(fn); }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add transaction support"

echo "  migrate() { return runMigrations(this.pool); }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add migration runner"

echo "  close() { this.pool.end(); }" >> "cursor-db-$((BATCH+2)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+2))): add close method"

git push origin "$BRANCH"
gh pr create --title "Cursor PR $((BATCH+2)): Database layer" --body "Cursor test batch $BATCH" --base "$MAIN_BRANCH" --head "$BRANCH"
echo "--- PR 2 done (7 commits) ---"

# --- PR 3: 9 commits ---
BRANCH="feat/cursor-batch-$((BATCH + 3))"
git checkout "$MAIN_BRANCH"
git checkout -b "$BRANCH"

echo "// API router v$((BATCH+3))" > "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): init API router"

echo "import express from 'express';" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add express import"

echo "const router = express.Router();" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): create router instance"

echo "router.get('/health', (req, res) => res.json({ok:true}));" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add health endpoint"

echo "router.get('/users', listUsers);" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add list users route"

echo "router.post('/users', createUser);" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add create user route"

echo "router.put('/users/:id', updateUser);" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add update user route"

echo "router.delete('/users/:id', deleteUser);" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): add delete user route"

echo "export default router;" >> "cursor-api-$((BATCH+3)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+3))): export router"

git push origin "$BRANCH"
gh pr create --title "Cursor PR $((BATCH+3)): API router" --body "Cursor test batch $BATCH" --base "$MAIN_BRANCH" --head "$BRANCH"
echo "--- PR 3 done (9 commits) ---"

# --- PR 4: 8 commits ---
BRANCH="feat/cursor-batch-$((BATCH + 4))"
git checkout "$MAIN_BRANCH"
git checkout -b "$BRANCH"

echo "// Cache module v$((BATCH+4))" > "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): init cache module"

echo "import Redis from 'ioredis';" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add redis import"

echo "export class CacheService {" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add CacheService class"

echo "  get(key: string) { return this.redis.get(key); }" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add get method"

echo "  set(key: string, val: string, ttl?: number) {}" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add set method with TTL"

echo "  del(key: string) { return this.redis.del(key); }" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add delete method"

echo "  flush() { return this.redis.flushdb(); }" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): add flush method"

echo "}" >> "cursor-cache-$((BATCH+4)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+4))): close class definition"

git push origin "$BRANCH"
gh pr create --title "Cursor PR $((BATCH+4)): Cache service" --body "Cursor test batch $BATCH" --base "$MAIN_BRANCH" --head "$BRANCH"
echo "--- PR 4 done (8 commits) ---"

# --- PR 5: 10 commits ---
BRANCH="feat/cursor-batch-$((BATCH + 5))"
git checkout "$MAIN_BRANCH"
git checkout -b "$BRANCH"

echo "// Logger module v$((BATCH+5))" > "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): init logger module"

echo "type Level = 'debug'|'info'|'warn'|'error';" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add log level types"

echo "export class Logger {" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add Logger class"

echo "  constructor(private level: Level = 'info') {}" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add constructor with default level"

echo "  debug(msg: string) { if (this.level === 'debug') console.log(msg); }" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add debug method"

echo "  info(msg: string) { console.log('[INFO]', msg); }" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add info method"

echo "  warn(msg: string) { console.warn('[WARN]', msg); }" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add warn method"

echo "  error(msg: string, err?: Error) { console.error('[ERROR]', msg, err); }" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add error method with stack trace"

echo "  child(prefix: string) { return new Logger(this.level); }" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): add child logger factory"

echo "}\nexport default new Logger();" >> "cursor-logger-$((BATCH+5)).ts"
git add . && git commit -m "feat(cursor-$((BATCH+5))): export default instance"

git push origin "$BRANCH"
gh pr create --title "Cursor PR $((BATCH+5)): Logger service" --body "Cursor test batch $BATCH" --base "$MAIN_BRANCH" --head "$BRANCH"
echo "--- PR 5 done (10 commits) ---"

git checkout "$MAIN_BRANCH"
echo ""
echo "=== Done: 5 PRs, 42 commits total ==="
echo "Check dashboard: http://localhost:3002/prs"
