from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd


DATA_PATH = Path("data/marketing_data.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#2F6EA9"
BLUE_LIGHT = "#8FB6D9"
ORANGE = "#F28E2B"
GRID = "#D9E2EC"
TEXT = "#243447"


plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#C7D0D9",
        "axes.labelcolor": TEXT,
        "axes.titlecolor": TEXT,
        "axes.titlesize": 16,
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
    return f"£{value:,.0f}"


def style_axes(ax: plt.Axes) -> None:
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.8)
    ax.grid(axis="x", visible=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#C7D0D9")
    ax.spines["bottom"].set_color("#C7D0D9")


def add_title_block(fig: plt.Figure, title: str, subtitle: str) -> None:
    fig.suptitle(title, fontsize=14.6, color=TEXT, y=0.965)
    fig.text(
        0.5,
        0.895,
        subtitle,
        ha="center",
        va="bottom",
        fontsize=10.0,
        color="#5B6B7A",
    )


def save_figure(fig: plt.Figure, filename: str) -> None:
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    print(f"Saved: {output_path}")


df = pd.read_csv(DATA_PATH, parse_dates=["week"]).sort_values("week").reset_index(drop=True)
print(df.info())
print(df.describe())

# --- 1. Correlation matrix ---
spend_cols = ["tv_spend", "digital_spend", "radio_spend", "sales"]
corr = df[spend_cols].corr()
print("\nCorrelation Matrix:")
print(corr.round(3))
corr.to_csv(OUTPUT_DIR / "correlation_matrix.csv")

# --- 2. Scatter plots with trend line ---
channel_labels = {
    "tv_spend": "TV Spend",
    "digital_spend": "Digital Spend",
    "radio_spend": "Radio Spend",
}

for channel, label in channel_labels.items():
    fig, ax = plt.subplots(figsize=(8.4, 5.6))

    x = df[channel]
    y = df["sales"]
    correlation = x.corr(y)

    ax.scatter(
        x,
        y,
        s=56,
        alpha=0.78,
        color=BLUE_LIGHT,
        edgecolors="white",
        linewidths=0.8,
        zorder=2,
    )

    coefficients = np.polyfit(x, y, 1)
    trend_line = np.poly1d(coefficients)
    x_line = np.linspace(x.min(), x.max(), 200)
    ax.plot(
        x_line,
        trend_line(x_line),
        color=ORANGE,
        linewidth=2.3,
        linestyle="--",
        label="Trend line",
        zorder=3,
    )

    relationship = (
        "Moderate positive relationship"
        if correlation >= 0.5
        else "Weak-to-moderate positive relationship"
        if correlation >= 0.25
        else "Little to no relationship"
    )

    add_title_block(fig, f"{label} vs Sales", f"{relationship}  |  Pearson r = {correlation:.3f}")
    ax.set_xlabel(label)
    ax.set_ylabel("Sales")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))
    style_axes(ax)
    ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.98), borderaxespad=0.0)
    fig.subplots_adjust(top=0.78)

    save_figure(fig, f"scatter_{channel}_vs_sales.png")

# --- 3. Time series with promo highlights ---
fig, ax = plt.subplots(figsize=(12.6, 5.8))

ax.plot(
    df["week"],
    df["sales"],
    color=BLUE,
    linewidth=2.2,
    label="Weekly sales",
    zorder=2,
)

rolling_sales = df["sales"].rolling(window=4, min_periods=1).mean()
ax.plot(
    df["week"],
    rolling_sales,
    color="#6C8EAD",
    linewidth=2,
    linestyle=":",
    label="4-week rolling average",
    zorder=1,
)

promo_df = df[df["promo_flag"] == 1]
ax.scatter(
    promo_df["week"],
    promo_df["sales"],
    s=78,
    color=ORANGE,
    edgecolors="white",
    linewidths=0.9,
    label="Promo week",
    zorder=3,
)

add_title_block(
    fig,
    "Weekly Sales with Promo Weeks Highlighted",
    f"{len(promo_df)} promo weeks highlighted across {len(df)} total weeks",
)
ax.set_xlabel("Week")
ax.set_ylabel("Sales")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
style_axes(ax)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, 0.83),
    ncol=3,
    bbox_transform=fig.transFigure,
    borderaxespad=0.0,
)
fig.subplots_adjust(top=0.76)

save_figure(fig, "timeseries_sales_promo.png")

print("\nDay 62 EDA complete.")
