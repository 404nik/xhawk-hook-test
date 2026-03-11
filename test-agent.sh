#!/bin/bash
# Test commit sync for a specific agent.
# Creates 1 PR with 5 commits, then runs xh backup.
#
# Usage: ./test-agent.sh <agent> [start_number]
#   agent: gemini | cursor | opencode | claude | codex
#
# Examples:
#   ./test-agent.sh gemini 50
#   ./test-agent.sh cursor 55
#   ./test-agent.sh opencode 60

set -e

AGENT=${1:?Usage: ./test-agent.sh <gemini|cursor|opencode|claude|codex> [start_number]}
START=${2:-50}
NUM_COMMITS=5

echo "=== Agent test: $AGENT | PR batch $START | $NUM_COMMITS commits ==="
echo ""

# Ensure we're on main and up to date
git checkout main
git pull origin main

BRANCH="feat/${AGENT}-test-${START}"
git checkout -b "$BRANCH"

for j in $(seq 1 $NUM_COMMITS); do
  FUNC_NAME="${AGENT}_test${START}_fn${j}"
  mkdir -p src/test
  cat > "src/test/${FUNC_NAME}.js" <<EOF
// Agent: $AGENT | Batch $START | Function $j ($(date +%s%N))
function ${FUNC_NAME}(a, b) {
  return a * b + $j;
}

module.exports = { ${FUNC_NAME} };
EOF
  git add "src/test/${FUNC_NAME}.js"
  git commit -m "feat($AGENT-$START): add ${FUNC_NAME}"
done

echo ""
echo "Pushing $BRANCH..."
git push origin "$BRANCH"

echo ""
echo "Creating PR..."
gh pr create \
  --repo 404nik/xhawk-hook-test \
  --head "$BRANCH" \
  --base main \
  --title "[$AGENT] Test batch $START: $NUM_COMMITS commits" \
  --body "Agent test — $AGENT — $NUM_COMMITS commits in batch $START."

echo ""
echo "Running xh backup..."
xh backup --yes

echo ""
echo "=== Done! PR created for $AGENT (batch $START, $NUM_COMMITS commits) ==="
echo "Check dashboard: https://app.xhawk.ai/prs"
