from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import statsmodels.api as sm


DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

BLUE = "#2F6EA9"
GREEN = "#2E9B4D"
AMBER = "#F4A62A"
RED = "#D94B45"
GRID = "#D9E2EC"
TEXT = "#243447"

CHANNEL_LABELS = {
    "tv": "TV",
    "digital": "Digital",
    "radio": "Radio",
}


plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#C7D0D9",
        "axes.labelcolor": TEXT,
        "axes.titlecolor": TEXT,
        "axes.titlesize": 15,
        "axes.labelsize": 12,
        "xtick.color": TEXT,
        "ytick.color": TEXT,
        "font.size": 11,
        "legend.frameon": True,
        "legend.facecolor": "white",
        "legend.edgecolor": "#D0D7DE",
    }
)


def currency_formatter(value: float, _: float) -> str:
    return f"£{value:,.2f}"


def style_axes(ax: plt.Axes) -> None:
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.85)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C7D0D9")
    ax.spines["bottom"].set_color("#C7D0D9")


def add_title_block(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.suptitle(title, fontsize=15.0, color=TEXT, y=0.965)
    fig.text(
        0.5,
        0.905,
        subtitle,
        ha="center",
        va="bottom",
        fontsize=10.0,
        color="#5B6B7A",
    )


def bar_color(return_per_pound: float) -> str:
    if return_per_pound >= 1.0:
        return GREEN
    if return_per_pound >= 0.9:
        return AMBER
    return RED


def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "mmm_data_adstocked.csv", parse_dates=["week"])


def build_model(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResultsWrapper:
    features = df[["tv_adstock", "digital_adstock", "radio_adstock", "promo_flag"]]
    target = df["sales"]
    features = sm.add_constant(features)
    return sm.OLS(target, features).fit()


def calculate_roi(df: pd.DataFrame, model: sm.regression.linear_model.RegressionResultsWrapper) -> pd.DataFrame:
    coefficients = {
        "tv": model.params["tv_adstock"],
        "digital": model.params["digital_adstock"],
        "radio": model.params["radio_adstock"],
    }

    avg_spend = {
        "tv": df["tv_spend"].mean(),
        "digital": df["digital_spend"].mean(),
        "radio": df["radio_spend"].mean(),
    }

    avg_adstock = {
        "tv": df["tv_adstock"].mean(),
        "digital": df["digital_adstock"].mean(),
        "radio": df["radio_adstock"].mean(),
    }

    rows = []
    for channel_key in ["tv", "digital", "radio"]:
        incremental_sales = coefficients[channel_key] * avg_adstock[channel_key]
        roi = (incremental_sales / avg_spend[channel_key]) - 1
        rows.append(
            {
                "channel_key": channel_key,
                "channel": CHANNEL_LABELS[channel_key],
                "coefficient": round(coefficients[channel_key], 4),
                "avg_weekly_spend": round(avg_spend[channel_key], 2),
                "avg_adstock": round(avg_adstock[channel_key], 2),
                "incremental_sales": round(incremental_sales, 2),
                "roi": round(roi, 4),
                "return_per_£1": round(roi + 1, 4),
            }
        )

    return pd.DataFrame(rows).sort_values("roi", ascending=False).reset_index(drop=True)


def save_roi_chart(roi_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9.2, 5.8))

    colors = [bar_color(value) for value in roi_df["return_per_£1"]]
    bars = ax.bar(
        roi_df["channel"],
        roi_df["return_per_£1"],
        color=colors,
        width=0.62,
        edgecolor="white",
        linewidth=1.0,
        zorder=3,
    )

    add_title_block(
        fig,
        "ROI per Channel: Sales Return per £1 Spent",
        "TV is the only channel currently operating above break-even in the model",
    )

    ax.axhline(y=1.0, color=TEXT, linestyle="--", linewidth=1.1, zorder=2)
    ax.text(
        0.99,
        1.01,
        "Break-even line",
        transform=ax.get_yaxis_transform(),
        ha="right",
        va="bottom",
        fontsize=9.5,
        color=TEXT,
    )

    style_axes(ax)
    ax.set_xlabel("Channel")
    ax.set_ylabel("£ sales return per £1 spent")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))
    ax.set_ylim(0, max(1.18, roi_df["return_per_£1"].max() + 0.10))

    for bar, value, roi_value in zip(bars, roi_df["return_per_£1"], roi_df["roi"]):
        label = f"£{value:.2f}\nROI {roi_value:+.2%}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.025,
            label,
            ha="center",
            va="bottom",
            fontsize=9.3,
            color=TEXT,
        )

    top_channel = roi_df.iloc[0]
    summary = (
        f"Best channel: {top_channel['channel']} | "
        f"£{top_channel['return_per_£1']:.2f} return per £1 spent"
    )
    ax.text(
        0.99,
        0.96,
        summary,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9.5,
        color=TEXT,
        bbox={"boxstyle": "round,pad=0.35", "facecolor": "#F8FAFC", "edgecolor": "#D0D7DE"},
    )

    fig.subplots_adjust(top=0.80)
    chart_path = OUTPUT_DIR / "roi_by_channel.png"
    fig.savefig(chart_path, dpi=180)
    plt.close(fig)
    print(f"Chart saved to: {chart_path}")


df = load_data()
model = build_model(df)
roi_df = calculate_roi(df, model)

print("\n--- ROI per Channel ---")
print(roi_df.drop(columns=["channel_key"]).to_string(index=False))

roi_path = OUTPUT_DIR / "roi_by_channel.csv"
roi_df.drop(columns=["channel_key"]).to_csv(roi_path, index=False)
print(f"\nROI table saved to: {roi_path}")

save_roi_chart(roi_df)

top = roi_df.iloc[0]
print(f"\nTop channel: {top['channel']}")
print(f"For every £1 spent on {top['channel']}, the model returns £{top['return_per_£1']:.2f} in sales.")
