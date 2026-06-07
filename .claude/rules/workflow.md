# 開発ワークフロールール

## フェーズ順守

作業は必ず **要件定義 → 外部設計 → 内部設計 → 実装** の順に進める。

- 前フェーズの必須ドキュメントが `docs/` に存在しない場合、次のフェーズに進んではならない。
- ユーザーから実装を求められても、設計ドキュメントが揃っていなければ先にドキュメント作成を提案する。

## 各フェーズの必須ドキュメント

| フェーズ | 必須ファイル |
|---|---|
| 要件定義 | `docs/requirements/requirements.md` |
| 外部設計 | `docs/external-design/scene-flow.md`, `ui-spec.md`, `game-rules.md`, `balance-params.md`, `asset-list.md`, `tone-and-manner.md`, `game-config.md` |
| 内部設計 | `docs/internal-design/ecs-design.md`, `component-types.md`, `event-spec.md`, `sequence.md` |

## 設計変更

どのフェーズ・どのタイミングであっても、設計に変更が生じた場合は以下の手順を必ず踏む。

1. **要件定義から見直す**: `requirements.md` を起点に、変更が各フェーズのドキュメントに与える影響を確認する
2. **影響があるドキュメントをすべて更新する**: 上流から順に (要件定義 → 外部設計 → 内部設計) 更新する
3. **`docs/CHANGELOG.md` に記録する**: 変更の背景・変更内容・影響確認結果を記載する (テンプレート → [docs-format.md](docs-format.md))
4. **ユーザーに確認する**: 更新内容と CHANGELOG への記録をユーザーに提示し、承認を得る
5. **承認後に実装を変更する**

設計ドキュメントと実装が乖離した状態を放置しない。  
CHANGELOG への記録を省略しない。
