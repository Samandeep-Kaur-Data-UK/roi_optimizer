import os
from pathlib import Path
import tempfile

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "roi-optimizer-demo-mpl"))
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter
import pandas as pd


BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data" / "powerbi"
OUT = BASE / "outputs" / "day67_powerbi_demo_dashboard.png"


COLORS = {
    "page_bg": "#F5F7FB",
    "panel_bg": "#FFFFFF",
    "panel_edge": "#D6DEE8",
    "text": "#1F2937",
    "muted": "#6B7280",
    "sales": "#1E3A5F",
    "tv": "#2563EB",
    "digital": "#0F766E",
    "radio": "#F59E0B",
    "promo": "#DC2626",
    "good": "#16A34A",
    "neutral": "#94A3B8",
}


def money_millions(value, _):
    return f"£{value/1_000_000:.1f}M"


def money_thousands(value, _):
    return f"£{value/1_000:.0f}K"


def style_panel(ax, title):
    ax.set_facecolor(COLORS["panel_bg"])
    for spine in ax.spines.values():
        spine.set_edgecolor(COLORS["panel_edge"])
        spine.set_linewidth(1.1)
    ax.grid(axis="y", color="#E8EDF3", linewidth=0.8)
    ax.tick_params(colors=COLORS["muted"], labelsize=9)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=COLORS["text"], pad=12)


def add_card(fig, rect, title, value, accent):
    ax = fig.add_axes(rect)
    ax.set_axis_off()
    ax.add_patch(
        FancyBboxPatch(
            (0, 0),
            1,
            1,
            boxstyle="round,pad=0.012,rounding_size=0.03",
            facecolor=COLORS["panel_bg"],
            edgecolor=COLORS["panel_edge"],
            linewidth=1.2,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (0.02, 0.88),
            0.96,
            0.08,
            boxstyle="round,pad=0,rounding_size=0.02",
            facecolor=accent,
            edgecolor=accent,
            linewidth=0,
        )
    )
    ax.text(0.08, 0.57, value, fontsize=22, fontweight="bold", color=COLORS["text"], va="center")
    ax.text(0.08, 0.28, title, fontsize=11, color=COLORS["muted"], va="center")


