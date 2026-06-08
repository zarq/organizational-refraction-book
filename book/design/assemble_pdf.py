#!/usr/bin/env python3
"""
Assemble final book PDF for Organizational Refraction.
Reads all manuscript content and produces a publication-ready PDF.
"""

import os
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.units import inch
pt = 1  # 1 pt = 1 reportlab unit
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, PageBreak, Image,
    KeepTogether, HRFlowable, Table, TableStyle
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Paths ────────────────────────────────────────────────────────────────────

BOOK_DIR = Path("/Users/ivo/.paperclip/instances/default/workspaces/4bcf9239-8440-41ec-90d8-aa4f472f0fa7/organizational-refraction-book")
DESIGN_DIR = Path("/Users/ivo/.paperclip/instances/default/workspaces/b3012109-f748-42f7-a65b-dcf33846c24d/book-design")
OUT_DIR = BOOK_DIR / "book" / "pdf"
OUT_DIR.mkdir(exist_ok=True)
OUT_PATH = OUT_DIR / "organizational-refraction-DRAFT.pdf"

# ── Page geometry ────────────────────────────────────────────────────────────

PAGE_W = 6.0 * inch
PAGE_H = 9.0 * inch
MARGIN_TOP    = 0.80 * inch
MARGIN_BOTTOM = 0.80 * inch
MARGIN_LEFT   = 1.00 * inch
MARGIN_RIGHT  = 0.75 * inch
BODY_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
BODY_H = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM

# ── Colour palette ────────────────────────────────────────────────────────────

NAVY    = colors.HexColor("#1A2744")
GOLD    = colors.HexColor("#C4952A")
BODY_BG = colors.HexColor("#F8F6F1")
TEXT    = colors.HexColor("#1C1C1C")
GREY    = colors.HexColor("#6B6B6B")
LGREY   = colors.HexColor("#EEECE8")
WHITE   = colors.white

# ── Chapter manifest ─────────────────────────────────────────────────────────

PARTS = [
    ("Part One", "The Mechanism", "Diagnosis → Mechanism"),
    ("Part Two", "Three Modes of Refraction", "Mechanism"),
    ("Part Three", "Compound Refraction", "Mechanism, extended"),
    ("Part Four", "Diagnosing and Reducing Refraction", "Prescription"),
]

CHAPTERS = [
    (1, "One",   "The Strategy-Reality Gap: A New Explanation",
     "Why 37 percent of your strategy disappears before it arrives",
     "chapter-01-strategy-reality-gap", "draft-v2.md", 0, None),
    (2, "Two",   "What Existing Frameworks Get Right — and What They Miss",
     "Five decades of management theory, and the one question none of it answers",
     "chapter-02-existing-frameworks", "draft-v2.md", 0, None),
    (3, "Three", "The Physics of Organizational Refraction",
     "Snell's Law, organizational density, and the diagnostic vocabulary of the medium",
     "chapter-03-physics-of-refraction", "draft-v1.md", 0, DESIGN_DIR / "ch03-diagram.png"),
    (4, "Four",  "Hierarchical Refraction: The Vertical Bend",
     "How intent bends going down, and ground truth bends coming up",
     "chapter-04-hierarchical-refraction", "draft-v1.md", 1, None),
    (5, "Five",  "Cultural Refraction: The Absorptive Boundary",
     "When the culture sincerely believes it is doing what you asked",
     "chapter-05-cultural-refraction", "draft-v1.md", 1, None),
    (6, "Six",   "Process Refraction: The Systematic Redirect",
     "When the metric becomes the strategy and no one notices for a decade",
     "chapter-06-process-refraction", "draft-v1.md", 1, None),
    (7, "Seven", "When Layers Combine: Compound Refraction",
     "Two disasters, one organization, seventeen years apart",
     "chapter-07-compound-refraction", "draft-v1.md", 2, None),
    (8, "Eight", "Total Internal Reflection: When Intent Never Penetrates",
     "The strategy everyone endorses and no one implements",
     "chapter-08-total-internal-reflection", "draft-v1.md", 2, DESIGN_DIR / "ch08-diagram.png"),
    (9, "Nine",  "Mapping Your Organization's Refractive Profile",
     "The refraction audit — changing the diagnostic target from symptoms to medium",
     "chapter-09-refractive-profile", "draft-v1.md", 3, DESIGN_DIR / "ch09-diagram.png"),
    (10,"Ten",   "Correcting the Angle: Interventions That Work",
     "Three structural levers, and why content-level fixes fail",
     "chapter-10-correcting-the-angle", "draft-v1.md", 3, None),
    (11,"Eleven","Designing Refraction-Resistant Organizations",
     "Structure as a transmission medium, not a control architecture",
     "chapter-11-refraction-resistant-organizations", "draft-v1.md", 3, None),
    (12,"Twelve","Leadership as Optics Work",
     "Ensuring intent arrives intact at the point of action",
     "chapter-12-leadership-as-optics-work", "draft-v1.md", 3, None),
]

# ── Styles ────────────────────────────────────────────────────────────────────

styles = getSampleStyleSheet()

def S(name, **kw):
    base = kw.pop("parent", "Normal")
    s = ParagraphStyle(name, parent=styles[base], **kw)
    return s

