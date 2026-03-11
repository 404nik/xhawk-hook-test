#!/bin/bash
# Creates 7 PRs simultaneously, each with 7-10 random commits.
# Usage: ./heavy-batch-prs.sh [start_number]
# Example: ./heavy-batch-prs.sh 24  (creates PRs for batches 24-30)

set -e

START=${1:-24}
END=$((START + 6))
TOTAL_COMMITS=0

echo "=== Heavy batch: creating PRs for batches $START to $END (7 PRs, 7-10 commits each) ==="
echo ""

# Ensure we're on main and up to date
git checkout main
git pull origin main

# Phase 1: Create branches with commits
for i in $(seq $START $END); do
  BRANCH="feat/heavy-$i"
  NUM_COMMITS=$(( (RANDOM % 4) + 7 ))  # 7 to 10

  git checkout main
  git checkout -b "$BRANCH"

  for j in $(seq 1 $NUM_COMMITS); do
    FUNC_NAME="heavy${i}_fn${j}"
    mkdir -p src/heavy
    cat > "src/heavy/${FUNC_NAME}.js" <<EOF
// Heavy batch $i - Function $j ($(date +%s%N))
function ${FUNC_NAME}(x, y) {
  const result = x * y + $j;
  return result > 0 ? result : -result;
}

function ${FUNC_NAME}_validate(input) {
  if (typeof input !== 'number') throw new Error('Expected number');
  return ${FUNC_NAME}(input, $j);
}

module.exports = { ${FUNC_NAME}, ${FUNC_NAME}_validate };
EOF
    git add "src/heavy/${FUNC_NAME}.js"
    git commit -m "feat($i): add ${FUNC_NAME} with validation"
  done

  TOTAL_COMMITS=$((TOTAL_COMMITS + NUM_COMMITS))
  echo "Branch $BRANCH: $NUM_COMMITS commits"
done

echo ""
echo "Total commits created: $TOTAL_COMMITS"
echo ""

# Phase 2: Push all branches in parallel
echo "Pushing all 7 branches..."
for i in $(seq $START $END); do
  git push origin "feat/heavy-$i" &
done
wait
echo "All branches pushed."

# Phase 3: Create PRs
echo ""
echo "Creating 7 PRs..."
for i in $(seq $START $END); do
  gh pr create \
    --repo 404nik/xhawk-hook-test \
    --head "feat/heavy-$i" \
    --base main \
    --title "Heavy batch $i: utility functions with validation" \
    --body "Heavy test PR #$i — stress test with 7-10 commits each.

Total commits in this batch run: ~$TOTAL_COMMITS across 7 PRs." &
done
wait

echo ""
echo "=== Done! Created 7 PRs (batches $START-$END) with ~$TOTAL_COMMITS total commits ==="
