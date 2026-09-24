#!/usr/bin/env python3
"""
Gera os SVGs decorativos do README de perfil (paleta azul marinho pastel):
  assets/banner.svg            -> banner com mosaico + nome + cargo
  assets/titles/<slug>.svg     -> um título de seção por tópico
  assets/icons/linkedin.svg    -> ícone do LinkedIn (não existe mais no Simple Icons)
  assets/icons/website.svg     -> ícone genérico de site/portfólio

Uso:
  python generate_assets.py --name "Maria Silva" --role "Engenheira de Software"
  python generate_assets.py --extra "certificacoes:CERTIFICAÇÕES" --extra "blog:BLOG"
  python generate_assets.py --seed 7        # muda o desenho dos pixels

Não precisa instalar nada: só Python 3.
"""
import argparse
import random
import zlib
from pathlib import Path
from xml.sax.saxutils import escape

# ----------------------------------------------------------------------------
# PALETA  (edite aqui para trocar o visual de tudo de uma vez)
# ----------------------------------------------------------------------------
BG = "#0f1b2d"      # fundo geral
CARD = "#16233a"    # fundo dos cards/títulos
BORDER = "#22334f"  # borda sutil
TEXT = "#c9d6ea"    # texto
TITLE = "#b8d0f0"   # títulos
ACCENT = "#7fa8d9"  # destaque
ACCENT2 = "#8fb3d9"
MUTED = "#5f7fa8"
ICON = "#6f97c9"    # ícones (legíveis no tema claro e no escuro do GitHub)

# Rampa usada nos "pixels": do mais escuro ao mais claro
RAMP = ["#1c2b45", "#2a4064", "#3d5a80", "#5f7fa8", "#7fa8d9", "#b8d0f0"]
RAMP_WEIGHTS = [3, 3, 3, 2, 2, 1]

FONT = "'Courier New', Courier, monospace"

# Títulos de seção padrão: (nome-do-arquivo, texto exibido)
DEFAULT_TITLES = [
    ("quem-sou-eu", "QUEM SOU EU"),
    ("o-que-faco", "O QUE FAÇO"),
    ("visao", "VISÃO"),
    ("alem-do-codigo", "ALÉM DO CÓDIGO"),
    ("contato", "CONTATO"),
    ("atividade", "ATIVIDADE"),
    ("skill-set", "SKILL SET"),
    ("projetos", "PROJETOS"),
]


def svg_open(w, h):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img">\n'
    )


def banner(name, role, seed):
    W, H, CELL = 1000, 240, 20
    rng = random.Random(seed)
    cols, rows, y0 = W // CELL, 6, 64
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n', svg_open(W, H)]
    out.append(f'<title>{escape(name)} — {escape(role)}</title>\n')
    out.append(f'<rect width="{W}" height="{H}" rx="6" fill="{CARD}"/>\n')
    out.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="6" fill="none" stroke="{BORDER}"/>\n')
    for c in range(cols):
        density = 0.93 - 0.68 * (c / cols) ** 1.3
        for r in range(-1, rows + 1):
            edge = r in (-1, rows)
            p = density * (0.18 if edge else 1)
            if rng.random() < p:
                color = rng.choices(RAMP, RAMP_WEIGHTS)[0]
                out.append(
                    f'<rect x="{c*CELL}" y="{y0 + r*CELL}" width="{CELL-1}" height="{CELL-1}" fill="{color}"/>\n'
                )
    out.append(
        f'<text x="24" y="44" font-family="{FONT}" font-size="34" letter-spacing="4" '
        f'fill="{TITLE}">{escape(name.upper())}</text>\n'
    )
    out.append(
        f'<text x="{W-24}" y="218" text-anchor="end" font-family="{FONT}" font-size="15" '
        f'letter-spacing="2" fill="{ACCENT2}">{escape(role.upper())}</text>\n'
    )
    out.append("</svg>\n")
    return "".join(out)


def title_svg(slug, text):
    W, H, PX = 800, 44, 8
    rng = random.Random(zlib.crc32(slug.encode()))  # padrão único por título
    cols = 36
    x0 = W - 16 - cols * PX
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n', svg_open(W, H)]
    out.append(f'<title>{escape(text)}</title>\n')
    out.append(f'<rect width="{W}" height="{H}" rx="4" fill="{CARD}"/>\n')
    out.append(
        f'<text x="16" y="29" font-family="{FONT}" font-size="20" letter-spacing="3" '
        f'fill="{TITLE}">{escape(text)}</text>\n'
    )
    for c in range(cols):
        p = 0.10 + 0.70 * (c / cols) ** 1.2
        for r in range(3):
            if rng.random() < p:
                color = rng.choices(RAMP[2:], RAMP_WEIGHTS[2:])[0]
                out.append(
                    f'<rect x="{x0 + c*PX}" y="{10 + r*PX}" width="{PX-1}" height="{PX-1}" fill="{color}"/>\n'
                )
    out.append("</svg>\n")
    return "".join(out)


def linkedin_icon():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" role="img">\n'
        '<title>LinkedIn</title>\n'
        f'<rect x="3" y="3" width="34" height="34" rx="6" fill="{ICON}"/>\n'
        f'<text x="20" y="29" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="22" font-weight="700" fill="{BG}">in</text>\n'
        '</svg>\n'
    )


def website_icon():
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" role="img">\n'
        '<title>Site</title>\n'
        f'<g fill="none" stroke="{ICON}" stroke-width="2.5" stroke-linecap="round">\n'
        '<circle cx="20" cy="20" r="14"/>\n'
        '<ellipse cx="20" cy="20" rx="6" ry="14"/>\n'
        '<line x1="6" y1="20" x2="34" y2="20"/>\n'
        '<path d="M9 12.5h22M9 27.5h22"/>\n'
        '</g>\n</svg>\n'
    )


def main():
    ap = argparse.ArgumentParser(description="Gera os SVGs do README de perfil.")
    ap.add_argument("--name", default="Seu Nome", help="nome exibido no banner")
    ap.add_argument("--role", default="Seu Cargo / Sua Área", help="cargo exibido no banner")
    ap.add_argument("--seed", type=int, default=2026, help="semente do mosaico")
    ap.add_argument("--out", default="assets", help="pasta de saída")
    ap.add_argument("--extra", action="append", default=[],
                    help='título extra no formato "slug:TEXTO" (pode repetir)')
    a = ap.parse_args()

    out = Path(a.out)
    (out / "titles").mkdir(parents=True, exist_ok=True)
    (out / "icons").mkdir(parents=True, exist_ok=True)

    (out / "banner.svg").write_text(banner(a.name, a.role, a.seed), encoding="utf-8")

    titles = list(DEFAULT_TITLES)
    for e in a.extra:
        slug, _, text = e.partition(":")
        titles.append((slug.strip(), (text or slug).strip().upper()))
    for slug, text in titles:
        (out / "titles" / f"{slug}.svg").write_text(title_svg(slug, text), encoding="utf-8")

    (out / "icons" / "linkedin.svg").write_text(linkedin_icon(), encoding="utf-8")
    (out / "icons" / "website.svg").write_text(website_icon(), encoding="utf-8")
    print(f"OK: banner + {len(titles)} títulos + 2 ícones em '{out}/'")


if __name__ == "__main__":
    main()
