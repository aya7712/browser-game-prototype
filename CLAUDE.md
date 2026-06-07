# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## コマンド

```bash
npm run dev          # 開発サーバー起動 (http://localhost:8080)、匿名テレメトリあり
npm run dev-nolog    # 開発サーバー起動、テレメトリなし
npm run build        # 本番ビルド (dist/ に出力)
npm run build-nolog  # 本番ビルド、テレメトリなし
```

テストランナーは未設定。

## アーキテクチャ

**Phaser 4 + React 19 + TypeScript** の構成で、Vite でビルドする。React が HTML シェルと UI を担当し、Phaser がゲームキャンバスとロジックを担当する二層構造。

Phaser 側のゲームロジックは目的に応じて **プレハブ** と **ECS** を使い分ける。

| 方式 | 採用場面 | 配置 |
|---|---|---|
| **プレハブ** (`Phaser.GameObjects` サブクラス) | 状態と描画が同一オブジェクト内で完結するもの（マップ上の固定オブジェクトなど） | `src/game/prefab/` |
| **ECS** (Entity / Component / System) | 複数 System が協調するもの（プレイヤーキャラクター・敵・タイルなど） | `src/game/ecs/` |

主要ファイル:
- [src/PhaserGame.tsx](src/PhaserGame.tsx) — React-Phaser ブリッジ。`{ game, scene }` を `forwardRef` で公開する。
- [src/game/EventBus.ts](src/game/EventBus.ts) — React-Phaser 間の唯一の通信経路。
- [src/game/main.ts](src/game/main.ts) — Phaser `GameConfig` (1280×720、アーケード物理演算、ピクセルアートレンダラー) と `StartGame` ファクトリ。
- [src/game/scenes/](src/game/scenes/) — シーン実行順: `Boot` → `Preloader` → `TitleScene` → 各シーン。

アセット・フォルダ構成・命名規則の詳細 → [.claude/rules/folder-structure.md](.claude/rules/folder-structure.md)  
Phaser-React ブリッジの詳細 → [.claude/rules/phaser-react-bridge.md](.claude/rules/phaser-react-bridge.md)  
プレハブの実装ルール → [.claude/rules/prefab.md](.claude/rules/prefab.md)  
ECS の実装ルール → [.claude/rules/ecs.md](.claude/rules/ecs.md)

---

## 開発ワークフロー

機能追加・新規ゲーム開発は必ず **要件定義 → 外部設計 → 内部設計 → 実装** の順に進める。  
フェーズ順守・設計変更ルール → [.claude/rules/workflow.md](.claude/rules/workflow.md)

---

### 1. 要件定義

> 参照ルール: なし

**保存先**: `docs/requirements/`  
**必須ドキュメント**: `requirements.md`

**このフェーズで決めること**
- ゲームの目的・コンセプト・ターゲットプレイヤー
- 機能要件 (ユーザーストーリー形式)
- 非機能要件・スコープ外・完了条件 (Definition of Done)

ドキュメントのテンプレート → [.claude/rules/docs-format.md](.claude/rules/docs-format.md)

---

### 2. 外部設計

> 参照ルール: [phaser-react-bridge.md](.claude/rules/phaser-react-bridge.md) (Phaser/React 振り分け基準)

**保存先**: `docs/external-design/`  
**必須ドキュメント**: `scene-flow.md`, `ui-spec.md`, `game-rules.md`, `balance-params.md`, `asset-list.md`, `tone-and-manner.md`, `game-config.md`

**このフェーズで決めること**
- 画面・シーン一覧と遷移フロー
- 各シーンのレイアウト・UI 要素・操作仕様
- 各 UI 要素を Phaser / React のどちらで実装するかの振り分け
- ゲームルール・スコア計算・勝敗条件 (`game-rules.md`)
- バランスパラメータ: 移動速度・攻撃速度・HP など開発者が調整する数値・デフォルト値・調整範囲 (`balance-params.md`)
- トンマナ: ビジュアルスタイル・カラーパレット・フォント・SE/BGM の雰囲気・テキスト文体
- アセット一覧 (画像・音声・フォント) と用途
- ゲームコンフィグ: ユーザーが調整できるパラメータ一覧・デフォルト値・値の範囲・UI での露出方法 (`game-config.md`)

ドキュメントのテンプレート → [.claude/rules/docs-format.md](.claude/rules/docs-format.md)

---

### 3. 内部設計

> 参照ルール: [ecs.md](.claude/rules/ecs.md), [phaser-react-bridge.md](.claude/rules/phaser-react-bridge.md), [folder-structure.md](.claude/rules/folder-structure.md), [data-layer.md](.claude/rules/data-layer.md)

