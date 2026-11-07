"""snk 가 만든 기여 그래프 SVG 뒤에 하늘·구름·잔디 언덕 배경을 덧붙이고, 칸을 통통하게 키운다.
뱀은 숨기고 칸이 먹혀 사라지는 애니메이션도 멈춰서, 기여 칸은 가만히 있고 구름만 움직이게 한다.

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
        "flower": "#ff9ebb",
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
        "flower": "#f08cad",
        # 밤하늘 별 몇 개
        "extra": "".join(
            f'<circle cx="{x}" cy="{y}" r="1.2" fill="#ffffff" opacity="0.7"/>'
            for x, y in [(60, -58), (210, -40), (340, -62), (520, -48), (690, -60), (800, -38)]
        ),
    },
}


def cloud(x: float, y: float, s: float, color: str, opacity: str, drift: str) -> str:
    """동글동글한 구름 하나. drift 는 천천히 좌우로 흔들리는 애니메이션 이름"""
    return (
        f'<g opacity="{opacity}" style="animation:{drift} 14s ease-in-out infinite alternate">'
        f'<g transform="translate({x} {y}) scale({s})" fill="{color}">'
        '<ellipse cx="0" cy="0" rx="22" ry="11"/>'
        '<circle cx="-10" cy="-6" r="10"/>'
        '<circle cx="6" cy="-9" r="13"/>'
        '<circle cx="19" cy="-2" r="8"/>'
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
        "<style>@keyframes driftA{to{transform:translateX(18px)}}"
        "@keyframes driftB{to{transform:translateX(-14px)}}</style>"
        + cloud(70, -46, 1.0, t["cloud"], t["cloud_opacity"], "driftA")
        + cloud(300, -52, 0.8, t["cloud"], t["cloud_opacity"], "driftB")
        + cloud(560, -44, 1.1, t["cloud"], t["cloud_opacity"], "driftA")
        + cloud(780, -54, 0.75, t["cloud"], t["cloud_opacity"], "driftB")
    )
    hills = (
        f'<path fill="{t["hill_back"]}" d="M{X0} 160 C 120 128, 260 150, 400 140 '
        f'S 680 120, {X1} 150 L {X1} {Y1} L {X0} {Y1} Z"/>'
        f'<path fill="{t["hill_front"]}" d="M{X0} 178 C 140 156, 300 176, 460 166 '
        f'S 720 158, {X1} 172 L {X1} {Y1} L {X0} {Y1} Z"/>'
    )
    # 잔디 잎과 작은 꽃
    blades = "".join(
        f'<path d="M{x} {y} q -3 -9 -1 -14 M{x} {y} q 3 -8 6 -12" stroke="{t["blade"]}" '
        'stroke-width="1.6" fill="none" stroke-linecap="round"/>'
        for x, y in [(40, 190), (150, 182), (250, 192), (380, 186), (500, 190), (610, 184), (720, 192), (830, 186)]
    )
    flowers = "".join(
        f'<g transform="translate({x} {y})" fill="{t["flower"]}">'
        '<circle cx="0" cy="-3" r="2.2"/><circle cx="3" cy="0" r="2.2"/>'
        '<circle cx="0" cy="3" r="2.2"/><circle cx="-3" cy="0" r="2.2"/>'
        '<circle cx="0" cy="0" r="1.6" fill="#fff6a8"/></g>'
        for x, y in [(95, 192), (330, 196), (560, 194), (790, 196)]
    )
    # 네 모서리를 둥글게 자르기 (언덕이 아래 모서리를 덮지 않게)
    clip = (
        '<clipPath id="sceneClip">'
        f'<rect x="{X0}" y="{Y0}" width="{WIDTH}" height="{HEIGHT}" rx="14"/></clipPath>'
    )
    return (
        f'<g id="scenery"><defs>{clip}</defs><g clip-path="url(#sceneClip)">'
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
    """뱀 도형(class s)을 지우고, 칸의 색 변화 애니메이션을 꺼서 기여 색이 그대로 남게 한다"""
    svg = re.sub(r'<rect class="s[^"]*"[^>]*/>', "", svg)
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
