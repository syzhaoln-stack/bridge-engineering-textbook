"""Generate six low-cognitive-load bridge-engineering teaching figures.

All numerical series in this file are dimensionless teaching examples unless a
caption explicitly gives material/geometric parameters.  They are not field
measurements from a real bridge.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data-figures"
OUT.mkdir(parents=True, exist_ok=True)

# Paper-white, cyan-blue, coral and amber — high contrast, colour-blind robust.
PAPER = "#FFFDF8"
INK = "#16324F"
MUTED = "#587084"
CYAN = "#087E8B"
CORAL = "#D95D39"
AMBER = "#E5A000"
GRID = "#D6E1E5"


def set_style():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "Noto Sans CJK SC", "SimHei", "Arial Unicode MS", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.titleweight": "bold",
        "axes.titlesize": 15,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "svg.fonttype": "none",
        "savefig.facecolor": PAPER,
    })


def base_ax(ax):
    ax.grid(axis="y", color=GRID, linewidth=0.8, zorder=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(MUTED)
    ax.tick_params(length=0)


def footer(fig, text):
    fig.text(0.055, 0.025, text, color=MUTED, fontsize=8.5, ha="left", va="bottom")


def save(fig, stem):
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight", pad_inches=0.12)
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def write_csv(stem, columns, rows):
    with (OUT / f"{stem}.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)


def fig_scale():
    stem = "01-scale-selfweight-capacity"
    lam = np.arange(0.5, 3.01, 0.25)
    moment = lam ** 4
    capacity = lam ** 3
    write_csv(stem, ["scale_lambda", "self_weight_moment_ratio", "capacity_ratio"], zip(lam, moment, capacity))
    fig, ax = plt.subplots(figsize=(8.3, 5.1))
    ax.plot(lam, moment, color=CORAL, lw=2.8, marker="o", ms=4, zorder=3)
    ax.plot(lam, capacity, color=CYAN, lw=2.8, marker="o", ms=4, zorder=3)
    ax.set_title("桥梁等比例放大后，为什么“更粗”反而更吃力？", loc="left", pad=14)
    ax.set_xlabel("几何尺度倍率 λ（原桥 = 1）")
    ax.set_ylabel("相对值（原桥 = 1）")
    ax.set_xlim(0.45, 3.32); ax.set_ylim(0, 86)
    ax.annotate("自重引起的弯矩  ∝ λ⁴", xy=(3, 81), xytext=(2.15, 72), color=CORAL, fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": CORAL, "lw": 1.2})
    ax.annotate("同材料、几何相似截面能力  ∝ λ³", xy=(3, 27), xytext=(1.82, 36), color=CYAN, fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": CYAN, "lw": 1.2})
    ax.axvline(1, color=MUTED, ls=":", lw=1)
    ax.text(1.04, 4, "原桥", color=MUTED, fontsize=9)
    base_ax(ax)
    footer(fig, "适用前提：同材料、完全几何相似；仅比较自重效应。量纲分析教学示意，非实桥测量。")
    fig.tight_layout(rect=(0.03, 0.07, 0.99, 1))
    save(fig, stem)


def fig_depth():
    stem = "02-depth-stiffness-deflection"
    h = np.arange(0.5, 2.01, 0.125)
    inertia = h ** 3
    deflection = h ** -3
    write_csv(stem, ["depth_multiplier_h_h0", "inertia_ratio_I_I0", "deflection_ratio_delta_delta0"], zip(h, inertia, deflection))
    fig, ax = plt.subplots(figsize=(8.3, 5.1))
    ax.plot(h, inertia, color=CYAN, lw=2.8, zorder=3)
    ax.plot(h, deflection, color=CORAL, lw=2.8, zorder=3)
    ax.scatter([1, 1], [1, 1], color=INK, s=20, zorder=4)
    ax.set_title("同一跨径下，梁高增加一点，刚度和挠度会怎样变？", loc="left", pad=14)
    ax.set_xlabel("梁高倍率 h / h0")
    ax.set_ylabel("相对值（基准梁 = 1）")
    ax.set_xlim(0.46, 2.22); ax.set_ylim(0, 8.8)
    ax.annotate("截面惯性矩 I  ∝ h³", xy=(2, 8), xytext=(1.48, 7.2), color=CYAN, fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": CYAN, "lw": 1.2})
    ax.annotate("同条件挠度 δ  ∝ 1 / h³", xy=(0.5, 8), xytext=(0.77, 6.5), color=CORAL, fontsize=10.5,
                arrowprops={"arrowstyle": "-", "color": CORAL, "lw": 1.2})
    base_ax(ax)
    footer(fig, "适用前提：矩形或等比例截面、材料与跨径不变，线弹性小挠度。无量纲教学示意，非设计计算。")
    fig.tight_layout(rect=(0.03, 0.07, 0.99, 1))
    save(fig, stem)


def fig_cable():
    stem = "03-cable-sag-horizontal-force"
    sag_ratio = np.arange(0.4, 2.51, 0.1)  # f/f0
    force_ratio = 1 / sag_ratio
    write_csv(stem, ["sag_ratio_f_f0", "horizontal_force_ratio_H_H0"], zip(sag_ratio, force_ratio))
    fig, ax = plt.subplots(figsize=(8.3, 5.1))
    ax.plot(sag_ratio, force_ratio, color=CYAN, lw=2.8, zorder=3)
    ax.scatter([1], [1], color=INK, s=24, zorder=4)
    ax.set_title("抛物线索的垂度变大，主缆水平力如何变化？", loc="left", pad=14)
    ax.set_xlabel("垂度倍率 f / f0")
    ax.set_ylabel("水平力倍率 H / H0")
    ax.set_xlim(0.35, 2.72); ax.set_ylim(0, 2.8)
    ax.annotate("H / H0 = f0 / f", xy=(2.5, 0.4), xytext=(1.66, 0.87), color=CYAN, fontsize=11,
                arrowprops={"arrowstyle": "-", "color": CYAN, "lw": 1.2})
    ax.annotate("基准状态", xy=(1, 1), xytext=(1.13, 1.45), color=MUTED, fontsize=9.5,
                arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 1})
    base_ax(ax)
    footer(fig, "适用前提：均布竖向荷载下的抛物线索；跨径、荷载不变，忽略索自重与大位移。无量纲教学示意。")
    fig.tight_layout(rect=(0.03, 0.07, 0.99, 1))
    save(fig, stem)


def fig_wind():
    stem = "04-wind-speed-square-law"
    v_ratio = np.arange(0.4, 2.01, 0.1)
    f_ratio = v_ratio ** 2
    write_csv(stem, ["wind_speed_ratio_V_V0", "wind_force_ratio_F_F0"], zip(v_ratio, f_ratio))
    fig, ax = plt.subplots(figsize=(8.3, 5.1))
    ax.plot(v_ratio, f_ratio, color=CORAL, lw=2.8, zorder=3)
    ax.scatter([1, 2], [1, 4], color=INK, s=25, zorder=4)
    ax.set_title("风速翻倍时，风力为什么不是翻倍而是四倍？", loc="left", pad=14)
    ax.set_xlabel("风速倍率 V / V0")
    ax.set_ylabel("风力倍率 F / F0")
    ax.set_xlim(0.35, 2.22); ax.set_ylim(0, 4.85)
    ax.annotate("F / F0 = (V / V0)²", xy=(2, 4), xytext=(1.18, 4.25), color=CORAL, fontsize=11,
                arrowprops={"arrowstyle": "-", "color": CORAL, "lw": 1.2})
    ax.annotate("2V0 → 4F0", xy=(2, 4), xytext=(1.57, 3.22), color=INK, fontsize=9.5,
                arrowprops={"arrowstyle": "-", "color": INK, "lw": 1})
    base_ax(ax)
    footer(fig, "适用前提：空气密度 ρ、阻力系数 C_d 和迎风面积 A 固定，F = ½ρC_dAV²。无量纲教学示意。")
    fig.tight_layout(rect=(0.03, 0.11, 0.99, 1))
    save(fig, stem)


def fig_amplification():
    stem = "05-single_dof_dynamic-amplification"
    r = np.linspace(0, 2, 801)
    zetas = [(0.03, CORAL), (0.08, AMBER), (0.20, CYAN)]
    cols = ["frequency_ratio_r"] + [f"amplification_zeta_{z:.2f}" for z, _ in zetas]
    vals = [r] + [1 / np.sqrt((1-r**2)**2 + (2*z*r)**2) for z, _ in zetas]
    write_csv(stem, cols, zip(*vals))
    fig, ax = plt.subplots(figsize=(8.3, 5.1))
    for zeta, color in zetas:
        amp = 1 / np.sqrt((1-r**2)**2 + (2*zeta*r)**2)
        ax.plot(r, amp, color=color, lw=2.5, zorder=3)
        peak_i = int(np.argmax(amp))
        ax.text(r[peak_i] + 0.055, amp[peak_i], f"ζ = {zeta:.2f}",
                color=color, fontsize=9.6, va="center", ha="left")
    ax.axvline(1, color=MUTED, ls=":", lw=1.2)
    ax.text(0.52, 17.15, "共振附近 r = 1", color=MUTED, fontsize=9.5)
    ax.set_title("激励频率接近自振频率时，阻尼为何决定响应峰值？", loc="left", pad=14)
    ax.set_xlabel("频率比 r = 激励频率 / 自振频率")
    ax.set_ylabel("稳态放大系数")
    ax.set_xlim(0, 2.28); ax.set_ylim(0, 18.3)
    base_ax(ax)
    footer(fig, "适用前提：线性单自由度、简谐外力、稳态响应；ζ 为阻尼比。模型曲线，非特定桥梁的实测振动。")
    fig.tight_layout(rect=(0.03, 0.07, 0.99, 1))
    save(fig, stem)


def fig_mesh_convergence():
    stem = "06-simply-supported-beam-mesh-convergence"
    # Exact Euler–Bernoulli result: delta_max = 5qL^4/(384EI).
    L, q, E, I = 10.0, 20_000.0, 30e9, 0.12
    exact_mm = 5*q*L**4/(384*E*I)*1000
    elements = np.array([2, 4, 8, 16, 32])
    # Explicit teaching-only second-order error model: e=0.8(h/L)^2.
    err_pct = 80 / elements**2
    approx_mm = exact_mm * (1 - err_pct/100)
    write_csv(stem, ["elements_N", "element_size_over_span_h_L", "exact_midspan_deflection_mm", "teaching_approx_deflection_mm", "theoretical_relative_error_percent"],
              zip(elements, 1/elements, np.full_like(elements, exact_mm, dtype=float), approx_mm, err_pct))
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10.0, 4.9), gridspec_kw={"width_ratios": [1.05, 1.35]})
    # Minimal structural context diagram.
    ax0.set_xlim(-0.5, 10.5); ax0.set_ylim(-1.8, 2.4); ax0.axis("off")
    ax0.plot([0, 10], [0, 0], color=INK, lw=4, solid_capstyle="round")
    ax0.fill([0, -0.38, 0.38], [-0.15, -0.8, -0.8], color=CYAN)
    ax0.plot([9.55, 10.45], [-0.75, -0.75], color=CYAN, lw=2.5)
    ax0.add_patch(plt.Circle((10, -0.45), 0.17, color=CYAN))
    for x in np.linspace(0.7, 9.3, 7):
        ax0.annotate("", xy=(x, 0.23), xytext=(x, 1.25), arrowprops={"arrowstyle": "-|>", "color": CORAL, "lw": 1.4})
    ax0.text(5, 1.54, "均布荷载 q = 20 kN/m", ha="center", color=CORAL, fontsize=10.5)
    ax0.annotate("", xy=(0, -1.28), xytext=(10, -1.28), arrowprops={"arrowstyle": "<->", "color": MUTED, "lw": 1.1})
    ax0.text(5, -1.61, "L = 10 m", ha="center", color=MUTED, fontsize=10)
    ax0.text(5, -0.43, f"解析解：δ_max = 5qL⁴/(384EI) = {exact_mm:.3f} mm", ha="center", color=INK, fontsize=9.5)
    ax0.set_title("可解析的简支梁", loc="left", fontsize=12.5, pad=8)
    ax1.plot(elements, err_pct, color=CYAN, lw=2.8, marker="o", ms=6, zorder=3)
    ax1.set_xscale("log", base=2); ax1.set_yscale("log")
    ax1.set_xticks(elements); ax1.get_xaxis().set_major_formatter(mpl.ticker.ScalarFormatter())
    ax1.set_xlabel("单元数 N（每增加一倍，h/L 减半）")
    ax1.set_ylabel("相对误差（%）")
    ax1.set_title("网格加密后，教学示意误差如何下降？", loc="left", fontsize=12.5, pad=8)
    ax1.annotate("设定的二阶收敛：误差 = 80 / N² %", xy=(16, 0.3125), xytext=(4.7, 2.8), color=CYAN, fontsize=9.8,
                 arrowprops={"arrowstyle": "-", "color": CYAN, "lw": 1.1})
    base_ax(ax1)
    footer(fig, "适用前提：Euler–Bernoulli 梁，E = 30 GPa，I = 0.12 m⁴。本误差序列按显式二阶教学模型构造，不是有限元或实桥测量。")
    fig.suptitle("有了解析解后，怎样判断网格是否足够细？", x=0.06, ha="left", fontsize=15, fontweight="bold", y=0.98)
    fig.tight_layout(rect=(0.03, 0.07, 0.99, 0.94))
    save(fig, stem)


if __name__ == "__main__":
    set_style()
    fig_scale()
    fig_depth()
    fig_cable()
    fig_wind()
    fig_amplification()
    fig_mesh_convergence()
    print(f"Wrote figures and CSV files to {OUT}")
