"""snk 가 만든 기여 그래프 SVG 뒤에 하늘·구름·잔디 언덕 배경을 덧붙이고, 칸을 통통하게 키운다.
뱀은 숨기고 칸이 먹혀 사라지는 애니메이션도 멈춰서 기여 칸은 가만히 두고, 구름이 계속 흘러가고 꽃과 잔디 잎이 흔들리게 한다.

snk 는 SVG 배경 그림 옵션이 없어서, 생성된 파일을 열어 <svg> 바로 안쪽(셀보다 먼저)에
배경 그룹을 넣고 위아래로 공간을 늘린다. 외부 이미지 없이 도형만 써서 GitHub 에서도 그대로 보인다.

사용: python3 scripts/decorate_snake.py <svg 경로> light|dark
"""

import re
import sys

# snk 기본 viewBox 는 "-16 -32 880 192" (잔디 그리드는 y 0~112).
# 위로 40px(구름), 아래로 48px(잔디 언덕)를 늘린다.
VIEWBOX = "-16 -72 880 280"
WIDTH, HEIGHT = 880, 280
X0, Y0, X1, Y1 = -16, -72, 864, 208

THEMES = {
    "light": {
        "sky_top": "#dcf1ff",
        "sky_bottom": "#f7fbff",
        "cloud": "#ffffff",
        "cloud_opacity": "0.95",
        "hill_back": "#cdeeb8",
        "hill_front": "#a6dc8c",
        "blade": "#8cc976",
        "stem": "#7cbf66",
        "petals": ["#ff9ebb", "#ffd75e"],  # 분홍, 노랑 꽃
        "center": "#fff6a8",
        "extra": "",
    },
    "dark": {
        "sky_top": "#0b1626",
        "sky_bottom": "#15233a",
        "cloud": "#3a4b66",
        "cloud_opacity": "0.55",
        "hill_back": "#24452f",
        "hill_front": "#2f5b3b",
        "blade": "#3f7a4f",
        "stem": "#3f7a4f",
        "petals": ["#f08cad", "#e8cf6a"],
        "center": "#fff1b0",
        # 밤하늘 별 몇 개
        "extra": "".join(
            f'<circle cx="{x}" cy="{y}" r="1.2" fill="#ffffff" opacity="0.7"/>'
            for x, y in [(60, -58), (210, -40), (340, -62), (520, -48), (690, -60), (800, -38)]
        ),
    },
}

# 구름: (높이 y, 크기, 한 바퀴 시간 s, 시작 위치를 정하는 지연 s)
# 왼쪽 밖에서 들어와 오른쪽 밖으로 계속 흘러간다. 속도가 달라 겹쳤다 떨어졌다 한다.
# 가장 낮은 구름은 잔디 칸 바로 위(y≈0)까지 내려온다.
CLOUDS = [
    (-38, 1.50, 62, 0),
    (-16, 1.15, 48, 14),
    (-48, 0.90, 74, 33),
    (-26, 1.60, 56, 40),
    (-10, 0.95, 44, 9),
    (-46, 1.10, 68, 52),
]
CLOUD_FROM, CLOUD_TO = -130, 920  # 화면 왼쪽 밖 → 오른쪽 밖 (px)

# 꽃: (x, y, 색 번호 0=분홍 1=노랑, 흔들리는 시간 s, 시작 지연 s)
FLOWERS = [
    (70, 196, 0, 2.6, 0.0),
    (150, 190, 1, 3.1, 0.4),
    (300, 198, 0, 2.8, 0.9),
    (420, 192, 1, 3.4, 0.2),
    (560, 196, 0, 2.9, 0.6),
    (650, 190, 1, 3.2, 1.1),
    (790, 197, 0, 2.7, 0.3),
]

# 잔디 잎: (x, y)
BLADES = [(40, 190), (110, 186), (215, 194), (250, 188), (370, 192), (470, 186),
          (520, 194), (610, 188), (720, 194), (760, 186), (840, 190)]

ANIMATIONS = (
    "<style>"
    # 꽃과 잔디 잎은 줄기 밑동을 기준으로 살랑살랑
    ".sway{transform-box:fill-box;transform-origin:50% 100%;"
    "animation:sway ease-in-out infinite alternate}"
    "@keyframes sway{from{transform:rotate(-9deg)}to{transform:rotate(9deg)}}"
    ".blade{transform-box:fill-box;transform-origin:50% 100%;"
    "animation:sway 3.6s ease-in-out infinite alternate}"
    "</style>"
)


def cloud(y: float, s: float, dur: int, delay: int, t: dict) -> str:
    """동글동글한 구름 하나. 바깥 g 가 왼쪽→오른쪽 이동, 안쪽 g 가 높이와 크기"""
    return (
        f'<g opacity="{t["cloud_opacity"]}" '
        f'style="animation:cloudMove {dur}s linear infinite;animation-delay:-{delay}s">'
        f'<g transform="translate(0 {y}) scale({s})" fill="{t["cloud"]}">'
        '<ellipse cx="0" cy="0" rx="22" ry="11"/>'
        '<circle cx="-10" cy="-6" r="10"/>'
        '<circle cx="6" cy="-9" r="13"/>'
        '<circle cx="19" cy="-2" r="8"/>'
        "</g></g>"
    )


