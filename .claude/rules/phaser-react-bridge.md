# Phaser-React ブリッジルール

参考: https://generalistprogrammer.com/tutorials/phaser-react-integration-guide

## 基本原則

React は「状態変化で再レンダリングする宣言的 UI」、Phaser は「ゲームループで動作する命令的エンジン」。この対比を常に意識し、**EventBus による疎結合**を徹底する。

---

## UI の Phaser / React 振り分け基準

外部設計の `ui-spec.md` で各 UI 要素を以下の基準で振り分ける。実装前に振り分けが決まっていない要素があれば、先に `ui-spec.md` を更新する。

### React を使う場合

- テキスト主体の画面 (設定メニュー、インベントリ、リーダーボード)
- フォーム入力・複雑なインタラクション
- アクセシビリティが必要な要素
- レスポンシブレイアウトが必要な画面
- ゲームキャンバスと**独立して**表示される UI

### Phaser を使う場合

- ゲームワールドに追従する要素 (キャラクター頭上の HP バー、ダメージ表示、ミニマップ)
- ピクセルパーフェクトな配置が必要な要素
- Phaser のカメラシステムと連動する UI
- 毎フレーム更新が必要な表示

### ハイブリッド配置

React UI をゲームキャンバスの上に重ねる場合は CSS の絶対配置を使う。

```css
#game-container { position: relative; }
.ui-overlay    { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.ui-overlay .interactive { pointer-events: auto; }
```

---

## EventBus の使い方

### 基本

```ts
import { EventBus } from './EventBus';

// 発火
EventBus.emit('score-updated', { score: 100 });

// 購読
EventBus.on('score-updated', (data) => { ... });

// 購読解除
EventBus.off('score-updated', handler);
```

### Phaser シーンでのライフサイクル管理

`create()` で登録し、`shutdown` イベントで必ず解除する。

```ts
create() {
  this.handlePause = () => { ... };
  EventBus.on('pause-requested', this.handlePause);

  this.events.on(Phaser.Scenes.Events.SHUTDOWN, () => {
    EventBus.off('pause-requested', this.handlePause);
  });

  EventBus.emit('current-scene-ready', this);
}
```

### React コンポーネントでのライフサイクル管理

`useEffect` 内で登録し、クリーンアップ関数で解除する。

```ts
useEffect(() => {
  const handler = (data: ScorePayload) => setScore(data.score);
  EventBus.on('score-updated', handler);
  return () => EventBus.off('score-updated', handler);
}, []);
```

### カスタムフックで定型化

```ts
function usePhaserEvent<T>(event: string, handler: (data: T) => void) {
  const stableHandler = useCallback(handler, [handler]);
  useEffect(() => {
    EventBus.on(event, stableHandler);
    return () => EventBus.off(event, stableHandler);
  }, [event, stableHandler]);
}
```

### 通信の方向性

| 方向 | 用途例 |
|---|---|
| React → Phaser | ポーズ要求、設定変更、ゲーム開始 |
| Phaser → React | スコア更新、ゲームオーバー通知、シーン切り替え完了 |

---

## current-scene-ready の規約

すべての Phaser シーンは `create()` の末尾で呼ぶ。

```ts
EventBus.emit('current-scene-ready', this);
```

---

## PhaserGame コンポーネントの注意点

- `gameRef` で二重生成を防ぐ (`if (game.current === null)` ガード)。
- アンマウント時は必ず `game.destroy(true)` を呼ぶ。
- `ref` 経由の `game` / `scene` インスタンスへの直接操作は避け、EventBus を使う。

---

## よくある落とし穴

| 問題 | 対策 |
|---|---|
| ホットリロード時に複数キャンバスが生成される | `gameRef` の `null` チェックで二重生成を防ぐ |
| React の状態が Phaser のクロージャに古い値でキャプチャされる | EventBus 経由で都度送信し、Phaser 側でローカル変数に保持する |
| キーボード入力が React と Phaser で競合する | フォーカス管理を明示的に行い、入力の所有者を一方に限定する |
| 60FPS でイベントを emit してパフォーマンスが落ちる | フレーム毎の更新は Phaser 内部で完結させ、React への通知は状態変化時のみにする |
