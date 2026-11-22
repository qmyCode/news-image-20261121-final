"""Build tool for the news-image-20261121 entry — REBUILD in the winning
anatomy (22 November 2026).

Renders entry.png (1024x1024): one page summing up the world news of
Saturday 21 November 2026, built the way the field's top pages are built:
a stat bar, a region tally, three large illustrated mains, ten illustrated
story cards, a numbered world map, a numbered ALSO column and a DATE CHECK
band that names what was left out and why.

Every story was verified against wire reporting: it happened, or was
first reported, on Saturday 21 November 2026 (UTC). Figures trace to the
research bank (newsimage-research/21nov) plus the wire re-verification of
22 November (Peru quake, the Saturday Hormuz hits, the CEPA signing, the
Sinaloa capture, the Sparta II). Sources are named on the page. This file
is a build tool only; main.py never imports it.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 40)
MUTE = (96, 92, 84)
RULE = (26, 26, 40)
ACCENT = (164, 32, 24)
GREEN = (22, 110, 62)
BLUE = (24, 62, 122)
CHIP_BG = (232, 224, 205)
SEA = (16, 44, 74)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF = FD + "DejaVuSerif.ttf"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, s, font, maxw, fill=INK, lh=None, max_lines=None):
    x, y = xy
    lines = wrap(d, s, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    if lh is None:
        lh = font.size + 3
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def vgrad(d, box, top, bot):
    x0, y0, x1, y1 = box
    steps = max(2, y1 - y0)
    for i in range(steps):
        t = i / (steps - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.line([x0, y0 + i, x1, y0 + i], fill=c)


def burst(d, cx, cy, r, col=(250, 160, 40), inner=(255, 230, 150)):
    import math
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=col)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
              fill=inner)


def smoke(d, cx, cy, s=1.0, col=(90, 88, 92)):
    for i, (dx, dy, r) in enumerate([(0, 0, 10), (7, -10, 13),
                                     (-4, -22, 16), (5, -36, 20)]):
        c = tuple(min(255, v + i * 14) for v in col)
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=c)


def tanker(d, cx, cy, s=1.0, flip=False):
    """A laden tanker side-on: hull, deck tanks, superstructure aft."""
    hull = (38, 34, 40)
    L = 118 * s
    Hh = 15 * s
    sg = -1 if flip else 1
    d.polygon([(cx - L / 2, cy), (cx + L / 2, cy),
               (cx + L / 2 - 12 * s * sg, cy + Hh),
               (cx - L / 2 + 6 * s * sg, cy + Hh)], fill=hull)
    d.rectangle([cx - L / 2, cy - 4 * s, cx + L / 2, cy], fill=(120, 40, 34))
    for i in range(4):
        tx = cx - L / 2 + (14 + i * 24) * s * (1 if not flip else -1)
        if flip:
            tx = cx + L / 2 - (14 + i * 24) * s
        d.rectangle([tx, cy - 11 * s, tx + 18 * s, cy - 4 * s],
                    fill=(168, 96, 52), outline=(90, 55, 30))
    sx = cx + (L / 2 - 16 * s) * sg
    d.rectangle([sx - 8 * s, cy - 24 * s, sx + 8 * s, cy - 4 * s],
                fill=(226, 222, 212))
    d.rectangle([sx - 2 * s, cy - 30 * s, sx + 2 * s, cy - 24 * s],
                fill=(120, 118, 110))


# ------------------------------------------------------------- main scenes

def scene_hormuz(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (24, 42, 84), (214, 132, 74))
    horizon = y0 + int((y1 - y0) * 0.52)
    vgrad(d, (x0, horizon, x1, y1), (28, 84, 118), (12, 40, 74))
    # Iran shore, top right; Oman (Musandam) shore, bottom left
    d.polygon([(x1 - 120, y0), (x1, y0), (x1, horizon - 26),
               (x1 - 66, horizon - 8), (x1 - 118, horizon - 20)],
              fill=(186, 152, 104))
    d.polygon([(x0, y1), (x0, horizon + 30), (86, horizon + 16),
               (128, y1)], fill=(172, 138, 94))
    text(d, (x1 - 30, y0 + 26), "IRAN", F(SANS_B, 10), fill=(70, 52, 30),
         anchor="ra")
    text(d, (x0 + 8, y1 - 16), "OMAN", F(SANS_B, 10), fill=(70, 52, 30))
    # dashed transit route through the strait
    for i in range(9):
        sx = x0 + 66 + i * 26
        sy = horizon + 6 + (6 if i % 2 else -4)
        d.line([sx, sy, sx + 13, sy + (3 if i % 2 else -2)],
               fill=(240, 240, 235), width=2)
    # tanker 1 (left): stern hit, fire and smoke
    tanker(d, x0 + 92, horizon + 14, 0.82)
    burst(d, x0 + 40, horizon + 8, 15)
    smoke(d, x0 + 44, horizon - 4, 0.8)
    # tanker 2 (right): engine-room hit
    tanker(d, x1 - 84, horizon + 34, 0.82, flip=True)
    burst(d, x1 - 36, horizon + 28, 13)
    smoke(d, x1 - 30, horizon + 16, 0.7)
    text(d, (x0 + 118, horizon - 14), "KHASAB", F(SANS_B, 9),
         fill=(250, 244, 224))


def scene_peru(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (196, 220, 236), (238, 232, 210))
    surf = y0 + int((y1 - y0) * 0.46)
    # Andes: three layered ridges with snow caps
    def ridge(base, col, peaks):
        pts = [(x0, base)]
        for px, py in peaks:
            pts.append((x0 + px, base - py))
        pts += [(x1, base), (x1, y1), (x0, y1)]
        d.polygon(pts, fill=col)
    ridge(surf + 8, (148, 162, 178),
          [(40, 44), (90, 26), (140, 52), (200, 30), (258, 46), (300, 28)])
    ridge(surf + 16, (104, 118, 138),
          [(20, 30), (76, 52), (128, 24), (188, 44), (246, 22), (296, 38)])
    d.polygon([(x0, surf), (x1, surf), (x1, y1), (x0, y1)],
              fill=(122, 88, 58))
    for i in range(3):
        d.line([x0, surf + 16 + i * 13, x1, surf + 13 + i * 13],
               fill=(100, 70, 44), width=2)
    # houses on the ridge line, one leaning
    for hx, lean in [(52, 0), (96, 5)]:
        d.rectangle([x0 + hx, surf - 16, x0 + hx + 22, surf - 2],
                    fill=(232, 224, 205))
        d.polygon([(x0 + hx - 3, surf - 16), (x0 + hx + 11, surf - 26 + lean),
                   (x0 + hx + 25, surf - 16)], fill=(150, 60, 40))
    # Lima skyline, right
    for i, bh in enumerate([20, 30, 24, 36, 27]):
        bx = x1 - 92 + i * 17
        d.rectangle([bx, surf - bh, bx + 14, surf], fill=(96, 104, 122))
    text(d, (x1 - 48, surf - 44), "LIMA", F(SANS_B, 9), fill=(70, 78, 96),
         anchor="ma")
    # epicentre: star + rings deep below the ridge
    ex, ey = x0 + 168, y1 - 26
    for r in (30, 21, 13):
        d.ellipse([ex - r, ey - r * 0.55, ex + r, ey + r * 0.55],
                  outline=(230, 120, 50), width=2)
    burst(d, ex, ey, 11, col=(226, 84, 40), inner=(255, 214, 140))
    d.line([x1 - 120, surf + 4, ex + 16, ey - 4], fill=(240, 240, 235),
           width=1)
    text(d, (x1 - 116, surf + 8), "108 km deep", F(SANS_B, 9),
         fill=(250, 244, 224))


def scene_cop31(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(14, 46, 54))
    # flags along the back wall
    cols = [(200, 40, 40), (240, 200, 60), (60, 120, 200),
            (240, 240, 240), (40, 160, 90), (200, 110, 30)]
    for i, c in enumerate(cols):
        fx = x0 + 20 + i * ((x1 - x0 - 40) // 5)
        d.line([fx, y0 + 8, fx, y0 + 30], fill=(210, 210, 210), width=2)
        d.rectangle([fx, y0 + 8, fx + 14, y0 + 18], fill=c)
    # globe, centre-left of the wall
    gx, gy, gr = x0 + 66, y0 + 62, 30
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(52, 110, 168))
    d.polygon([(gx - 20, gy - 16), (gx - 6, gy - 22), (gx - 2, gy - 8),
               (gx - 14, gy + 2), (gx - 22, gy - 4)], fill=(64, 148, 84))
    d.polygon([(gx + 6, gy + 8), (gx + 20, gy + 4), (gx + 22, gy + 18),
               (gx + 10, gy + 22)], fill=(64, 148, 84))
    d.polygon([(gx + 2, gy - 20), (gx + 14, gy - 24), (gx + 16, gy - 12),
               (gx + 6, gy - 10)], fill=(64, 148, 84))
    # thermometer: the 1.5 line long passed
    tx = x0 + 128
    d.rectangle([tx, y0 + 34, tx + 9, y0 + 88], fill=(226, 222, 212))
    d.rectangle([tx + 2, y0 + 44, tx + 7, y0 + 88], fill=ACCENT)
    d.ellipse([tx - 4, y0 + 82, tx + 13, y0 + 99], fill=ACCENT)
    text(d, (tx + 16, y0 + 40), "1.5°C", F(SANS_B, 11),
         fill=(250, 244, 224))
    # clock past midnight, right
    cx, cy, r = x1 - 40, y0 + 56, 21
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(240, 230, 200),
              width=2)
    d.line([cx, cy, cx, cy - 14], fill=(240, 230, 200), width=2)
    d.line([cx, cy, cx + 10, cy + 5], fill=(240, 230, 200), width=2)
    text(d, (cx, cy + r + 4), "DAY 13", F(SANS_B, 9), fill=(250, 244, 224),
         anchor="ma")
    # the long table and its delegates
    ty = y1 - 30
    d.rectangle([x0 + 12, ty, x1 - 12, y1 - 8], fill=(96, 64, 32))
    skins = [(222, 190, 150), (150, 104, 66), (240, 208, 170),
             (120, 78, 48), (232, 198, 160), (170, 122, 84),
             (210, 176, 138), (96, 62, 40)]
    for i, sk in enumerate(skins):
        cx = x0 + 34 + i * ((x1 - x0 - 68) // 7)
        d.polygon([(cx - 11, ty + 2), (cx + 11, ty + 2), (cx + 7, ty - 10),
                   (cx - 7, ty - 10)], fill=(52, 62, 84))
        d.ellipse([cx - 6, ty - 22, cx + 6, ty - 10], fill=sk)
        d.rectangle([cx - 8, ty + 4, cx + 8, ty + 10], fill=(238, 234, 222))
    # the draft, struck through, centre of the table
    dx0, dy0, dx1, dy1 = (x0 + x1) // 2 - 52, ty - 26, (x0 + x1) // 2 + 52, ty - 4
    d.rectangle([dx0, dy0, dx1, dy1], fill=(238, 234, 222))
    text(d, ((dx0 + dx1) // 2, dy0 + 3), "FOSSIL FUELS", F(SANS_B, 10),
         fill=(90, 88, 80), anchor="ma")
    d.line([dx0 + 4, dy0 + 15, dx1 - 4, dy0 + 6], fill=ACCENT, width=3)


# ------------------------------------------------------------ card banners

def banner_cepa(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(18, 40, 92))
    # EU flag: circle of stars
    import math
    cx, cy = x0 + 30, (y0 + y1) // 2
    for i in range(12):
        a = i * math.pi / 6
        sx, sy = cx + 13 * math.cos(a), cy + 13 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 204, 60))
    # Indonesian flag
    fx, fy = x1 - 52, y0 + 9
    d.rectangle([fx, fy, fx + 34, fy + 11], fill=(206, 42, 42))
    d.rectangle([fx, fy + 11, fx + 34, fy + 22], fill=(244, 244, 244))
    # the signed document between them
    dx0, dy0 = (x0 + x1) // 2 - 17, y0 + 6
    d.rectangle([dx0, dy0, dx0 + 34, dy0 + 34], fill=(240, 236, 226))
    for i in range(3):
        d.line([dx0 + 5, dy0 + 8 + i * 6, dx0 + 29, dy0 + 8 + i * 6],
               fill=(150, 148, 140), width=2)
    d.line([dx0 + 20, dy0 + 30, dx0 + 33, dy0 + 19], fill=ACCENT, width=3)


def banner_riyadh(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(9, 12, 36))
    for sx, sy in [(18, 8), (60, 16), (110, 6), (150, 14), (84, 22),
                   (36, 26)]:
        d.point((x0 + sx, y0 + sy), fill=(228, 228, 218))
    base = y1 - 4
    for i, bh in enumerate([14, 22, 17, 26, 15, 20]):
        bx = x0 + 8 + i * 28
        d.rectangle([bx, base - bh, bx + 22, base], fill=(20, 24, 48))
    for sx, ex, peak in [(30, 96, 26), (66, 128, 32)]:
        for t in range(13):
            px = sx + (ex - sx) * t / 12
            py = y0 + 6 + peak * (t / 12) ** 1.6
            d.point((int(px), int(py)), fill=(250, 190, 90))
    burst(d, x0 + 100, y0 + 34, 9)
    burst(d, x0 + 132, y0 + 40, 7)
    for t in range(11):
        px = x0 + 44 + 52 * t / 10
        py = y1 - 12 - 22 * (t / 10) + 8 * (t / 10) ** 2
        d.point((int(px), int(py)), fill=(140, 220, 160))


def banner_sparta(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (70, 96, 128), (18, 48, 84))
    wy = y1 - 12
    d.rectangle([x0, wy, x1, y1], fill=(14, 44, 78))
    for i in range(5):
        d.arc([x0 + 12 + i * 32, wy - 2, x0 + 36 + i * 32, wy + 8],
              180, 360, fill=(120, 170, 210), width=2)
    tanker(d, (x0 + x1) // 2, wy - 12, 0.62)
    burst(d, (x0 + x1) // 2 + 8, wy - 24, 8)
    smoke(d, (x0 + x1) // 2 + 12, wy - 14, 0.35)
    # the drone, top left
    dx, dy = x0 + 26, y0 + 12
    d.line([dx - 8, dy - 5, dx + 8, dy + 5], fill=(30, 30, 36), width=3)
    d.line([dx - 8, dy + 5, dx + 8, dy - 5], fill=(30, 30, 36), width=3)
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(30, 30, 36))


def banner_bitcoin(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(16, 18, 26))
    pts = [(6, 10), (34, 14), (58, 24), (82, 38), (98, 40), (116, 30),
           (138, 22)]
    for i in range(len(pts) - 1):
        col = ACCENT if i < 4 else (52, 178, 100)
        d.line([x0 + pts[i][0], y0 + pts[i][1], x0 + pts[i + 1][0],
                y0 + pts[i + 1][1]], fill=col, width=3)
    for px, py in pts:
        d.ellipse([x0 + px - 2, y0 + py - 2, x0 + px + 2, y0 + py + 2],
                  fill=(240, 240, 240))
    cx, cy = x1 - 22, (y0 + y1) // 2
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(240, 148, 32))
    text(d, (cx, cy - 10), "B", F(SANS_B, 19), fill=(255, 255, 255),
         anchor="ma")
    d.line([cx - 4, cy - 12, cx - 4, cy + 12], fill=(255, 255, 255),
           width=2)
    d.line([cx + 2, cy - 12, cx + 2, cy + 12], fill=(255, 255, 255),
           width=2)


def banner_mercury(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(6, 8, 18))
    for sx, sy in [(16, 8), (52, 20), (90, 6), (128, 16), (150, 30),
                   (30, 34), (70, 28)]:
        d.point((x0 + sx, y0 + sy), fill=(220, 220, 215))
    px, py, pr = x1 - 34, (y0 + y1) // 2, 19
    d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(168, 160, 150))
    d.pieslice([px - pr, py - pr, px + pr, py + pr], 90, 270,
               fill=(104, 98, 92))
    for dx, dy, r in [(-6, -6, 4), (5, 3, 3), (-2, 9, 2), (9, -9, 2)]:
        d.ellipse([px + dx - r, py + dy - r, px + dx + r, py + dy + r],
                  outline=(120, 112, 104))
    # the stack: bus + two solar wings, on a dashed approach arc
    sx, sy = x0 + 34, y0 + 16
    d.rectangle([sx - 12, sy - 3, sx - 4, sy + 4], fill=(70, 110, 190))
    d.rectangle([sx + 4, sy - 3, sx + 12, sy + 4], fill=(70, 110, 190))
    d.rectangle([sx - 4, sy - 5, sx + 4, sy + 6], fill=(226, 222, 212))
    d.arc([sx - 6, sy - 8, px + 26, py + 30], 150, 235,
          fill=(200, 200, 195), width=1)


def banner_sinaloa(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (120, 52, 30), (232, 138, 66))
    gy = y1 - 10
    d.rectangle([x0, gy, x1, y1], fill=(52, 40, 34))
    # house silhouette, left
    d.rectangle([x0 + 8, gy - 20, x0 + 34, gy], fill=(40, 30, 30))
    d.polygon([(x0 + 5, gy - 20), (x0 + 21, gy - 29), (x0 + 37, gy - 20)],
              fill=(30, 22, 22))
    # burning roadblock, centre
    bx = (x0 + x1) // 2
    for i, dx in enumerate([-14, -5, 5, 14]):
        d.line([bx + dx, gy, bx + dx // 2, gy - 9], fill=(70, 44, 22),
               width=4)
    burst(d, bx, gy - 14, 11)
    smoke(d, bx + 4, gy - 16, 0.35)
    # helicopter, top right
    hx, hy = x1 - 34, y0 + 12
    d.ellipse([hx - 12, hy - 4, hx + 12, hy + 5], fill=(30, 26, 26))
    d.line([hx - 26, hy - 8, hx + 26, hy - 8], fill=(30, 26, 26), width=2)
    d.line([hx + 10, hy + 2, hx + 24, hy - 2], fill=(30, 26, 26), width=3)
    d.line([hx - 6, hy + 5, hx - 6, hy + 9], fill=(30, 26, 26), width=2)
    d.line([hx + 6, hy + 5, hx + 6, hy + 9], fill=(30, 26, 26), width=2)


def banner_wellington(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(34, 110, 52))
    d.rectangle([x0, y1 - 14, x1, y1], fill=(196, 178, 138))
    for i in range(3):
        d.rectangle([x1 - 34 + i * 7, y0 + 12, x1 - 31 + i * 7, y0 + 30],
                    fill=(240, 230, 190))
    # batsman, right of the crease
    bx, by = x1 - 62, y0 + 14
    d.ellipse([bx - 5, by - 8, bx + 5, by + 2], fill=(240, 240, 240))
    d.line([bx, by + 2, bx, by + 16], fill=(240, 240, 240), width=5)
    d.line([bx, by + 16, bx - 8, by + 30], fill=(240, 240, 240), width=5)
    d.line([bx, by + 16, bx + 7, by + 30], fill=(240, 240, 240), width=5)
    d.line([bx + 1, by + 6, bx + 16, by + 20], fill=(150, 110, 60),
           width=5)
    # bowler, left, arm up; the red ball between them
    gx, gy = x0 + 22, y0 + 12
    d.ellipse([gx - 5, gy - 6, gx + 5, gy + 4], fill=(30, 30, 90))
    d.line([gx, gy + 4, gx, gy + 18], fill=(30, 30, 90), width=5)
    d.line([gx, gy + 7, gx + 13, gy - 4], fill=(30, 30, 90), width=4)
    d.line([gx, gy + 18, gx - 7, gy + 32], fill=(30, 30, 90), width=4)
    d.line([gx, gy + 18, gx + 8, gy + 32], fill=(30, 30, 90), width=4)
    d.ellipse([x0 + 66, y0 + 20, x0 + 72, y0 + 26], fill=(200, 40, 40))


def banner_england(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(26, 92, 44))
    for i in range(4):
        d.rectangle([x0 + i * 44, y0, x0 + i * 44 + 22, y1],
                    fill=(30, 102, 50))
    # posts
    px = x0 + 34
    d.line([px, y0 + 6, px, y1 - 4], fill=(244, 244, 244), width=3)
    d.line([px + 22, y0 + 6, px + 22, y1 - 4], fill=(244, 244, 244),
           width=3)
    d.line([px, y0 + 22, px + 22, y0 + 22], fill=(244, 244, 244), width=3)
    # the ball, kicked high
    bx, by = x1 - 52, y0 + 14
    d.ellipse([bx - 9, by - 6, bx + 9, by + 6], fill=(240, 236, 226))
    d.line([bx - 5, by, bx + 5, by], fill=(150, 60, 40), width=2)


def banner_robots(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(20, 22, 34))
    # robot head
    cx, cy = x0 + 40, (y0 + y1) // 2 + 2
    d.line([cx, cy - 22, cx, cy - 15], fill=(170, 176, 190), width=2)
    d.ellipse([cx - 3, cy - 25, cx + 3, cy - 19], fill=(250, 190, 60))
    d.rounded_rectangle([cx - 17, cy - 15, cx + 17, cy + 15], 6,
                        fill=(150, 158, 175))
    d.ellipse([cx - 10, cy - 5, cx - 3, cy + 2], fill=(20, 24, 34))
    d.ellipse([cx + 3, cy - 5, cx + 10, cy + 2], fill=(20, 24, 34))
    d.line([cx - 8, cy + 8, cx + 8, cy + 8], fill=(20, 24, 34), width=2)
    # rifle silhouette under a prohibition sign, right
    rx, ry = x1 - 62, cy
    d.polygon([(rx, ry + 2), (rx + 34, ry + 2), (rx + 38, ry + 6),
               (rx + 12, ry + 6), (rx + 10, ry + 12), (rx + 4, ry + 12),
               (rx + 2, ry + 6), (rx, ry + 6)], fill=(196, 200, 210))
    d.ellipse([rx + 2, ry - 16, rx + 34, ry + 16], outline=ACCENT, width=3)
    d.line([rx + 6, ry + 11, rx + 30, ry - 11], fill=ACCENT, width=3)


def banner_xavier(d, b):
    x0, y0, x1, y1 = b
    vgrad(d, b, (52, 108, 132), (24, 66, 92))
    import math
    cx, cy = x0 + 44, (y0 + y1) // 2
    for r in (17, 12, 7):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
              fill=(230, 240, 244), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(230, 240, 244))
    # bent palm, right
    tx = x1 - 36
    d.line([tx, y1 - 4, tx - 6, y0 + 14], fill=(90, 64, 36), width=4)
    for a in (-30, -8, 14, 36):
        ex = tx - 6 + int(17 * math.sin(a * math.pi / 180)) + 8
        ey = y0 + 12 - int(6 * math.cos(a * math.pi / 180))
        d.line([tx - 6, y0 + 13, ex, ey], fill=(52, 148, 84), width=3)
    # waves + rain
    for i in range(4):
        d.arc([x0 + 66 + i * 24, y1 - 12, x0 + 86 + i * 24, y1 - 2],
              180, 360, fill=(150, 200, 220), width=2)
    for i in range(6):
        rx = x0 + 78 + i * 14
        d.line([rx, y0 + 6, rx - 4, y0 + 14], fill=(170, 205, 225),
               width=1)


# ---------------------------------------------------------------- content

TIMELINE = [
    ("00:09", "Peru M6.7 quake"), ("02:00", "Sinaloa raid"),
    ("04:00", "Vegas qualifying"), ("05:00", "Tanker hit off Khasab"),
    ("13:30", "Bitcoin rebounds"), ("18:24", "Mercury burn starts"),
    ("22:10", "COP31 pauses to Sunday"),
]

STATS = [
    ("6.7", "Peru quake magnitude, 108 km deep (USGS)"),
    ("2", "tankers hit leaving Hormuz (UKMTO)"),
    ("90.4%", "of Indonesia's tariff lines duty-free (CEPA)"),
    ("$55,130", "bitcoin's Saturday low, a two-year low"),
    ("128", "nations back killer-robot talks (UN)"),
    ("37–12", "England over New Zealand, a record win"),
]

REGIONS = [
    ("EUROPE", 23, (24, 62, 122)), ("ASIA", 5, (196, 120, 40)),
    ("AMERICAS", 3, (22, 110, 62)), ("MIDEAST", 2, (164, 32, 24)),
    ("OCEANIA", 2, (110, 70, 150)), ("GLOBAL", 2, (70, 130, 140)),
]

MAINS = [
    dict(scene=scene_hormuz, kicker="GULF: TANKERS HIT",
         tag="1 · STRAIT OF HORMUZ · IRAN WAR", badge="CONFIRMED",
         head="Two tankers hit off Oman; a plant burns in Bahrain",
         deck="One struck on the stern, one in the engine room off "
              "Khasab — no casualties. Bahrain says an Iranian attack "
              "set a civilian plant ablaze.",
         src="Reuters · UKMTO · Al Jazeera"),
    dict(scene=scene_peru, kicker="PERU: QUAKE 6.7",
         tag="2 · JUNÍN, PERU · EARTHQUAKE", badge="CONFIRMED",
         head="A deep 6.7 earthquake shakes central Peru",
         deck="Centred near Carhuamayo and felt in Lima; landslides "
              "and minor damage, no deaths and no tsunami threat.",
         src="USGS · AP · AFP"),
    dict(scene=scene_cop31, kicker="COP31: OVERTIME",
         tag="3 · ANTALYA, TÜRKİYE · CLIMATE", badge="CONFIRMED",
         head="COP31 runs into overtime with no deal",
         deck="Talks ran through Saturday over fossil fuels and "
              "finance; the draft names no coal, oil or gas. "
              "Approval session set for Sunday 06:00 GMT.",
         src="Reuters · AFP · Al Jazeera"),
]

CARDS = [
    dict(scene=banner_cepa, tag="4 · BRUSSELS", badge="OFFICIAL",
         head="EU and Indonesia sign a trade pact",
         deck="A decade of talks ends: duties go on 90.4% of lines "
              "from day one.", stat="90.4%", src="Reuters"),
    dict(scene=banner_riyadh, tag="5 · RIYADH · WAR", badge="CONFIRMED",
         head="Three missiles down over Riyadh",
         deck="Second Houthi attack in three days intercepted; "
              "no casualties.", stat=None, src="Reuters"),
    dict(scene=banner_sparta, tag="6 · GULF OF FINLAND",
         badge="CONFIRMED", head="Drone-hit ship burns off Finland",
         deck="The Sparta II's 16 crew are safe; Finland blames "
              "Ukraine.", stat="16 SAFE", src="Reuters"),
    dict(scene=banner_bitcoin, tag="7 · WORLD · MARKETS", badge="CONFIRMED",
         head="Bitcoin's two-year low: $55,130",
         deck="$2.4bn of bets flushed out; back over $60,000 by "
              "afternoon.", stat=None, src="CoinGlass"),
    dict(scene=banner_mercury, tag="8 · SPACE · ESA + JAXA",
         badge="OFFICIAL", head="BepiColombo reaches Mercury",
         deck="After eight years, a 37-minute burn; only the second "
              "Mercury orbiter.", stat=None, src="ESA"),
    dict(scene=banner_sinaloa, tag="9 · GUASAVE · MEXICO",
         badge="CONFIRMED", head="Cartel boss ‘El Chapo Isidro’ held",
         deck="An FBI top-ten fugitive is seized in Guasave; 11 die "
              "in the clashes.", stat=None, src="Reuters · AP"),
    dict(scene=banner_wellington, tag="10 · WELLINGTON",
         badge="CONFIRMED", head="Rahul's 136 puts India on top",
         deck="India close day three 486/4 against 368; Gill 98, "
              "Nicholls 175*.", stat="486/4", src="BCCI"),
    dict(scene=banner_england, tag="11 · LONDON · RUGBY", badge="OFFICIAL",
         head="England rout the All Blacks",
         deck="New Zealand's heaviest defeat by England, at "
              "Twickenham.", stat="37–12", src="RNZ"),
    dict(scene=banner_robots, tag="12 · GENEVA · ARMS",
         badge="CONFIRMED", head="128 nations back robot-arms talks",
         deck="The UN sets a two-year path; big powers resist binding "
              "rules.", stat="128", src="AFP"),
    dict(scene=banner_xavier, tag="13 · SOUTH PACIFIC",
         badge="CONFIRMED", head="Record cyclone Xavier weakens",
         deck="The strongest November cyclone on record; Nassau "
              "under an emergency.", stat=None, src="NASA · JTWC"),
]

ALSO = [
    "Newcastle Utd 2–2 Arsenal (Premier League)",
    "Man City 1–1 Fulham (Premier League)",
    "Chelsea 1–4 Leeds Utd (Premier League)",
    "Coventry City 3–2 Crystal Palace (Premier League)",
    "Bournemouth 2–0 Nott'm Forest (Premier League)",
    "Tottenham 2–0 Ipswich Town (Premier League)",
    "Aston Villa 0–0 Sunderland (Premier League)",
    "Ireland 20–17 South Africa (Nations Championship)",
    "Scotland 67–5 Japan (Nations Championship)",
    "France 45–17 Argentina (Nations Championship)",
    "Wales 26–29 Australia (Nations Championship)",
    "Italy 16–21 Fiji (Nations Championship)",
    "Alcaraz bt Shelton 3–6 6–3 7–6(1) — Turin SF",
    "Zverev bt Medvedev 7–6(0) 6–4 — Turin SF",
    "Antonelli fastest in qualifying; Verstappen pole (F1)",
    "Hockey: India 2–1 South Korea, in Bhopal",
    "Kyiv: no new barrage; blackouts, bridge repairs",
    "Odisha: schools shut Saturday; Akvan clear-up, no deaths",
    "Spain: bank levy to 2027 — €1.4bn, all for housing (Reuters)",
    "Paris: 82,500 march on living costs (interior ministry)",
    "Italy: transport strike disrupts trains nationwide",
    "Delhi: SCO forum's second day; Pakistan's minister attends",
    "Banda Sea: M6.8 quake felt in Darwin; no tsunami (USGS)",
    "Taipei: 21 Chinese jets patrol; 15 cross the median line",
]

DATE_CHECK = (
    "Left out (other day): the ICJ Rohingya ruling (Thu) · Friday's "
    "Kyiv barrage — only Saturday's repairs are in · Wall Street's "
    "Friday close · Friday's first Khasab tanker fire — Saturday's two "
    "hits are separate · the Pakistan–Sri Lanka Test (Fri). Not yet: "
    "the Las Vegas race, the ATP final (Sun), COP31's session "
    "(Sun 06:00 GMT).")

# ------------------------------------------------------------- world map

LAND = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-70, 55), (-65, 50), (-70, 45), (-75, 40),
     (-76, 35), (-80, 32), (-81, 26), (-84, 22), (-90, 20), (-94, 17),
     (-97, 16), (-102, 14), (-105, 20), (-110, 23), (-114, 29),
     (-120, 34), (-124, 40), (-124, 46), (-130, 54), (-150, 60),
     (-165, 60)],
    [(-45, 60), (-30, 68), (-22, 70), (-20, 76), (-30, 80), (-55, 76),
     (-58, 68), (-52, 62)],
    [(-77, 7), (-70, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -22), (-48, -27), (-52, -33),
     (-58, -39), (-62, -41), (-65, -45), (-67, -50), (-68, -54),
     (-71, -54), (-73, -50), (-73, -44), (-73, -37), (-71, -30),
     (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1)],
    [(-6, 35), (0, 36), (10, 37), (20, 32), (30, 31), (34, 28),
     (38, 22), (43, 12), (48, 11), (51, 10), (44, 0), (40, -6),
     (39, -15), (36, -22), (33, -27), (28, -33), (20, -35), (17, -32),
     (15, -27), (13, -18), (12, -10), (9, -2), (9, 4), (-2, 5),
     (-8, 5), (-13, 8), (-17, 12), (-17, 15), (-16, 20), (-15, 25),
     (-13, 28), (-9, 31)],
    [(-10, 36), (-9, 43), (-2, 49), (0, 51), (5, 53), (8, 55), (8, 57),
     (18, 56), (21, 55), (24, 58), (30, 60), (28, 66), (35, 65),
     (45, 68), (60, 69), (75, 72), (90, 73), (105, 74), (120, 73),
     (135, 72), (150, 70), (160, 66), (170, 66), (178, 65), (170, 60),
     (162, 58), (158, 52), (150, 50), (142, 50), (140, 46), (138, 42),
     (135, 35), (130, 33), (127, 30), (122, 28), (120, 25), (115, 23),
     (108, 18), (106, 10), (104, 6), (100, 8), (97, 16), (92, 16),
     (89, 22), (86, 20), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (61, 25), (55, 26), (50, 29), (48, 30), (44, 29),
     (40, 31), (36, 36), (30, 36), (26, 38), (22, 37), (19, 40),
     (15, 38), (12, 42), (10, 44), (3, 43), (0, 39)],
    [(95, 5), (105, 0), (112, -2), (118, -3), (124, -1), (131, -2),
     (138, -3), (142, -4), (138, -6), (128, -5), (118, -6), (108, -4),
     (99, 2)],
    [(113, -22), (114, -30), (118, -35), (124, -33), (130, -32),
     (132, -31), (135, -35), (138, -36), (140, -38), (145, -38),
     (150, -37), (153, -32), (153, -27), (151, -24), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 54), (1, 52)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 42), (138, 38), (134, 35), (131, 33)],
]

PINS = [
    (1, 56, 26.5), (2, -76, -11), (3, 31, 37), (4, 4.5, 50.8),
    (5, 46.7, 24.6), (6, 29, 60), (9, -108.5, 25.6), (10, 174.8, -41.3),
    (11, -0.1, 51.5), (12, 6.1, 46.2), (13, -165.4, -11.6),
]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(233, 226, 208))

    def proj(lon, lat):
        return (x0 + (lon + 170) / 360 * (x1 - x0),
                y0 + (78 - lat) / 138 * (y1 - y0))

    for poly in LAND:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=(203, 184, 148))
    for lon, lat in [(172, -41), (168, -46)]:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(203, 184, 148))
    offsets = {4: (6, -5), 11: (-7, -3), 12: (7, 7)}
    for num, lon, lat in PINS:
        px, py = proj(lon, lat)
        ox, oy = offsets.get(num, (0, 0))
        px, py = px + ox, py + oy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=ACCENT)
        text(d, (px, py - 6), str(num), F(SANS_B, 9),
             fill=(255, 255, 255), anchor="ma")


# ---------------------------------------------------------------- layout

def paint(img, fn, box):
    """Paint a scene into its box on a private layer, so nothing a
    scene draws can spill over the box's edges onto neighbouring text."""
    x0, y0, x1, y1 = (int(v) for v in box)
    layer = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    ld = ImageDraw.Draw(layer)
    fn(ld, (0, 0, x1 - x0, y1 - y0))
    img.paste(layer, (x0, y0))


