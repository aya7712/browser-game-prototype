# データ層ルール

## 概要

ECS の Component はエンティティに付随する**動的なデータ**を持つ。
一方、アイテム定義・作物定義・交配レシピなどの**静的マスターデータ**は Component ではなく、`src/game/data/` 以下の定数ファイルで管理する。

## ファイル配置

```
src/game/data/
  items.ts     # アイテム一覧（種別・対応キー・使用時間など）
  crops.ts     # 作物一覧（種別・育成日数・売値・スコアなど）
  recipes.ts   # 交配レシピ一覧（素材A × 素材B → 結果）
```

## 書き方の原則

- `as const` で定義し、型を `typeof` から導出する。`any` は使わない。
- 値はすべて `balance-params.md` に記載されたデフォルト値に従う。
- System・Entity ファクトリはこれらの定数をインポートして参照する。直接マジックナンバーを書かない。

```ts
// ✅ 正しい
export const CROP_DEFS = {
  tomato: { growthDays: 1, sellPrice: 50, score: 20 },
  wheat:  { growthDays: 1, sellPrice: 50, score: 5 },
  // ...
} as const;

export type CropKind = keyof typeof CROP_DEFS;

// ❌ 誤り — System の中にマジックナンバーを書く
if (crop.kind === 'tomato') remainingDays = 1;
```

## 内部設計での扱い

`ecs-design.md` の「データ層」セクションに以下を記載する。

- 定義するファイル名と格納する定数の一覧
- 各定数の主要フィールド（`balance-params.md` の値を引用）
- System・Entity ファクトリからの参照関係
