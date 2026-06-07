# browser game prototype Template

React フレームワークとPhaserを用いたブラウザゲームのプロトタイプを作成するためのテンプレートプロジェクトです。

### バージョン

このテンプレートは以下のバージョンに対応しています:

- [Phaser 4](https://github.com/phaserjs/phaser)
- [React 19.0.0](https://github.com/facebook/react)
- [Vite 6.3.1](https://github.com/vitejs/vite)
- [TypeScript 5.7.2](https://github.com/microsoft/TypeScript)

## 必要環境

依存関係のインストールや `npm` 経由でのスクリプト実行には [Node.js](https://nodejs.org) が必要です。

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
