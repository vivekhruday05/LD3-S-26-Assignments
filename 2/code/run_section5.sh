#!/bin/bash
set -e

# Configuration
BASE_DIR=".."
HINDI_DIR="$BASE_DIR/HDTB_pre_release_version-0.05/IntraChunk/CoNLL/utf/news_articles_and_heritage"
DEV_DIR="$HINDI_DIR/Development"
TEST_DIR="$HINDI_DIR/Testing"

# Output files
DEV_TAB="hindi_dev.tab"
TEST_TAB="hindi_test.tab"

echo "======================================================="
echo "Generating .tab files from Hindi Treebank..."
echo "======================================================="

# Convert Development Set
if [ -d "$DEV_DIR" ]; then
    echo "Converting Development Set..."
    python3 convert_hindi_to_tab.py "$DEV_DIR" "$DEV_TAB"
    echo "Done. Created $DEV_TAB"
else
    echo "Error: Development directory not found at $DEV_DIR"
    exit 1
fi

# Convert Test Set
if [ -d "$TEST_DIR" ]; then
    echo "Converting Test Set..."
    python3 convert_hindi_to_tab.py "$TEST_DIR" "$TEST_TAB"
    echo "Done. Created $TEST_TAB"
else
    echo "Error: Test directory not found at $TEST_DIR"
    exit 1
fi

echo ""
echo "======================================================="
echo "Running Evaluation (Section 5)"
echo "======================================================="

echo ""
echo "--- ARC-EAGER Evaluation ---"
echo "Development Set:"
python3 evaluate.py "$DEV_TAB" --system arc-eager
echo ""
echo "Test Set:"
python3 evaluate.py "$TEST_TAB" --system arc-eager

echo ""
echo "--- ARC-STANDARD Evaluation ---"
echo "Development Set:"
python3 evaluate.py "$DEV_TAB" --system arc-standard
echo ""
echo "Test Set:"
python3 evaluate.py "$TEST_TAB" --system arc-standard

echo ""
echo "======================================================="
echo "Evaluation Complete."
echo "======================================================="
