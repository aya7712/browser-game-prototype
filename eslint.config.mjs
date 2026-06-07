// @ts-check
import tseslint from 'typescript-eslint';

/**
 * 重点 lint 設定（flat config）。
 *
 * 目的: src/components のコンポーネントで「静的なインラインスタイル」を禁止する。
 *   静的スタイルは Xxx.module.css に書く。実行時に JS で計算される値が必要な場合のみ、
 *   該当行に `// eslint-disable-next-line no-restricted-syntax` を付けて意図を明示する。
 *
 * 詳細ルール → .claude/rules/css.md「インラインスタイル (style={{}}) の禁止」
 *
 * 注: eslint:recommended / typescript-eslint recommended などの広域ルールは
 *     既存コードに大量の指摘を出すため、ここでは意図的に有効化していない。
 *     広域 lint の整備は別途行う。
 */
export default tseslint.config(
    { ignores: ['dist', 'storybook-static'] },
    {
        files: ['src/components/**/*.tsx'],
        ignores: ['**/*.stories.tsx'],
        languageOptions: {
            parser: tseslint.parser,
            parserOptions: { ecmaFeatures: { jsx: true } },
        },
        rules: {
            'no-restricted-syntax': ['error', {
                selector: "JSXAttribute[name.name='style']",
                message: '静的スタイルは CSS Modules (Xxx.module.css) に書く。実行時計算値が必要な場合のみ // eslint-disable-next-line no-restricted-syntax で明示する。',
            }],
        },
    },
);