def main():
    marketing = pd.read_csv(DATA / "marketing_data_powerbi.csv", parse_dates=["week"])
    roi = pd.read_csv(DATA / "roi_by_channel_powerbi.csv")
    budget = pd.read_csv(DATA / "budget_allocation_powerbi.csv")

    monthly = (
        marketing.assign(year_month=marketing["week"].dt.to_period("M").dt.to_timestamp())
        .groupby("year_month", as_index=False)[["tv_spend", "digital_spend", "radio_spend"]]
        .sum()
    )

    total_sales = marketing["sales"].sum()
    total_spend = marketing[["tv_spend", "digital_spend", "radio_spend"]].sum().sum()
    promo_weeks = int(marketing["promo_flag"].sum())
    roas = total_sales / total_spend

    plt.rcParams["font.family"] = "DejaVu Sans"
    fig = plt.figure(figsize=(18, 10), facecolor=COLORS["page_bg"])

    fig.text(0.05, 0.955, "Marketing Mix Model Dashboard Demo", fontsize=24, fontweight="bold", color=COLORS["text"])
    fig.text(
        0.05,
        0.925,
        "Day 67 reference layout: KPI cards + sales trend + channel spend + ROI + budget allocation",
        fontsize=11,
        color=COLORS["muted"],
    )

    card_y = 0.79
    card_w = 0.2
    card_h = 0.11
    gap = 0.02
    add_card(fig, [0.05, card_y, card_w, card_h], "Total Sales", f"£{total_sales/1_000_000:.2f}M", COLORS["sales"])
    add_card(fig, [0.05 + (card_w + gap), card_y, card_w, card_h], "Total Spend", f"£{total_spend/1_000_000:.2f}M", COLORS["tv"])
    add_card(fig, [0.05 + 2 * (card_w + gap), card_y, card_w, card_h], "Promo Weeks", f"{promo_weeks}", COLORS["radio"])
    add_card(fig, [0.05 + 3 * (card_w + gap), card_y, card_w, card_h], "ROAS", f"{roas:.2f}", COLORS["good"])

    ax1 = fig.add_axes([0.05, 0.42, 0.43, 0.28])
    style_panel(ax1, "1. Weekly Sales Trend")
    ax1.plot(marketing["week"], marketing["sales"], color=COLORS["sales"], linewidth=2.4, label="Sales")
    promo = marketing[marketing["promo_flag"] == 1]
    ax1.scatter(promo["week"], promo["sales"], color=COLORS["promo"], s=36, zorder=3, label="Promo week")
    ax1.set_ylabel("Sales", color=COLORS["muted"])
    ax1.yaxis.set_major_formatter(FuncFormatter(money_thousands))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax1.legend(frameon=False, loc="upper left")
    ax1.text(
        0.01,
        -0.2,
        "Axis: X = Date[Date], Y = Total Sales. Red markers = promo weeks.",
        transform=ax1.transAxes,
        fontsize=9,
        color=COLORS["muted"],
    )

    ax2 = fig.add_axes([0.52, 0.42, 0.43, 0.28])
    style_panel(ax2, "2. Monthly Spend by Channel")
    x = range(len(monthly))
    width = 0.25
    ax2.bar([i - width for i in x], monthly["tv_spend"], width=width, color=COLORS["tv"], label="TV")
    ax2.bar(x, monthly["digital_spend"], width=width, color=COLORS["digital"], label="Digital")
    ax2.bar([i + width for i in x], monthly["radio_spend"], width=width, color=COLORS["radio"], label="Radio")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(monthly["year_month"].dt.strftime("%b\n%Y"), rotation=0, ha="center", fontsize=8)
    ax2.set_ylabel("Spend", color=COLORS["muted"])
    ax2.yaxis.set_major_formatter(FuncFormatter(money_thousands))
    ax2.legend(frameon=False, ncol=3, loc="upper left")
    ax2.text(
        0.01,
        -0.24,
        "Axis: X = Date[Year Month], Y = TV Spend / Digital Spend / Radio Spend.",
        transform=ax2.transAxes,
        fontsize=9,
        color=COLORS["muted"],
    )

    ax3 = fig.add_axes([0.05, 0.08, 0.43, 0.25])
    style_panel(ax3, "3. Return per £1 by Channel")
    roi_sorted = roi.sort_values("return_per_gbp1", ascending=True)
    bar_colors = [COLORS["radio"], COLORS["digital"], COLORS["tv"]]
    ax3.barh(roi_sorted["channel"], roi_sorted["return_per_gbp1"], color=bar_colors, height=0.55)
    ax3.axvline(1.0, color=COLORS["promo"], linestyle="--", linewidth=1.6)
    ax3.set_xlabel("Return per £1", color=COLORS["muted"])
    ax3.set_xlim(0, max(1.15, roi["return_per_gbp1"].max() + 0.1))
    for i, v in enumerate(roi_sorted["return_per_gbp1"]):
        ax3.text(v + 0.02, i, f"{v:.3f}", va="center", fontsize=10, color=COLORS["text"])
    ax3.text(1.005, 1.02, "Break-even line", transform=ax3.get_xaxis_transform(), fontsize=9, color=COLORS["promo"])
    ax3.text(
        0.01,
        -0.22,
        "Axis: X = return_per_gbp1, Y = channel. Dashed line at 1.0 = break-even.",
        transform=ax3.transAxes,
        fontsize=9,
        color=COLORS["muted"],
    )

    ax4 = fig.add_axes([0.52, 0.08, 0.43, 0.25])
    style_panel(ax4, "4. Recommended Budget Allocation")
    budget_sorted = budget.sort_values("recommended_spend", ascending=True)
    ax4.barh(budget_sorted["channel"], budget_sorted["recommended_spend"], color=[COLORS["neutral"], COLORS["neutral"], COLORS["good"]], height=0.55)
    ax4.set_xlabel("Recommended Spend", color=COLORS["muted"])
    ax4.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"£{x/1000:.0f}K"))
    ax4.set_xlim(0, 55000)
    for i, row in enumerate(budget_sorted.itertuples(index=False)):
        label = f"£{row.recommended_spend:,.0f} | {row.weight_pct:.0f}% | Exp sales £{row.expected_sales:,.0f}"
        ax4.text(max(row.recommended_spend, 600) + 1000, i, label, va="center", fontsize=9.5, color=COLORS["text"])
    ax4.text(
        0.01,
        -0.22,
        "Axis: X = recommended_spend, Y = channel. Labels show spend, weight %, and expected sales.",
        transform=ax4.transAxes,
        fontsize=9,
        color=COLORS["muted"],
    )

    fig.text(
        0.05,
        0.015,
        "Color system: Sales = navy, TV = blue, Digital = teal, Radio = amber, Promo = red, Positive outcome = green",
        fontsize=10,
        color=COLORS["muted"],
    )

    fig.savefig(OUT, dpi=220, bbox_inches="tight")
    print(OUT)


if __name__ == "__main__":
    main()
