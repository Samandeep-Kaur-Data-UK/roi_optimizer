#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"
export MPLCONFIGDIR="${TMPDIR:-/tmp}/roi_optimizer-mpl"
export MPLBACKEND="Agg"
mkdir -p "$MPLCONFIGDIR"

if [ -x ".venv/bin/python" ]; then
  PYTHON_BIN=".venv/bin/python"
elif [ -x "venv/bin/python" ]; then
  PYTHON_BIN="venv/bin/python"
else
  PYTHON_BIN="python3"
fi

echo "==============================================="
echo "ROI Optimizer - Starting MMM pipeline"
echo "==============================================="

echo ""
echo "Using Python interpreter: $PYTHON_BIN"
echo "Matplotlib config directory: $MPLCONFIGDIR"

echo ""
echo "Step 1: Inspecting source data..."
"$PYTHON_BIN" scripts/01_inspect.py
echo "Step 1 complete."

echo ""
echo "Step 2: Running exploratory analysis..."
"$PYTHON_BIN" scripts/01_eda.py
echo "Step 2 complete."

echo ""
echo "Step 3: Applying adstock transformation..."
"$PYTHON_BIN" scripts/03_adstock.py
echo "Step 3 complete."

echo ""
echo "Step 4: Fitting MMM regression..."
"$PYTHON_BIN" scripts/02_mmm_model.py
echo "Step 4 complete."

echo ""
echo "Step 5: Calculating ROI by channel..."
"$PYTHON_BIN" scripts/03_roi_calculator.py
echo "Step 5 complete."

echo ""
echo "Step 6: Optimising a £1,000 budget..."
"$PYTHON_BIN" scripts/04_budget_optimizer.py --budget 1000
echo "Step 6 complete."

echo ""
echo "Step 7: Running scenario analysis..."
"$PYTHON_BIN" scripts/05_scenario_analysis.py
echo "Step 7 complete."

echo ""
echo "==============================================="
echo "MMM pipeline complete. Outputs refreshed."
echo "==============================================="
