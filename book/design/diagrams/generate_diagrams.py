"""
Chapter diagrams for Organizational Refraction book.
Generates all 12 chapter diagrams following the design system spec from REF-101.
Output: ch{N:02d}-diagram.png at 300 DPI each.

Design system: Navy Deep #0D1B2E / Amber #D4860B palette,
               white incoming ray, amber-light refracted ray, slate dashed counterfactual.
Snell's Law: n1*sin(θ1) = n2*sin(θ2) — all ray-path diagrams are physically plausible.
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc, Wedge, Polygon
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import os

# ── Design System Colors ────────────────────────────────────────────────────
ND = '#0D1B2E'   # Navy Deep
NM = '#16284B'   # Navy Mid
NL = '#20406E'   # Navy Light
AM = '#D4860B'   # Amber
AL = '#F0AC32'   # Amber Light
AP = '#FCE6A5'   # Amber Pale
NN = '#F5F3EE'   # Neutral Light (warm off-white)
SL = '#78889A'   # Slate
BT = '#2C2C2C'   # Body Text
WH = '#FFFFFF'   # White
BG = '#FAFAF8'   # Background for diagrams

DPI = 300
OUT = os.path.dirname(os.path.abspath(__file__))

# ── Font settings ───────────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'text.color': BT,
    'axes.facecolor': BG,
    'figure.facecolor': BG,
})

# ── Shared helpers ───────────────────────────────────────────────────────────

def new_fig(w=5.2, h=4.2):
    fig, ax = plt.subplots(figsize=(w, h), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def add_caption(fig, num, sub, text):
    fig.text(0.5, 0.015, f"Figure {num}.{sub}  —  {text}",
             ha='center', va='bottom', fontsize=6.5, color=SL, style='normal')


def draw_arrow_ray(ax, x1, y1, x2, y2, color=WH, lw=2.5,
                   dashed=False, zorder=5, arrowscale=10):
    """Draw a ray segment with a solid-filled arrowhead at the end."""
    ls = (0, (6, 3)) if dashed else '-'
    ax.annotate('',
                xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle=f'-|>,head_width=0.06,head_length=0.10',
                    color=color, lw=lw,
                    linestyle='dashed' if dashed else 'solid',
                    connectionstyle='arc3,rad=0',
                ),
                zorder=zorder)


def ray_seg(ax, x1, y1, x2, y2, color=WH, lw=2.5, dashed=False, zorder=5):
    """Draw a plain line segment (no arrowhead)."""
    ls = (0, (8, 4)) if dashed else '-'
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, linestyle=ls,
            solid_capstyle='round', zorder=zorder)


def org_box(ax, x, y, w, h, label='', sublabel='', alpha=0.88, zorder=3):
    """Draw an organizational medium rectangle."""
    r = FancyBboxPatch((x, y), w, h,
                       boxstyle="square,pad=0",
                       facecolor=NL, edgecolor=AM, linewidth=1.5,
                       alpha=alpha, zorder=zorder)
    ax.add_patch(r)
    if label:
        ax.text(x + w/2, y + h/2 + (0.06 if sublabel else 0),
                label, ha='center', va='center',
                color=WH, fontsize=7.5, fontweight='bold', zorder=zorder+1)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.09,
                sublabel, ha='center', va='center',
                color=AP, fontsize=5.5, zorder=zorder+1)


def angle_arc(ax, cx, cy, r, theta1, theta2, color=AP, lw=1.0, zorder=6):
    arc = Arc((cx, cy), 2*r, 2*r, angle=0,
              theta1=min(theta1, theta2), theta2=max(theta1, theta2),
              color=color, lw=lw, zorder=zorder)
    ax.add_patch(arc)


def snell_refract(theta_i_deg, n1=1.0, n2=1.5):
    """Return refracted angle (degrees) via Snell's Law. Returns None for TIR."""
    sin_r = n1 * math.sin(math.radians(theta_i_deg)) / n2
    if abs(sin_r) > 1:
        return None
    return math.degrees(math.asin(sin_r))


def critical_angle(n1, n2):
    """Critical angle for TIR (n1 > n2)."""
    return math.degrees(math.asin(n2 / n1))


