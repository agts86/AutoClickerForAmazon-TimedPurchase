#!/bin/bash
# Amazon自動購入ツール - 起動スクリプト

set -e  # エラー時に終了

# 色付き出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Amazon自動購入ツール - 起動中...${NC}"

# uvのパスを設定
export PATH="$HOME/.local/bin:$PATH"

# uvが利用可能かチェック
if ! command -v uv &> /dev/null; then
    echo -e "${RED}エラー: uv がインストールされていません${NC}"
    echo "以下のコマンドでインストールしてください:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# プロジェクトディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${YELLOW}プロジェクトディレクトリ: $SCRIPT_DIR${NC}"

# 仮想環境と依存関係の同期
echo -e "${YELLOW}依存関係を同期中...${NC}"
if ! uv sync; then
    echo -e "${RED}エラー: 依存関係の同期に失敗しました${NC}"
    echo "手動で 'uv sync' を実行して問題を確認してください"
    exit 1
fi

# Chromeの存在確認
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo -e "${YELLOW}警告: Google Chrome が見つかりません${NC}"
    echo "Chromeをインストールすることを推奨します:"
    echo "sudo apt update && sudo apt install -y google-chrome-stable"
    echo ""
    echo "続行しますか？ (y/N)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "起動をキャンセルしました"
        exit 0
    fi
fi

# メインプログラム実行
echo -e "${GREEN}Amazon自動購入ツールを開始します...${NC}"
echo ""

uv run python main.py

echo ""
echo -e "${BLUE}プログラムが終了しました${NC}"