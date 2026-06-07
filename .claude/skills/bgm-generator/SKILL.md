---
name: bgm-generator
description: >
  このプロジェクト用のBGM（ループ音楽・WAV）を生成するスキル。
  「タイトル曲が欲しい」「ステージのBGMを作って」「エンディングの音楽を追加して」
  など、BGM・背景音楽・ループ曲の生成・追加を
  依頼されたときに必ず使うこと。
  Claude自身がBeepBoxのJSON楽曲を設計し、beepbox の render-wav CLI でWAVに
  レンダリングして public/assets/bgm/ に保存する。SE（短い効果音）は別スキル
  sfx-generator を使うこと。
---

## 概要

[BeepBox](https://www.beepbox.co/)（チップチューン作曲ツール）の合成エンジンを
CLI化した `vendor/beepbox/cli/render-wav.mjs` を使ってBGMを生成する。
Claude自身が楽曲（コード進行・メロディ・楽器）をBeepBoxのJSON形式で設計し、
CLIでWAVにレンダリングする——APIコール不要。外部リポジトリへの依存を避けるため、
ビルド済みCLIをスキルに同梱している。

BGMの方向性（曲調・テンポ・楽器構成など）は `docs/external-design/tone-and-manner.md` に
定義されたシーンごとの雰囲気に従う。

## ファイル配置

生成したWAVは `public/assets/bgm/` に保存する。ファイル名は
`docs/external-design/asset-list.md` の「BGM」表に記載された名前の拡張子を
`.wav` にしたものを使う（例: `bgm/title` → `public/assets/bgm/title.wav`）。

> 音声フォーマットは BGM・SE とも **WAV 形式に統一する**（`.ogg` や `.mp3` は使わない）。
> 詳細 → [docs-format.md](../../rules/docs-format.md) の音声フォーマット規則。

作曲スクリプトは `scripts/compose-<name>.mjs` に作成する（bg-generatorと同じ流儀）。

## 手順

### 1. 要件確認

以下を読んでから作曲する:
- `docs/external-design/tone-and-manner.md` — 各シーンの雰囲気
- `docs/external-design/asset-list.md` — 対象ファイル名・用途
- `docs/external-design/scene-flow.md` — そのBGMが流れる場面

### 2. 作曲スクリプトを書く

`scripts/compose-<name>.mjs` を作成し、同梱ヘルパー
`.claude/skills/bgm-generator/lib/beepbox-compose.mjs` を import して
楽曲内容（コード進行・メロディ・ベース等）を定義し、`printSong()` で
JSONを標準出力する。

```javascript
import { m, note, channel, buildSong, printSong, barTicks }
  from "../.claude/skills/bgm-generator/lib/beepbox-compose.mjs";

const BAR = barTicks(4, 4); // 1小節 = 16 tick（4拍 × ticksPerBeat 4）

// コード進行（MIDIで記述。例: 穏やかな曲調 C - G - Am - F）
const chords = [
  [48, 52, 55],     // C   (C3 E3 G3)
  [43, 47, 50, 55], // G   (G2 B2 D3 G3)
  [45, 48, 52],     // Am  (A2 C3 E3)
  [41, 45, 48, 52], // F   (F2 A2 C3 E3)
];

const pad = channel(3, {
  type: "harmonics", volume: 80,
  fadeInSeconds: 0.2, fadeOutTicks: 72,
  effects: ["reverb", "chorus"], reverb: 80, chorus: 50,
}, chords.map((c) => [note(c, 0, BAR, 67)]));

const melody = channel(4, {
  type: "chip", wave: "rounded", volume: 100,
  fadeInSeconds: 0.02, fadeOutTicks: 24,
  effects: ["reverb"], reverb: 50,
}, [
  [note(72, 0, 8, 100), note(67, 8, 16, 100)], // C5 .. G4
  [note(74, 0, 8, 100), note(71, 8, 16, 100)], // D5 .. B4
  [note(72, 0, 8, 100), note(69, 8, 16, 100)], // C5 .. A4
  [note(65, 0, 16, 100)],                       // F4（全音符）
]);

const bass = channel(2, {
  type: "chip", wave: "rounded", volume: 80,
  fadeInSeconds: 0.03, fadeOutTicks: 48,
  effects: ["reverb"], reverb: 25,
}, [[note(36,0,BAR,70)],[note(31,0,BAR,70)],[note(33,0,BAR,70)],[note(29,0,BAR,70)]]);

printSong(buildSong({
  key: "C", scale: "normal :)",
  tempo: 96,            // シーン別の目安は下表
  beatsPerBar: 4, ticksPerBeat: 4,
  introBars: 0,         // ループBGMは intro 無しで曲全体をループ点にする
  channels: [pad, melody, bass],
}));
```

### 3. レンダリング

```bash
mkdir -p public/assets/bgm
node scripts/compose-<name>.mjs > /tmp/<name>.json
node .claude/skills/bgm-generator/vendor/beepbox/cli/render-wav.mjs \
  --in /tmp/<name>.json \
  -o public/assets/bgm/<name>.wav \
  --loop-count 1
```

- **ループBGMは曲全体が1ループ**になるよう作る（ゲーム側がファイルを繰り返す）。
  `introBars: 0` にして `--loop-count 1` でレンダリングすれば、ファイルの末尾→
  先頭が自然につながる。
- もっと長い1ファイルにしたいときは `--loop-count 2` 等で複数回展開する。

### 4. 確認・報告

```bash
# 長さ・レベルの確認（クリップしていないか）
node -e 'const fs=require("fs");const b=fs.readFileSync(process.argv[1]);let mx=0;for(let i=44;i+1<b.length;i+=2){const a=Math.abs(b.readInt16LE(i));if(a>mx)mx=a;}console.log("peak",(mx/32767*100).toFixed(1)+"%","sec",((b.length-44)/4/48000).toFixed(1));' public/assets/bgm/<name>.wav
```

報告する内容:
- 保存先パス・長さ（秒）・ピークレベル
- 曲の設計意図（キー/テンポ/コード進行/楽器・エフェクトの狙い）

ピークが極端に小さい/大きい場合は楽器の `volume` や note の `volume` を調整する。

---

## BeepBox JSON 作曲リファレンス

ヘルパーを使えば多くは隠蔽されるが、内部モデルを理解しておくこと。

### ピッチ・拍・小節

- **ピッチは絶対値**。合成時にキーの basePitch（C は 12）が足される。常に
  `key: "C"` を使い、`m(midi)=midi-12` でMIDI番号から変換する（ヘルパーが処理）。
  調を変えたいときはキーではなくMIDI番号をずらす。
  - 目安: C4(中央ド)=MIDI 60、A4=69、C3=48、C2=36。可聴域の旋律は概ね MIDI 48〜84。
- **tick** は `ticksPerBeat` 単位。1小節 = `beatsPerBar × ticksPerBeat` tick
  （例: 4拍 × 4 = 16）。note の tick は小節内の 0〜小節長。
- **1パターン = 1小節**。`sequence` が各小節にパターン番号（1始まり、0=空）を割り当てる
  （ヘルパーが各小節を順に並べる）。
- **同一チャンネル内で音は時間的に重ねられない**。和音は1つの note に複数ピッチを
  入れて表現する（`note([48,52,55], ...)`）。

### 曲の主要フィールド（buildSong が生成）

`format:"BeepBox"`, `version:9`, `scale`, `key`, `introBars`, `loopBars`,
`beatsPerBar`, `ticksPerBeat`, `beatsPerMinute`(=tempo, 30〜300),
`layeredInstruments:false`, `patternInstruments:false`, `channels`。

### 楽器フィールド（instrument オブジェクト）

| フィールド | 内容 |
|---|---|
| `type` | 楽器タイプ（下記）。チップチューンは `chip` / `harmonics` が基本 |
| `wave` | `chip` のとき波形名（下記） |
| `volume` | 0〜100。**100=最大音量、低いほど静か**（20刻みが綺麗に対応） |
| `effects` | 使うエフェクト名の配列（下記）。配列で明示すること |
| `reverb` / `chorus` | 各 0〜100。`effects` に `"reverb"` / `"chorus"` を含めた時のみ有効 |
| `fadeInSeconds` | 立ち上がりの柔らかさ（秒）。パッドは 0.2〜0.4 と長め |
| `fadeOutTicks` | 余韻の長さ（tick）。長いほど滑らかに減衰 |
| `unison` | ユニゾン名（下記）。`none` が基本 |
| `chord` | 和音の鳴らし方。アルペジオは `"arpeggio"` + `effects` に `"chord type"` 必須 |

note の `volume`（points内）は 0〜100 で音量を表す（内部で 0〜3 に丸められる）。

### 有効な名前（これ以外を書くとデフォルトに落ちる）

- **type**: `chip`, `FM`, `noise`, `spectrum`, `drumset`, `harmonics`, `PWM`, `Picked String`, `supersaw`
- **wave**（chip用）: `rounded`, `triangle`, `square`, `1/4 pulse`, `1/8 pulse`, `sawtooth`, `double saw`, `double pulse`, `spiky`
- **effects**: `reverb`, `chorus`, `panning`, `distortion`, `bitcrusher`, `note filter`, `echo`, `pitch shift`, `detune`, `vibrato`, `transition type`, `chord type`
- **scale**: `easy :)`, `easy :(`, `island :)`, `blues :)`, `normal :)`(長調・明るい), `normal :(`(短調・暗い), `double harmonic :)`, `strange`, `expert` ほか
- **key**: `C`〜`B`（基本は `C` 固定）
- **chord**: `simultaneous`(既定の同時和音), `strum`, `arpeggio`, `custom interval`
- **unison**: `none`, `shimmer`, `hum`, `fifth`, `octave`, `piano` ほか
- **vibrato**: `none`, `light`, `delayed`, `heavy`, `shaky`

### 雰囲気別の作曲ガイド（参考値）

シーンの雰囲気に応じて、おおよそ以下の傾向を目安にする。
具体的な雰囲気は `tone-and-manner.md` の記述に従って調整する。

| 雰囲気の方向性 | tempo | scale | コード進行の例 | 楽器・雰囲気の傾向 |
|---|---|---|---|---|
| 期待感・神秘的（タイトル等） | 80〜100 | `normal :)` | C - G - Am - F | harmonicsパッド+柔らかメロ |
| 穏やか・のどか | 96〜120 | `normal :)` / `easy :)` | C - F - G - C | 軽快なchip(rounded)、跳ねるベース |
| 軽い緊張感 | 100〜130 | `normal :(` | Am - F - C - G | やや速め、最小限の楽器 |
| 焦燥感・激しさ | 130〜160 | `normal :(` / `strange` | Dm - Bb - C - A | 速い・低音強め・distortion少量 |
| 重厚・不穏 | 50〜70 | `normal :(` / `double harmonic :(` | 持続する短和音、半音進行 | 低いパッド+不協、reverb深 |
| 明るい・ファンファーレ | 110〜140 | `normal :)` | C - G - F - G - C | 明るいリード+高めアルペジオ |

### ループを綺麗につなぐコツ

- 最後の小節のメロディ/ベースが**1小節目に自然に戻る**音で終わるようにする
  （例: 主和音やドミナント→主音へ）。
- reverb/echo の残響はファイル末尾で切れるため、ループ境界で軽いプツッが出る場合は
  最終小節の note を少し早めに切る（例: 0〜14 tick で終える）か reverb を下げる。
- 確認用に `--loop-count 2` でレンダリングして、つなぎ目を実際に聴いて調整する。