STYLE = dict(
    body=S("body",
           fontName="Times-Roman", fontSize=11.5, leading=18,
           textColor=TEXT, alignment=TA_JUSTIFY,
           spaceAfter=8, firstLineIndent=0),
    body_indent=S("body_indent",
           fontName="Times-Roman", fontSize=11.5, leading=18,
           textColor=TEXT, alignment=TA_JUSTIFY,
           spaceAfter=8, firstLineIndent=22),
    h1=S("h1",
         fontName="Helvetica-Bold", fontSize=24, leading=30,
         textColor=NAVY, spaceBefore=24, spaceAfter=8,
         alignment=TA_LEFT),
    h2=S("h2",
         fontName="Helvetica-Bold", fontSize=15, leading=22,
         textColor=NAVY, spaceBefore=20, spaceAfter=6,
         alignment=TA_LEFT),
    h3=S("h3",
         fontName="Helvetica-Bold", fontSize=12.5, leading=18,
         textColor=TEXT, spaceBefore=14, spaceAfter=4),
    h4=S("h4",
         fontName="Helvetica-BoldOblique", fontSize=11.5, leading=16,
         textColor=GREY, spaceBefore=10, spaceAfter=4),
    pullquote=S("pullquote",
                fontName="Times-Italic", fontSize=14, leading=22,
                textColor=NAVY, spaceBefore=16, spaceAfter=16,
                leftIndent=24, rightIndent=24, alignment=TA_LEFT),
    caption=S("caption",
              fontName="Helvetica", fontSize=8.5, leading=12,
              textColor=GREY, spaceBefore=4, spaceAfter=8,
              alignment=TA_CENTER),
    section_num=S("section_num",
                  fontName="Helvetica-BoldOblique", fontSize=12,
                  textColor=GOLD, spaceBefore=18, spaceAfter=4),
    toc_part=S("toc_part",
               fontName="Helvetica-Bold", fontSize=11.5,
               textColor=NAVY, spaceBefore=14, spaceAfter=2,
               leftIndent=0),
    toc_ch=S("toc_ch",
             fontName="Times-Roman", fontSize=10.5, leading=16,
             textColor=TEXT, spaceBefore=4, spaceAfter=0,
             leftIndent=12),
    toc_sub=S("toc_sub",
              fontName="Times-Italic", fontSize=9.5, leading=14,
              textColor=GREY, spaceBefore=0, spaceAfter=2,
              leftIndent=24),
    bib_entry=S("bib_entry",
                fontName="Times-Roman", fontSize=10, leading=15,
                textColor=TEXT, spaceBefore=3, spaceAfter=0,
                leftIndent=18, firstLineIndent=-18),
    bib_letter=S("bib_letter",
                 fontName="Helvetica-Bold", fontSize=13,
                 textColor=NAVY, spaceBefore=12, spaceAfter=4),
    small=S("small",
            fontName="Helvetica", fontSize=9, leading=13,
            textColor=GREY),
    running_head=S("running_head",
                   fontName="Helvetica", fontSize=8, leading=10,
                   textColor=GREY, alignment=TA_LEFT),
)

# ── Decorative flowables ──────────────────────────────────────────────────────

class ThinRule(Flowable):
    def __init__(self, width, thickness=0.5, colour=GOLD):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.colour = colour
        self.height = thickness + 4

    def draw(self):
        self.canv.setStrokeColor(self.colour)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness / 2, self.width, self.thickness / 2)


class ChapterOpener(Flowable):
    """Full-page-width chapter opener block."""

    def __init__(self, num_word, num_int, title, subtitle, part_label):
        super().__init__()
        self.num_word  = num_word
        self.num_int   = num_int
        self.title     = title
        self.subtitle  = subtitle
        self.part_label = part_label
        self.width  = BODY_W
        self.height = 3.8 * inch

    def draw(self):
        c = self.canv
        w = self.width
        h = self.height

        # dark background slab
        c.setFillColor(NAVY)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        # gold horizontal rule at top
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        c.line(0, h - 2, w, h - 2)

        # part label (small caps style)
        if self.part_label:
            c.setFillColor(GOLD)
            c.setFont("Helvetica", 8.5)
            c.drawString(16, h - 24, self.part_label.upper())

        # Chapter label
        c.setFillColor(GOLD)
        c.setFont("Helvetica", 10)
        c.drawString(16, h - 44, f"CHAPTER {self.num_int}")

        # Chapter number word (large)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 54)
        c.drawString(16, h - 110, self.num_word.upper())

        # decorative light-ray diagram
        self._draw_ray(c, w, h)

        # Title
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 18)
        # Wrap title manually
        words = self.title.split()
        lines, line = [], []
        for w_t in words:
            test = " ".join(line + [w_t])
            if c.stringWidth(test, "Helvetica-Bold", 18) < w - 32:
                line.append(w_t)
            else:
                lines.append(" ".join(line))
                line = [w_t]
        if line:
            lines.append(" ".join(line))
        y = h - 136
        for ln in lines:
            c.drawString(16, y, ln)
            y -= 24

        # Subtitle
        if self.subtitle:
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Oblique", 10.5)
            sub = self.subtitle
            if c.stringWidth(sub, "Helvetica-Oblique", 10.5) > self.width - 32:
                sub = sub[:70] + "…"
            c.drawString(16, y - 8, sub)

    def _draw_ray(self, c, w, h):
        """Draw a simple refraction light-ray motif in the upper-right of the opener."""
        import math
        x0 = w - 10
        y0 = h - 4
        # boundary
        bx = w * 0.72
        c.setStrokeColor(colors.HexColor("#FFFFFF22"))
        c.setLineWidth(0.4)
        c.line(bx, h, bx, 0)
        # incident ray
        angle_i = 40 * math.pi / 180
        ray_len = 1.4 * inch
        x1 = bx - ray_len * math.cos(angle_i)
        y1 = h * 0.68 + ray_len * math.sin(angle_i)
        x2 = bx
        y2 = h * 0.68
        c.setStrokeColor(colors.HexColor("#FFFFFF88"))
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)
        # refracted ray (steeper)
        angle_r = 25 * math.pi / 180
        rx2 = bx + ray_len * math.cos(angle_r)
        ry2 = h * 0.68 - ray_len * math.sin(angle_r)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        c.line(x2, y2, rx2, ry2)
        # small angle labels
        c.setFillColor(colors.HexColor("#FFFFFF55"))
        c.setFont("Helvetica", 7)
        c.drawString(x2 - 36, y2 + 10, "θ₁")
        c.drawString(x2 + 8, y2 - 14, "θ₂")


class PartDivider(Flowable):
    """Full-page part divider."""

    def __init__(self, part_num, part_title, part_subtitle):
        super().__init__()
        self.part_num = part_num
        self.part_title = part_title
        self.part_subtitle = part_subtitle
        self.width  = BODY_W
        self.height = BODY_H

    def draw(self):
        c = self.canv
        w, h = self.width, self.height

        c.setFillColor(NAVY)
        c.rect(0, 0, w, h, fill=1, stroke=0)

        c.setFillColor(GOLD)
        c.setFont("Helvetica", 10)
        c.drawString(0, h * 0.62, self.part_num.upper())

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 34)
        c.drawString(0, h * 0.54, self.part_title.upper())

        c.setFillColor(GOLD)
        c.setLineWidth(1.5)
        c.line(0, h * 0.52, w * 0.55, h * 0.52)

        c.setFillColor(colors.HexColor("#FFFFFFCC"))
        c.setFont("Helvetica-Oblique", 12)
        c.drawString(0, h * 0.46, self.part_subtitle)

        # decorative refraction array
        self._draw_prism(c, w, h)

    def _draw_prism(self, c, w, h):
        import math
        # A simple triangular prism outline in lower right
        cx, cy = w * 0.78, h * 0.28
        size = 0.9 * inch
        pts = [
            (cx, cy + size),
            (cx - size * math.cos(math.pi/6), cy - size * 0.5),
            (cx + size * math.cos(math.pi/6), cy - size * 0.5),
        ]
        c.setStrokeColor(colors.HexColor("#FFFFFF44"))
        c.setLineWidth(1)
        c.lines([(pts[0][0], pts[0][1], pts[1][0], pts[1][1]),
                 (pts[1][0], pts[1][1], pts[2][0], pts[2][1]),
                 (pts[2][0], pts[2][1], pts[0][0], pts[0][1])])
        # rainbow rays through prism
        spectrum = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF"]
        for i, hx in enumerate(spectrum):
            offset = (i - 1.5) * 6
            x1 = cx - 1.4 * inch
            y1 = cy + offset
            xm = cx - size * 0.3
            ym = cy + offset * 0.5
            x2 = cx + 1.2 * inch
            y2 = cy - 0.15 * inch + offset * 1.8
            c.setStrokeColor(colors.HexColor(hx + "AA"))
            c.setLineWidth(0.8)
            c.line(x1, y1, xm, ym)
            c.line(xm, ym, x2, y2)


