"""
=========================================================
Savings Chart Generator

Reads savings_report.csv and produces a bar chart comparing
energy consumption across closed-loop iterations.
=========================================================
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")           # headless — no display needed
import matplotlib.pyplot as plt
from pathlib import Path

from energyplus.config import IDF_FILE

REPORTS_DIR = IDF_FILE.parent.parent / "reports"


def generate_chart():
    csv_path = REPORTS_DIR / "savings_report.csv"

    if not csv_path.exists():
        print(f"[chart] No savings_report.csv at {csv_path}. Run controller first.")
        return

    df = pd.read_csv(csv_path)

    # Support both column name variants
    energy_col = "energy_kwh" if "energy_kwh" in df.columns else "total_energy_kwh"

    # Build readable x-axis labels (handle "Baseline" setpoints)
    def _sp(val):
        try:
            return f"{float(val):.1f}"
        except Exception:
            return str(val)

    cool_col = "cooling_setpoint" if "cooling_setpoint" in df.columns else "applied_cooling_setpoint_c"
    heat_col = "heating_setpoint" if "heating_setpoint" in df.columns else "applied_heating_setpoint_c"

    labels = [
        f"Iteration {row.iteration}\n(Clg {_sp(getattr(row, cool_col))} / Htg {_sp(getattr(row, heat_col))})"
        for row in df.itertuples()
    ]

    energies = df[energy_col].tolist()

    # Build colour list: first bar grey (baseline), rest blue gradient
    colors = ["#94A3B8"] + ["#2563EB"] * (len(df) - 1)

    fig, ax = plt.subplots(figsize=(max(8, len(df) * 3), 5))

    bars = ax.bar(labels, energies, color=colors, width=0.5)

    # Value labels on bars
    for bar, val in zip(bars, energies):
        if val is not None:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 20,
                f"{val:,.3f} kWh",
                ha="center", va="bottom", fontsize=9, fontweight="bold",
            )

    # Net change annotation
    if len(df) >= 2:
        first = energies[0]
        last  = energies[-1]
        if first and last and first != 0:
            pct = ((first - last) / first) * 100
            color = "#16A34A" if pct > 0 else "#DC2626"
            label = f"Net Savings: {pct:.2f}%" if pct > 0 else f"Net Change: {pct:.2f}%"
            ax.text(0.5, 0.97, label, transform=ax.transAxes,
                    ha="center", va="top", fontsize=12, fontweight="bold", color=color)

    ax.set_ylabel("Total Energy Consumption (kWh)")
    ax.set_title("AI Closed-Loop Optimisation — Energy per Iteration", fontsize=12)
    ax.set_ylim(bottom=0, top=max(energies) * 1.15 if energies else 10000)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    out = REPORTS_DIR / "savings_chart.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"[chart] Saved → {out}")


if __name__ == "__main__":
    generate_chart()