def badge(d, x, y, s, anchor_right=None):
    col = GREEN if s == "CONFIRMED" else BLUE
    label = "✓ " + s
    w = d.textlength(label, font=F(SANS_B, 10))
    if anchor_right is not None:
        x = anchor_right - w
    text(d, (x, y), label, F(SANS_B, 10), fill=col)
    return w


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 24
    # top strip
    text(d, (MX, 10), "THE WORLD IN ONE DAY", F(SANS_B, 13), fill=ACCENT)
    text(d, (W - MX, 11),
         "37 STORIES · 6 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026 (UTC)",
         F(SANS_B, 11), anchor="ra")
    d.line([MX, 30, W - MX, 30], fill=RULE, width=2)
    # title + sub-headline
    text(d, (W // 2, 38), "Saturday 21 November 2026", F(SERIF_B, 60),
         anchor="ma")
    text(d, (W // 2, 106),
         "Two tankers hit off Oman · COP31 runs into overtime · "
         "A deep quake shakes Peru", F(SERIF, 16), fill=MUTE, anchor="ma")
    # timeline
    ty = 132
    d.rectangle([MX, ty, MX + 82, ty + 40], fill=INK)
    text(d, (MX + 41, ty + 6), "THE DAY", F(SANS_B, 10),
         fill=(247, 243, 234), anchor="ma")
    text(d, (MX + 41, ty + 20), "IN UTC", F(SANS_B, 10),
         fill=(247, 243, 234), anchor="ma")
    lx0, lx1 = MX + 98, W - MX
    d.line([lx0, ty + 20, lx1, ty + 20], fill=MUTE, width=1)
    for i, (tm, label) in enumerate(TIMELINE):
        cx = lx0 + (lx1 - lx0) * (i + 0.5) / len(TIMELINE)
        d.ellipse([cx - 3, ty + 17, cx + 3, ty + 23], fill=ACCENT)
        text(d, (cx, ty - 1), tm, F(SANS_B, 10), anchor="ma")
        if i == 0:
            para(d, (lx0 + 2, ty + 26), label, F(SANS, 8), 118,
                 fill=MUTE, lh=10)
        elif i == len(TIMELINE) - 1:
            for j, ln in enumerate(wrap(d, label, F(SANS, 8), 118)):
                text(d, (lx1 - 2, ty + 26 + j * 10), ln, F(SANS, 8),
                     fill=MUTE, anchor="ra")
        else:
            para(d, (cx, ty + 26), label, F(SANS, 8), 118, fill=MUTE,
                 lh=10)
    # stat bar
    sy = 182
    cw = (W - 2 * MX) / 6
    for i, (num, cap) in enumerate(STATS):
        cx = MX + i * cw
        if i:
            d.line([cx, sy + 4, cx, sy + 52], fill=ACCENT, width=2)
        text(d, (cx + 10, sy), num, F(SERIF_B, 32), fill=INK)
        para(d, (cx + 10, sy + 40), cap, F(SANS, 9), cw - 18, fill=MUTE,
             lh=11)
    # region tally
    gy = 246
    total = sum(n for _, n, _ in REGIONS)
    gx = MX
    for name, n, col in REGIONS:
        wseg = (W - 2 * MX) * n / total
        d.rectangle([gx, gy, gx + wseg, gy + 20], fill=col)
        text(d, (gx + wseg / 2, gy + 5), f"{name} {n}", F(SANS_B, 8),
             fill=(255, 255, 255), anchor="ma")
        gx += wseg
    # mains
    my = 278
    mw = (W - 2 * MX - 24) / 3
    for i, m in enumerate(MAINS):
        x = MX + i * (mw + 12)
        paint(img, m["scene"], (x, my, x + mw, my + 138))
        kw = d.textlength(m["kicker"], font=F(SANS_B, 12)) + 18
        d.rectangle([x, my, x + kw, my + 24], fill=ACCENT)
        text(d, (x + 9, my + 5), m["kicker"], F(SANS_B, 12),
             fill=(255, 255, 255))
        sw = d.textlength(m["src"], font=F(SANS, 8)) + 12
        d.rectangle([x, my + 118, x + sw, my + 138], fill=(10, 10, 16))
        text(d, (x + 6, my + 124), m["src"], F(SANS, 8),
             fill=(240, 238, 230))
        d.ellipse([x, my + 146, x + 18, my + 164], fill=ACCENT)
        text(d, (x + 9, my + 149), str(i + 1), F(SANS_B, 11),
             fill=(255, 255, 255), anchor="ma")
        text(d, (x + 24, my + 149), m["tag"].split("·", 1)[1].strip(),
             F(SANS_B, 10), fill=MUTE)
        badge(d, 0, my + 149, m["badge"], anchor_right=x + mw)
        para(d, (x, my + 168), m["head"], F(SERIF_B, 19), mw, lh=22,
             max_lines=2)
        para(d, (x, my + 214), m["deck"], F(SANS, 11), mw, lh=13,
             max_lines=3)
    # cards, two rows of five
    cw2 = (W - 2 * MX - 40) / 5
    for r in range(2):
        for c in range(5):
            m = CARDS[r * 5 + c]
            x = MX + c * (cw2 + 10)
            y = 538 + r * 132
            d.rectangle([x, y, x + cw2, y + 124], outline=RULE, width=1)
            paint(img, m["scene"], (x + 2, y + 2, x + cw2 - 2, y + 48))
            if m["stat"]:
                tw = d.textlength(m["stat"], font=F(SERIF_B, 14)) + 12
                d.rectangle([x + cw2 - tw - 2, y + 26, x + cw2 - 2,
                             y + 48], fill=(10, 10, 16))
                text(d, (x + cw2 - tw + 4, y + 30), m["stat"],
                     F(SERIF_B, 14), fill=(255, 214, 120))
            tw = d.textlength(m["src"], font=F(SANS, 7)) + 8
            d.rectangle([x + 2, y + 34, x + 2 + tw, y + 48],
                        fill=(10, 10, 16))
            text(d, (x + 6, y + 38), m["src"], F(SANS, 7),
                 fill=(240, 238, 230))
            num = m["tag"].split("·")[0].strip()
            d.ellipse([x + 6, y + 53, x + 20, y + 67], fill=ACCENT)
            text(d, (x + 13, y + 56), num, F(SANS_B, 8),
                 fill=(255, 255, 255), anchor="ma")
            text(d, (x + 24, y + 55), m["tag"].split("·", 1)[1].strip(),
                 F(SANS_B, 8), fill=MUTE)
            badge_y = y + 55
            bw = d.textlength("✓ " + m["badge"], font=F(SANS_B, 8))
            text(d, (x + cw2 - 6 - bw, badge_y), "✓ " + m["badge"],
                 F(SANS_B, 8),
                 fill=GREEN if m["badge"] == "CONFIRMED" else BLUE)
            para(d, (x + 6, y + 70), m["head"], F(SERIF_B, 13), cw2 - 12,
                 lh=15, max_lines=2)
            para(d, (x + 6, y + 100), m["deck"], F(SANS, 9), cw2 - 12,
                 lh=11, max_lines=2)
    # bottom band: map + ALSO
    by = 802
    text(d, (MX, by), "WHERE IT HAPPENED", F(SANS_B, 11), fill=ACCENT)
    draw_map(d, (MX, by + 16, MX + 306, by + 140))
    para(d, (MX, by + 160),
         "Pins carry the mains' and cards' story numbers; 7 and 8 "
         "have no pin. Badges: CONFIRMED = 2+ outlets · OFFICIAL = "
         "on the record.", F(SANS, 8), 306, fill=MUTE, lh=10)
    ax = MX + 322
    text(d, (ax, by), "ALSO ON SATURDAY 21 NOVEMBER — 24 MORE",
         F(SANS_B, 11), fill=ACCENT)
    colw = (W - MX - ax - 12) / 2
    for j, item in enumerate(ALSO):
        col = 0 if j < 12 else 1
        row = j % 12
        ix = ax + col * (colw + 12)
        iy = by + 18 + row * 12.5
        text(d, (ix, iy), str(j + 14), F(SANS_B, 9), fill=ACCENT)
        para(d, (ix + 20, iy), item, F(SANS, 9), colw - 20, lh=11,
             max_lines=1)
    # date check
    dy = 972
    d.rectangle([MX, dy, W - MX, dy + 34], outline=ACCENT, width=2)
    d.rectangle([MX, dy, MX + 76, dy + 34], fill=ACCENT)
    text(d, (MX + 38, dy + 5), "DATE", F(SANS_B, 10),
         fill=(255, 255, 255), anchor="ma")
    text(d, (MX + 38, dy + 18), "CHECK", F(SANS_B, 10),
         fill=(255, 255, 255), anchor="ma")
    para(d, (MX + 86, dy + 5), DATE_CHECK, F(SANS, 9), W - 2 * MX - 96,
         lh=12, max_lines=2)
    # footer
    text(d, (MX, 1012),
         "Every story here happened, or was first reported, on Saturday "
         "21 November 2026 (UTC). Officials' counts and claims are "
         "attributed.", F(SANS, 8), fill=MUTE)
    text(d, (W - MX, 1012), "Sources named beside each story · "
         "Original drawings", F(SANS, 8), fill=MUTE, anchor="ra")
    return img


if __name__ == "__main__":
    img = build()
    img.save("entry.png", optimize=True)
    img.resize((300, 300), Image.LANCZOS).save("entry-300.png")
    import os
    print("entry.png", os.path.getsize("entry.png"), "bytes")