class DiagramPlaceholder(Flowable):
    """Auto-generated refraction diagram for chapters without attached PNG."""

    TEMPLATES = {
        1: "strategy_reality_gap",
        2: "framework_comparison",
        4: "hierarchical_bend",
        5: "cultural_absorption",
        6: "process_redirect",
        7: "compound_layers",
        10: "angle_correction",
        11: "resistant_design",
        12: "leadership_optics",
    }

    def __init__(self, ch_num, ch_title):
        super().__init__()
        self.ch_num   = ch_num
        self.ch_title = ch_title
        self.width  = BODY_W
        self.height = 2.2 * inch

    def draw(self):
        tpl = self.TEMPLATES.get(self.ch_num, "generic")
        getattr(self, f"_draw_{tpl}", self._draw_generic)()

    def _rect(self, x, y, w, h, fill=None, stroke=None, lw=0.8):
        c = self.canv
        if fill:
            c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
        c.setLineWidth(lw)
        c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1 if stroke else 0)

    def _label(self, x, y, text, size=8, bold=False, colour=TEXT, anchor="c"):
        c = self.canv
        c.setFillColor(colour)
        fn = "Helvetica-Bold" if bold else "Helvetica"
        c.setFont(fn, size)
        if anchor == "c":
            c.drawCentredString(x, y, text)
        elif anchor == "l":
            c.drawString(x, y, text)
        elif anchor == "r":
            c.drawRightString(x, y, text)

    def _arrow(self, x1, y1, x2, y2, colour=NAVY, lw=1.2):
        import math
        c = self.canv
        c.setStrokeColor(colour)
        c.setLineWidth(lw)
        c.line(x1, y1, x2, y2)
        ang = math.atan2(y2 - y1, x2 - x1)
        hs = 6
        ax1 = x2 - hs * math.cos(ang - 0.4)
        ay1 = y2 - hs * math.sin(ang - 0.4)
        ax2 = x2 - hs * math.cos(ang + 0.4)
        ay2 = y2 - hs * math.sin(ang + 0.4)
        c.line(x2, y2, ax1, ay1)
        c.line(x2, y2, ax2, ay2)

    # ── background box ──────────────────────────────────────────────────────
    def _bg(self):
        c = self.canv
        c.setFillColor(colors.HexColor("#F4F2EE"))
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)

    def _draw_generic(self):
        import math
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        cx, cy = w / 2, h / 2

        # two-layer refraction ray
        bx = cx
        # incident
        c.setStrokeColor(NAVY)
        c.setLineWidth(2)
        angle_i = 38 * math.pi / 180
        rl = 1.3 * inch
        c.line(bx - rl * math.cos(angle_i), cy + rl * math.sin(angle_i), bx, cy)
        # refracted
        c.setStrokeColor(GOLD)
        angle_r = 22 * math.pi / 180
        c.line(bx, cy, bx + rl * math.cos(angle_r), cy - rl * math.sin(angle_r))
        # boundary
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.6)
        c.line(bx - 18, 0, bx - 18, h)
        # labels
        self._label(cx - rl * 0.6 * math.cos(angle_i), cy + rl * 0.6 * math.sin(angle_i) + 10,
                    "Intent", 8, colour=NAVY)
        self._label(cx + rl * 0.6 * math.cos(angle_r), cy - rl * 0.6 * math.sin(angle_r) - 12,
                    "Outcome", 8, colour=GOLD)
        self._label(cx, h - 14, f"Figure {self.ch_num}: Organizational Refraction", 8, colour=GREY)

    def _draw_strategy_reality_gap(self):
        self._bg()
        c = self.canv
        w, h = self.width, self.height

        # three columns: Strategy / Organisation / Reality
        col_w = w / 3
        for i, (label, bg) in enumerate([("STRATEGY", "#D9E8F5"), ("ORGANISATION", "#EDE8D9"), ("REALITY", "#D9F0E3")]):
            x = i * col_w + 8
            cw = col_w - 16
            self._rect(x, h * 0.12, cw, h * 0.72, fill=colors.HexColor(bg), stroke=colors.HexColor("#AAAAAA"))
            self._label(x + cw / 2, h * 0.88, label, 8, bold=True, colour=NAVY)

        # arrows showing refraction between columns
        for ix in [col_w, col_w * 2]:
            c.setStrokeColor(GOLD)
            c.setLineWidth(1.5)
            self._arrow(ix - 4, h * 0.5, ix + 4, h * 0.42, colour=GOLD)

        # 63% label
        self._label(w / 2, h * 0.02, "Figure 1: 37% of strategy value lost through organisational refraction", 8, colour=GREY)

    def _draw_framework_comparison(self):
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Radar-like concentric arcs for 5 framework categories
        import math
        cx, cy = w / 2, h * 0.52
        maxr = min(w, h) * 0.35
        frames = ["Process", "Signal", "Complexity", "Structural", "Cultural"]
        scores = [0.65, 0.72, 0.58, 0.80, 0.68]
        n = len(frames)
        pts = []
        for i, (fr, sc) in enumerate(zip(frames, scores)):
            ang = math.pi / 2 + i * 2 * math.pi / n
            r = maxr * sc
            px, py = cx + r * math.cos(ang), cy + r * math.sin(ang)
            pts.append((px, py))
            # spoke
            c.setStrokeColor(colors.HexColor("#CCCCCC"))
            c.setLineWidth(0.4)
            c.line(cx, cy, cx + maxr * math.cos(ang), cy + maxr * math.sin(ang))
            # label
            lx = cx + (maxr + 14) * math.cos(ang)
            ly = cy + (maxr + 14) * math.sin(ang)
            self._label(lx, ly - 4, fr, 7.5, colour=NAVY)

        # polygon
        c.setFillColor(colors.HexColor("#C4952A33"))
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.2)
        path = c.beginPath()
        path.moveTo(*pts[0])
        for p in pts[1:]:
            path.lineTo(*p)
        path.close()
        c.drawPath(path, fill=1, stroke=1)
        self._label(w / 2, h * 0.02, "Figure 2: Existing framework coverage — gaps in refraction-layer analysis", 8, colour=GREY)

    def _draw_hierarchical_bend(self):
        import math
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Vertical layers
        layers = [("Board", h*0.78), ("Top Mgmt", h*0.58), ("Middle Mgmt", h*0.38), ("Front Line", h*0.18)]
        bar_h = h * 0.14
        for label, y in layers:
            density = layers.index((label, y)) + 1
            alpha = 30 + density * 16
            self._rect(w * 0.1, y, w * 0.6, bar_h,
                       fill=colors.HexColor(f"#1A2744{alpha:02X}"),
                       stroke=colors.HexColor("#1A2744"))
            self._label(w * 0.4, y + bar_h / 2 - 4, label, 9, bold=True, colour=WHITE)

        # intent signal arrow bending
        pts_down = [
            (w * 0.22, h * 0.94),
            (w * 0.30, h * 0.72),
            (w * 0.38, h * 0.52),
            (w * 0.50, h * 0.32),
            (w * 0.60, h * 0.12),
        ]
        c.setStrokeColor(GOLD)
        c.setLineWidth(2)
        for i in range(len(pts_down) - 1):
            c.line(*pts_down[i], *pts_down[i+1])

        self._label(w * 0.2, h * 0.96, "Intent", 8, bold=True, colour=NAVY)
        self._label(w * 0.63, h * 0.08, "Outcome", 8, bold=True, colour=GOLD)
        self._label(w * 0.85, h / 2, "Refractive\nindex →", 7.5, colour=GREY)
        self._label(w / 2, h * 0.01, "Figure 4: Hierarchical refraction — intent bends at each management layer", 8, colour=GREY)

    def _draw_cultural_absorption(self):
        self._bg()
        c = self.canv
        w, h = self.width, self.height

        # Showing absorption vs transmission
        bx = w * 0.5
        c.setFillColor(colors.HexColor("#EDE8D944"))
        c.rect(bx - w * 0.22, h * 0.08, w * 0.44, h * 0.84, fill=1, stroke=0)
        self._label(bx, h * 0.94, "Cultural Medium", 8.5, bold=True, colour=NAVY)

        # incident rays
        for i, frac in enumerate([0.35, 0.50, 0.65]):
            yi = h * frac
            c.setStrokeColor(NAVY)
            c.setLineWidth(1.5)
            c.line(w * 0.12, yi, bx - w * 0.22, yi)
            # absorbed ray (fades into medium)
            c.setStrokeColor(colors.HexColor("#1A274422"))
            c.setLineWidth(4)
            c.line(bx - w * 0.22, yi, bx + w * 0.05, yi)
            # tiny transmitted fraction
            c.setStrokeColor(GOLD)
            c.setLineWidth(0.8)
            c.line(bx + w * 0.22, yi, bx + w * 0.34, yi - (i - 1) * 14)

        self._label(w * 0.09, h * 0.94, "Strategic\nDirectives", 8, colour=NAVY)
        self._label(w * 0.88, h * 0.94, "Enacted\nBehavior", 8, colour=GOLD)
        self._label(w / 2, h * 0.01, "Figure 5: Cultural absorption — strategy absorbed before transmission", 8, colour=GREY)

    def _draw_process_redirect(self):
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Funnel: intent → metric → behavior
        stages = [
            (w*0.15, h*0.72, w*0.14, h*0.26, "Strategic\nIntent", "#1A2744"),
            (w*0.38, h*0.60, w*0.14, h*0.30, "Proxy\nMetric", "#C4952A"),
            (w*0.61, h*0.48, w*0.14, h*0.36, "Measured\nBehavior", "#6B6B6B"),
            (w*0.84, h*0.36, w*0.12, h*0.40, "Actual\nOutcome", "#8B3A3A"),
        ]
        for x, y, bw, bh, label, colour in stages:
            self._rect(x, y, bw, bh, fill=colors.HexColor(colour + "CC"),
                       stroke=colors.HexColor(colour))
            self._label(x + bw/2, y + bh/2 - 5, label, 8.5, bold=True, colour=WHITE)
        # arrows between stages
        for i in range(len(stages)-1):
            x1 = stages[i][0] + stages[i][2]
            y1 = stages[i][1] + stages[i][3] / 2
            x2 = stages[i+1][0]
            y2 = stages[i+1][1] + stages[i+1][3] / 2
            self._arrow(x1+2, y1, x2-2, y2, colour=GREY, lw=1.0)

        self._label(w/2, h*0.01, "Figure 6: Process refraction — metric substitution progressively redirects strategy", 8, colour=GREY)

    def _draw_compound_layers(self):
        import math
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Three coloured layers stacked horizontally
        layer_colours = [
            ("#1A274466", "Hierarchical"),
            ("#C4952A44", "Cultural"),
            ("#6B6B6B33", "Process"),
        ]
        lw_each = w * 0.22
        offsets = [w*0.25, w*0.47, w*0.69]
        for x, (bg, label) in zip(offsets, layer_colours):
            self._rect(x, h*0.08, lw_each, h*0.84,
                       fill=colors.HexColor(bg), stroke=colors.HexColor(bg[:7]))
            self._label(x + lw_each/2, h*0.94, label, 8, bold=True, colour=NAVY)

        # input ray
        c.setStrokeColor(NAVY)
        c.setLineWidth(2)
        c.line(w*0.05, h*0.62, w*0.25, h*0.62)
        # compound refraction path
        pts = [(w*0.25, h*0.62), (w*0.47, h*0.52), (w*0.69, h*0.40), (w*0.91, h*0.28)]
        for i in range(len(pts)-1):
            c.setStrokeColor(GOLD)
            c.setLineWidth(1.8)
            c.line(*pts[i], *pts[i+1])
        # labels
        self._label(w*0.03, h*0.65, "n₁", 9, bold=True, colour=NAVY)
        self._label(w*0.92, h*0.24, "n₄", 9, bold=True, colour=GOLD)
        self._label(w/2, h*0.01, "Figure 7: Compound refraction — multiplicative distortion across three layers", 8, colour=GREY)

    def _draw_angle_correction(self):
        import math
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Before (refracted) and after (corrected) side by side
        # Left — before
        bx1 = w * 0.28
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.6)
        c.line(bx1, h*0.08, bx1, h*0.92)
        ai = 40 * math.pi/180
        ar = 22 * math.pi/180
        rl = 0.9 * inch
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.5)
        c.line(bx1 - rl*math.cos(ai), h*0.6 + rl*math.sin(ai), bx1, h*0.6)
        c.setStrokeColor(colors.HexColor("#AA3333"))
        c.line(bx1, h*0.6, bx1 + rl*math.cos(ar), h*0.6 - rl*math.sin(ar))
        self._label(bx1, h*0.04, "Before", 9, bold=True, colour=TEXT)

        # Right — after
        bx2 = w * 0.72
        c.setStrokeColor(colors.HexColor("#AAAAAA"))
        c.setLineWidth(0.6)
        c.line(bx2, h*0.08, bx2, h*0.92)
        ai2 = 18 * math.pi/180
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.5)
        c.line(bx2 - rl*math.cos(ai2), h*0.6 + rl*math.sin(ai2), bx2, h*0.6)
        c.setStrokeColor(GOLD)
        c.line(bx2, h*0.6, bx2 + rl*math.cos(ai2*0.8), h*0.6 - rl*math.sin(ai2*0.8))
        self._label(bx2, h*0.04, "After: Reduced Index", 9, bold=True, colour=GOLD)

        # divider
        c.setStrokeColor(LGREY)
        c.setLineWidth(0.6)
        c.line(w/2, h*0.08, w/2, h*0.92)
        self._label(w/2, h*0.01, "Figure 10: Correcting the angle — index reduction and angle adjustment", 8, colour=GREY)

    def _draw_resistant_design(self):
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Parallel direct channels vs layered
        # Left: high-refraction (many layers)
        self._label(w*0.22, h*0.92, "Layered", 9, bold=True, colour=TEXT)
        import math
        for i, ang in enumerate([35, 25, 15, 5]):
            y = h * (0.22 + i * 0.16)
            a = ang * math.pi / 180
            c.setStrokeColor(NAVY)
            c.setLineWidth(1)
            bx = w * 0.32
            c.line(w*0.06, y, bx, y)
            c.setStrokeColor(GOLD)
            c.line(bx, y, bx + 0.6*inch*math.cos(a), y - 0.6*inch*math.sin(a))
        # Right: refraction-resistant (minimal crossing)
        self._label(w*0.72, h*0.92, "Low-Refraction", 9, bold=True, colour=GOLD)
        for i in range(4):
            y = h * (0.22 + i * 0.16)
            c.setStrokeColor(NAVY)
            c.setLineWidth(1)
            c.line(w*0.56, y, w*0.88, y)

        c.setStrokeColor(LGREY)
        c.setLineWidth(0.8)
        c.line(w/2, h*0.08, w/2, h*0.86)
        self._label(w/2, h*0.01, "Figure 11: Refraction-resistant design — minimal layer crossings", 8, colour=GREY)

    def _draw_leadership_optics(self):
        import math
        self._bg()
        c = self.canv
        w, h = self.width, self.height
        # Lens metaphor — intent → lens → clear transmission
        # Draw a biconvex lens
        cx, cy = w*0.5, h*0.52
        rx, ry = 0.55*inch, h*0.38
        # left arc
        c.setFillColor(colors.HexColor("#1A274422"))
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.2)
        path = c.beginPath()
        path.moveTo(cx, cy - ry)
        path.curveTo(cx - rx*1.8, cy - ry, cx - rx*1.8, cy + ry, cx, cy + ry)
        path.curveTo(cx + rx*1.8, cy + ry, cx + rx*1.8, cy - ry, cx, cy - ry)
        c.drawPath(path, fill=1, stroke=1)
        self._label(cx, cy + 4, "Leadership\nLens", 9, bold=True, colour=NAVY)

        # incoming rays (intent)
        c.setStrokeColor(NAVY)
        c.setLineWidth(1.5)
        for offset in [-22, -8, 8, 22]:
            c.line(w*0.06, cy + offset, w*0.32, cy + offset * 0.4)

        # outgoing rays (converged intent)
        c.setStrokeColor(GOLD)
        c.setLineWidth(1.5)
        for offset in [-16, -5, 5, 16]:
            c.line(w*0.68, cy + offset * 0.3, w*0.92, cy + offset * 0.7)

        self._label(w*0.06, h*0.92, "Strategic\nIntent", 8, colour=NAVY)
        self._label(w*0.88, h*0.92, "Point of\nAction", 8, colour=GOLD)
        self._label(w/2, h*0.01, "Figure 12: Leadership as optics — converging intent through the organisation", 8, colour=GREY)


