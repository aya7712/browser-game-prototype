# ECS アーキテクチャルール

## 原則

このプロジェクトは Entity Component System アーキテクチャを採用する。

- **Entity**: 数値 ID のみ。ロジックもデータも持たない。
- **Component**: データのみ。メソッド・ロジックを持たない。
- **System**: ロジックのみ。特定の Component の組み合わせを持つ Entity を毎フレーム処理する。

## Component の書き方

```ts
// ✅ 正しい — データのみ
interface PositionComponent {
  x: number;
  y: number;
}

// ❌ 誤り — ロジックを持たせない
interface PositionComponent {
  x: number;
  y: number;
  moveTo(x: number, y: number): void; // 禁止
}
```

## System の書き方

- 1 つの System は 1 つの責務のみ持つ。
- `update(entities: Entity[], delta: number): void` を基本シグネチャとする。
- System 間の依存は持たない。System 間の連携が必要な場合は EventBus を使う。

```ts
// ✅ 正しい
class MovementSystem {
  update(entities: Entity[], delta: number): void { ... }
}

// ❌ 誤り — 別 System を直接呼ばない
class MovementSystem {
  constructor(private collisionSystem: CollisionSystem) {}
}
```

## Phaser との統合

- Phaser の `Sprite` などの GameObject は `RenderComponent` としてラップし、Entity に紐付ける。
- 描画・物理演算の更新は `RenderSystem` が担い、Phaser API の呼び出しを一箇所に集約する。
- Phaser Scene の `update()` から各 System の `update()` を呼び出す。

## System の実行順序

`docs/internal-design/ecs-design.md` に定義された順序を必ず守る。順序変更は設計ドキュメントの更新を先に行う。
