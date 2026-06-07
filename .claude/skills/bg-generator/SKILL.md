---
name: bg-generator
description: >
  このプロジェクト用のゲーム背景画像（PNG）を生成するスキル。
  「タイトル背景を作って」「ダンジョン背景が欲しい」「ゲームクリア画面の背景を生成して」など、
  背景・背景画像・シーン背景の生成・追加を依頼されたときに必ず使うこと。
  canvas-designスキルで高品質な元画像を生成し、ドット絵風に変換して public/assets/scenes/ に保存する。
---

## 概要

`canvas-design` スキルで高品質な背景画像（PNG）を生成し、
`scripts/to-pixel-art.py` でドット絵風に変換してアセットとして保存する。

## ファイル配置

| ファイル | 説明 |
|---|---|
| `public/assets/scenes/<name>-raw.png` | 生成した元画像（1280×720px） |
| `public/assets/scenes/<name>.png` | ドット絵変換済み（ゲームで使う本番ファイル） |

ファイル名は `docs/external-design/asset-list.md` に記載された名前に従う（例: `title-bg.png`）。

## 手順

### 1. シーンの要件確認

以下を読んでからコードを書く:
- `docs/external-design/tone-and-manner.md` — カラーパレット・ビジュアルスタイル
- `docs/external-design/asset-list.md` — 対象ファイル名・サイズ・用途

### 2. canvas-design スキルで元画像を生成する

`canvas-design` スキルを呼び出して背景画像を生成する。
プロンプトには以下を必ず含める:

- `tone-and-manner.md` のカラーパレットとビジュアルスタイル
- **ドット絵変換前提の構成指示**: 「細かいテクスチャより大きな色面・シルエットを優先」
- 出力先: `public/assets/scenes/<name>-raw.png`
- サイズ: `1280×720px`（`asset-list.md` で異なる場合はそれに従う）

### 3. ドット絵変換

スキル同梱の `to-pixel-art.py` を使って変換する:

```bash
uv run --with pillow python3 .claude/skills/bg-generator/scripts/to-pixel-art.py \
  public/assets/scenes/<name>-raw.png \
  --block 6 --colors 32 \
  --out public/assets/scenes/<name>.png
```

**パラメータの目安**:

| シーン | `--block` | `--colors` | 理由 |
|---|---|---|---|
| タイトル・通常背景 | 6 | 32 | 適度なドット感 |
| 演出シーン（明るめ） | 8 | 24 | より強いレトロ感 |
| 演出シーン（暗め・シリアス） | 8 | 16 | 色数を絞ってシリアスに |

### 5. 確認・報告

生成した2ファイルのパスをユーザーに報告する。
画質に問題があれば `--block` や `--colors` を調整して再変換する。