# ── Markdown → flowable parser ────────────────────────────────────────────────

def clean_html_comments(text):
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

def escape_xml(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))

def inline_markup(text):
    """Convert markdown inline markup to reportlab XML."""
    text = escape_xml(text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*',         r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_',           r'<i>\1</i>', text)
    text = re.sub(r'`(.+?)`',           r'<font name="Courier" size="10">\1</font>', text)
    return text

def parse_markdown(filepath, ch_num=None, diagram_png=None):
    """Parse a markdown file and return a list of reportlab flowables."""
    raw = Path(filepath).read_text(encoding="utf-8")
    raw = clean_html_comments(raw)
    lines = raw.split('\n')

    flowables = []
    i = 0
    in_list = False
    list_items = []

    def flush_list():
        nonlocal list_items, in_list
        if list_items:
            for item in list_items:
                flowables.append(Paragraph(f"<bullet>&bull;</bullet>{inline_markup(item.strip())}", STYLE['body']))
        list_items = []
        in_list = False

    # track whether we've placed the diagram yet
    diagram_placed = False

    def place_diagram():
        nonlocal diagram_placed
        if diagram_placed:
            return
        diagram_placed = True
        flowables.append(Spacer(1, 12))
        if diagram_png and Path(diagram_png).exists():
            img = Image(str(diagram_png), width=BODY_W * 0.88, height=2.2 * inch, kind='proportional')
            flowables.append(img)
        elif ch_num:
            from chapters import CHAPTER_TITLES_MAP
            title = CHAPTER_TITLES_MAP.get(ch_num, "")
            flowables.append(DiagramPlaceholder(ch_num, title))
        flowables.append(Spacer(1, 12))

    while i < len(lines):
        line = lines[i].rstrip()

        # blank line
        if not line.strip():
            flush_list()
            i += 1
            continue

        # --- horizontal rule
        if re.match(r'^---+\s*$', line) or re.match(r'^\*\*\*+\s*$', line):
            flush_list()
            flowables.append(Spacer(1, 6))
            flowables.append(ThinRule(BODY_W * 0.3, colour=LGREY))
            flowables.append(Spacer(1, 6))
            i += 1
            continue

        # headings
        m4 = re.match(r'^####\s+(.*)', line)
        m3 = re.match(r'^###\s+(.*)', line)
        m2 = re.match(r'^##\s+(.*)', line)
        m1 = re.match(r'^#\s+(.*)', line)

        if m1:
            flush_list()
            text = m1.group(1).strip()
            # Skip chapter title we already put in opener
            if re.match(r'^Chapter', text, re.I):
                i += 1
                continue
            flowables.append(Paragraph(inline_markup(text), STYLE['h1']))
            i += 1
            continue
        if m2:
            flush_list()
            flowables.append(Paragraph(inline_markup(m2.group(1).strip()), STYLE['h2']))
            i += 1
            continue
        if m3:
            flush_list()
            flowables.append(Paragraph(inline_markup(m3.group(1).strip()), STYLE['h3']))
            i += 1
            continue
        if m4:
            flush_list()
            flowables.append(Paragraph(inline_markup(m4.group(1).strip()), STYLE['h4']))
            i += 1
            continue

        # Roman numeral section markers  **I.** / **II.** etc.
        m_sec = re.match(r'^\*\*([IVXivx]+\.)\*\*\s*$', line)
        if m_sec:
            flush_list()
            # Place diagram after section II (once per chapter)
            if not diagram_placed and re.match(r'II\.', m_sec.group(1)):
                place_diagram()
            flowables.append(Spacer(1, 8))
            flowables.append(Paragraph(m_sec.group(1), STYLE['section_num']))
            i += 1
            continue

        # italic-only line → treat as pull-quote or subtitle
        m_italic = re.match(r'^\*(.+)\*\s*$', line)
        if m_italic and len(line) < 200:
            flush_list()
            text = m_italic.group(1).strip()
            if len(text) > 40:
                flowables.append(Paragraph(f"<i>{escape_xml(text)}</i>", STYLE['pullquote']))
            else:
                flowables.append(Paragraph(f"<i>{escape_xml(text)}</i>", STYLE['h4']))
            i += 1
            continue

        # bold-only line → pull-quote header
        m_bold = re.match(r'^\*\*(.+)\*\*\s*$', line)
        if m_bold and len(line) < 120 and not re.match(r'^\*\*[IVX]+\.\*\*$', line):
            flush_list()
            flowables.append(Paragraph(f"<b>{escape_xml(m_bold.group(1))}</b>", STYLE['h3']))
            i += 1
            continue

        # bullet list
        m_li = re.match(r'^[-*]\s+(.*)', line)
        if m_li:
            in_list = True
            list_items.append(m_li.group(1))
            i += 1
            continue

        # numbered list
        m_ol = re.match(r'^\d+\.\s+(.*)', line)
        if m_ol:
            in_list = True
            list_items.append(m_ol.group(1))
            i += 1
            continue

        # regular paragraph
        flush_list()
        # accumulate multi-line paragraph
        para_lines = [line]
        while i + 1 < len(lines) and lines[i + 1].strip() and \
              not re.match(r'^(#+|[-*]|\d+\.|\*\*[IVX]+\.\*\*|---)', lines[i + 1]):
            i += 1
            para_lines.append(lines[i].rstrip())
        text = ' '.join(para_lines)

        # skip owner/version/status metadata lines
        if re.match(r'\*\*(Owner|Version|Date|Status|Word count):', text):
            i += 1
            continue

        flowables.append(Paragraph(inline_markup(text), STYLE['body']))
        i += 1

    flush_list()

    # If diagram wasn't placed mid-chapter, place at end
    if not diagram_placed and (diagram_png or ch_num):
        place_diagram()

    return flowables

