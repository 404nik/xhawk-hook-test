#!/bin/bash
# Creates 5 PRs simultaneously, each with 3-5 random commits.
# Usage: ./batch-prs.sh [start_number]
# Example: ./batch-prs.sh 19  (creates PRs for batches 19-23)

set -e

START=${1:-19}
END=$((START + 4))

echo "Creating batches $START to $END..."

# Ensure we're on main and up to date
git checkout main
git pull origin main

# Phase 1: Create branches with commits
for i in $(seq $START $END); do
  BRANCH="feat/batch-test-$i"
  NUM_COMMITS=$(( (RANDOM % 3) + 3 ))  # 3 to 5

  git checkout main
  git checkout -b "$BRANCH"

  for j in $(seq 1 $NUM_COMMITS); do
    FUNC_NAME="batch${i}_f${j}"
    mkdir -p src
    cat > "src/${FUNC_NAME}.js" <<EOF
// Batch $i - Function $j
function ${FUNC_NAME}(a, b) {
  return a + b + $j;
}
module.exports = { ${FUNC_NAME} };
EOF
    git add "src/${FUNC_NAME}.js"
    git commit -m "feat: add ${FUNC_NAME} utility function"
  done

  echo "Branch $BRANCH: $NUM_COMMITS commits created"
done

# Phase 2: Push all branches in parallel
echo ""
echo "Pushing all branches..."
for i in $(seq $START $END); do
  git push origin "feat/batch-test-$i" &
done
wait
echo "All branches pushed."

# Phase 3: Create PRs
echo ""
echo "Creating PRs..."
for i in $(seq $START $END); do
  gh pr create \
    --repo 404nik/xhawk-hook-test \
    --head "feat/batch-test-$i" \
    --base main \
    --title "Add batch $i utility functions" \
    --body "Batch test PR #$i with utility functions" &
done
wait

echo ""
echo "Done! Created PRs for batches $START to $END."
