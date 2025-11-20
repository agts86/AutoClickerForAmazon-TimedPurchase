#!/usr/bin/env python3
"""
デバッグ用スクリプト - Amazon自動購入ツールの動作確認とトラブルシューティング
"""

import sys
import os
from datetime import datetime
import traceback

def check_imports():
    """必要なライブラリのインポートをチェック"""
    print("=== ライブラリインポートチェック ===")
    
    imports_to_check = [
        ("tkinter", "GUI ダイアログ表示"),
        ("stdiomask", "パスワード入力非表示"),
        ("playwright.sync_api", "ブラウザ操作"),
        ("ntplib", "NTP サーバ時刻取得"),
        ("re", "正規表現"),
    ]
    
    results = {}
    
    for module_name, description in imports_to_check:
        try:
            if module_name == "webdriver_manager.chrome":
                from webdriver_manager.chrome import ChromeDriverManager
            else:
                __import__(module_name)
            print(f"✅ {module_name:20} - {description}")
            results[module_name] = True
        except ImportError as e:
            print(f"❌ {module_name:20} - {description} (エラー: {e})")
            results[module_name] = False
        except Exception as e:
            print(f"⚠️  {module_name:20} - {description} (警告: {e})")
            results[module_name] = "warning"
    
    return results

def check_local_modules():
    """ローカルモジュールのインポートをチェック"""
    print("\n=== ローカルモジュールチェック ===")
    
    local_modules = [
        "OperateAmazon",
        "NTPClient", 
        "TimeUtiltys",
        "CheckUtiltys"
    ]
    
    results = {}
    
    for module_name in local_modules:
        try:
            module = __import__(module_name)
            print(f"✅ {module_name:15} - インポート成功")
            
            # クラスが存在するかチェック
            if hasattr(module, module_name):
                cls = getattr(module, module_name)
                print(f"   └── クラス {module_name} が見つかりました")
                results[module_name] = True
            else:
                print(f"   └── 警告: クラス {module_name} が見つかりません")
                results[module_name] = "no_class"
                
        except ImportError as e:
            print(f"❌ {module_name:15} - インポートエラー: {e}")
            results[module_name] = False
        except Exception as e:
            print(f"⚠️  {module_name:15} - その他のエラー: {e}")
            results[module_name] = "error"
    
    return results

def check_playwright_availability():
    """Playwright ブラウザの利用可能性をチェック"""
    print("\n=== Playwright ブラウザ チェック ===")
    
    try:
        from playwright.sync_api import sync_playwright
        
        print("Playwright ブラウザ起動テスト中...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # 簡単なページにアクセステスト
            page.goto("https://www.google.com")
            title = page.title()
            print(f"✅ ページタイトル取得成功: {title}")
            
            browser.close()
        
        print("✅ Playwright は正常に動作しています")
        return True
        
    except Exception as e:
        print(f"❌ Playwright エラー: {e}")
        print("   解決策:")
        print("   - playwright install chromium を実行してください")
        print("   - または uv run playwright install chromium")
        return False

def check_ntp_connection():
    """NTP サーバへの接続をチェック"""
    print("\n=== NTP 接続チェック ===")
    
    try:
        import ntplib
        
        ntp_servers = [
            "ntp.nict.jp",
            "pool.ntp.org", 
            "time.google.com"
        ]
        
        for server in ntp_servers:
            try:
                client = ntplib.NTPClient()
                response = client.request(server, version=3)
                ntp_time = datetime.fromtimestamp(response.tx_time)
                print(f"✅ {server:15} - 時刻: {ntp_time}")
                return True
            except Exception as e:
                print(f"❌ {server:15} - エラー: {e}")
        
        print("⚠️  すべてのNTPサーバで接続に失敗しました")
        return False
        
    except ImportError:
        print("❌ ntplib がインストールされていません")
        return False

def check_validation_functions():
    """バリデーション関数をテスト"""
    print("\n=== バリデーション関数テスト ===")
    
    try:
        from CheckUtiltys import CheckUtiltys
        
        # テストケース
        test_cases = [
            ("メールアドレス", CheckUtiltys.CheckMailAddress, [
                ("test@example.com", True),
                ("invalid-email", False),
                ("user.name+tag@domain.co.jp", True)
            ]),
            ("電話番号", CheckUtiltys.CheckPhoneNumber, [
                ("090-1234-5678", True),
                ("09012345678", True),
                ("invalid-phone", False)
            ]),
            ("URL", lambda url: CheckUtiltys.CheckURL(url, "www.amazon.co.jp"), [
                ("https://www.amazon.co.jp/dp/B0123456", True),
                ("http://www.amazon.co.jp/product", True),
                ("https://www.google.com", False)
            ])
        ]
        
        all_passed = True
        
        for test_name, func, cases in test_cases:
            print(f"\n{test_name}テスト:")
            for test_input, expected in cases:
                try:
                    result = bool(func(test_input))
                    status = "✅" if result == expected else "❌"
                    print(f"  {status} '{test_input}' -> {result} (期待値: {expected})")
                    if result != expected:
                        all_passed = False
                except Exception as e:
                    print(f"  ❌ '{test_input}' -> エラー: {e}")
                    all_passed = False
        
        return all_passed
        
    except ImportError as e:
        print(f"❌ CheckUtiltys インポートエラー: {e}")
        return False

def environment_info():
    """環境情報を表示"""
    print("\n=== 環境情報 ===")
    print(f"Python バージョン: {sys.version}")
    print(f"Python パス: {sys.executable}")
    print(f"現在のディレクトリ: {os.getcwd()}")
    print(f"実行時刻: {datetime.now()}")
    
    # 仮想環境チェック
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ 仮想環境内で実行中")
        if 'VIRTUAL_ENV' in os.environ:
            print(f"   環境パス: {os.environ['VIRTUAL_ENV']}")
    else:
        print("⚠️  システムPythonで実行中（仮想環境推奨）")

def main():
    """デバッグメイン関数"""
    print("Amazon 自動購入ツール - デバッグ診断")
    print("=" * 50)
    
    # 環境情報
    environment_info()
    
    # 各種チェック実行
    results = {}
    
    try:
        results['imports'] = check_imports()
        results['local_modules'] = check_local_modules()
        results['validation'] = check_validation_functions()
        results['playwright'] = check_playwright_availability()
        results['ntp'] = check_ntp_connection()
        
        # 結果サマリー
        print("\n" + "=" * 50)
        print("=== 診断結果サマリー ===")
        
        issues = []
        
        if not all(results['imports'].values()):
            issues.append("一部ライブラリのインポートに失敗")
        
        if not all(v == True for v in results['local_modules'].values()):
            issues.append("ローカルモジュールに問題")
            
        if not results.get('playwright', False):
            issues.append("Playwrightブラウザに問題")
            
        if not results.get('ntp', False):
            issues.append("NTP接続に問題")
            
        if not results.get('validation', False):
            issues.append("バリデーション関数に問題")
        
        if not issues:
            print("✅ すべてのチェックが正常に完了しました")
            print("   メインプログラム (main.py) を実行できます")
        else:
            print("⚠️  以下の問題が見つかりました:")
            for issue in issues:
                print(f"   - {issue}")
            
        print("\n修正後は再度このスクリプトを実行して確認してください:")
        print("uv run python debug.py")
        
    except Exception as e:
        print(f"\n❌ 診断中に予期しないエラーが発生しました:")
        print(f"エラー: {e}")
        print("\nスタックトレース:")
        traceback.print_exc()

if __name__ == "__main__":
    main()