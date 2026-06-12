"""Generate assets/0scarito-marquee.svg — a contribution-grid marquee in the style of ratacat's.

Green GitHub-graph tiles travel along stepped routes to assemble "0scarito",
hold with a glow, fade, and loop. Self-contained CSS animation, no JS.
"""
import random

# --- pixel font (7 rows; x-height letters occupy rows 2-6) ---------------
F = {
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    's': ["0000","0000","0111","1000","0110","0001","1110"],
    'c': ["0000","0000","0111","1000","1000","1000","0111"],
    'a': ["0000","0000","0110","0001","0111","1001","0111"],
    'r': ["0000","0000","1011","1100","1000","1000","1000"],
    'i': ["1","0","1","1","1","1","1"],
    't': ["010","010","111","010","010","010","011"],
    'o': ["0000","0000","0110","1001","1001","1001","0110"],
}
WORD = "0scarito"

PITCH, CELL = 16, 13
STAGE_X, STAGE_Y, STAGE_W, STAGE_H = 42, 42, 1116, 276
COLS = (STAGE_W + 3) // PITCH          # 69
ROWS = (STAGE_H + 3) // PITCH          # 17
GX = STAGE_X + (STAGE_W - (COLS * PITCH - 3)) / 2
GY = STAGE_Y + (STAGE_H - (ROWS * PITCH - 3)) / 2

# --- word layout ----------------------------------------------------------
cols_word = sum(len(F[ch][0]) for ch in WORD) + (len(WORD) - 1)
start_col = (COLS - cols_word) // 2
start_row = (ROWS - 7) // 2

lit = []                                # (col, row)
col = start_col
for ch in WORD:
    w = len(F[ch][0])
    for r in range(7):
        for c in range(w):
            if F[ch][r][c] == '1':
                lit.append((col + c, start_row + r))
    col += w + 1

word_cols = {c for c, _ in lit}
word_rows = {r for _, r in lit}

# --- routes (12 stepped travel paths) ------------------------------------
DX = [-420, 380, -300, 260, -480, 420, -340, 300, -260, 440, -380, 340]
DY = [-180, -140, 160, 180, -120, 140, -160, 120, 180, -180, 130, -130]
N_ROUTES = 12

def route_css(k):
    a = 4.0 + k * 0.9          # appear %
    b = 26.0 + k * 0.7         # arrive %
    f0 = 80.0 + (k % 4) * 0.6  # fade start %
    dx, dy = DX[k], DY[k]
    pts = [(dx, dy), (dx, dy * 0.5), (dx * 0.5, dy * 0.5), (dx * 0.5, 0), (dx * 0.15, 0), (0, 0)]
    n = len(pts) - 1
    kf = [f"  0%, {a:.1f}% {{ opacity: 0; transform: translate({dx}px, {dy}px); }}"]
    for j, (x, y) in enumerate(pts):
        pct = a + (b - a) * j / n
        kf.append(f"  {pct:.1f}% {{ opacity: 1; transform: translate({x:.0f}px, {y:.0f}px); }}")
    kf.append(f"  {f0:.1f}% {{ opacity: 1; transform: translate(0, 0); }}")
    kf.append(f"  {f0 + 9:.1f}%, 100% {{ opacity: 0; transform: translate(0, 0); }}")
    return "@keyframes tile-%d {\n%s\n}" % (k, "\n".join(kf))

# --- noise cells (gentle flicker outside the word) ------------------------
rng = random.Random(27)
noise = []
while len(noise) < 26:
    c, r = rng.randrange(COLS), rng.randrange(ROWS)
    if c in word_cols and r in word_rows:
        continue
    if (c, r) not in noise:
        noise.append((c, r))

# --- build SVG ------------------------------------------------------------
GREENS = ["#39d353", "#26a641", "#39d353", "#2ea043"]
tiles = []
for i, (c, r) in enumerate(lit):
    x = GX + c * PITCH
    y = GY + r * PITCH
    k = (i * 7) % N_ROUTES
    fill = GREENS[i % len(GREENS)]
    tiles.append(f'<use href="#cell" x="{x:.0f}" y="{y:.0f}" fill="{fill}" class="bit tile-{k}"/>')

