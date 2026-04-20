import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# --- Paths ---
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- ROI values from Day 65 model results ---
# return_per_£1: how much £1 of effective spend returns in sales
ROI_PER_CHANNEL = {
    "TV":      1.0559,
    "Digital": 0.9780,
    "Radio":   0.1203,
}

def optimise_budget(total_budget: float, roi_per_channel: dict) -> pd.DataFrame:
    """
    Allocate budget proportionally by ROI weight.
    Channels with negative or very low ROI receive zero allocation.
    Only channels above break-even (return_per_£1 > 1.0) receive budget.
    """
    # Filter to profitable channels only
    profitable = {ch: roi for ch, roi in roi_per_channel.items() if roi > 1.0}

    if not profitable:
        print("Warning: No channels above break-even. Allocating to highest ROI channel only.")
        best = max(roi_per_channel, key=roi_per_channel.get)
        profitable = {best: roi_per_channel[best]}

    # Calculate weights
    total_roi = sum(profitable.values())
    results = []

    for channel, roi in roi_per_channel.items():
        if channel in profitable:
            weight = roi / total_roi
            allocation = round(total_budget * weight, 2)
            expected_sales = round(allocation * roi, 2)
        else:
            weight = 0.0
            allocation = 0.0
            expected_sales = 0.0

        results.append({
            "channel":          channel,
            "return_per_£1":    roi,
            "recommended_spend": allocation,
            "weight_pct":       round(weight * 100, 1),
            "expected_sales":   expected_sales,
        })

    return pd.DataFrame(results).sort_values("recommended_spend", ascending=False)


def save_chart(df: pd.DataFrame, total_budget: float) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        f"Recommended Budget Allocation: £{total_budget:,.0f}",
        fontsize=14, fontweight="bold", y=1.01
    )

    # --- Bar chart: spend allocation ---
    colors = ["#2ECC71" if s > 0 else "#E0E0E0" for s in df["recommended_spend"]]
    axes[0].bar(df["channel"], df["recommended_spend"], color=colors, edgecolor="white")
    axes[0].set_title("Spend Allocation by Channel", fontsize=11)
    axes[0].set_ylabel("Recommended Spend (£)")
    axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    for i, (spend, pct) in enumerate(zip(df["recommended_spend"], df["weight_pct"])):
        if spend > 0:
            axes[0].text(i, spend + 5, f"£{spend:,.0f}\n({pct}%)", ha="center", fontsize=9)

    # --- Bar chart: expected sales return ---
    colors2 = ["#3498DB" if s > 0 else "#E0E0E0" for s in df["expected_sales"]]
    axes[1].bar(df["channel"], df["expected_sales"], color=colors2, edgecolor="white")
    axes[1].set_title("Expected Sales Return by Channel", fontsize=11)
    axes[1].set_ylabel("Expected Sales (£)")
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    for i, sales in enumerate(df["expected_sales"]):
        if sales > 0:
            axes[1].text(i, sales + 5, f"£{sales:,.0f}", ha="center", fontsize=9)

    plt.tight_layout()
    chart_path = OUTPUT_DIR / "budget_allocation.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Chart saved to: {chart_path}")


# --- CLI entry point ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MMM Budget Optimiser")
    parser.add_argument("--budget", type=float, default=1000.0,
                        help="Total budget to allocate in £ (default: 1000)")
    args = parser.parse_args()

    print(f"\nOptimising allocation for budget: £{args.budget:,.2f}")
    print("ROI source: Day 65 OLS regression model\n")

    df = optimise_budget(args.budget, ROI_PER_CHANNEL)

    # --- Print results ---
    print("--- Recommended Budget Allocation ---")
    print(df.to_string(index=False))

    total_expected = df["expected_sales"].sum()
    print(f"\nTotal expected sales return: £{total_expected:,.2f}")
    print(f"Overall return on £{args.budget:,.0f} budget: £{total_expected:,.2f}")

    # --- Save outputs ---
    csv_path = OUTPUT_DIR / "budget_allocation.csv"
    df.to_csv(csv_path, index=False)
    print(f"Allocation table saved to: {csv_path}")

    save_chart(df, args.budget)