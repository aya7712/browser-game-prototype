# フォルダー構成ルール

## src/ 以下の構成

```
src/
  main.tsx                  # React エントリーポイント
  App.tsx                   # ルート React コンポーネント
  PhaserGame.tsx            # React-Phaser ブリッジコンポーネント
  components/               # React UI コンポーネント (Storybook 対象)
    Button/
      Button.tsx
      Button.stories.tsx    # コンポーネントと同階層に置く
      Button.module.css
  game/
    main.ts                 # Phaser GameConfig・StartGame ファクトリ
    EventBus.ts             # React-Phaser 間イベントバス
    scenes/                 # Phaser シーン (Boot, Preloader, Game など)
    ecs/
      components/           # Component の型定義 (interface のみ)
      systems/              # System クラス
      world.ts              # Entity/Component の登録・検索を管理する World クラス
    prefab/                 # Phaser.GameObjects サブクラス（プレハブ）

.storybook/
  main.ts                   # Storybook 設定
  preview.ts                # グローバルデコレーター・スタイル
```

## ファイル配置の判断基準

| 追加するもの | 置き場所 |
|---|---|
| 新しいシーン | `src/game/scenes/` |
| プレハブ（`GameObjects` サブクラス） | `src/game/prefab/` |
| Component の型 | `src/game/ecs/components/` |
| System クラス | `src/game/ecs/systems/` |
| React UI コンポーネント | `src/components/コンポーネント名/` (1 コンポーネント 1 フォルダ) |
| Storybook ストーリー | コンポーネントと同じフォルダ内に `Xxx.stories.tsx` |
| 静的アセット | `public/assets/` |

## docs/ 以下の構成

```
docs/
  CHANGELOG.md              # 設計変更の一元管理 (変更があるたびに必ず記録)
  requirements/
    requirements.md
  external-design/
    scene-flow.md
    ui-spec.md
    game-rules.md
    balance-params.md
    asset-list.md
    tone-and-manner.md
    game-config.md
  internal-design/
    ecs-design.md
    component-types.md
    event-spec.md
    sequence.md
```

## CSS ファイルの配置

CSS の管理方針の詳細 → [css.md](css.md)

| ファイル | 用途 |
|---|---|
| `public/style.css` | グローバルスタイル・CSS カスタムプロパティ定義 |
| `src/components/Xxx/Xxx.module.css` | コンポーネントスコープのスタイル (CSS Modules) |
| `.storybook/preview.ts` | Storybook 用グローバルスタイルのインポート |

## Storybook の対象範囲

- `src/components/` 以下の React UI コンポーネントのみが対象。
- `src/game/` 以下 (Phaser シーン・ECS) は Storybook の対象外。Phaser の Canvas が必要なものは Storybook では扱わない。
- `.stories.tsx` はコンポーネントと**同じフォルダに置く**。離れた場所に集めると、コンポーネントの移動・削除時に stories が取り残されるため。

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| Component 型 | `XxxComponent` (interface) | `PositionComponent` |
| System クラス | `XxxSystem` | `MovementSystem` |
| Entity ファクトリ | `createXxx` | `createPlayer` |
| Phaser シーン | PascalCase | `GameScene` |
| ファイル名 | クラス名と同じ | `MovementSystem.ts` |
