# browser game prototype Template

React と Phaser を用いたブラウザゲームのプロトタイプを、Claude Code と一緒に作るためのテンプレートプロジェクトです。

「○○なゲームを作りたい」と伝えるだけで、Claude が要件定義・外部設計・内部設計から
実装、さらに背景・スプライト・BGM・SE といったアセット生成までを実行します。
プロジェクトに同梱された `CLAUDE.md` と `.claude/` 以下のルール・スキルに沿って進めるため、
開発の進め方やコーディング規約を自分で調べる必要はありません。

### バージョン

このテンプレートは以下のバージョンに対応しています:

- [Phaser 4](https://github.com/phaserjs/phaser)
- [React 19.0.0](https://github.com/facebook/react)
- [Vite 6.3.1](https://github.com/vitejs/vite)
- [TypeScript 5.7.2](https://github.com/microsoft/TypeScript)

## 必要環境

- [Node.js](https://nodejs.org) — 依存関係のインストールや `npm` 経由でのスクリプト実行に使用します。
- [uv](https://docs.astral.sh/uv/) — アセット生成スキル（`bg-generator`・`sprite-generator`）が
  Python（Pillow）スクリプトを `uv run --with pillow python3 ...` の形で実行するために使用します。
- [Claude Code](https://claude.com/claude-code) — `.claude/` 以下のルール・スキルを使った開発を行う場合に必要です。

## 利用可能なコマンド

| コマンド | 説明 |
|---------|-------------|
| `npm install` | プロジェクトの依存関係をインストールします |
| `npm run dev` | 開発用サーバーを起動します |
| `npm run build` | `dist` フォルダに本番用ビルドを生成します |
| `npm run dev-nolog` | 匿名データを送信せずに開発用サーバーを起動します（下記の「log.js について」を参照） |
| `npm run build-nolog` | 匿名データを送信せずに `dist` フォルダへ本番用ビルドを生成します（下記の「log.js について」を参照） |

## コードを書く

1. リポジトリのクローン
   `git clone https://github.com/aya7712/browser-game-prototype.git <game-name>-prototype`
2. 依存関係のインストール
   `npm install`
3. Claude Code を起動し、作りたいゲームを伝える
   ルールやワークフローを自分で読み込む必要はありません。Claude が `CLAUDE.md` と
   `.claude/rules/` を踏まえて要件定義から進めてくれます。例えば次のように頼んでください。

   > 「○○なゲームを作りたいです。要件定義から始めてください」
   > 「アイテムを集めて育成するローグライクゲームの企画を一緒に考えてほしい」

   Claude が要件定義 → 外部設計 → 内部設計 → アセット生成 → TODOリスト作成 → 実装の順に
   提案し、各フェーズの完了ごとに確認を求めてきます。内容を確認し、問題なければ
   「OK」「次に進めてください」のように伝えるだけで開発が進みます。
4. 動作確認は Claude に依頼する
   「`npm run dev` でブラウザから確認したい」「実装した○○の動きを確認してほしい」
   のように伝えれば、開発サーバーの起動や画面確認まで Claude が行います。

## ワークフロー

機能追加・新規ゲーム開発は、必ず次の順序で進めます（詳細は `CLAUDE.md` および
`.claude/rules/workflow.md` を参照）。

1. **要件定義** — `docs/requirements/requirements.md` にコンセプト・機能要件・非機能要件・DoD を記載する
2. **外部設計** — `docs/external-design/` にシーン構成・UI仕様・ゲームルール・バランス・トンマナ・アセット一覧・ゲームコンフィグを記載する
3. **内部設計** — `docs/internal-design/` に ECS設計・Component型・EventBus仕様・シーケンスを記載する
4. **アセット生成** — 外部設計の `asset-list.md` に基づき、下記の「スキル」を使ってアセットを生成する
5. **TODOリスト作成** — `docs/iteration/todo_impl_phase<N>.md` に実装タスクを洗い出す
6. **実装** — TODOリストを1タスクずつ実装し、確認・承認・コミットを繰り返す

前フェーズの必須ドキュメントが揃っていない状態で次フェーズに進んではいけません。
設計に変更が生じた場合は、要件定義から見直して関連ドキュメントを更新し、
`docs/CHANGELOG.md` に記録してからユーザーの承認を得て実装を変更します。

## スキル

`.claude/skills/` 以下に、ゲーム用アセットを生成するための Claude Code スキルを同梱しています。
いずれも外部の API キーやアカウントを必要とせず、スキル単体で動作します。

| スキル | 生成するもの | 保存先 |
|---|---|---|
| `bg-generator` | 背景画像（PNG、1280×720px、ドット絵風変換つき） | `public/assets/scenes/` |
| `sprite-generator` | 小型ドット絵（スプライト・アイコン・タイル、64px以下） | `public/assets/<category>/` |
| `bgm-generator` | BGM（ループ音楽、WAV） | `public/assets/bgm/` |
| `sfx-generator` | 効果音（SE、WAV） | `public/assets/sfx/` |

各スキルは外部設計フェーズで作成する `docs/external-design/asset-list.md` と
`docs/external-design/tone-and-manner.md` を参照してアセットを生成します。
音声アセット（BGM・SE）はすべて WAV 形式で統一して管理します。

`bgm-generator` は [BeepBox](https://www.beepbox.co/) の合成エンジンを、
`sfx-generator` は [ai-sfx](https://github.com/siliconjungle/ai-sfx) の jsfxr ラッパーを
それぞれ MIT ライセンスのもとでビルド済みの形で同梱しています
（`vendor/` 以下に同梱元の `LICENSE` を配置）。

## 注意事項

本プロジェクトはゲームのプロトタイプを作ることを目的としています。本番相当の品質、著作権管理は保証していません。  
本プロジェクトで作った成果物によるトラブルには一切責任を負いません。

## テンプレートのカスタマイズ

### Vite

ビルドをカスタマイズしたい場合（CSS やフォントを読み込むプラグインの追加など）は、プロジェクト全体に影響する変更であれば `vite/config.*.mjs` ファイルを編集してください。あるいは新しい設定ファイルを作成し、`package.json` 内の各 npm タスクから参照することもできます。詳しくは [Vite のドキュメント](https://vitejs.dev/) を参照してください。

## log.js について

node スクリプトを確認すると `log.js` というファイルがあることに気付くと思います。このファイルは `gryzor.co` というドメインに対して、サイレントに 1 回だけ API 呼び出しを行います。このドメインは Phaser Studio Inc. が所有しており、お気に入りのレトロゲームへのオマージュとして名付けられています。

このAPIには次の3つのデータを送信しています: 使用しているテンプレート名（vue, react など）、ビルドが 'dev' か 'prod' か、そして使用している Phaser のバージョンです。

個人情報が収集・送信されることは一切ありません。プロジェクトファイルやデバイス、ブラウザなどの情報を取得することもありません。気になる場合は `log.js` ファイルの中身を確認してみてください。

データを送信したくない場合は、以下のコマンドを代わりに使用できます。

開発時:

```bash
npm run dev-nolog
```

ビルド時:

```bash
npm run build-nolog
```

または、ログ送信自体を完全に無効にしたい場合は、`log.js` ファイルを削除し、`package.json` の `scripts` セクションからその呼び出しを削除してください。

変更前:

```json
"scripts": {
    "dev": "node log.js dev & dev-template-script",
    "build": "node log.js build & build-template-script"
},
```

変更後:

```json
"scripts": {
    "dev": "dev-template-script",
    "build": "build-template-script"
},
```