**保存先**: `docs/internal-design/`  
**必須ドキュメント**: `ecs-design.md`, `component-types.md`, `event-spec.md`, `sequence.md`

**このフェーズで決めること**
- Entity の種類と各 Entity が持つ Component の組み合わせ
- Component の型定義 (データのみ・ロジックなし)
- System 一覧・各 System が読み書きする Component・実行順序
- EventBus のイベント名・ペイロード型・発火タイミング
- ファイル配置計画 (`entities/`, `components/`, `systems/` の構成)
- 静的マスターデータ (アイテム・作物・交配レシピ) の定義ファイルと主要フィールド (`data-layer.md` 参照)

ドキュメントのテンプレート → [.claude/rules/docs-format.md](.claude/rules/docs-format.md)

---

### 4. アセット生成

> 参照ルール: なし（各スキルの README に従う）

**保存先**: `public/assets/`  
**依拠ドキュメント**: `docs/external-design/asset-list.md`, `docs/external-design/tone-and-manner.md`

**このフェーズで行うこと**
- `asset-list.md` に記載された全アセットを生成・配置する
- 各アセットは対応するスキルを使って生成する:

| アセット種別 | 使用スキル |
|---|---|
| 背景画像 (1280×720px のシーン背景) | `bg-generator` |
| スプライト・アイコン・タイル (64px 以下) | `sprite-generator` |
| BGM (ループ音楽・WAV) | `bgm-generator` |
| SE (効果音・WAV) | `sfx-generator` |

**音声フォーマット**: BGM・SE はすべて **WAV 形式** で生成・保存する (`*.wav`)。

複数アセットを同時に生成する場合は、種別ごとにサブエージェントを並列起動して効率化する。

---

### 5. TODOリスト作成

> 参照ルール: [todo-list.md](.claude/rules/todo-list.md)

**保存先**: `docs/iteration/`  
**ファイル名規則**: `todo_impl_phase<N>.md`（例: `todo_impl_phase1.md`）

**このフェーズで行うこと**
- 内部設計ドキュメント全体を読み、実装タスクを以下の4カテゴリに分解してリストアップする
  1. **共通Reactコンポーネントパーツ** — 複数シーンで使い回す汎用UIパーツ
  2. **シーンごとのReactコンポーネント** — 各シーンのUIオーバーレイ
  3. **Phaserシーン** — 各シーンの Phaser 実装
  4. **機能ごとの実装** — 動作確認可能な単位に細分化したタスク（「タイトル→メインシーンへの遷移」「キャラクターの移動」など）
- 各タスクに **動作確認ポイント**（何が見えれば完了か）を記載する
- 完了したタスクは `[x]` に更新する。ファイルは実装完了まで `docs/iteration/` に残す

詳細ルール → [.claude/rules/todo-list.md](.claude/rules/todo-list.md)

---

### 6. 実装

> 参照ルール: [ecs.md](.claude/rules/ecs.md), [coding-rules.md](.claude/rules/coding-rules.md), [phaser-react-bridge.md](.claude/rules/phaser-react-bridge.md), [folder-structure.md](.claude/rules/folder-structure.md), [css.md](.claude/rules/css.md)

TODOリストのタスクを **1タスクずつ** 順に実装し、完了のたびにユーザー確認→コミットを行う。

#### 1タスクの進め方

1. **実装する** — TODOリストの先頭の未着手タスクを1つ選んで実装する
2. **確認させる** — ユーザーがブラウザで確認できる状態にしてから報告する
   - **React コンポーネント（カテゴリ1・2）**: Storybook（`npm run storybook`）を起動して `http://localhost:6006` で確認させる。コンポーネントと同フォルダに `*.stories.tsx` を必ず作成する
   - **Phaser シーン・機能（カテゴリ3・4）**: 開発サーバー（`npm run dev-nolog`）を起動して `http://localhost:8080` で確認させる
3. **ユーザーの承認を得る** — 「OK」が来るまで次に進まない。修正依頼が来た場合は修正して再確認させる
4. **コミットする** — 承認後に `git commit` する
5. **TODOを更新する** — `docs/iteration/todo_impl_phase<N>.md` の該当行を `[x]` に更新する
6. **次のタスクへ** — 1に戻る

#### その他のルール

- 設計からの逸脱が生じた場合は設計ドキュメントを先に更新し、ユーザーの承認を得てから実装を変更する
- 新たに必要なタスクが判明した場合はTODOリストの末尾に追加してよい（ユーザー確認不要）