def flower(x: float, y: float, color: str, dur: float, delay: float, t: dict) -> str:
    """줄기 + 꽃잎 4장. 바깥 g 는 자리, 안쪽 g 는 흔들림"""
    return (
        f'<g transform="translate({x} {y})">'
        f'<g class="sway" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
        f'<path d="M0 0 q 1 -6 0 -11" stroke="{t["stem"]}" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
        f'<g transform="translate(0 -13)" fill="{color}">'
        '<circle cx="0" cy="-3" r="2.4"/><circle cx="3" cy="0" r="2.4"/>'
        '<circle cx="0" cy="3" r="2.4"/><circle cx="-3" cy="0" r="2.4"/>'
        f'<circle cx="0" cy="0" r="1.7" fill="{t["center"]}"/></g>'
        "</g></g>"
    )


def background(t: dict) -> str:
    sky = (
        '<defs><linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{t["sky_top"]}"/>'
        f'<stop offset="1" stop-color="{t["sky_bottom"]}"/>'
        "</linearGradient></defs>"
        f'<rect x="{X0}" y="{Y0}" width="{WIDTH}" height="{HEIGHT}" rx="14" fill="url(#skyGrad)"/>'
    )
    clouds = (
        "<style>@keyframes cloudMove{"
        f"from{{transform:translateX({CLOUD_FROM}px)}}to{{transform:translateX({CLOUD_TO}px)}}}}</style>"
        + "".join(cloud(*c, t) for c in CLOUDS)
    )
    hills = (
        f'<path fill="{t["hill_back"]}" d="M{X0} 160 C 120 128, 260 150, 400 140 '
        f'S 680 120, {X1} 150 L {X1} {Y1} L {X0} {Y1} Z"/>'
        f'<path fill="{t["hill_front"]}" d="M{X0} 178 C 140 156, 300 176, 460 166 '
        f'S 720 158, {X1} 172 L {X1} {Y1} L {X0} {Y1} Z"/>'
    )
    blades = "".join(
        f'<g transform="translate({x} {y})"><path class="blade" '
        f'style="animation-delay:-{(i * 0.37) % 3:.2f}s" d="M0 0 q -3 -9 -1 -14 M0 0 q 3 -8 6 -12" '
        f'stroke="{t["blade"]}" stroke-width="1.6" fill="none" stroke-linecap="round"/></g>'
        for i, (x, y) in enumerate(BLADES)
    )
    flowers = "".join(flower(x, y, t["petals"][c], dur, delay, t) for x, y, c, dur, delay in FLOWERS)
    # 네 모서리를 둥글게 자르기 (언덕이 아래 모서리를 덮지 않게)
    clip = (
        '<clipPath id="sceneClip">'
        f'<rect x="{X0}" y="{Y0}" width="{WIDTH}" height="{HEIGHT}" rx="14"/></clipPath>'
    )
    return (
        f'<g id="scenery">{ANIMATIONS}<defs>{clip}</defs><g clip-path="url(#sceneClip)">'
        f'{sky}{t["extra"]}{clouds}{hills}{blades}{flowers}</g></g>'
    )


def chubby_cells(svg: str) -> str:
    """잔디 칸을 12px → 14px, 모서리 반지름 2 → 5 로 키워 동글동글하게.
    snk 는 칸 크기 옵션이 없어서 결과 SVG 를 직접 고친다. 칸 간격(16px)은 그대로라 1px 씩 당겨 가운데를 맞춘다."""
    svg = svg.replace("width:12px;height:12px}", "width:14px;height:14px}")

    def bigger(m: re.Match) -> str:
        x, y = float(m.group(2)) - 1, float(m.group(3)) - 1
        return f'<rect class="{m.group(1)}" x="{x:g}" y="{y:g}" rx="5" ry="5"/>'

    return re.sub(r'<rect class="(c[^"]*)" x="([\d.]+)" y="([\d.]+)" rx="2" ry="2"/>', bigger, svg)


def without_snake(svg: str) -> str:
    """뱀 도형(class s)과 뱀이 먹은 만큼 차오르는 아래쪽 진행 막대(class u)를 지우고,
    칸의 색 변화 애니메이션을 꺼서 기여 색이 그대로 남게 한다"""
    svg = re.sub(r'<rect class="[su][ "][^>]*/>', "", svg)
    return svg.replace("</svg>", "<style>.c{animation:none!important}</style></svg>")


def main(path: str, theme: str) -> None:
    svg = open(path, encoding="utf-8").read()
    if 'id="scenery"' in svg:
        return  # 이미 꾸민 파일
    head = re.match(r"<svg[^>]*>", svg)
    if not head:
        raise SystemExit(f"{path}: <svg> 태그를 찾지 못했어요")
    new_head = (
        f'<svg viewBox="{VIEWBOX}" width="{WIDTH}" height="{HEIGHT}" '
        'xmlns="http://www.w3.org/2000/svg">'
    )
    svg = new_head + background(THEMES[theme]) + without_snake(chubby_cells(svg[head.end():]))
    open(path, "w", encoding="utf-8").write(svg)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
