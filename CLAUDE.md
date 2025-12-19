# lawkit-python

Python/pip向けのlawkitバインディング。Rustのlawkit-coreをPyO3でラップ。

## アーキテクチャ

```
lawkit-core (crates.io 2.5)   ←  Rustネイティブライブラリ
      ↓
lawkit-python (this)          ←  PyO3でPythonバインディング
      ↓
pip package                   ←  maturinでwheelを生成
```

## 構造

```
lawkit-python/
├── src/lib.rs              # PyO3バインディング実装
├── src/lawkit_python/      # Pythonモジュール
│   └── __init__.py         # re-export + ユーティリティ関数
├── Cargo.toml              # lawkit-core依存（crates.io版）
├── pyproject.toml          # maturin設定 + pytest設定
├── tests/                  # pytestテスト
│   └── test_law.py
└── .github/workflows/
    ├── ci.yml              # push/PR → fmt + clippy + build + test
    └── release.yml         # タグ → マルチプラットフォームビルド + Release作成
```

## ビルド

```bash
# 開発環境セットアップ
uv sync --all-extras

# pre-commitフックをインストール
uv run pre-commit install

# ビルド（開発モード）
uv run maturin develop

# テスト
uv run pytest

# Rustフォーマット＆lint
cargo fmt --check
cargo clippy

# 手動でpre-commitを実行
uv run pre-commit run --all-files
```

## GitHub Actions

| ワークフロー | トリガー | 動作 |
|-------------|---------|------|
| ci.yml | push/PR to main | fmt + clippy + Linux x64ビルド + テスト |
| release.yml | タグ v* | マルチプラットフォームビルド + GitHub Release作成 |

### ビルドターゲット（release.yml）

- x86_64-unknown-linux-gnu
- x86_64-unknown-linux-musl
- aarch64-unknown-linux-gnu
- x86_64-apple-darwin
- aarch64-apple-darwin
- x86_64-pc-windows-msvc

## リリース手順

1. `pyproject.toml`、`Cargo.toml`、`src/lib.rs`のバージョンを更新
2. コミット & プッシュ
3. `git tag v2.5.16 && git push origin v2.5.16`
4. GitHub Actionsがビルド → Release作成 → wheelを添付
5. `pip install lawkit-python`（PyPIから）または wheelから直接インストール

## API

### law(subcommand, data, **kwargs)
統計法則分析を実行。

サブコマンド:
- `benford` - ベンフォードの法則分析
- `pareto` - パレート分析
- `zipf` - ジップの法則分析
- `normal` - 正規分布分析
- `poisson` - ポアソン分布分析
- `validate` - データ検証

オプション（kwargs）:
- `confidence_level` - 信頼水準
- `risk_threshold` - リスク閾値 ("low", "medium", "high")

### ユーティリティ
- `law_from_file(file_path, subcommand, **kwargs)` - ファイルからデータを読み込んで分析

## 開発ルール

- lawkit-coreはcrates.ioの公開版を使用（ローカルパス依存禁止）
- コミット前にcargo fmtが自動実行される（pre-commit）
- バージョンは3箇所を同期: pyproject.toml, Cargo.toml, src/lib.rs