class CoverPage(Flowable):
    """Full-bleed cover — draws directly on the canvas ignoring frame dimensions."""

    def __init__(self, img_path=None):
        super().__init__()
        self.img_path = img_path
        self.width  = BODY_W
        self.height = BODY_H

    def draw(self):
        c = self.canv
        c.saveState()
        if self.img_path:
            from reportlab.lib.utils import ImageReader
            try:
                ir = ImageReader(self.img_path)
                # Draw from bottom-left of page, full page size
                # We're inside the frame so offset back by margins
                x_offset = -MARGIN_LEFT
                y_offset = -MARGIN_BOTTOM
                c.drawImage(ir, x_offset, y_offset, width=PAGE_W, height=PAGE_H,
                            preserveAspectRatio=False)
            except Exception:
                self._draw_fallback(c)
        else:
            self._draw_fallback(c)
        c.restoreState()

    def _draw_fallback(self, c):
        x_off, y_off = -MARGIN_LEFT, -MARGIN_BOTTOM
        c.setFillColor(NAVY)
        c.rect(x_off, y_off, PAGE_W, PAGE_H, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 34)
        c.drawCentredString(PAGE_W/2 - MARGIN_LEFT, PAGE_H*0.62 - MARGIN_BOTTOM,
                            "Organizational Refraction")
        c.setFillColor(colors.HexColor("#FFFFFFCC"))
        c.setFont("Helvetica-Oblique", 13)
        c.drawCentredString(PAGE_W/2 - MARGIN_LEFT, PAGE_H*0.50 - MARGIN_BOTTOM,
                            "Why Your Strategy Arrives Somewhere It Was Never Aimed")
        c.setFillColor(GREY)
        c.setFont("Helvetica", 10)
        c.drawCentredString(PAGE_W/2 - MARGIN_LEFT, PAGE_H*0.14 - MARGIN_BOTTOM,
                            "[Author Name — TBD]")


