from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd


DATA_PATH = Path("data/marketing_data.csv")
ADSTOCKED_PATH = Path("data/mmm_data_adstocked.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DECAY_RATES = {
    "tv_spend": 0.6,
    "digital_spend": 0.3,
    "radio_spend": 0.4,
}

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


def parse_week(series: pd.Series) -> pd.Series:
    """Parse week labels safely for either ISO or UK-style date strings."""
    parsed = pd.to_datetime(series, format="%Y-%m-%d", errors="coerce")
    if parsed.isna().any():
        parsed = parsed.fillna(pd.to_datetime(series, format="%d/%m/%Y", errors="coerce"))
    if parsed.isna().any():
        raise ValueError("Unable to parse one or more values in the 'week' column.")
    return parsed


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["week"] = parse_week(df["week"])
    return df.sort_values("week").reset_index(drop=True)


def adstock(spend_series: pd.Series, decay_rate: float) -> pd.Series:
    """Geometric adstock with weekly carry-over."""
    if not 0 <= decay_rate < 1:
        raise ValueError("decay_rate must be between 0 and 1.")

    result = np.zeros(len(spend_series), dtype=float)
    values = spend_series.to_numpy(dtype=float)
    result[0] = values[0]

    for index in range(1, len(values)):
        result[index] = values[index] + decay_rate * result[index - 1]

    return pd.Series(result, index=spend_series.index, name=spend_series.name)


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


def save_figure(fig: plt.Figure, filename: str) -> None:
    output_path = OUTPUT_DIR / filename
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    print(f"Saved: {output_path}")


def summarise_channel(df: pd.DataFrame, spend_col: str, adstock_col: str, decay_rate: float) -> str:
    original_mean = df[spend_col].mean()
    adstock_mean = df[adstock_col].mean()
    lift = ((adstock_mean / original_mean) - 1) * 100
    return f"Decay {decay_rate:.1f} | Avg carry-over uplift {lift:.0f}%"


df = load_data()
print(f"Loaded {len(df)} rows")
print(df[["week", "tv_spend", "digital_spend", "radio_spend"]].head().to_string(index=False))

# --- Apply adstock to all three channels ---
for spend_col, decay_rate in DECAY_RATES.items():
    adstock_col = spend_col.replace("_spend", "_adstock")
    df[adstock_col] = adstock(df[spend_col], decay_rate=decay_rate)

print("\nAdstock applied. Sample output:")
print(
    df[
        [
            "week",
            "tv_spend",
            "tv_adstock",
            "digital_spend",
            "digital_adstock",
            "radio_spend",
            "radio_adstock",
        ]
    ]
    .head(10)
    .to_string(index=False)
)

# --- Plot: TV original vs adstocked ---
fig, ax = plt.subplots(figsize=(12.6, 5.8))

ax.plot(
    df["week"],
    df["tv_spend"],
    color=BLUE,
    linewidth=2.0,
    alpha=0.7,
    label="TV spend (original)",
    zorder=2,
)
ax.plot(
    df["week"],
    df["tv_adstock"],
    color=ORANGE,
    linewidth=2.4,
    linestyle="--",
    label="TV adstock (decay = 0.6)",
    zorder=3,
)
ax.fill_between(
    df["week"],
    df["tv_spend"],
    df["tv_adstock"],
    where=df["tv_adstock"] >= df["tv_spend"],
    color=ORANGE,
    alpha=0.08,
    zorder=1,
)

add_title_block(
    fig,
    "TV Spend: Original vs Adstocked",
    "Adstock smooths weekly spend and carries advertising effect forward over time",
)

ax.set_xlabel("Week")
ax.set_ylabel("Spend")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(currency_formatter))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
style_axes(ax)
ax.legend(loc="upper left", bbox_to_anchor=(0.01, 0.985), borderaxespad=0.0)

summary_text = summarise_channel(df, "tv_spend", "tv_adstock", DECAY_RATES["tv_spend"])
ax.text(
    0.99,
    0.98,
    summary_text,
    transform=ax.transAxes,
    ha="right",
    va="top",
    fontsize=9.5,
    color=TEXT,
    bbox={"boxstyle": "round,pad=0.35", "facecolor": "#F8FAFC", "edgecolor": "#D0D7DE"},
)

fig.subplots_adjust(top=0.79)
save_figure(fig, "tv_adstock_plot.png")

# --- Save adstocked dataset ---
df.to_csv(ADSTOCKED_PATH, index=False, date_format="%Y-%m-%d")
print(f"Adstocked dataset saved: {ADSTOCKED_PATH}")

print("\nDay 63 Adstock complete.")
