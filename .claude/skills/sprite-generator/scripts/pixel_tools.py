#!/usr/bin/env python3
"""ドット絵スプライト/アイコンを「ASCIIグリッド + パレット」から生成するヘルパー。

小型スプライト(16〜64px)は高解像度から縮小するより、ネイティブ解像度の
1セル=1ピクセルで直接置いた方が輪郭がくっきりしてドット絵らしくなる。
このモジュールは生成スクリプトから import して使う想定。

使い方の例:
    from pixel_tools import save_sprite

    PALETTE = {
        ".": None,          # 透明
        "w": "#b8e8f0",     # 水色
        "o": "#d8a0c8",     # 枠線
    }
    GRID = [
        "..ooo..",
        ".owwwo.",
        "..ooo..",
    ]
    save_sprite(GRID, PALETTE, "public/assets/ui/icon-foo.png")

save_sprite はネイティブ解像度の本番PNGを保存し、加えて目視確認用の
拡大プレビュー(既定 /tmp/<name>-preview.png)も書き出す。プレビューを
Read で開いて確認し、グリッドを直接編集して作り込む。
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    print("Pillow が必要です: uv run --with pillow python3 ...")
    sys.exit(1)


def hex_to_rgba(value: str) -> tuple[int, int, int, int]:
    """#RGB / #RRGGBB / #RRGGBBAA を (r,g,b,a) に変換する。"""
    s = value.lstrip("#")
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) == 6:
        s += "ff"
    if len(s) != 8:
        raise ValueError(f"不正なカラーコード: {value}")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4, 6))  # type: ignore[return-value]


# 透明として扱う文字（パレットに無くても透明になる）
TRANSPARENT_CHARS = {".", " "}


def grid_to_image(rows: list[str], palette: dict[str, str | None]) -> "Image.Image":
    """ASCIIグリッドを RGBA 画像に変換する。行は左揃え・余白は透明。"""
    h = len(rows)
    w = max((len(r) for r in rows), default=0)
    if w == 0 or h == 0:
        raise ValueError("グリッドが空です")
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in TRANSPARENT_CHARS:
                continue
            if ch not in palette:
                raise KeyError(f"パレット未定義の文字 '{ch}' (行{y} 列{x})")
            col = palette[ch]
            if col is None:
                continue
            px[x, y] = hex_to_rgba(col)
    return img


def add_outline(img: "Image.Image", color: str = "#4a3050") -> "Image.Image":
    """不透明ピクセルの外周(上下左右)に1pxの縁取りを足す。

    ドット絵で被写体を背景から際立たせる定番技法。透明セルのうち、
    隣接する不透明ピクセルがあるセルを縁取り色で塗る。
    """
    w, h = img.size
    src = img.load()
    out = img.copy()
    dst = out.load()
    line = hex_to_rgba(color)
    for y in range(h):
        for x in range(w):
            if src[x, y][3] != 0:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src[nx, ny][3] != 0:
                    dst[x, y] = line
                    break
    return out


def save_sprite(
    rows: list[str],
    palette: dict[str, str | None],
    out_path: str | Path,
    *,
    outline: str | None = None,
    preview_path: str | Path | None = None,
    preview_scale: int = 12,
) -> "Image.Image":
    """グリッドからスプライトを生成し本番PNGと拡大プレビューを保存する。

    out_path        : 本番ファイル(ネイティブ解像度)。asset-list.md のパスに従う。
    outline          : 縁取り色(例 "#4a3050")。None なら縁取りなし。
    preview_path     : 拡大プレビューの保存先。None なら /tmp/<name>-preview.png。
    preview_scale    : プレビューの拡大率(NEAREST)。確認しやすいよう既定12倍。
    """
    out_path = Path(out_path)
    img = grid_to_image(rows, palette)
    if outline is not None:
        img = add_outline(img, outline)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)

    if preview_path is None:
        preview_path = Path("/tmp") / f"{out_path.stem}-preview.png"
    preview_path = Path(preview_path)
    big = img.resize(
        (img.width * preview_scale, img.height * preview_scale), Image.NEAREST
    )
    big.save(preview_path)

    print(f"本番   : {out_path}  ({img.width}x{img.height})")
    print(f"確認用 : {preview_path}  (x{preview_scale})")
    return img
