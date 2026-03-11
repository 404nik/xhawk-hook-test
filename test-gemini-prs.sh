#!/bin/bash
# Create 5 PRs with 7-10 commits each for Gemini testing.
# Run this from the xhawk-hook-test repo root.
#
# Usage: ./test-gemini-prs.sh

set -e

AGENT="gemini"
NUM_PRS=5

echo "=== Creating $NUM_PRS PRs for $AGENT testing ==="
echo ""

for i in $(seq 1 $NUM_PRS); do
  # Random commit count between 7-10
  NUM_COMMITS=$(( RANDOM % 4 + 7 ))
  BATCH=$((200 + i))
  BRANCH="feat/${AGENT}-batch-${BATCH}"

  echo "--- PR $i/$NUM_PRS: branch=$BRANCH commits=$NUM_COMMITS ---"

  # Ensure we're on main and up to date
  git checkout main
  git pull origin main

  git checkout -b "$BRANCH"

  for j in $(seq 1 $NUM_COMMITS); do
    FUNC_NAME="${AGENT}_b${BATCH}_fn${j}"
    mkdir -p src/test
    cat > "src/test/${FUNC_NAME}.js" <<EOF
// Agent: $AGENT | PR $i | Batch $BATCH | Function $j ($(date +%s%N))
function ${FUNC_NAME}(x, y) {
  const result = x * y + $j;
  console.log('${FUNC_NAME}:', result);
  return result;
}

module.exports = { ${FUNC_NAME} };
EOF
    git add "src/test/${FUNC_NAME}.js"
    git commit -m "feat($AGENT-$BATCH): add ${FUNC_NAME}"
  done

  echo ""
  echo "Pushing $BRANCH..."
  git push origin "$BRANCH"

  echo "Creating PR..."
  gh pr create \
    --repo 404nik/xhawk-hook-test \
    --head "$BRANCH" \
    --base main \
    --title "[$AGENT] Batch $BATCH: $NUM_COMMITS commits" \
    --body "Gemini test — $NUM_COMMITS commits in batch $BATCH (PR $i of $NUM_PRS)."

  echo "--- PR $i done ---"
  echo ""
done

echo "Running xh backup..."
xh backup --yes

echo ""
echo "=== Done! $NUM_PRS PRs created for $AGENT ==="
echo "Check dashboard: https://app.xhawk.ai/prs"
