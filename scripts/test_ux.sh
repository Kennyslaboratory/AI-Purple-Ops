#!/bin/bash
# Test user experience flow

set -e

echo "========================================="
echo "AI Purple Ops UX Testing Script"
echo "========================================="
echo ""

echo "1. Testing basic run..."
aipop run --suite normal --adapter mock
echo "✓ Basic run test passed"
echo ""

echo "2. Testing recipe list..."
aipop recipe list
echo "✓ Recipe list test passed"
echo ""

echo "3. Testing recipe run..."
aipop recipe run safety/content_policy_baseline --mock
echo "✓ Recipe run test passed"
echo ""

echo "4. Testing gate..."
aipop gate --summary out/reports/summary.json
echo "✓ Gate test passed"
echo ""

echo "5. Testing quicktest..."
aipop quicktest mock --adapter mock
echo "✓ Quicktest passed"
echo ""

echo "========================================="
echo "All UX tests passed!"
echo "========================================="
