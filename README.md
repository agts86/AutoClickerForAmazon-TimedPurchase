＃AutoClickerForAmazon
アマゾンで自動購入するツールです。
ログインIDとログインpasswordと購入したい商品のURLと購入時刻を入力して
指定された時刻にSeleniumによる自動操作で購入させます。
対応ページは指定時刻に「今すぐ購入」ボタンが押せるページのみになります。
「注文内容を確認・変更する」画面で「注文を確定する」ボタンが表示されることが条件になります。

2021/08/15
衣類のサイズやカラー選択ができるようになりました。
全ページの購入個数の指定ができるようになりました。

2021/09/01
全商品のサイズやカラー選択ができるようになりました。
iconを設定しました。
パスワードの非表示化
電話番号でのログインが可能になりました。

2021/09/22
低スペック用に各処理にリトライ機能を追加
webdriver-managerを追加

## uv を使ったセットアップ手順

このプロジェクトは Python パッケージ管理に [uv](https://github.com/astral-sh/uv) を利用できます。

### 1. uv のインストール
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"   # あるいは新しいシェルを開く
```

### 2. 依存関係の同期
```bash
cd AutoClickerForAmazon-TimedPurchase
uv sync
```
初回同期で `.venv` 仮想環境が生成されます。`tkinter` はシステムパッケージなので別途:
```bash
sudo apt install -y python3-tk
```

### 3. Playwrightブラウザのインストール
```bash
uv run playwright install chromium
```

### 3.1 日本語フォントのインストール（文字化け対策）
```bash
sudo apt install -y fonts-noto-cjk fonts-noto-cjk-extra language-pack-ja
sudo fc-cache -fv
```

### 4. 実行
```bash
uv run python main.py
```

### 5. インポート確認(任意)
Bash の履歴展開(!)を避けるため、Python ワンライナーはシングルクォートで囲みます。
```bash
uv run python -c 'import tkinter, stdiomask, playwright; print("All imports successful!")'
```
もし `!` を含む文字列でエラーになる場合は `set +H` を一時的に実行すると履歴展開を無効化できます。

### 使用ライブラリ
- playwright : ブラウザ操作（Chrome/Chromiumを自動管理）
- ntplib : NTP サーバ時刻取得
- stdiomask : パスワード入力非表示
- tkinter (python3-tk) : GUI ダイアログ表示

### Git管理について
- `.venv/` (仮想環境) は `.gitignore` で除外済みです。
- `uv.lock` はコミットして依存関係のバージョンを固定することを推奨します。
- `pyproject.toml` も依存関係定義なのでコミット対象です。

### 注意事項
- Playwrightが自動でブラウザを管理するため、Chrome のインストールは不要です。
- 処理前にカートを空にし、決済方法を一つに統一してください。
- 高速版(ヘッドレス)は初回はオフにして挙動確認を推奨します。