# ════════════════════════════════════════════════════════════════════════════
# Ch 1 — Strategy-Reality Gap
# Before/after ray path: white intended ray vs amber deflected ray, with gap
# ════════════════════════════════════════════════════════════════════════════
def ch01():
    fig, ax = plt.subplots(figsize=(5.5, 4.0), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 4.0)

    # Organizational boundary (vertical interface at x=2.2)
    BX = 2.2
    theta_i = 35.0   # degrees from normal (horizontal)
    theta_r = snell_refract(theta_i, n1=1.0, n2=1.8)  # ≈ 18.8°

    # Convert: ray going right, normal = horizontal (x-axis)
    # Incoming from upper-left: angle θ_i above the normal pointing right
    # In Cartesian: incoming direction = (cos(θ_i_from_right), -sin(θ_i_from_right))
    # We define the ray as travelling generally to the right

    yi = 2.8   # entry y
    # Incoming ray: from left
    ix1, iy1 = 0.3, yi + 1.0 * math.tan(math.radians(theta_i))
    ix2, iy2 = BX, yi

    # Refracted ray: bends toward normal (smaller angle from normal)
    rx1, ry1 = BX, yi
    rx2 = 5.0
    ry2 = yi - (rx2 - rx1) * math.tan(math.radians(theta_r))

    # Intended (counterfactual) ray — continues at same angle
    cx1, cy1 = BX, yi
    cx2 = 5.0
    cy2 = yi - (cx2 - cx1) * math.tan(math.radians(theta_i))

    # Draw boundary band (organizational medium — thin strip)
    band_w = 0.25
    band = FancyBboxPatch((BX - band_w/2, 0.5), band_w, 3.0,
                          boxstyle="square,pad=0",
                          facecolor=NL, edgecolor=AM, linewidth=1.5, alpha=0.8, zorder=3)
    ax.add_patch(band)
    ax.text(BX, 0.35, 'ORGANIZATIONAL\nBOUNDARY',
            ha='center', va='top', fontsize=5.5, color=AM,
            fontweight='bold', zorder=4)

    # Draw incoming ray
    ray_seg(ax, ix1, iy1, ix2, iy2, color=WH, lw=2.5, zorder=5)
    draw_arrow_ray(ax, ix1 + 0.7*(ix2-ix1), iy1 + 0.7*(iy2-iy1),
                   ix2, iy2, color=WH, lw=2.5, zorder=6)

    # Draw intended (counterfactual) dashed ray
    ray_seg(ax, cx1, cy1, cx2, cy2, color=SL, lw=1.5, dashed=True, zorder=5)
    draw_arrow_ray(ax, cx1 + 0.7*(cx2-cx1), cy1 + 0.7*(cy2-cy1),
                   cx2, cy2, color=SL, lw=1.5, zorder=6)

    # Draw refracted ray
    ray_seg(ax, rx1, ry1, rx2, ry2, color=AL, lw=2.5, zorder=5)
    draw_arrow_ray(ax, rx1 + 0.7*(rx2-rx1), ry1 + 0.7*(ry2-ry1),
                   rx2, ry2, color=AL, lw=2.5, zorder=6)

    # Gap brace at x=4.5
    gx = 4.5
    gy_intent = cy2 - (cx2 - gx) * (cy2 - cy1) / (cx2 - cx1) if cx2 != cx1 else cy1
    gy_actual = ry2 - (rx2 - gx) * (ry2 - ry1) / (rx2 - rx1) if rx2 != rx1 else ry1
    ax.annotate('', xy=(gx, gy_intent), xytext=(gx, gy_actual),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5,
                                mutation_scale=8), zorder=7)
    gap_mid = (gy_intent + gy_actual) / 2
    ax.text(gx + 0.12, gap_mid, 'STRATEGY–\nREALITY GAP',
            ha='left', va='center', fontsize=6, color=AP, fontweight='bold', zorder=7)

    # Labels
    ax.text(0.3, iy1 + 0.05, 'Strategy\nas Designed', ha='left', va='bottom',
            fontsize=7, color=WH, fontweight='bold')
    ax.text(5.05, cy2 + 0.05, 'Intended\nDestination', ha='left', va='bottom',
            fontsize=6.5, color=SL, style='italic')
    ax.text(5.05, ry2 - 0.05, 'Actual\nDelivery', ha='left', va='top',
            fontsize=6.5, color=AL, style='italic')

    # Normal line (dashed, at boundary)
    ax.plot([BX, BX], [1.0, 3.5], color=SL, lw=0.75, linestyle=(0,(4,4)), zorder=4, alpha=0.5)

    # Angle arc — incidence
    angle_arc(ax, BX, yi, 0.45, 90, 90+theta_i, color=AP, lw=1.0)
    ax.text(BX - 0.08, yi + 0.52, f'θ₁={theta_i:.0f}°',
            ha='right', va='bottom', fontsize=5.5, color=AP)

    # Angle arc — refraction
    angle_arc(ax, BX, yi, 0.35, 90+theta_r, 90+theta_i, color=AM, lw=1.0)
    ax.text(BX + 0.1, yi - 0.52, f'θ₂={theta_r:.1f}°',
            ha='left', va='top', fontsize=5.5, color=AM)

    add_caption(fig, 1, 1,
                'Strategy-reality gap: the ray of strategic intent deviates at the '
                'organizational boundary, arriving somewhere it was never aimed.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch01-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch01 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 2 — Existing Frameworks: Gap matrix
# What popular strategy frameworks see vs. what they miss
# ════════════════════════════════════════════════════════════════════════════
def ch02():
    fig, ax = plt.subplots(figsize=(5.5, 4.5), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 5.5)
    ax.set_ylim(0, 4.5)

    frameworks = ['SWOT /\nPESTLE', 'Balanced\nScorecard', "Porter's\nFive Forces",
                  'OKRs', 'McKinsey 7-S']
    dimensions = ['Strategy\nFormulation', 'Goal\nAlignment', 'Competitive\nAnalysis',
                  'Execution\nTracking', 'Cultural\nDynamics', 'Refraction\nIndex']

    nf = len(frameworks)
    nd = len(dimensions)

    col_w = 0.78
    row_h = 0.55
    x0 = 1.45
    y0 = 3.75

    # Column headers (frameworks)
    for j, fw in enumerate(frameworks):
        cx = x0 + j * col_w + col_w/2
        rect = FancyBboxPatch((x0 + j*col_w + 0.04, y0 + 0.05),
                              col_w - 0.08, 0.42,
                              boxstyle="round,pad=0.03",
                              facecolor=ND, edgecolor=AM, lw=1.0, zorder=3)
        ax.add_patch(rect)
        ax.text(cx, y0 + 0.26, fw, ha='center', va='center',
                fontsize=5.8, color=WH, fontweight='bold', zorder=4)

    # Row headers (dimensions)
    for i, dim in enumerate(dimensions):
        ry = y0 - (i+1)*row_h
        rect = FancyBboxPatch((0.08, ry + 0.04), 1.32, row_h - 0.08,
                              boxstyle="round,pad=0.03",
                              facecolor=NM, edgecolor=NL, lw=0.8, zorder=3)
        ax.add_patch(rect)
        ax.text(0.74, ry + row_h/2, dim, ha='center', va='center',
                fontsize=5.8, color=WH, fontweight='bold', zorder=4)

    # Coverage matrix
    # COVERED=full, PARTIAL=half, MISSING=empty
    # Last row (Refraction Index) is all missing — that's the book's insight
    coverage = [
        ['full', 'full',    'full',    'partial', 'partial'],   # Strategy Formulation
        ['partial', 'full', 'partial', 'full',    'full'   ],   # Goal Alignment
        ['full', 'partial', 'full',    'partial', 'partial'],   # Competitive Analysis
        ['partial', 'full', 'partial', 'full',    'partial'],   # Execution Tracking
        ['miss', 'partial', 'miss',    'miss',    'full'   ],   # Cultural Dynamics
        ['miss', 'miss',    'miss',    'miss',    'miss'   ],   # Refraction Index ← the gap
    ]

    for i, row in enumerate(coverage):
        ry = y0 - (i+1)*row_h
        for j, cov in enumerate(row):
            cx = x0 + j*col_w + col_w/2
            cy = ry + row_h/2

            # Cell background
            bg = '#EAE7E0' if (i + j) % 2 == 0 else BG
            crect = FancyBboxPatch((x0 + j*col_w + 0.04, ry + 0.04),
                                   col_w - 0.08, row_h - 0.08,
                                   boxstyle="square,pad=0",
                                   facecolor=bg, edgecolor='#D0CCC4', lw=0.4, zorder=2)
            ax.add_patch(crect)

            if cov == 'full':
                ax.text(cx, cy, '✓', ha='center', va='center',
                        fontsize=13, color='#1A7A3C', fontweight='bold', zorder=5)
            elif cov == 'partial':
                ax.text(cx, cy, '◑', ha='center', va='center',
                        fontsize=11, color=AM, zorder=5)
            else:  # miss
                ax.text(cx, cy, '✗', ha='center', va='center',
                        fontsize=12, color='#B82020', fontweight='bold', zorder=5)

    # Highlight the bottom row (Refraction Index) as the gap
    gap_y = y0 - nd * row_h
    highlight = FancyBboxPatch((0.06, gap_y + 0.02), x0 + nf*col_w - 0.06, row_h - 0.04,
                               boxstyle="square,pad=0",
                               facecolor='none', edgecolor=AM, lw=2.0, zorder=8, linestyle='--')
    ax.add_patch(highlight)
    ax.text(x0 + nf*col_w/2 + x0/2, gap_y - 0.15,
            '← THE BLIND SPOT: No existing framework measures organizational refraction',
            ha='center', va='top', fontsize=6.0, color=AM, fontweight='bold', zorder=9)

    # Legend
    legend_y = 0.22
    for sym, col, label in [('✓', '#1A7A3C', 'Addressed'), ('◑', AM, 'Partial'), ('✗', '#B82020', 'Not addressed')]:
        ax.text(0.7 + ['✓','◑','✗'].index(sym)*1.6, legend_y, sym + '  ' + label,
                ha='center', va='center', fontsize=6.5, color=col, fontweight='bold')

    ax.set_facecolor(BG)
    add_caption(fig, 2, 1,
                'Framework coverage matrix: existing strategy tools address formulation and '
                'execution tracking, but none measures organizational refraction — the critical blind spot.')
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch02-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch02 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 3 — Core Refraction Model (publication-quality primary diagram)
# Full Snell's Law diagram: incident → boundary → refracted, all layers labeled
# ════════════════════════════════════════════════════════════════════════════
def ch03():
    fig, ax = plt.subplots(figsize=(6.0, 5.0), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(-0.5, 6.5)
    ax.set_ylim(-0.3, 5.2)

    # ── Boundary at x=3.0 ──
    BX = 3.0
    theta_i = 40.0   # degrees from normal
    n1, n2 = 1.0, 1.7
    theta_r = snell_refract(theta_i, n1, n2)   # ≈ 22.3°

    # Entry point
    py = 2.8

    # Incoming ray
    ix1 = 0.2
    iy1 = py + (BX - ix1) * math.tan(math.radians(theta_i))
    ix2, iy2 = BX, py

    # Refracted ray
    rx2 = 6.0
    ry2 = py - (rx2 - BX) * math.tan(math.radians(theta_r))

    # Intended (counterfactual)
    cx2 = 6.0
    cy2 = py - (cx2 - BX) * math.tan(math.radians(theta_i))

    # ── Organizational boundary zone ──
    bw = 0.5
    org_rect = FancyBboxPatch((BX - bw/2, 0.2), bw, 4.7,
                              boxstyle="square,pad=0",
                              facecolor=NL, edgecolor=AM, linewidth=2.0,
                              alpha=0.82, zorder=3)
    ax.add_patch(org_rect)

    # Layer labels inside boundary
    for ly, label in [(3.7, 'BOARD'), (2.9, 'EXECUTIVE'), (2.1, 'MANAGEMENT'), (1.3, 'OPERATIONS')]:
        ax.text(BX, ly, label, ha='center', va='center',
                fontsize=4.5, color=AP, fontweight='bold', zorder=4, alpha=0.9)

    ax.text(BX, 4.65, 'ORGANIZATIONAL\nBOUNDARY', ha='center', va='top',
            fontsize=5.5, color=AM, fontweight='bold', zorder=4)

    # ── Normal line ──
    ax.plot([BX, BX], [0.5, 5.0], color=SL, lw=0.8,
            linestyle=(0, (4, 3)), alpha=0.6, zorder=4)
    ax.text(BX + 0.08, 4.9, 'NORMAL', ha='left', va='top',
            fontsize=5.0, color=SL, alpha=0.8)

    # ── Incoming ray (white) ──
    ray_seg(ax, ix1, iy1, ix2, iy2, color=WH, lw=3.0, zorder=5)
    draw_arrow_ray(ax, ix1 + 0.6*(ix2-ix1), iy1 + 0.6*(iy2-iy1),
                   ix2, iy2, color=WH, lw=3.0, zorder=6)

    # ── Intended direction (dashed slate) ──
    ray_seg(ax, BX, py, cx2, cy2, color=SL, lw=1.5, dashed=True, zorder=5)
    draw_arrow_ray(ax, BX + 0.6*(cx2-BX), py + 0.6*(cy2-py),
                   cx2, cy2, color=SL, lw=1.5, zorder=5)

    # ── Refracted ray (amber light) ──
    ray_seg(ax, BX, py, rx2, ry2, color=AL, lw=3.0, zorder=5)
    draw_arrow_ray(ax, BX + 0.6*(rx2-BX), py + 0.6*(ry2-py),
                   rx2, ry2, color=AL, lw=3.0, zorder=6)

    # ── Angle of incidence arc ──
    angle_arc(ax, BX, py, 0.7, 90, 90+theta_i, color=WH, lw=1.2)
    ax.text(BX - 0.2, py + 0.85, f'θ₁ = {theta_i:.0f}°\n(angle of incidence)',
            ha='right', va='bottom', fontsize=6.0, color=WH, fontweight='bold')

    # ── Angle of refraction arc ──
    angle_arc(ax, BX, py, 0.55, 90-theta_r, 90, color=AL, lw=1.2)
    ax.text(BX + 0.18, py - 0.7,
            f'θ₂ = {theta_r:.1f}°\n(angle of refraction)',
            ha='left', va='top', fontsize=6.0, color=AL, fontweight='bold')

    # ── Snell's Law annotation ──
    ax.text(5.5, 4.9,
            f'Snell\'s Law:\nn₁ sin θ₁ = n₂ sin θ₂\n\n'
            f'n₁ (environment) = {n1:.1f}\n'
            f'n₂ (organization) = {n2:.1f}',
            ha='right', va='top', fontsize=6.0, color=NM,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=AP, edgecolor=AM, lw=1.2))

    # ── Refractive index labels ──
    ax.text(1.2, 0.6, f'ENVIRONMENT\nn₁ = {n1:.1f}',
            ha='center', fontsize=6.5, color=SL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=BG, edgecolor=SL, lw=0.8))
    ax.text(4.8, 0.6, f'ORGANIZATION\nn₂ = {n2:.1f}',
            ha='center', fontsize=6.5, color=AL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor=NM, edgecolor=AM, lw=0.8))

    # ── Gap indicator at right edge ──
    gx = 5.8
    gy_i = cy2
    gy_r = ry2
    ax.annotate('', xy=(gx, gy_i), xytext=(gx, gy_r),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5, mutation_scale=8),
                zorder=7)
    ax.text(gx + 0.1, (gy_i+gy_r)/2, 'DEVIATION\nGAP',
            ha='left', va='center', fontsize=5.5, color=AP, fontweight='bold')

    # ── Ray labels ──
    ax.text(ix1 - 0.08, iy1, 'STRATEGY\nAS DESIGNED', ha='right', va='top',
            fontsize=6.5, color=WH, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=ND, edgecolor=WH, lw=0.6))
    ax.text(rx2 + 0.08, ry2, 'STRATEGY\nAS DELIVERED', ha='left', va='top',
            fontsize=6.5, color=AL, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=NM, edgecolor=AL, lw=0.6))
    ax.text(cx2 + 0.08, cy2, 'INTENDED\nDESTINATION', ha='left', va='bottom',
            fontsize=5.8, color=SL, style='italic')

    add_caption(fig, 3, 1,
                'Core organizational refraction model: strategy enters the organizational medium '
                'and bends away from its intended direction. '
                f'Refractive index n₂={n2} vs environment n₁={n1}; '
                f'deviation angle Δθ = {theta_i - theta_r:.1f}°.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch03-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch03 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 4 — Hierarchical Refraction (Challenger case)
# Multi-layer refraction: each authority layer bends the signal further
# ════════════════════════════════════════════════════════════════════════════
def ch04():
    fig, ax = plt.subplots(figsize=(6.0, 5.0), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(-0.2, 6.2)
    ax.set_ylim(0, 5.0)

    # Four hierarchy layers — vertical strips
    layers = [
        (1.0, 1.2, 'C-SUITE',        'n = 1.2', 1.2),
        (2.4, 1.2, 'VP LAYER',       'n = 1.5', 1.5),
        (3.8, 1.2, 'MIDDLE MGMT',    'n = 1.8', 1.8),
        (5.2, 1.0, 'FRONT LINE',     'n = 2.1', 2.1),
    ]

    # Draw layers
    for lx, lw, name, ri, n in layers:
        r = FancyBboxPatch((lx, 0.4), lw, 4.0,
                           boxstyle="square,pad=0",
                           facecolor=NL, edgecolor=AM, linewidth=1.5,
                           alpha=0.7 + 0.07*(n-1), zorder=3)
        ax.add_patch(r)
        ax.text(lx + lw/2, 4.15, name, ha='center', va='bottom',
                fontsize=5.5, color=WH, fontweight='bold', zorder=4)
        ax.text(lx + lw/2, 0.25, ri, ha='center', va='top',
                fontsize=5.5, color=AL, zorder=4)

    # "Environment" label on left
    ax.text(0.5, 4.15, 'EXTERNAL\nENVIRONMENT', ha='center', va='bottom',
            fontsize=5.5, color=SL, fontweight='bold')
    ax.text(0.5, 0.25, 'n = 1.0', ha='center', va='top', fontsize=5.5, color=SL)

    # Trace the ray through all layers using Snell's Law cumulatively
    # Ray going right, entering from left
    # Angles from normal (vertical/y-axis since layers are vertical)
    # Actually layers are vertical so normal is horizontal
    # Let's compute: start angle θ₀ = 25° from horizontal normal

    entry_angles = [25.0]   # θ from normal (horizontal)
    ns = [1.0, 1.2, 1.5, 1.8, 2.1]
    for i in range(1, len(ns)):
        sin_r = ns[i-1] * math.sin(math.radians(entry_angles[-1])) / ns[i]
        sin_r = min(sin_r, 1.0)
        entry_angles.append(math.degrees(math.asin(sin_r)))

    # x-positions of boundaries
    bx_positions = [1.0, 2.4, 3.8, 5.2, 6.2]
    # Starting point: x=0, y=center
    px, py = 0.0, 2.7

    points = [(px, py)]
    for i, bx in enumerate(bx_positions):
        angle = entry_angles[i]
        dy = (bx - px) * math.tan(math.radians(angle))
        ny = py - dy   # going downward (refracted away from normal)
        points.append((bx, ny))
        px, py = bx, ny

    # Draw ray segments
    for i in range(len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        col = WH if i == 0 else AL
        lw = 2.5
        ax.plot([x1, x2], [y1, y2], color=col, lw=lw, zorder=5)
        # Arrowhead midway
        mx = (x1+x2)/2; my = (y1+y2)/2
        draw_arrow_ray(ax, mx, my, x2, y2, color=col, lw=lw, zorder=6)

    # Intended path (straight dashed from entry to end)
    ix1, iy1 = 0.0, 2.7
    ix2 = 6.2
    iy2 = iy1 - (ix2 - ix1) * math.tan(math.radians(25.0))
    ray_seg(ax, ix1, iy1, ix2, iy2, color=SL, lw=1.2, dashed=True, zorder=4)
    draw_arrow_ray(ax, ix1 + 0.8*(ix2-ix1), iy1 + 0.8*(iy2-iy1),
                   ix2, iy2, color=SL, lw=1.2, zorder=5)

    # Angle labels at each boundary
    for i, bx in enumerate(bx_positions[:-1]):
        by = points[i+1][1]
        a = entry_angles[i+1]
        ax.text(bx + 0.05, by + 0.18, f'θ={a:.1f}°',
                ha='left', va='bottom', fontsize=5.0, color=AP, zorder=6)

    # Final gap indicator
    gx = 6.1
    gy_i = iy2
    gy_r = points[-1][1]
    if abs(gy_r - gy_i) > 0.05:
        ax.annotate('', xy=(gx, gy_i), xytext=(gx, gy_r),
                    arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5, mutation_scale=8),
                    zorder=7)
        ax.text(gx + 0.05, (gy_i+gy_r)/2, f'Δ = {abs(gy_r-gy_i):.2f}',
                ha='left', va='center', fontsize=5.5, color=AP, fontweight='bold')

    ax.text(0.0, 2.85, 'STRATEGY\nINTENT', ha='left', va='bottom',
            fontsize=6.0, color=WH, fontweight='bold')

    add_caption(fig, 4, 1,
                'Hierarchical refraction (Challenger case): each authority layer '
                'carries a higher refractive index, bending the signal cumulatively '
                'until the strategy at front-line level is unrecognizable from its original aim.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch04-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch04 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 5 — Cultural Refraction (Wells Fargo)
# Culture as a wide, dense refractive medium
# ════════════════════════════════════════════════════════════════════════════
def ch05():
    fig, ax = plt.subplots(figsize=(5.8, 4.5), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 5.8)
    ax.set_ylim(0, 4.5)

    # Wide cultural medium (thick band from x=1.4 to x=4.4)
    MX1, MX2 = 1.4, 4.4
    mw = MX2 - MX1

    # Cultural medium fill
    culture_box = FancyBboxPatch((MX1, 0.4), mw, 3.7,
                                 boxstyle="square,pad=0",
                                 facecolor=NM, edgecolor=AM, linewidth=2.0,
                                 alpha=0.9, zorder=3)
    ax.add_patch(culture_box)

    # Cultural texture — subtle diagonal lines
    for yi in np.arange(0.4, 4.1, 0.25):
        ax.plot([MX1, MX2], [yi, yi], color=NL, lw=0.4, alpha=0.4, zorder=3)

    ax.text((MX1+MX2)/2, 3.8, 'CULTURAL MEDIUM',
            ha='center', va='bottom', fontsize=8, color=AL,
            fontweight='bold', zorder=5)
    ax.text((MX1+MX2)/2, 3.55, '"Revenue at all costs"  (Wells Fargo n = 2.4)',
            ha='center', va='bottom', fontsize=5.5, color=AP, zorder=5)

    # Boundaries labeled
    ax.text(MX1, 0.25, 'ENTRY\nBOUNDARY', ha='center', va='top',
            fontsize=5.5, color=AM, fontweight='bold', zorder=5)
    ax.text(MX2, 0.25, 'EXIT\nBOUNDARY', ha='center', va='top',
            fontsize=5.5, color=AM, fontweight='bold', zorder=5)

    # Snell's Law with n_culture = 2.4
    theta_i = 30.0
    n_env, n_cult = 1.0, 2.4
    theta_m = snell_refract(theta_i, n_env, n_cult)   # entering culture
    theta_out = snell_refract(theta_m, n_cult, n_env)  # exiting culture (= theta_i by reversibility)

    entry_y = 2.6

    # Incoming
    ix1, iy1 = 0.1, entry_y + (MX1-0.1)*math.tan(math.radians(theta_i))
    ax.plot([ix1, MX1], [iy1, entry_y], color=WH, lw=2.5, zorder=5)
    draw_arrow_ray(ax, ix1+0.6*(MX1-ix1), iy1+0.6*(entry_y-iy1),
                   MX1, entry_y, color=WH, lw=2.5, zorder=6)

    # Inside medium
    mid_x = (MX1 + MX2) / 2
    mid_y = entry_y - (mid_x - MX1) * math.tan(math.radians(theta_m))
    ax.plot([MX1, MX2], [entry_y, mid_y], color=AL, lw=2.5, zorder=5)
    draw_arrow_ray(ax, MX1+0.5*(MX2-MX1), entry_y+0.5*(mid_y-entry_y),
                   MX2, mid_y, color=AL, lw=2.5, zorder=6)

    # Exiting (bends back to θ_i but is displaced)
    exit_y = mid_y
    ex2 = 5.5
    ey2 = exit_y - (ex2 - MX2) * math.tan(math.radians(theta_i))
    ax.plot([MX2, ex2], [exit_y, ey2], color=AL, lw=2.5, zorder=5)
    draw_arrow_ray(ax, MX2+0.5*(ex2-MX2), exit_y+0.5*(ey2-exit_y),
                   ex2, ey2, color=AL, lw=2.5, zorder=6)

    # Intended path (straight through)
    intent_y_end = entry_y - (ex2 - ix1) * math.tan(math.radians(theta_i))
    ray_seg(ax, MX1, entry_y, ex2, entry_y - (ex2-MX1)*math.tan(math.radians(theta_i)),
            color=SL, lw=1.2, dashed=True, zorder=4)
    draw_arrow_ray(ax, MX1+0.7*(ex2-MX1), entry_y+0.7*(intent_y_end-entry_y-0.1),
                   ex2, entry_y - (ex2-MX1)*math.tan(math.radians(theta_i)),
                   color=SL, lw=1.2, zorder=5)

    # Normal lines at boundaries
    for nx in [MX1, MX2]:
        ax.plot([nx, nx], [0.6, 3.9], color=SL, lw=0.7,
                linestyle=(0,(4,3)), alpha=0.5, zorder=4)

    # Angle labels
    ax.text(MX1 - 0.1, entry_y + 0.45, f'θ={theta_i:.0f}°',
            ha='right', va='bottom', fontsize=6.5, color=WH, fontweight='bold')
    ax.text(MX1 + 0.15, entry_y - 0.3, f'θ={theta_m:.1f}°',
            ha='left', va='top', fontsize=6.5, color=AL, fontweight='bold')

    # Lateral displacement label
    gx = 5.4
    gy_intended = entry_y - (gx - MX1) * math.tan(math.radians(theta_i))
    gy_actual = exit_y - (gx - MX2) * math.tan(math.radians(theta_i))
    ax.annotate('', xy=(gx, gy_intended), xytext=(gx, gy_actual),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5, mutation_scale=8), zorder=7)
    ax.text(gx + 0.08, (gy_intended+gy_actual)/2,
            'LATERAL\nDISPLACEMENT\n(cultural drift)',
            ha='left', va='center', fontsize=5.5, color=AP, fontweight='bold')

    ax.text(0.1, iy1 + 0.08, 'EXECUTIVE\nDIRECTIVE', ha='left', va='bottom',
            fontsize=6.5, color=WH, fontweight='bold')
    ax.text(ex2 + 0.05, ey2, 'FRONT-LINE\nBEHAVIOR', ha='left', va='center',
            fontsize=6.5, color=AL, fontweight='bold')

    add_caption(fig, 5, 1,
                'Cultural refraction (Wells Fargo): the "revenue at all costs" culture '
                '(n=2.4) acts as a dense medium that laterally displaces the executive directive '
                '— the output angle equals the input angle, but the destination has shifted entirely.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch05-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch05 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 6 — Process Refraction (GE Vitality Curve)
# Process pipeline as a sequence of small refracting nodes
# ════════════════════════════════════════════════════════════════════════════
def ch06():
    fig, ax = plt.subplots(figsize=(6.0, 4.2), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 6.0)
    ax.set_ylim(0, 4.2)

    # Process nodes (pipeline steps that each add a small refraction)
    process_steps = [
        (1.1, 'BUDGETING\nPROCESS',   0.12),
        (2.1, 'HR RANKING\nCYCLE',     0.18),
        (3.1, 'PERFORMANCE\nREVIEW',   0.22),
        (4.1, 'COMPENSATION\nTIER',    0.15),
        (5.1, 'PROMOTION\nGATEKEEP',   0.20),
    ]

    entry_x = 0.2
    entry_y = 2.8
    current_x = entry_x
    current_y = entry_y
    current_angle = 12.0  # degrees from horizontal

    # Draw intent line (straight horizontal dashed)
    ray_seg(ax, entry_x, entry_y, 5.8, entry_y - (5.8-entry_x)*math.tan(math.radians(current_angle)),
            color=SL, lw=1.2, dashed=True, zorder=4)

    path_points = [(current_x, current_y)]
    angles = [current_angle]

    for px, label, delta_angle in process_steps:
        next_y = current_y - (px - current_x) * math.tan(math.radians(current_angle))
        path_points.append((px, next_y))
        current_angle += delta_angle * 180 / math.pi * 1.8  # additive refraction
        current_x = px
        current_y = next_y
        angles.append(current_angle)

    # Final exit
    ex = 5.8
    ey = current_y - (ex - current_x) * math.tan(math.radians(current_angle))
    path_points.append((ex, ey))

    # Draw the full ray path
    for i in range(len(path_points)-1):
        x1, y1 = path_points[i]
        x2, y2 = path_points[i+1]
        col = WH if i == 0 else AL
        lw = 2.5 if i == 0 else 2.5
        ax.plot([x1, x2], [y1, y2], color=col, lw=lw, zorder=5)
        draw_arrow_ray(ax, x1+0.6*(x2-x1), y1+0.6*(y2-y1), x2, y2, color=col, lw=lw, zorder=6)

    # Draw process nodes
    node_r = 0.22
    for i, (px, label, _) in enumerate(process_steps):
        py_node = path_points[i+1][1]
        circle = plt.Circle((px, py_node), node_r,
                             facecolor=NL, edgecolor=AM, linewidth=1.8, zorder=7)
        ax.add_patch(circle)
        ax.text(px, py_node, str(i+1), ha='center', va='center',
                fontsize=8, color=WH, fontweight='bold', zorder=8)
        ax.text(px, py_node - node_r - 0.08, label,
                ha='center', va='top', fontsize=5.0, color=AM, fontweight='bold', zorder=8)

    # Gap at exit
    intent_y_end = entry_y - (ex - entry_x) * math.tan(math.radians(12.0))
    ax.annotate('', xy=(ex, intent_y_end), xytext=(ex, ey),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5, mutation_scale=8), zorder=7)
    ax.text(ex + 0.05, (intent_y_end + ey)/2, 'PROCESS\nDISTORTION\nGAP',
            ha='left', va='center', fontsize=5.5, color=AP, fontweight='bold')

    # Labels
    ax.text(entry_x - 0.05, entry_y + 0.12, 'PERFORMANCE\nSTRATEGY\n(GE intent)',
            ha='left', va='bottom', fontsize=6.5, color=WH, fontweight='bold')
    ax.text(5.85, ey - 0.05, 'VITALITY CURVE\nOUTCOME', ha='left', va='top',
            fontsize=6.0, color=AL, fontweight='bold')
    ax.text(5.85, intent_y_end + 0.05, 'Intended\noutcome', ha='left', va='bottom',
            fontsize=5.5, color=SL, style='italic')

    # Legend
    ax.text(0.3, 0.35, 'Each process node (① – ⑤) refracts the signal by a small angle; '
            'cumulative distortion is large.',
            ha='left', va='bottom', fontsize=5.5, color=SL, style='italic')

    add_caption(fig, 6, 1,
                'Process refraction (GE Vitality Curve): sequential process gates each '
                'introduce a small angular distortion; the compounded effect redirects '
                'the performance strategy toward unintended ranking behaviors.')
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch06-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch06 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 7 — Compound Refraction
# Stacked hierarchy + culture + process + political layers, cumulative deviation
# ════════════════════════════════════════════════════════════════════════════
def ch07():
    fig, ax = plt.subplots(figsize=(6.0, 5.2), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 6.0)
    ax.set_ylim(0, 5.2)

    # Stacked horizontal layers (compound refraction)
    layers = [
        (4.6, 0.5, 'POLITICAL LAYER',   'n = 1.3', 1.3, '#1A3455'),
        (3.8, 0.7, 'PROCESS LAYER',     'n = 1.6', 1.6, '#1E3D66'),
        (2.8, 0.9, 'CULTURAL LAYER',    'n = 2.0', 2.0, '#204875'),
        (1.6, 1.1, 'HIERARCHICAL\nLAYER', 'n = 2.5', 2.5, '#1E4480'),
    ]

    # Draw layers (horizontal bands, bottom to top)
    for ly, lh, lname, ri, n, fc in layers:
        r = FancyBboxPatch((0.2, ly), 5.5, lh,
                           boxstyle="square,pad=0",
                           facecolor=fc, edgecolor=AM, linewidth=1.3,
                           alpha=0.9, zorder=3)
        ax.add_patch(r)
        ax.text(0.35, ly + lh/2, lname, ha='left', va='center',
                fontsize=6.0, color=WH, fontweight='bold', zorder=4)
        ax.text(5.55, ly + lh/2, ri, ha='right', va='center',
                fontsize=5.5, color=AL, zorder=4)

    # Entry region label
    ax.text(3.0, 5.0, 'STRATEGY ENTRY\n(External Environment, n = 1.0)',
            ha='center', va='top', fontsize=6.5, color=SL, fontweight='bold')

    # Execution region label
    ax.text(3.0, 0.22, 'EXECUTION LAYER  (Target Destination)',
            ha='center', va='top', fontsize=6.0, color=SL)

    # Compute cumulative refraction through layers
    ns = [1.0, 2.5, 2.0, 1.6, 1.3]
    theta = 30.0  # initial angle from vertical normal
    boundaries_y = [4.7, 2.7, 1.6, 0.9, 0.4]  # top of each layer + exit
    px, py = 3.0, 4.7
    points = [(px, py)]
    thetas = [theta]

    for i in range(len(ns)-1):
        t_new = snell_refract(theta, ns[i], ns[i+1])
        if t_new is None:
            t_new = 90.0  # shouldn't happen here
        by = boundaries_y[i+1]
        # ray goes downward; horizontal displacement = (dy) * tan(theta)
        dy = py - by
        nx = px + dy * math.tan(math.radians(theta))
        points.append((nx, by))
        px, py = nx, by
        theta = t_new
        thetas.append(theta)

    # Intended vertical path (straight down from entry)
    int_x = 3.0
    ray_seg(ax, 3.0, 4.7, 3.0, 0.5, color=SL, lw=1.2, dashed=True, zorder=4)
    draw_arrow_ray(ax, 3.0, 4.7, 3.0, 0.5, color=SL, lw=1.2, zorder=5)

    # Draw actual compound ray
    for i in range(len(points)-1):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        col = WH if i == 0 else AL
        ax.plot([x1, x2], [y1, y2], color=col, lw=2.5, zorder=6)
        draw_arrow_ray(ax, x1+0.6*(x2-x1), y1+0.6*(y2-y1), x2, y2, color=col, lw=2.5, zorder=7)

    # Final deviation marker
    fx, fy = points[-1]
    ax.annotate('', xy=(3.0, 0.5), xytext=(fx, 0.5),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.8, mutation_scale=10), zorder=8)
    ax.text((3.0+fx)/2, 0.35, f'COMPOUND DEVIATION: {abs(fx-3.0):.2f} units',
            ha='center', va='top', fontsize=6.0, color=AP, fontweight='bold', zorder=8)

    # Entry label
    ax.text(3.05, 4.85, 'STRATEGY AS\nDESIGNED', ha='left', va='top',
            fontsize=6.5, color=WH, fontweight='bold')

    # Total refraction label
    total_dev = abs(fx - 3.0)
    ax.text(5.7, 2.5,
            f'n₁ = 1.0 → n₄ = 1.3\n'
            f'4 refracting layers\n'
            f'Δx = {total_dev:.2f} units',
            ha='right', va='center', fontsize=6.0, color=AP,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=NM, edgecolor=AM, lw=1.0))

    add_caption(fig, 7, 1,
                'Compound refraction: hierarchical, cultural, process, and political layers '
                'stack to produce a cumulative deviation far greater than any single layer alone. '
                'Even modest individual refractions combine to redirect strategy entirely.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch07-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch07 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 8 — Total Internal Reflection
# Strategy trapped inside org — never reaches execution layer
# ════════════════════════════════════════════════════════════════════════════
def ch08():
    fig, ax = plt.subplots(figsize=(5.8, 5.0), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 5.8)
    ax.set_ylim(0, 5.0)

    # Dense organizational medium (upper zone, n_org > n_exec)
    n_org, n_exec = 1.8, 1.0
    theta_c = critical_angle(n_org, n_exec)   # ≈ 33.75°
    theta_incident = 50.0   # > critical angle → TIR

    # Execution boundary: horizontal line at y = 1.5
    BY = 1.5

    # Medium fill
    org_med = FancyBboxPatch((0.2, BY), 5.4, 3.2,
                             boxstyle="square,pad=0",
                             facecolor=NM, edgecolor=AM, linewidth=2.0,
                             alpha=0.88, zorder=3)
    ax.add_patch(org_med)

    # Execution zone (below boundary)
    exec_zone = FancyBboxPatch((0.2, 0.2), 5.4, BY - 0.2,
                               boxstyle="square,pad=0",
                               facecolor='#0A1520', edgecolor=SL, linewidth=1.0,
                               alpha=0.7, zorder=3)
    ax.add_patch(exec_zone)

    # Labels
    ax.text(2.9, BY + 3.0, 'ORGANIZATIONAL MEDIUM',
            ha='center', va='top', fontsize=7, color=AL, fontweight='bold', zorder=5)
    ax.text(2.9, BY + 2.75, f'(n = {n_org})', ha='center', va='top',
            fontsize=6, color=AP, zorder=5)
    ax.text(2.9, 0.45, 'EXECUTION LAYER  (unreachable)',
            ha='center', va='bottom', fontsize=6.5, color=SL, style='italic', zorder=5)
    ax.text(2.9, 0.25, f'(n = {n_exec})', ha='center', va='bottom',
            fontsize=5.5, color=SL, zorder=5)

    # Normal line at bounce point
    bounce_x = 2.9
    ax.plot([bounce_x, bounce_x], [0.3, 3.5], color=SL, lw=0.8,
            linestyle=(0,(4,3)), alpha=0.6, zorder=4)
    ax.text(bounce_x + 0.05, 3.45, 'NORMAL', ha='left', va='top',
            fontsize=5.0, color=SL, alpha=0.8)

    # Incident ray (downward, from upper-left)
    # Angle measured from normal (vertical)
    # Ray going downward-right at θ_incident from vertical
    ix1 = bounce_x - BY * math.tan(math.radians(theta_incident))
    iy1 = BY + BY   # above boundary
    ix2, iy2 = bounce_x, BY

    ax.plot([ix1, ix2], [iy1, iy2], color=WH, lw=2.5, zorder=5)
    draw_arrow_ray(ax, ix1+0.6*(ix2-ix1), iy1+0.6*(iy2-iy1),
                   ix2, iy2, color=WH, lw=2.5, zorder=6)

    # Reflected ray (symmetric about normal)
    rx2 = bounce_x + (iy1 - BY) * math.tan(math.radians(theta_incident))
    ry2 = iy1

    ax.plot([ix2, rx2], [BY, ry2], color=AL, lw=2.5, zorder=5)
    draw_arrow_ray(ax, ix2+0.5*(rx2-ix2), BY+0.5*(ry2-BY),
                   rx2, ry2, color=AL, lw=2.5, zorder=6)

    # Transmitted (evanescent / would-be) ray — very faint dashed
    # This is what WOULD happen below critical angle — show faint
    theta_ghost = 25.0  # a sub-critical angle ray for comparison
    gx1 = bounce_x - BY * math.tan(math.radians(theta_ghost))
    gy1 = BY + BY
    ax.plot([gx1, bounce_x], [gy1, BY], color=SL, lw=1.2,
            linestyle=(0,(6,4)), alpha=0.5, zorder=4)

    theta_refr_ghost = snell_refract(theta_ghost, n_org, n_exec)
    if theta_refr_ghost:
        gex = bounce_x + 1.0 * math.tan(math.radians(theta_refr_ghost))
        ax.plot([bounce_x, gex], [BY, BY - 1.0], color=SL, lw=1.2,
                linestyle=(0,(6,4)), alpha=0.5, zorder=4)
        ax.text(gex + 0.05, BY - 1.0, '(sub-critical:\nstrategy penetrates)',
                ha='left', va='center', fontsize=5.0, color=SL, style='italic', alpha=0.7)

    # Angle labels
    angle_arc(ax, bounce_x, BY, 0.6, 90, 90+theta_incident, color=WH, lw=1.0)
    ax.text(bounce_x - 0.15, BY + 0.75, f'θ = {theta_incident:.0f}°',
            ha='right', va='bottom', fontsize=6.5, color=WH, fontweight='bold')

    angle_arc(ax, bounce_x, BY, 0.6, 90-theta_incident, 90, color=AL, lw=1.0)
    ax.text(bounce_x + 0.15, BY + 0.75, f'θ = {theta_incident:.0f}°',
            ha='left', va='bottom', fontsize=6.5, color=AL, fontweight='bold')

    # Critical angle label
    ax.text(0.35, BY - 0.22,
            f'Critical angle θc = {theta_c:.1f}°\n'
            f'Strategy angle θ = {theta_incident:.0f}° > θc → Total Internal Reflection',
            ha='left', va='top', fontsize=5.8, color=AP,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=NM, edgecolor=AM, lw=1.2),
            zorder=8)

    # Ray labels
    ax.text(ix1 - 0.08, iy1, 'STRATEGY\nDIRECTIVE', ha='right', va='top',
            fontsize=6.5, color=WH, fontweight='bold')
    ax.text(rx2 + 0.08, ry2, 'REFLECTED:\nStrategy sent back\nto leadership',
            ha='left', va='top', fontsize=6.0, color=AL, fontweight='bold')

    # Execution unreachable indicator
    ax.text(2.9, 0.9, '✗  Strategy never penetrates\n      to execution layer',
            ha='center', va='center', fontsize=6.5, color='#C04040',
            fontweight='bold', zorder=8)

    add_caption(fig, 8, 1,
                f'Total internal reflection: when the organizational refractive index exceeds '
                f'the critical threshold (θ > θc = {theta_c:.1f}°), strategy is reflected entirely '
                f'back into the leadership layer and never reaches execution.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch08-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch08 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 9 — Refractive Profile
# Spider/radar chart for self-assessment
# ════════════════════════════════════════════════════════════════════════════
def ch09():
    fig, ax = plt.subplots(figsize=(5.2, 5.0), dpi=DPI,
                           subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    dimensions = [
        'Hierarchical\nRefraction', 'Cultural\nRefraction',
        'Process\nRefraction', 'Political\nRefraction',
        'Temporal\nRefraction', 'Communication\nRefraction',
    ]

    n = len(dimensions)
    angles = np.linspace(0, 2*np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    # Sample organization profile (0–5 scale, 5 = highest refraction)
    sample_vals = [3.8, 4.2, 2.9, 3.5, 2.1, 3.0]
    target_vals  = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5]  # ideal low-refraction target
    sample_vals += sample_vals[:1]
    target_vals  += target_vals[:1]

    # Grid circles
    for r in [1, 2, 3, 4, 5]:
        ax.plot(angles, [r]*len(angles), color=SL, lw=0.5, alpha=0.3)
        if r < 5:
            ax.text(0, r + 0.05, str(r), ha='center', va='bottom',
                    fontsize=5.5, color=SL, alpha=0.7)

    # Spoke lines
    for angle in angles[:-1]:
        ax.plot([angle, angle], [0, 5], color=SL, lw=0.5, alpha=0.3)

    # Fill area — actual profile
    ax.fill(angles, sample_vals, color=AL, alpha=0.3)
    ax.plot(angles, sample_vals, color=AL, lw=2.5, zorder=5)
    for i, (a, v) in enumerate(zip(angles[:-1], sample_vals[:-1])):
        ax.scatter(a, v, s=45, color=AL, zorder=6)

    # Fill area — target profile
    ax.fill(angles, target_vals, color='#2A7A2A', alpha=0.2)
    ax.plot(angles, target_vals, color='#2A7A2A', lw=1.5, linestyle='--', zorder=5)

    # Dimension labels
    for i, (angle, dim) in enumerate(zip(angles[:-1], dimensions)):
        x = (5.4) * np.cos(angle - np.pi/2)
        y = (5.4) * np.sin(angle - np.pi/2)
        ha = 'center'
        if np.cos(angle) < -0.1: ha = 'right'
        elif np.cos(angle) > 0.1: ha = 'left'
        ax.text(angle, 5.8, dim, ha='center', va='center',
                fontsize=6.5, color=BT, fontweight='bold',
                transform=ax.transData)

    # Max refraction labels
    ax.set_ylim(0, 5)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.spines['polar'].set_visible(False)
    ax.grid(False)

    # Legend
    legend_elements = [
        Line2D([0], [0], color=AL, lw=2.5, label='Organization profile'),
        Line2D([0], [0], color='#2A7A2A', lw=1.5, linestyle='--', label='Target (low-refraction)'),
    ]
    ax.legend(handles=legend_elements, loc='lower center',
              bbox_to_anchor=(0.5, -0.12), ncol=2,
              fontsize=6.5, framealpha=0.85,
              facecolor=BG, edgecolor=SL)

    # Score labels on spokes
    for i, (angle, val) in enumerate(zip(angles[:-1], sample_vals[:-1])):
        ax.text(angle, val + 0.3, f'{val:.1f}',
                ha='center', va='bottom', fontsize=6, color=AL, fontweight='bold')

    ax.set_title('ORGANIZATIONAL REFRACTIVE PROFILE', pad=18,
                 fontsize=9, fontweight='bold', color=ND)

    fig.text(0.5, 0.015,
             'Figure 9.1  —  Refractive profile instrument: score each dimension 0–5 '
             '(5 = maximum distortion). The shaded area shows '
             'compound refraction risk.',
             ha='center', va='bottom', fontsize=6.5, color=SL)
    fig.tight_layout(rect=[0, 0.04, 1, 0.97])
    fig.savefig(os.path.join(OUT, 'ch09-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch09 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 10 — Correcting the Angle
# A corrective prism/lens that restores the signal direction
# ════════════════════════════════════════════════════════════════════════════
def ch10():
    fig, ax = plt.subplots(figsize=(6.0, 4.5), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 6.0)
    ax.set_ylim(0, 4.5)

    # ── Without correction (top half) ──────────────────────────────────────
    ax.text(3.0, 4.35, 'WITHOUT CORRECTION', ha='center', va='top',
            fontsize=7, color='#B82020', fontweight='bold')

    # Simple refraction (no lens) — top diagram
    theta_i = 35.0
    n1, n2 = 1.0, 1.7
    theta_r = snell_refract(theta_i, n1, n2)
    bx_top = 2.8
    py_top = 3.5

    # Medium
    med_top = FancyBboxPatch((bx_top - 0.2, 2.5), 0.4, 1.5,
                             boxstyle="square,pad=0",
                             facecolor=NL, edgecolor=AM, linewidth=1.2, alpha=0.7, zorder=3)
    ax.add_patch(med_top)

    # Incoming
    ix1, iy1 = 0.4, py_top + 2.3*math.tan(math.radians(theta_i))
    ax.plot([ix1, bx_top], [iy1, py_top], color=WH, lw=2.5, zorder=5)
    draw_arrow_ray(ax, ix1+0.5*(bx_top-ix1), iy1+0.5*(py_top-iy1),
                   bx_top, py_top, color=WH, lw=2.5, zorder=6)

    # Refracted (deviating)
    rx2_t = 5.6
    ry2_t = py_top - (rx2_t - bx_top)*math.tan(math.radians(theta_r))
    ax.plot([bx_top, rx2_t], [py_top, ry2_t], color=AL, lw=2.5, zorder=5)
    draw_arrow_ray(ax, bx_top+0.6*(rx2_t-bx_top), py_top+0.6*(ry2_t-py_top),
                   rx2_t, ry2_t, color=AL, lw=2.5, zorder=6)

    # Intended
    cy2_t = py_top - (rx2_t - bx_top)*math.tan(math.radians(theta_i))
    ray_seg(ax, bx_top, py_top, rx2_t, cy2_t, color=SL, lw=1.0, dashed=True, zorder=4)

    ax.annotate('', xy=(rx2_t, cy2_t), xytext=(rx2_t, ry2_t),
                arrowprops=dict(arrowstyle='<->', color=AP, lw=1.5, mutation_scale=8), zorder=7)
    ax.text(rx2_t + 0.05, (cy2_t+ry2_t)/2, 'Gap', ha='left', va='center',
            fontsize=6.0, color=AP, fontweight='bold')

    # ── Divider ─────────────────────────────────────────────────────────────
    ax.plot([0.2, 5.8], [2.2, 2.2], color=SL, lw=0.8, linestyle='--', alpha=0.6)

    # ── With correction (bottom half) ──────────────────────────────────────
    ax.text(3.0, 2.1, 'WITH CORRECTIVE LENS (Intervention)', ha='center', va='top',
            fontsize=7, color='#1A7A3C', fontweight='bold')

    # Entry medium
    bx_bot1 = 1.8
    bx_bot2 = 3.8   # corrective lens position
    py_bot = 1.2

    med_bot = FancyBboxPatch((bx_bot1 - 0.2, 0.4), 0.4, 1.5,
                             boxstyle="square,pad=0",
                             facecolor=NL, edgecolor=AM, linewidth=1.2, alpha=0.7, zorder=3)
    ax.add_patch(med_bot)

    # Corrective lens (prism shape)
    lens_pts = np.array([
        [bx_bot2 - 0.15, 0.35],
        [bx_bot2 + 0.15, 0.35],
        [bx_bot2 + 0.15, 1.85],
        [bx_bot2 - 0.15, 1.85],
    ])
    lens_patch = Polygon(lens_pts, closed=True,
                         facecolor='#2A5A2A', edgecolor='#3A9A3A', linewidth=1.5,
                         alpha=0.85, zorder=3)
    ax.add_patch(lens_patch)
    ax.text(bx_bot2, 1.95, 'CORRECTIVE\nINTERVENTION', ha='center', va='bottom',
            fontsize=5.5, color='#3A9A3A', fontweight='bold', zorder=5)

    # Incoming
    iix1, iiy1 = 0.3, py_bot + (bx_bot1-0.3)*math.tan(math.radians(theta_i))
    ax.plot([iix1, bx_bot1], [iiy1, py_bot], color=WH, lw=2.5, zorder=5)
    draw_arrow_ray(ax, iix1+0.5*(bx_bot1-iix1), iiy1+0.5*(py_bot-iiy1),
                   bx_bot1, py_bot, color=WH, lw=2.5, zorder=6)

    # After first medium (refracted)
    ry_mid = py_bot - (bx_bot2 - bx_bot1)*math.tan(math.radians(theta_r))
    ax.plot([bx_bot1, bx_bot2], [py_bot, ry_mid], color=AL, lw=2.0, zorder=5)
    draw_arrow_ray(ax, bx_bot1+0.5*(bx_bot2-bx_bot1), py_bot+0.5*(ry_mid-py_bot),
                   bx_bot2, ry_mid, color=AL, lw=2.0, zorder=6)

    # After corrective lens — restored to original angle
    crx2 = 5.6
    cry2 = ry_mid - (crx2 - bx_bot2)*math.tan(math.radians(theta_i))
    ax.plot([bx_bot2, crx2], [ry_mid, cry2], color='#3ADA3A', lw=2.5, zorder=5)
    draw_arrow_ray(ax, bx_bot2+0.6*(crx2-bx_bot2), ry_mid+0.6*(cry2-ry_mid),
                   crx2, cry2, color='#3ADA3A', lw=2.5, zorder=6)

    # Intended line (what original trajectory would be)
    intent_y_end = py_bot - (crx2 - bx_bot1)*math.tan(math.radians(theta_i))
    ray_seg(ax, bx_bot1, py_bot, crx2, intent_y_end, color=SL, lw=1.0, dashed=True, zorder=4)

    ax.text(crx2 + 0.05, cry2, 'Corrected\ntrajectory', ha='left', va='center',
            fontsize=6.0, color='#3ADA3A', fontweight='bold')

    # Annotate correction effect
    ax.annotate('', xy=(crx2, intent_y_end), xytext=(crx2, cry2),
                arrowprops=dict(arrowstyle='<->', color='#3ADA3A', lw=1.2, mutation_scale=7),
                zorder=7)
    ax.text(crx2 + 0.05, (intent_y_end+cry2)/2 - 0.1, 'Minimal\nresidual gap',
            ha='left', va='center', fontsize=5.5, color='#3ADA3A')

    add_caption(fig, 10, 1,
                'Correcting the angle: a targeted intervention (corrective lens) '
                'counteracts the organizational refraction, restoring the strategy '
                'signal toward its intended destination.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch10-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch10 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 11 — Refraction-Resistant Design
# Side-by-side: high-refraction vs low-refraction org design
# ════════════════════════════════════════════════════════════════════════════
def ch11():
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 5.0), dpi=DPI)
    fig.patch.set_facecolor(BG)

    configs = [
        {
            'ax': axes[0],
            'title': 'HIGH-REFRACTION\nORGANIZATION',
            'title_color': '#B82020',
            'layers': [
                ('BOARD', 1.8, 1.8),
                ('C-SUITE', 1.6, 1.6),
                ('SVP LAYER', 1.7, 1.4),
                ('VP LAYER', 1.5, 1.2),
                ('DIRECTORS', 1.4, 1.0),
                ('MANAGERS', 1.3, 0.8),
                ('EXECUTION', 1.1, 0.4),
            ],
            'n_vals': [1.0, 1.8, 1.6, 1.7, 1.5, 1.4, 1.3, 1.1],
            'theta_i': 20.0,
            'facecolor': '#1C2030',
            'edgecolor': '#B82020',
        },
        {
            'ax': axes[1],
            'title': 'LOW-REFRACTION\nORGANIZATION',
            'title_color': '#1A7A3C',
            'layers': [
                ('LEADERSHIP', 1.3, 1.8),
                ('TEAM LEADS', 1.15, 1.2),
                ('EXECUTION', 1.05, 0.6),
            ],
            'n_vals': [1.0, 1.3, 1.15, 1.05],
            'theta_i': 20.0,
            'facecolor': '#141E2A',
            'edgecolor': '#1A7A3C',
        },
    ]

    for cfg in configs:
        ax = cfg['ax']
        ax.set_facecolor(BG)
        ax.axis('off')
        ax.set_xlim(0, 3.0)
        ax.set_ylim(0, 5.0)

        # Title
        ax.text(1.5, 4.9, cfg['title'], ha='center', va='top',
                fontsize=7.5, color=cfg['title_color'], fontweight='bold')

        # Draw layers (horizontal bands)
        layer_ys = np.linspace(4.2, 0.6, len(cfg['layers'])+1)
        layer_h = (layer_ys[0] - layer_ys[-1]) / len(cfg['layers'])

        for i, (lname, n, _) in enumerate(cfg['layers']):
            ly = layer_ys[i+1]
            lh = layer_h - 0.05
            alpha = 0.55 + 0.06 * i
            r = FancyBboxPatch((0.1, ly), 2.8, lh,
                               boxstyle="square,pad=0",
                               facecolor=NM, edgecolor=cfg['edgecolor'],
                               linewidth=0.8, alpha=min(alpha, 0.95), zorder=3)
            ax.add_patch(r)
            ax.text(0.25, ly + lh/2, lname, ha='left', va='center',
                    fontsize=5.5, color=WH, fontweight='bold', zorder=4)
            ax.text(2.8, ly + lh/2, f'n={n:.2f}', ha='right', va='center',
                    fontsize=5.0, color=AL, zorder=4)

        # ── Trace ray ──
        ns = cfg['n_vals']
        theta = cfg['theta_i']
        py_start = layer_ys[0]
        px = 0.6

        points = [(px, py_start)]
        current_theta = theta
        for i in range(len(ns)-1):
            by = layer_ys[i+1] if i < len(layer_ys)-1 else 0.6
            dy = points[-1][1] - by
            dx = dy * math.tan(math.radians(current_theta))
            nx = points[-1][0] + dx
            # clamp to bounds
            nx = min(max(nx, 0.15), 2.85)
            points.append((nx, by))
            t_new = snell_refract(current_theta, ns[i], ns[i+1])
            if t_new is None: t_new = current_theta
            current_theta = t_new

        # Intended path (straight at initial angle)
        int_end_y = 0.6
        int_end_x = px + (py_start - int_end_y) * math.tan(math.radians(theta))
        int_end_x = min(int_end_x, 2.85)
        ray_seg(ax, px, py_start, int_end_x, int_end_y,
                color=SL, lw=0.8, dashed=True, zorder=4)

        # Draw actual path
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            col = WH if i == 0 else AL
            ax.plot([x1, x2], [y1, y2], color=col, lw=2.0, zorder=5)
            draw_arrow_ray(ax, x1+0.5*(x2-x1), y1+0.5*(y2-y1), x2, y2, color=col, lw=2.0, zorder=6)

        # Final deviation
        fx, fy = points[-1]
        dev = abs(fx - int_end_x)
        color_dev = '#C03030' if cfg['title_color'] == '#B82020' else '#1A9A4A'
        ax.text(1.5, 0.3, f'Deviation: {dev:.2f} units',
                ha='center', va='top', fontsize=6.5, color=color_dev, fontweight='bold')

        # Refractive profile badge
        n_max = max(cfg['n_vals'])
        n_avg = sum(cfg['n_vals']) / len(cfg['n_vals'])
        ax.text(1.5, 0.05, f'max n={n_max:.2f} · avg n={n_avg:.2f}',
                ha='center', va='bottom', fontsize=5.5, color=SL)

    fig.suptitle('', fontsize=8)
    fig.text(0.5, 0.015,
             'Figure 11.1  —  Structural comparison: a 7-layer high-refraction hierarchy (left) '
             'vs a 3-layer low-refraction design (right). '
             'Fewer, lower-index layers reduce compound deviation.',
             ha='center', va='bottom', fontsize=6.5, color=SL, wrap=True)
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch11-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch11 done')


# ════════════════════════════════════════════════════════════════════════════
# Ch 12 — Leadership as Optics Work
# Leader as lens-maker adjusting the optical system
# ════════════════════════════════════════════════════════════════════════════
def ch12():
    fig, ax = plt.subplots(figsize=(6.0, 5.0), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.axis('off')
    ax.set_xlim(0, 6.0)
    ax.set_ylim(0, 5.0)

    # ── Title ──
    ax.text(3.0, 4.85, 'THE LEADER AS OPTICS ENGINEER',
            ha='center', va='top', fontsize=9, color=AM, fontweight='bold')
    ax.text(3.0, 4.55, 'Designing the optical system, not just aiming the beam',
            ha='center', va='top', fontsize=6.5, color=SL, style='italic')

    # ── Optical system diagram ──
    # Components laid out left-to-right:
    # [Vision source] → [Collimating lens] → [Org prism] → [Focusing lens] → [Impact target]

    components = [
        (0.5, 2.5, 'VISION\nSOURCE', WH),
        (1.8, 2.5, 'CULTURE\nLENS', AL),
        (3.0, 2.5, 'ORGANIZATIONAL\nSYSTEM', NL),
        (4.2, 2.5, 'ALIGNMENT\nLENS', AL),
        (5.5, 2.5, 'STRATEGIC\nIMPACT', '#3ADA3A'),
    ]

    # Draw ray path
    ray_y = 2.5
    prev_x = 0.5
    for i, (cx, cy, label, col) in enumerate(components[1:], 1):
        pcx = components[i-1][0]
        ray_seg(ax, pcx + 0.3, ray_y, cx - 0.3, ray_y, color=WH, lw=2.5, zorder=5)
        draw_arrow_ray(ax, pcx + 0.3, ray_y, cx - 0.3, ray_y, color=WH, lw=2.5, zorder=6)

    # Draw component symbols
    for i, (cx, cy, label, col) in enumerate(components):
        if i == 0:  # Source — starburst
            circle = plt.Circle((cx, cy), 0.22, color=WH, zorder=5, alpha=0.9)
            ax.add_patch(circle)
            for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
                ex = cx + 0.35 * np.cos(angle)
                ey = cy + 0.35 * np.sin(angle)
                ax.plot([cx, ex], [cy, ey], color=WH, lw=1.0, alpha=0.6, zorder=4)
        elif i == len(components)-1:  # Target — bullseye
            for r, c in [(0.28, '#3ADA3A'), (0.18, BG), (0.08, '#3ADA3A')]:
                circle = plt.Circle((cx, cy), r, color=c, zorder=5, alpha=0.9)
                ax.add_patch(circle)
        elif label in ['CULTURE\nLENS', 'ALIGNMENT\nLENS']:  # Lens shapes (biconvex)
            xs = [cx - 0.05, cx, cx + 0.05, cx, cx - 0.05]
            ys = [cy - 0.35, cy - 0.4, cy, cy + 0.4, cy + 0.35]
            lens = plt.Polygon(list(zip(xs, ys)), closed=True,
                               facecolor=AL, edgecolor=AM, lw=1.5, alpha=0.85, zorder=5)
            # Biconvex lens as ellipse pair
            from matplotlib.patches import Ellipse
            e1 = Ellipse((cx - 0.1, cy), 0.25, 0.75, color=AL, alpha=0.7, zorder=5)
            e2 = Ellipse((cx + 0.1, cy), 0.25, 0.75, color=AL, alpha=0.7, zorder=5)
            ax.add_patch(e1); ax.add_patch(e2)
        else:  # Prism (organizational system)
            prism_pts = np.array([
                [cx - 0.35, cy - 0.35],
                [cx + 0.35, cy - 0.35],
                [cx, cy + 0.42],
            ])
            prism = Polygon(prism_pts, closed=True,
                            facecolor=NL, edgecolor=AM, linewidth=2.0,
                            alpha=0.9, zorder=5)
            ax.add_patch(prism)

        ax.text(cx, cy - 0.62, label, ha='center', va='top',
                fontsize=5.5, color=col if col != NL else WH,
                fontweight='bold', zorder=7)

    # ── Leader figure (abstract) ──────────────────────────────────────────
    # Represented as annotations showing leadership actions
    leadership_actions = [
        (1.8, 3.6, 'Set cultural\nrefractive index', AL),
        (3.0, 3.8, 'Design org\narchitecture', WH),
        (4.2, 3.6, 'Align\nincentives', AL),
    ]

    for lx, ly, action, col in leadership_actions:
        ax.annotate('', xy=(lx, 2.95), xytext=(lx, ly - 0.1),
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.2,
                                    mutation_scale=8), zorder=7)
        ax.text(lx, ly, action, ha='center', va='bottom',
                fontsize=5.8, color=col, style='italic',
                bbox=dict(boxstyle='round,pad=0.2', facecolor=NM,
                          edgecolor=col, lw=0.8, alpha=0.9))

    # Leader crown/figure at top center
    leader_x = 3.0
    leader_y = 4.3
    ax.text(leader_x, leader_y, '⚙ LEADER', ha='center', va='center',
            fontsize=9, color=AM, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=ND,
                      edgecolor=AM, lw=1.5, alpha=0.95))

    # Bracket arrows from leader to each component
    for lx, ly, _, col in leadership_actions:
        ax.annotate('', xy=(lx, ly + 0.12), xytext=(leader_x, leader_y - 0.25),
                    arrowprops=dict(arrowstyle='->', color=AM, lw=0.8,
                                    connectionstyle='arc3,rad=0.2',
                                    mutation_scale=7), zorder=6)

    # ── Without vs with leader annotation ────────────────────────────────
    ax.text(0.3, 0.95,
            'The leader\'s task is not to aim the beam harder —\n'
            'but to engineer the lenses so the beam arrives where intended.',
            ha='left', va='top', fontsize=6.5, color=WH, style='italic',
            wrap=True,
            bbox=dict(boxstyle='round,pad=0.35', facecolor=NM, edgecolor=AM, lw=1.2))

    # Refractive index dashboard
    ax.text(5.7, 1.2,
            'Optical audit:\n'
            'Culture n: 1.3 ✓\n'
            'Process n: 1.2 ✓\n'
            'Hierarchy n: 1.4 ✓\n'
            'Compound Δ: 0.8°',
            ha='right', va='top', fontsize=5.8, color=AP,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=NM, edgecolor=AM, lw=1.0))

    add_caption(fig, 12, 1,
                'Leadership as optics work: the leader engineers the optical system '
                '(culture, architecture, incentives) rather than merely directing the beam. '
                'Low-index lenses at each stage ensure strategy arrives where intended.')
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(os.path.join(OUT, 'ch12-diagram.png'), dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print('ch12 done')


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print(f'Generating diagrams in: {OUT}')
    ch01()
    ch02()
    ch03()
    ch04()
    ch05()
    ch06()
    ch07()
    ch08()
    ch09()
    ch10()
    ch11()
    ch12()
    print('\nAll 12 diagrams generated.')