# provide the CHAPTER_TITLES_MAP to the closure
import sys
_mod = sys.modules[__name__]
_mod.CHAPTER_TITLES_MAP = {
    ch[0]: ch[2] for ch in CHAPTERS
}

# monkey-patch so parse_markdown can use it
import builtins
class _FakeModule:
    CHAPTER_TITLES_MAP = _mod.CHAPTER_TITLES_MAP
sys.modules['chapters'] = _FakeModule()


# ── Page canvas callbacks ─────────────────────────────────────────────────────

_page_state = {"chapter_title": "", "is_chapter_opener": False, "page_num": 0}

def on_page(canvas_obj, doc):
    pn = doc.page
    _page_state["page_num"] = pn

    canvas_obj.saveState()

    # Don't add headers/footers on cover page, half-title, part dividers
    is_decorative = pn <= 2  # cover + blank verso
    if is_decorative:
        canvas_obj.restoreState()
        return

    # running header
    canvas_obj.setFont("Helvetica", 7.5)
    canvas_obj.setFillColor(GREY)
    if pn % 2 == 0:  # even page: left — chapter title
        canvas_obj.drawString(MARGIN_LEFT, PAGE_H - MARGIN_TOP * 0.5,
                              _page_state["chapter_title"].upper())
    else:  # odd page: right — book title
        book = "ORGANIZATIONAL REFRACTION"
        canvas_obj.drawRightString(PAGE_W - MARGIN_RIGHT, PAGE_H - MARGIN_TOP * 0.5, book)

    # rule under header
    canvas_obj.setStrokeColor(LGREY)
    canvas_obj.setLineWidth(0.4)
    y_rule = PAGE_H - MARGIN_TOP * 0.62
    canvas_obj.line(MARGIN_LEFT, y_rule, PAGE_W - MARGIN_RIGHT, y_rule)

    # page number
    if pn > 4:  # skip page numbers on frontmatter
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(GREY)
        if pn % 2 == 0:
            canvas_obj.drawString(MARGIN_LEFT, MARGIN_BOTTOM * 0.45, str(pn))
        else:
            canvas_obj.drawRightString(PAGE_W - MARGIN_RIGHT, MARGIN_BOTTOM * 0.45, str(pn))

    canvas_obj.restoreState()


