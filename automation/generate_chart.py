"""
=========================================================
Savings Chart Generator

Reads the savings_report.csv exported by the closed-loop
controller and produces a bar chart comparing energy
consumption across iterations, proving the AI-driven
reduction visually.
=========================================================
"""

import pandas as pd
import matplotlib.pyplot as plt

from energyplus.config import IDF_FILE

REPORTS_DIR = IDF_FILE.parent.parent / "reports"


def generate_chart():

    csv_path = REPORTS_DIR / "savings_report.csv"

    if not csv_path.exists():
        print(
            f"No savings report found at {csv_path}. "
            "Run automation.controller first."
        )
        return

    df = pd.read_csv(csv_path)

    labels = [
    f"Iteration {row.iteration}\n"
    f"(Clg {row.applied_cooling_setpoint_c} / Htg {row.applied_heating_setpoint_c})"
    for row in df.itertuples()
]
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        labels,
        df["total_energy_kwh"],
        color=["#94A3B8"] + ["#2563EB"] * (len(df) - 1),
    )

    for bar, value in zip(bars, df["total_energy_kwh"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:,.0f} kWh",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    ax.set_ylabel("Total Energy Consumption (kWh)")
    ax.set_title(
        "AI-Driven Closed-Loop Optimization: Energy Consumption per Iteration"
    )

    if len(df) >= 2:
        first = df["total_energy_kwh"].iloc[0]
        last = df["total_energy_kwh"].iloc[-1]

        if first:
            pct = round(((first - last) / first) * 100, 2)

            ax.text(
                0.5,
                0.95,
                f"Net Change: {pct}%",
                transform=ax.transAxes,
                ha="center",
                fontsize=12,
                fontweight="bold",
                color="#16A34A" if pct > 0 else "#DC2626",
            )

    plt.tight_layout()

    output_path = REPORTS_DIR / "savings_chart.png"
    plt.savefig(output_path, dpi=150)

    print(f"Chart saved to: {output_path}")


if __name__ == "__main__":
    generate_chart()