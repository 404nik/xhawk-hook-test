#!/bin/bash
# Creates 4 PRs with 7, 8, 9, 10, 11 commits (randomly assigned).
# Usage: ./test-4prs.sh [start_number]
# Example: ./test-4prs.sh 31

set -e

START=${1:-31}
END=$((START + 3))
COMMIT_COUNTS=(7 8 9 10)
TOTAL_COMMITS=0

echo "=== Creating 4 PRs (batches $START-$END) with 7,8,9,10 commits ==="
echo ""

# Ensure we're on main and up to date
git checkout main
git pull origin main

# Phase 1: Create branches with commits
idx=0
for i in $(seq $START $END); do
  BRANCH="feat/test-$i"
  NUM_COMMITS=${COMMIT_COUNTS[$idx]}
  idx=$((idx + 1))

  git checkout main
  git checkout -b "$BRANCH"

  for j in $(seq 1 $NUM_COMMITS); do
    FUNC_NAME="test${i}_fn${j}"
    mkdir -p src/test
    cat > "src/test/${FUNC_NAME}.js" <<EOF
// Test batch $i - Function $j ($(date +%s%N))
function ${FUNC_NAME}(a, b) {
  return a * b + $j;
}

module.exports = { ${FUNC_NAME} };
EOF
    git add "src/test/${FUNC_NAME}.js"
    git commit -m "feat($i): add ${FUNC_NAME}"
  done

  TOTAL_COMMITS=$((TOTAL_COMMITS + NUM_COMMITS))
  echo "Branch $BRANCH: $NUM_COMMITS commits"
done

echo ""
echo "Total commits created: $TOTAL_COMMITS"
echo ""

# Phase 2: Push all branches in parallel
echo "Pushing all 4 branches..."
for i in $(seq $START $END); do
  git push origin "feat/test-$i" &
done
wait
echo "All branches pushed."

# Phase 3: Create PRs
echo ""
echo "Creating 4 PRs..."
for i in $(seq $START $END); do
  gh pr create \
    --repo 404nik/xhawk-hook-test \
    --head "feat/test-$i" \
    --base main \
    --title "Test batch $i: functions" \
    --body "Test PR #$i — $TOTAL_COMMITS total commits across 4 PRs." &
done
wait

echo ""
echo "=== Done! Created 4 PRs (batches $START-$END) with $TOTAL_COMMITS total commits ==="