# ── Document assembly ─────────────────────────────────────────────────────────

def build_story():
    story = []

    # ── 1. Cover page ────────────────────────────────────────────────────────
    _page_state["chapter_title"] = ""
    cover_img = DESIGN_DIR / "cover-front.png"
    story.append(CoverPage(str(cover_img) if cover_img.exists() else None))
    story.append(PageBreak())

    # ── 2. Title page + copyright ────────────────────────────────────────────
    _page_state["chapter_title"] = "Title Page"
    title_md = BOOK_DIR / "book/frontmatter/title-page.md"
    story.extend(_make_title_page(title_md))
    story.append(PageBreak())

    # ── 3. Table of contents ─────────────────────────────────────────────────
    _page_state["chapter_title"] = "Table of Contents"
    story.extend(_make_toc())
    story.append(PageBreak())

    # ── 4. Parts and chapters ────────────────────────────────────────────────
    current_part = -1
    for ch_data in CHAPTERS:
        ch_num, ch_num_word, ch_title, ch_subtitle, ch_dir, ch_file, part_idx, diag = ch_data

        # Part divider when part changes
        if part_idx != current_part:
            current_part = part_idx
            part_num, part_title, part_sub = PARTS[part_idx]
            story.append(PageBreak())
            story.append(PartDivider(part_num, part_title, part_sub))
            story.append(PageBreak())

        # Chapter opener
        _page_state["chapter_title"] = f"Chapter {ch_num}: {ch_title}"
        story.append(ChapterOpener(
            ch_num_word, ch_num, ch_title, ch_subtitle,
            PARTS[part_idx][0] + " — " + PARTS[part_idx][1]
        ))
        story.append(Spacer(1, 24))

        # Body text
        ch_path = BOOK_DIR / "book/chapters" / ch_dir / ch_file
        if ch_path.exists():
            body = parse_markdown(str(ch_path), ch_num=ch_num, diagram_png=diag)
            story.extend(body)
        else:
            story.append(Paragraph(f"[Manuscript for Chapter {ch_num} not found at {ch_path}]",
                                   STYLE['small']))

        story.append(PageBreak())

    # ── 5. Bibliography ──────────────────────────────────────────────────────
    _page_state["chapter_title"] = "Bibliography"
    story.append(PageBreak())
    story.extend(_make_bibliography())

    # ── 6. Index ─────────────────────────────────────────────────────────────
    _page_state["chapter_title"] = "Index"
    story.append(PageBreak())
    story.extend(_make_index())

    return story


def _make_fallback_cover():
    """Text-only cover if image missing."""
    from reportlab.platypus.flowables import Flowable

    class FallbackCover(Flowable):
        def __init__(self):
            super().__init__()
            self.width = PAGE_W
            self.height = PAGE_H

        def draw(self):
            c = self.canv
            c.setFillColor(NAVY)
            c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
            c.setFillColor(GOLD)
            c.setFont("Helvetica", 10)
            c.drawCentredString(PAGE_W/2, PAGE_H*0.78, "ORGANIZATIONAL REFRACTION CO.")
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 32)
            c.drawCentredString(PAGE_W/2, PAGE_H*0.62, "Organizational")
            c.drawCentredString(PAGE_W/2, PAGE_H*0.54, "Refraction")
            c.setFillColor(GOLD)
            c.setLineWidth(1.5)
            c.line(PAGE_W*0.2, PAGE_H*0.51, PAGE_W*0.8, PAGE_H*0.51)
            c.setFillColor(colors.HexColor("#FFFFFFCC"))
            c.setFont("Helvetica-Oblique", 13)
            c.drawCentredString(PAGE_W/2, PAGE_H*0.44,
                                "Why Your Strategy Arrives Somewhere")
            c.drawCentredString(PAGE_W/2, PAGE_H*0.39, "It Was Never Aimed")
            c.setFillColor(GREY)
            c.setFont("Helvetica", 10)
            c.drawCentredString(PAGE_W/2, PAGE_H*0.14, "[Author Name — TBD]")

    return FallbackCover()


def _make_title_page(md_path):
    flowables = []
    flowables.append(Spacer(1, 1.5 * inch))

    # Half title
    flowables.append(Paragraph("ORGANIZATIONAL REFRACTION",
                                ParagraphStyle("halftitle",
                                               fontName="Helvetica", fontSize=12,
                                               textColor=NAVY, alignment=TA_CENTER,
                                               spaceAfter=6)))
    flowables.append(Spacer(1, 0.5 * inch))

    # Full title
    flowables.append(Paragraph("Organizational Refraction",
                                ParagraphStyle("title_big",
                                               fontName="Helvetica-Bold", fontSize=30,
                                               textColor=NAVY, alignment=TA_CENTER,
                                               spaceAfter=10, leading=36)))
    flowables.append(ThinRule(BODY_W * 0.6, colour=GOLD))
    flowables.append(Spacer(1, 10))
    flowables.append(Paragraph(
        "<i>Why Your Strategy Arrives Somewhere It Was Never Aimed</i>",
        ParagraphStyle("subtitle_tp",
                       fontName="Times-Italic", fontSize=14, leading=20,
                       textColor=TEXT, alignment=TA_CENTER, spaceAfter=30)))

    flowables.append(Spacer(1, 0.8 * inch))
    flowables.append(Paragraph("[Author Name — TBD]",
                                ParagraphStyle("author_tp",
                                               fontName="Helvetica", fontSize=12,
                                               textColor=TEXT, alignment=TA_CENTER,
                                               spaceAfter=6)))
    flowables.append(Spacer(1, 0.4 * inch))
    flowables.append(Paragraph("[Series — TBD]",
                                ParagraphStyle("series_tp",
                                               fontName="Helvetica", fontSize=10,
                                               textColor=GREY, alignment=TA_CENTER,
                                               spaceAfter=4)))
    flowables.append(Paragraph("[Publisher / Imprint — TBD]",
                                ParagraphStyle("pub_tp",
                                               fontName="Helvetica", fontSize=10,
                                               textColor=GREY, alignment=TA_CENTER)))

    flowables.append(PageBreak())

    # Copyright verso
    flowables.append(Spacer(1, 3.0 * inch))
    for line in [
        "Copyright © [YEAR — TBD] by [Author Name — TBD].",
        "All rights reserved.",
        "",
        "Published by [Publisher / Imprint — TBD].",
        "First edition: [YEAR — TBD].",
        "",
        "ISBN: [ISBN — TBD]",
        "",
        "Printed in [Country — TBD].",
        "",
        "<i>This is a DRAFT manuscript. Not for distribution.</i>",
    ]:
        if line:
            flowables.append(Paragraph(inline_markup(line),
                                       ParagraphStyle("copy_p",
                                                      fontName="Times-Roman", fontSize=9,
                                                      leading=14, textColor=GREY,
                                                      alignment=TA_LEFT, spaceAfter=2)))
        else:
            flowables.append(Spacer(1, 5))

    return flowables