noise_uses = []
for i, (c, r) in enumerate(noise):
    x = GX + c * PITCH
    y = GY + r * PITCH
    noise_uses.append(f'<use href="#cell" x="{x:.0f}" y="{y:.0f}" fill="#0e4429" class="noise noise-{i % 3}"/>')

routes = "\n".join(route_css(k) for k in range(N_ROUTES))
tile_classes = "\n".join(f"      .tile-{k} {{ animation-name: tile-{k}; }}" for k in range(N_ROUTES))

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 1200 360">
  <title id="title">0scarito animated contribution-grid marquee</title>
  <desc id="desc">Green contribution-graph tiles travel along stepped paths to assemble 0scarito, hold with a glow, then fade away.</desc>
  <defs>
    <linearGradient id="backdrop" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#05080d"/>
      <stop offset="0.54" stop-color="#0d1117"/>
      <stop offset="1" stop-color="#10171f"/>
    </linearGradient>
    <clipPath id="stage-clip">
      <rect x="{STAGE_X}" y="{STAGE_Y}" width="{STAGE_W}" height="{STAGE_H}" rx="14"/>
    </clipPath>
    <filter id="arrival-glow" x="-18%" y="-28%" width="136%" height="156%">
      <feGaussianBlur stdDeviation="4.5" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="0 0 0 0 0.22  0 0 0 0 0.95  0 0 0 0 0.35  0 0 0 .85 0" result="greenBlur"/>
      <feMerge>
        <feMergeNode in="greenBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <rect id="cell" width="{CELL}" height="{CELL}" rx="3"/>
    <pattern id="grid" x="{GX:.0f}" y="{GY:.0f}" width="{PITCH}" height="{PITCH}" patternUnits="userSpaceOnUse">
      <rect width="{CELL}" height="{CELL}" rx="3" fill="#161b22"/>
    </pattern>
    <style>
      .bit {{
        animation-duration: 13.2s;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
        opacity: 0;
        transform-box: fill-box;
        transform-origin: center;
      }}
{tile_classes}
      .noise {{
        animation: noise-pulse 13.2s ease-in-out infinite;
        opacity: 0.35;
      }}
      .noise-1 {{ animation-delay: -4.4s; }}
      .noise-2 {{ animation-delay: -8.8s; }}
      .subtitle {{
        animation: subtitle-pop 13.2s ease-in-out infinite;
        opacity: 0;
      }}
{routes}
      @keyframes noise-pulse {{
        0%, 100% {{ opacity: 0.15; }}
        50% {{ opacity: 0.55; }}
      }}
      @keyframes subtitle-pop {{
        0%, 34% {{ opacity: 0; }}
        42%, 78% {{ opacity: 1; }}
        88%, 100% {{ opacity: 0; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .bit {{ animation: none; opacity: 1; transform: none; }}
        .subtitle {{ animation: none; opacity: 1; }}
        .noise {{ animation: none; }}
      }}
    </style>
  </defs>

  <rect width="1200" height="360" fill="url(#backdrop)"/>
  <rect x="{STAGE_X}" y="{STAGE_Y}" width="{STAGE_W}" height="{STAGE_H}" rx="14" fill="none" stroke="#21262d" stroke-width="2"/>
  <g clip-path="url(#stage-clip)">
    <rect x="{STAGE_X}" y="{STAGE_Y}" width="{STAGE_W}" height="{STAGE_H}" fill="url(#grid)"/>
    {"".join(noise_uses)}
    <g filter="url(#arrival-glow)">
      {"".join(tiles)}
    </g>
  </g>
  <text class="subtitle" x="600" y="344" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="20" fill="#7ee787">finance &#215; AI</text>
</svg>
'''

with open("assets/0scarito-marquee.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(f"tiles: {len(lit)}, noise: {len(noise)}, bytes: {len(svg)}")
