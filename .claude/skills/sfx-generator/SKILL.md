---
name: sfx-generator
description: >
  このプロジェクト用の効果音（WAV）を生成するスキル。
  「ダッシュの効果音を作って」「ジャンプSEが欲しい」「コイン取得音を追加して」など、
  効果音・SE・サウンドエフェクトの生成・追加を依頼されたときに必ず使うこと。
  jsfxrパラメータをClaude自身が設計し、generate-sfx.mjsに渡してWAVを生成する。
---

## 概要

jsfxr（レトロゲーム音声合成ライブラリ）を使って効果音WAVを生成する。
Claude自身がパラメータを設計してスクリプトを呼び出す——APIコール不要。

生成には `vendor/ai-sfx/generate-sfx.mjs` を使う。外部リポジトリへの依存を
避けるため、このスキル単体で動作するように同梱している。

## ファイル配置

生成したWAVは必ず `public/assets/sfx/` に保存する。
ファイル名はケバブケース（例: `coin-pickup.wav`, `player-dash.wav`）。

## 手順

### 1. パラメータ設計

下記スキーマに従ってjsfxrパラメータJSONを設計する。
音の特性に応じて各値を調整すること。

```
{
  "oldParams": true,
  "wave_type": 0,          // 0=square 1=sawtooth 2=sine 3=noise
  "p_env_attack":    0,    // アタック時間 [0,1]
  "p_env_sustain":   0.1,  // サステイン時間 [0,1]
  "p_env_punch":     0,    // サステインパンチ [0,1]
  "p_env_decay":     0.2,  // ディケイ時間 [0,1]
  "p_base_freq":     0.3,  // 基本周波数 [0,1]
  "p_freq_limit":    0,    // 最低周波数カットオフ [0,1]
  "p_freq_ramp":     0,    // 周波数スライド [-1,1] (正=上昇, 負=下降)
  "p_freq_dramp":    0,    // デルタスライド [-1,1]
  "p_vib_strength":  0,    // ビブラート深さ [0,1]
  "p_vib_speed":     0,    // ビブラート速度 [0,1]
  "p_arp_mod":       0,    // アルペジオ音程変化 [-1,1]
  "p_arp_speed":     0,    // アルペジオ速度 [0,1]
  "p_duty":          0,    // デューティ比（square用）[0,1]
  "p_duty_ramp":     0,    // デューティ比変化 [-1,1]
  "p_repeat_speed":  0,    // リピート速度 [0,1]
  "p_pha_offset":    0,    // フェイザーオフセット [-1,1]
  "p_pha_ramp":      0,    // フェイザー変化 [-1,1]
  "p_lpf_freq":      1,    // LPFカットオフ [0,1] (1=全開)
  "p_lpf_ramp":      0,    // LPF変化 [-1,1]
  "p_lpf_resonance": 0,    // LPFレゾナンス [0,1]
  "p_hpf_freq":      0,    // HPFカットオフ [0,1]
  "p_hpf_ramp":      0,    // HPF変化 [-1,1]
  "sound_vol":       0.5,  // 音量 [0,1]
  "sample_rate":     44100,
  "sample_size":     16    // 必ず16
}
```

### 2. WAV生成

```bash
mkdir -p public/assets/sfx
node .claude/skills/sfx-generator/vendor/ai-sfx/generate-sfx.mjs '<JSON>' public/assets/sfx/<name>.wav
```

### 3. 完了報告

- 保存先パス
- パラメータの設計意図（波形選択・周波数・エンベロープの狙い）

## 音別の典型パラメータ傾向

| 音の種類 | wave_type | p_base_freq | p_freq_ramp | 特徴 |
|---------|-----------|-------------|-------------|------|
| コイン・ピックアップ | square(0) | 0.5〜0.7 | 0（+ arp_mod） | 短く明るい |
| ジャンプ | square(0)/sine(2) | 0.3〜0.5 | +0.2〜0.4 | 上昇スライド |
| ダッシュ | sawtooth(1) | 0.5〜0.6 | -0.3〜-0.4 | 下降スライド |
| 爆発 | noise(3) | 0.2〜0.4 | -0.1〜-0.3 | 長めのdecay |
| ヒット/ダメージ | square(0)/noise(3) | 0.3〜0.5 | -0.1〜-0.2 | 短くパンチ感 |
| レベルアップ | square(0)/sine(2) | 0.3〜0.4 | +0.1 | アルペジオ上昇 |
