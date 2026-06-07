#!/usr/bin/env python3
"""
画像をドット絵風に変換するスクリプト

使い方:
  python scripts/to-pixel-art.py <input> [options]

例:
  python scripts/to-pixel-art.py input.png
  python scripts/to-pixel-art.py input.png --block 8 --colors 32 --out output.png
"""

import argparse
import sys
from pathlib import Path


def to_pixel_art(
    input_path: Path,
    output_path: Path,
    block_size: int = 4,
    num_colors: int | None = None,
) -> None:
    try:
        from PIL import Image
    except ImportError:
        print("Pillow が必要です: pip install pillow")
        sys.exit(1)

    img = Image.open(input_path).convert("RGBA")
    w, h = img.size

    # ダウンスケール → アップスケールでドット絵化
    small_w = max(1, w // block_size)
    small_h = max(1, h // block_size)
    small = img.resize((small_w, small_h), Image.NEAREST)

    # 減色（色数制限でよりドット絵らしく）
    if num_colors is not None:
        rgb = small.convert("RGB")
        quantized = rgb.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
        small = quantized.convert("RGBA")

    # 元のサイズに戻す（ニアレストネイバーで拡大）
    result = small.resize((w, h), Image.NEAREST)
    result.save(output_path)
    print(f"保存しました: {output_path}  ({w}x{h}, block={block_size}px, colors={num_colors or 'unlimited'})")


def main() -> None:
    parser = argparse.ArgumentParser(description="画像をドット絵風に変換する")
    parser.add_argument("input", help="入力画像パス")
    parser.add_argument("--out", help="出力パス（省略時: <入力名>_pixel.png）")
    parser.add_argument("--block", type=int, default=4, help="ブロックサイズ (px) [default: 4]")
    parser.add_argument("--colors", type=int, default=None, help="最大色数 [default: 制限なし]")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ファイルが見つかりません: {input_path}")
        sys.exit(1)

    if args.out:
        output_path = Path(args.out)
    else:
        output_path = input_path.parent / f"{input_path.stem}_pixel{input_path.suffix}"

    to_pixel_art(input_path, output_path, block_size=args.block, num_colors=args.colors)


if __name__ == "__main__":
    main()
