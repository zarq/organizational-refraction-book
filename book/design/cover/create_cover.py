"""
Cover design for Organizational Refraction book.
Output: cover-front.png (1600x2400px)
Motif: A light ray entering an organizational "prism" and emerging refracted
       — visually representing strategy diverging from original aim.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# ── Canvas ──────────────────────────────────────────────────────────────────
W, H = 1600, 2400
img = Image.new("RGB", (W, H), "#0D1B2E")
draw = ImageDraw.Draw(img)

# ── Palette (matches design system) ─────────────────────────────────────────
NAVY_DEEP    = (13,  27,  46)
NAVY_MID     = (22,  44,  75)
NAVY_LIGHT   = (32,  64, 110)
AMBER        = (212, 134,  11)
AMBER_LIGHT  = (240, 172,  50)
AMBER_PALE   = (252, 230, 165)
WHITE        = (255, 255, 255)
WHITE_DIM    = (210, 218, 228)
SLATE        = (120, 138, 160)

# ── Background gradient (top-to-bottom navy) ─────────────────────────────────
for y in range(H):
    t = y / H
    r = int(NAVY_DEEP[0] + (NAVY_MID[0] - NAVY_DEEP[0]) * t)
    g = int(NAVY_DEEP[1] + (NAVY_MID[1] - NAVY_DEEP[1]) * t)
    b = int(NAVY_DEEP[2] + (NAVY_MID[2] - NAVY_DEEP[2]) * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── Helper: anti-aliased thick line via rectangle ───────────────────────────
def thick_line(draw, x0, y0, x1, y1, width, color, alpha=255):
    """Draw a thick line as a rotated rectangle for visual weight."""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = -dy / length, dx / length
    hw = width / 2
    pts = [
        (x0 + ux * hw, y0 + uy * hw),
        (x1 + ux * hw, y1 + uy * hw),
        (x1 - ux * hw, y1 - uy * hw),
        (x0 - ux * hw, y0 - uy * hw),
    ]
    draw.polygon(pts, fill=color)

# ── Refraction visual: prism/lens zone ──────────────────────────────────────
# Centre of visual element
CX = W // 2
CY = int(H * 0.42)

# Draw a subtle radial glow behind the lens area
GLOW_LAYERS = [
    (300, (22, 44, 75, 20)),
    (220, (28, 58, 100, 30)),
    (150, (32, 68, 120, 40)),
    (100, (38, 78, 135, 50)),
]
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
odraw = ImageDraw.Draw(overlay)
for radius, color in GLOW_LAYERS:
    odraw.ellipse(
        [CX - radius, CY - radius, CX + radius, CY + radius],
        fill=color,
    )
img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, overlay)
img = img_rgba.convert("RGB")
draw = ImageDraw.Draw(img)

# ── "Organizational medium" — hexagonal prism shape ──────────────────────────
# A slightly-flattened hexagon representing the org as a refractive medium
PRISM_R = 140  # outer radius
PRISM_INNER = 125
prism_pts_outer = []
prism_pts_inner = []
for i in range(6):
    angle = math.radians(90 + 60 * i)
    prism_pts_outer.append((CX + PRISM_R * math.cos(angle),
                             CY + PRISM_R * math.sin(angle)))
    prism_pts_inner.append((CX + PRISM_INNER * math.cos(angle),
                             CY + PRISM_INNER * math.sin(angle)))

# Fill prism body — amber-tinted translucent overlay
overlay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
o2draw = ImageDraw.Draw(overlay2)
o2draw.polygon(prism_pts_outer, fill=(40, 65, 110, 110))  # dark navy fill
img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, overlay2)
img = img_rgba.convert("RGB")
draw = ImageDraw.Draw(img)

# Prism border — amber glow
thick_line(draw, *prism_pts_outer[0], *prism_pts_outer[1], 3, AMBER)
thick_line(draw, *prism_pts_outer[1], *prism_pts_outer[2], 3, AMBER)
thick_line(draw, *prism_pts_outer[2], *prism_pts_outer[3], 3, AMBER)
thick_line(draw, *prism_pts_outer[3], *prism_pts_outer[4], 3, AMBER)
thick_line(draw, *prism_pts_outer[4], *prism_pts_outer[5], 3, AMBER)
thick_line(draw, *prism_pts_outer[5], *prism_pts_outer[0], 3, AMBER)

# ── Incoming ray (STRATEGY — intended direction) ─────────────────────────────
# Ray enters from upper-left at ~20° above horizontal, hits the prism left side
ray_in_start = (CX - 500, CY - 140)
ray_in_end   = (CX - PRISM_R + 10, CY - 20)   # hits left edge

# Intended continuation (dashed) — where strategy *should* have gone
intended_end = (CX + 550, CY - 85)

# Actual refracted ray — deflected downward
refracted_end = (CX + 490, CY + 210)

# Draw intended path (faint dashed white)
dash_len = 20
gap_len = 12
dx = intended_end[0] - (CX + PRISM_R + 10)
dy = intended_end[1] - (CY - 20)
total = math.hypot(dx, dy)
ux, uy = dx / total, dy / total
d = 0
draw_dash = True
sx, sy = CX + PRISM_R + 10, CY - 20
while d < total:
    step = min(dash_len if draw_dash else gap_len, total - d)
    ex, ey = sx + ux * step, sy + uy * step
    if draw_dash:
        thick_line(draw, sx, sy, ex, ey, 2, (180, 195, 215))
    sx, sy = ex, ey
    d += step
    draw_dash = not draw_dash

# Small label: "Intended direction"
# (will be placed after fonts are loaded)

# Draw incoming ray — solid, white-bright, with amber glow
for w, col in [(10, (80, 110, 150, 60)), (5, (160, 185, 210, 90)), (2.5, WHITE)]:
    thick_line(draw, *ray_in_start, *ray_in_end, w, col)

# Arrowhead on incoming ray (pointing toward prism)
arrow_tip = ray_in_end
angle_in = math.atan2(ray_in_end[1] - ray_in_start[1], ray_in_end[0] - ray_in_start[0])
alen = 18
for aw, ac in [(3, WHITE)]:
    ax1 = arrow_tip[0] - alen * math.cos(angle_in - 0.4)
    ay1 = arrow_tip[1] - alen * math.sin(angle_in - 0.4)
    ax2 = arrow_tip[0] - alen * math.cos(angle_in + 0.4)
    ay2 = arrow_tip[1] - alen * math.sin(angle_in + 0.4)
    draw.polygon([arrow_tip, (ax1, ay1), (ax2, ay2)], fill=WHITE)

# Draw refracted ray — amber, bending downward
for w, col in [(10, (140, 90, 10, 50)), (5, (210, 150, 30, 80)), (2.5, AMBER_LIGHT)]:
    thick_line(draw, CX + PRISM_R - 10, CY + 10, *refracted_end, w, col)

# Arrowhead on refracted ray
arrow_tip2 = refracted_end
angle_ref = math.atan2(refracted_end[1] - (CY + 10), refracted_end[0] - (CX + PRISM_R - 10))
ax1 = arrow_tip2[0] - alen * math.cos(angle_ref - 0.4)
ay1 = arrow_tip2[1] - alen * math.sin(angle_ref - 0.4)
ax2 = arrow_tip2[0] - alen * math.cos(angle_ref + 0.4)
ay2 = arrow_tip2[1] - alen * math.sin(angle_ref + 0.4)
draw.polygon([arrow_tip2, (ax1, ay1), (ax2, ay2)], fill=AMBER_LIGHT)

# ── Divergence indicator lines ───────────────────────────────────────────────
# Arc/bracket showing the gap between intended and actual
div_x = CX + 450
for i in range(5):
    y_int = CY - 85 + (intended_end[1] - (CY - 85)) * (i / 4)
    y_ref = CY + 210 + (refracted_end[1] - (CY + 210)) * (i / 4)
    # these are end points — just draw two tick marks
iy_end = intended_end[1]
ry_end = refracted_end[1]
# Bracket: vertical line
thick_line(draw, div_x, int(iy_end + 10), div_x, int(ry_end - 10), 2, (180, 160, 100))
# Top tick
thick_line(draw, div_x - 10, int(iy_end + 10), div_x + 10, int(iy_end + 10), 2, (180, 160, 100))
# Bottom tick
thick_line(draw, div_x - 10, int(ry_end - 10), div_x + 10, int(ry_end - 10), 2, (180, 160, 100))

# Small dot at prism center
draw.ellipse([CX-6, CY-6, CX+6, CY+6], fill=AMBER_PALE)

# ── Decorative micro-grid (faint, structural feel) ───────────────────────────
grid_col = (30, 48, 75)
for x in range(0, W, 80):
    draw.line([(x, 0), (x, H)], fill=grid_col, width=1)
for y in range(0, H, 80):
    draw.line([(0, y), (W, y)], fill=grid_col, width=1)
# Mask grid over the prism area with a filled polygon to keep it clean
overlay3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
o3draw = ImageDraw.Draw(overlay3)
o3draw.ellipse([CX - PRISM_R - 20, CY - PRISM_R - 20, CX + PRISM_R + 20, CY + PRISM_R + 20],
               fill=(13, 25, 44, 220))
img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, overlay3)
img = img_rgba.convert("RGB")
draw = ImageDraw.Draw(img)

# Redraw prism border after mask
thick_line(draw, *prism_pts_outer[0], *prism_pts_outer[1], 3, AMBER)
thick_line(draw, *prism_pts_outer[1], *prism_pts_outer[2], 3, AMBER)
thick_line(draw, *prism_pts_outer[2], *prism_pts_outer[3], 3, AMBER)
thick_line(draw, *prism_pts_outer[3], *prism_pts_outer[4], 3, AMBER)
thick_line(draw, *prism_pts_outer[4], *prism_pts_outer[5], 3, AMBER)
thick_line(draw, *prism_pts_outer[5], *prism_pts_outer[0], 3, AMBER)
draw.ellipse([CX-6, CY-6, CX+6, CY+6], fill=AMBER_PALE)

# ── Typography — load system fonts ──────────────────────────────────────────
def find_font(names, size):
    """Try each font name and fall back to default."""
    font_dirs = [
        "/System/Library/Fonts/",
        "/Library/Fonts/",
        "/usr/share/fonts/",
        "/usr/share/fonts/truetype/",
    ]
    for name in names:
        # Direct path
        if os.path.isabs(name) and os.path.exists(name):
            try:
                return ImageFont.truetype(name, size)
            except Exception:
                pass
        # Search dirs
        for d in font_dirs:
            for root, dirs, files in os.walk(d):
                for f in files:
                    if name.lower() in f.lower() and f.endswith((".ttf", ".otf")):
                        try:
                            return ImageFont.truetype(os.path.join(root, f), size)
                        except Exception:
                            pass
    return ImageFont.load_default()

# Try to load good fonts
font_title    = find_font(["HelveticaNeue-Bold", "Helvetica Neue Bold", "Helvetica-Bold",
                            "Arial Bold", "ArialBold", "NotoSans-Bold", "DejaVuSans-Bold"], 96)
font_title_sm = find_font(["HelveticaNeue-Bold", "Helvetica Neue Bold", "Arial Bold",
                            "NotoSans-Bold", "DejaVuSans-Bold"], 40)
font_subtitle = find_font(["HelveticaNeue", "Helvetica Neue", "Helvetica-Light",
                            "Arial", "NotoSans", "DejaVuSans"], 36)
font_author   = find_font(["HelveticaNeue", "Georgia", "Times New Roman",
                            "NotoSerif", "DejaVuSerif"], 28)
font_small    = find_font(["HelveticaNeue", "Helvetica Neue", "Arial",
                            "NotoSans", "DejaVuSans"], 22)
font_label    = find_font(["HelveticaNeue", "Arial", "NotoSans", "DejaVuSans"], 18)

# ── Title block — upper portion ──────────────────────────────────────────────
# "ORGANIZATIONAL" — large
title_line1 = "ORGANIZATIONAL"
title_line2 = "REFRACTION"

# Measure and center
try:
    bb1 = draw.textbbox((0, 0), title_line1, font=font_title)
    w1 = bb1[2] - bb1[0]
    bb2 = draw.textbbox((0, 0), title_line2, font=font_title)
    w2 = bb2[2] - bb2[0]
except Exception:
    w1 = len(title_line1) * 50
    w2 = len(title_line2) * 50

T_Y = 110  # top of title block

# Subtle amber underline bar behind ORGANIZATIONAL
draw.rectangle([80, T_Y - 10, W - 80, T_Y + 108], fill=(18, 35, 62))

draw.text(((W - w1) // 2, T_Y), title_line1, fill=WHITE, font=font_title)
# "REFRACTION" — amber accent
draw.text(((W - w2) // 2, T_Y + 108), title_line2, fill=AMBER_LIGHT, font=font_title)

# Thin amber rule under title
draw.rectangle([80, T_Y + 208, W - 80, T_Y + 213], fill=AMBER)

# ── Subtitle ──────────────────────────────────────────────────────────────────
# Two lines to keep readable
sub1 = "Why Your Strategy Arrives"
sub2 = "Somewhere It Was Never Aimed"

try:
    sb1 = draw.textbbox((0, 0), sub1, font=font_subtitle)
    sw1 = sb1[2] - sb1[0]
    sb2 = draw.textbbox((0, 0), sub2, font=font_subtitle)
    sw2 = sb2[2] - sb2[0]
except Exception:
    sw1, sw2 = len(sub1) * 18, len(sub2) * 18

SUB_Y = T_Y + 230
draw.text(((W - sw1) // 2, SUB_Y), sub1, fill=WHITE_DIM, font=font_subtitle)
draw.text(((W - sw2) // 2, SUB_Y + 52), sub2, fill=WHITE_DIM, font=font_subtitle)

# ── Ray labels (small caps style) ─────────────────────────────────────────────
label_intended = "INTENDED DIRECTION"
label_actual   = "ACTUAL ARRIVAL"
label_org      = "ORGANIZATION"

try:
    li_bb = draw.textbbox((0, 0), label_intended, font=font_label)
    liw = li_bb[2] - li_bb[0]
    la_bb = draw.textbbox((0, 0), label_actual, font=font_label)
    law = la_bb[2] - la_bb[0]
    lo_bb = draw.textbbox((0, 0), label_org, font=font_label)
    low = lo_bb[2] - lo_bb[0]
except Exception:
    liw = law = low = 120

# Intended direction label — upper right of prism diagram
draw.text((intended_end[0] - liw - 18, int(intended_end[1]) - 28),
          label_intended, fill=(160, 180, 200), font=font_label)

# Actual arrival label — lower right
draw.text((refracted_end[0] - law - 18, int(refracted_end[1]) + 12),
          label_actual, fill=(210, 155, 50), font=font_label)

# Org label — centred on prism
draw.text((CX - low // 2, CY - 12), label_org, fill=AMBER_PALE, font=font_label)

# ── Author block — below prism area ──────────────────────────────────────────
AUTHOR_Y = int(H * 0.68)
author_text = "[Author Name — TBD]"
try:
    ab = draw.textbbox((0, 0), author_text, font=font_author)
    aw = ab[2] - ab[0]
except Exception:
    aw = len(author_text) * 14
draw.text(((W - aw) // 2, AUTHOR_Y), author_text, fill=SLATE, font=font_author)

# Thin rule above author name
draw.rectangle([(W - aw) // 2 - 20, AUTHOR_Y - 18,
                (W + aw) // 2 + 20, AUTHOR_Y - 15], fill=(60, 80, 110))

# ── Bottom decorative band ────────────────────────────────────────────────────
BAND_Y = H - 140
draw.rectangle([0, BAND_Y, W, BAND_Y + 3], fill=AMBER)
draw.rectangle([0, BAND_Y + 3, W, H], fill=(8, 16, 30))

# Publisher placeholder
pub_text = "[Publisher — TBD]"
try:
    pb = draw.textbbox((0, 0), pub_text, font=font_small)
    pw = pb[2] - pb[0]
except Exception:
    pw = 160
draw.text(((W - pw) // 2, BAND_Y + 18), pub_text, fill=SLATE, font=font_small)

# ── Save ──────────────────────────────────────────────────────────────────────
out_path = "/Users/ivo/.paperclip/instances/default/workspaces/b3012109-f748-42f7-a65b-dcf33846c24d/book-design/cover-front.png"
img.save(out_path, "PNG", dpi=(300, 300))
print(f"Saved: {out_path} ({W}x{H}px)")
size_kb = os.path.getsize(out_path) // 1024
print(f"File size: {size_kb} KB")
