# CSS 管理ルール

## 3層構成

| 層 | ファイル | 用途 |
|---|---|---|
| グローバル | `public/style.css` | ページリセット・`#game-container` レイアウト・CSS カスタムプロパティ定義 |
| コンポーネント | `src/components/Xxx/Xxx.module.css` | 各 React コンポーネントのスコープ付きスタイル |
| Storybook | `.storybook/preview.ts` でインポート | Storybook 上でグローバルスタイルを再現するための読み込み |

## グローバルスタイル (`public/style.css`)

- ページ全体のリセットと `#game-container` に関わるレイアウトはここに書く。
- トンマナで定義したカラーパレット・フォントは CSS カスタムプロパティとして定義し、コンポーネントから参照する。

```css
:root {
  --color-primary: #xxxxxx;
  --color-bg: #xxxxxx;
  --font-base: 'FontName', sans-serif;
}
```

- Phaser キャンバス (`#game-container`) に関するスタイルのみここに書く。React コンポーネントのスタイルをここに書かない。

## コンポーネントスタイル (CSS Modules)

- `src/components/Xxx/Xxx.module.css` をコンポーネントと同じフォルダに置く。
- クラス名はキャメルケースで書く (`primaryButton` など)。
- カラー・フォントは CSS カスタムプロパティ経由で参照し、値をハードコードしない。

```css
/* ✅ 正しい */
.button {
  background: var(--color-primary);
  font-family: var(--font-base);
}

/* ❌ 誤り — 値の直書き */
.button {
  background: #ff0000;
}
```

## インラインスタイル (`style={{}}`) の禁止

React コンポーネントの**静的なスタイルは必ず `Xxx.module.css` に書く**。
JSX の `style={{}}` は「実行時に JS で計算される値」専用とし、それ以外で使わない。

| 用途 | 可否 |
|---|---|
| 色・余白・サイズ・flex などの静的スタイル | ❌ CSS Modules に書く |
| JS の計算結果を渡す (例: `RecipeTree` の `width={leaves * SLOT}`、`NewCropModal` の per-sparkle 座標) | ✅ 許容。`// eslint-disable-next-line no-restricted-syntax` を付けて意図を明示する |

- 視覚スタイルを持つコンポーネントを新規作成するときは、必ず同階層に `.module.css` を作る。
- このルールは `eslint.config.mjs` の `no-restricted-syntax`（`src/components/**/*.tsx` 対象、`*.stories.tsx` は除外）で機械的に検出する。`npm run lint` で実行。

## デザイントークン (`:root`)

色・フォントサイズ・余白・角丸・影は `public/style.css` の `:root` で定義したトークンを参照する。
コンポーネント CSS で**生の値（`#hex`・`rgb()`/`rgba()`・直接の `px`）を書かない**。

| 種別 | トークン |
|---|---|
| 色 | `--color-*` |
| フォントサイズ | `--font-size-xs` / `-sm` / `-md` / `-lg` |
| 余白 | `--space-2xs` / `-xs` / `-sm` / `-md` / `-lg` / `-xl` |
| 角丸 | `--radius-base` |
| 影 | `--shadow-tile` / `--shadow-tile-pressed` |

- 新しい色・サイズが必要なら、**まず `:root` にトークンを追加してから**参照する。
- 色の直書き（`#hex`・`rgb()`/`rgba()`）は `stylelint`（`color-no-hex` / `function-disallowed-list`）で `*.module.css` を検査して弾く。`:root` を持つ `public/style.css` は検査対象外。

## 全画面オーバーレイ

ゲームキャンバスに重ねる中央寄せの全画面オーバーレイは、`public/style.css` のグローバルクラス
`.ui-overlay` を使う（設計意図 → [phaser-react-bridge.md](phaser-react-bridge.md)）。
コンポーネント CSS で `position: absolute; inset: 0` の中央寄せオーバーレイを再定義しない。
中央寄せ以外の特殊レイアウト（縦並び・下寄せなど）のみ個別に定義してよい。

## Storybook との連携

`.storybook/preview.ts` で `public/style.css` をインポートし、Storybook 上でもカスタムプロパティとグローバルスタイルが適用される状態を維持する。

```ts
// .storybook/preview.ts
import '../public/style.css';
```

## Phaser 側のスタイル

Phaser のゲーム内 UI (スプライト・テキスト・Graphics) は CSS で管理しない。スタイルに相当する値 (色・フォントサイズ) は `docs/external-design/tone-and-manner.md` で定義し、Phaser の API (`setTint`, `setStyle` など) で適用する。