def _make_toc():
    flowables = []
    flowables.append(Spacer(1, 0.3 * inch))
    flowables.append(Paragraph("Table of Contents",
                                ParagraphStyle("toc_head",
                                               fontName="Helvetica-Bold", fontSize=22,
                                               textColor=NAVY, spaceAfter=6, leading=28)))
    flowables.append(ThinRule(BODY_W, colour=GOLD))
    flowables.append(Spacer(1, 16))

    flowables.append(Paragraph("Front Matter", STYLE['toc_part']))
    for fm in ["Title Page", "Copyright", "Table of Contents"]:
        flowables.append(Paragraph(f"  {fm}", STYLE['toc_ch']))

    flowables.append(Spacer(1, 12))

    current_part = -1
    for ch_num, ch_num_word, ch_title, ch_subtitle, _, _, part_idx, _ in CHAPTERS:
        if part_idx != current_part:
            current_part = part_idx
            pn, pt, ps = PARTS[part_idx]
            flowables.append(Spacer(1, 10))
            flowables.append(Paragraph(f"{pn} — {pt}  <i>({ps})</i>",
                                        STYLE['toc_part']))

        flowables.append(Paragraph(
            f"Chapter {ch_num} — {ch_title}",
            STYLE['toc_ch']))
        flowables.append(Paragraph(f"<i>{ch_subtitle}</i>", STYLE['toc_sub']))

    flowables.append(Spacer(1, 16))
    flowables.append(Paragraph("Back Matter", STYLE['toc_part']))
    for bm in ["Bibliography", "Index"]:
        flowables.append(Paragraph(f"  {bm}", STYLE['toc_ch']))

    return flowables


def _make_bibliography():
    flowables = []
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(Paragraph("Bibliography",
                                ParagraphStyle("bib_head",
                                               fontName="Helvetica-Bold", fontSize=22,
                                               textColor=NAVY, spaceAfter=6, leading=28)))
    flowables.append(ThinRule(BODY_W, colour=GOLD))
    flowables.append(Spacer(1, 8))
    flowables.append(Paragraph(
        "<i>All citations follow Chicago author-date style. "
        "Chapter references in brackets indicate where each source is cited.</i>",
        STYLE['small']))
    flowables.append(Spacer(1, 16))

    bib_path = BOOK_DIR / "book/backmatter/bibliography.md"
    raw = bib_path.read_text(encoding="utf-8")
    raw = clean_html_comments(raw)
    for line in raw.split('\n'):
        line = line.rstrip()
        if not line:
            flowables.append(Spacer(1, 3))
            continue
        if re.match(r'^#\s', line):
            continue  # main heading
        if re.match(r'^##\s', line):
            letter = line[3:].strip()
            flowables.append(Paragraph(letter, STYLE['bib_letter']))
            continue
        if line.startswith('---'):
            flowables.append(ThinRule(BODY_W * 0.3, colour=LGREY))
            continue
        flowables.append(Paragraph(inline_markup(line), STYLE['bib_entry']))

    return flowables


def _make_index():
    flowables = []
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(Paragraph("Index",
                                ParagraphStyle("idx_head",
                                               fontName="Helvetica-Bold", fontSize=22,
                                               textColor=NAVY, spaceAfter=6, leading=28)))
    flowables.append(ThinRule(BODY_W, colour=GOLD))
    flowables.append(Spacer(1, 16))

    idx_path = BOOK_DIR / "book/backmatter/index.md"
    raw = idx_path.read_text(encoding="utf-8")
    raw = clean_html_comments(raw)

    for line in raw.split('\n'):
        line = line.rstrip()
        if not line:
            continue
        if re.match(r'^#\s', line):
            continue
        if re.match(r'^##\s', line):
            letter = line[3:].strip()
            flowables.append(Spacer(1, 6))
            flowables.append(Paragraph(letter, STYLE['bib_letter']))
            continue
        if line.startswith('---'):
            flowables.append(ThinRule(BODY_W * 0.3, colour=LGREY))
            continue
        # table rows |...|...|
        if '|' in line:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if cells and not re.match(r'^[-:]+$', cells[0]):
                row_text = "  ".join(inline_markup(c) for c in cells)
                flowables.append(Paragraph(row_text,
                                           ParagraphStyle("idx_entry",
                                                          fontName="Times-Roman", fontSize=9.5,
                                                          leading=15, textColor=TEXT,
                                                          spaceAfter=2)))
        else:
            flowables.append(Paragraph(inline_markup(line),
                                       ParagraphStyle("idx_line",
                                                      fontName="Times-Roman", fontSize=9.5,
                                                      leading=15, textColor=TEXT,
                                                      spaceAfter=2)))

    return flowables


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Building PDF → {OUT_PATH}")

    frame = Frame(
        MARGIN_LEFT, MARGIN_BOTTOM, BODY_W, BODY_H,
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
        id="body"
    )

    doc = BaseDocTemplate(
        str(OUT_PATH),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Organizational Refraction — DRAFT",
        author="[Author Name — TBD]",
        subject="Why Your Strategy Arrives Somewhere It Was Never Aimed",
    )

    template = PageTemplate(id="main", frames=[frame], onPage=on_page)
    doc.addPageTemplates([template])

    story = build_story()

    print(f"  Story elements: {len(story)}")
    doc.build(story)

    import os
    size_kb = os.path.getsize(OUT_PATH) // 1024
    print(f"  Done. File size: {size_kb} KB")
    print(f"  Output: {OUT_PATH}")


if __name__ == "__main__":
    main()
