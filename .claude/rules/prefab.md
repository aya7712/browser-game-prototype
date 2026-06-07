# Phaser プレハブルール

## プレハブとは

`Phaser.GameObjects` のサブクラスとして実装する再利用可能なゲームオブジェクト。
位置・外観・状態・ビヘイビアをひとつのクラスにカプセル化する。

```ts
// 基本形
export class FarmPlot extends Phaser.GameObjects.Image {
    constructor(scene: Phaser.Scene, x: number, y: number) {
        super(scene, x, y, 'texture-key');
        this.scene.add.existing(this); // シーンに自己登録
        this.setInteractive();
    }

    // ビヘイビアはメソッドで定義
    plant(cropKind: CropKind) { ... }
    advance() { ... }
    harvest() { ... }
}
```

## ファイル配置

```
src/game/prefab/
  FarmPlot.ts
  DungeonTile.ts   （今後追加予定）
  Player.ts        （今後追加予定）
```

## ECS との使い分け

| ケース | 採用 |
|---|---|
| Phaser の描画 API と密結合し、状態変化もそのオブジェクト内で完結する | **プレハブ** |
| 複数の System が同一 Component を読み書きする（ダンジョンの Player など） | **ECS** |
| 毎フレーム大量の Entity を処理するパフォーマンス重視の場面 | **ECS** |

このゲームでの方針:
- **農場区画 (FarmPlot)**: プレハブ。日送り・植付け・収穫はシーン内で閉じており System 連携が不要なため。
- **ダンジョン Player・DungeonTile**: ECS。InputSystem・MovementSystem・RenderSystem が協調して処理するため。

## 実装ルール

### インポート
`import Phaser from 'phaser'` はデフォルトエクスポートが存在しないため使用禁止。
名前付きインポートを使う。

```ts
// ✅ 正しい
import { GameObjects, Scene } from 'phaser';
export class FarmPlot extends GameObjects.Image { ... }

// ❌ 誤り
import Phaser from 'phaser';
export class FarmPlot extends Phaser.GameObjects.Image { ... }
```

### シーンへの登録
コンストラクタ内で `this.scene.add.existing(this)` を呼ぶ。
シーン側で `this.add.existing(instance)` を呼ぶ必要はない。

### EventBus との連携
プレハブ内から EventBus を emit してよい。購読（on）はシーン側で行い、
プレハブがシーンのライフサイクルに依存しないようにする。

```ts
// ✅ プレハブ内で emit はOK
this.on('pointerdown', () => EventBus.emit('plot-tapped', { ... }));

// ❌ プレハブ内で on/off はNG（シーンの shutdown で解除できない）
EventBus.on('crop-planted', this.handler);
```

### 子スプライトの管理
プレハブがタイルの上に重ねるスプライト（作物など）を持つ場合、
`this.scene.add.image(...)` で生成してプロパティとして保持し、`destroy()` 時に合わせて破棄する。

### 状態
プレハブの状態は `status` などのプロパティとして持つ。
ECS の Component に書かない（プレハブを使う場合は World への登録不要）。

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| プレハブクラス | PascalCase | `FarmPlot`, `DungeonTile`, `Player` |
| ファイル名 | クラス名と同じ | `FarmPlot.ts` |
| 配置フォルダ | `src/game/prefab/` | — |
