# コーディングルール

## TypeScript

- `any` は禁止。型が不明な場合は `unknown` を使い、型ガードで絞り込む。
- Component は `interface` で定義する。`class` は使わない。
- Entity の ID は `number` 型のエイリアス `type EntityId = number` を使う。
- `null` より `undefined` を優先する。ただし Phaser API が `null` を返す箇所はそのまま扱う。

## ECS 固有

- Component のプロパティはすべて mutable にする (`readonly` を付けない)。System が書き換えるため。
- World から Entity を検索する際は Component の組み合わせでフィルタリングし、存在しない Component へのアクセスはしない。
- System のコンストラクタには World への参照のみ受け取る。Phaser の Scene を渡す場合は `RenderSystem` など描画専用 System に限定する。

## Phaser

- Phaser オブジェクトの直接操作は System の中からのみ行う。Scene の `create()` では生成のみ行い、ロジックは System に委譲する。
- `this.add.xxx()` で生成した GameObject は対応する Component に格納し、Scene のフィールドとして持たない。

## 一般

- `console.log` はデバッグ用途のみ。コミット前に削除する。
- マジックナンバーは `const` で名前を付ける。
