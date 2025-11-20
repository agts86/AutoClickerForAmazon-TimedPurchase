#!/usr/bin/env python3
"""
文字化けテスト用スクリプト - Playwrightで日本語表示確認
"""

from playwright.sync_api import sync_playwright
import sys

def test_japanese_display():
    """日本語表示のテスト"""
    print("=== Playwright 日本語表示テスト ===")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,  # 表示確認のため非ヘッドレス
                args=[
                    '--lang=ja-JP',
                    '--no-first-run',
                    '--disable-blink-features=AutomationControlled',
                    '--font-render-hinting=none',
                    '--disable-font-subpixel-positioning',
                    '--force-device-scale-factor=1'
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='ja-JP',
                timezone_id='Asia/Tokyo',
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                extra_http_headers={
                    'Accept-Language': 'ja-JP,ja;q=0.9,en;q=0.8',
                    'Accept-Charset': 'utf-8'
                }
            )
            
            page = context.new_page()
            
            # 日本語エンコーディング確保
            page.add_init_script("""
                Object.defineProperty(navigator, 'language', {
                    get: function() { return 'ja-JP'; }
                });
                Object.defineProperty(navigator, 'languages', {
                    get: function() { return ['ja-JP', 'ja', 'en']; }
                });
            """)
            
            print("Amazon.co.jp にアクセス中...")
            page.goto("https://www.amazon.co.jp/")
            
            # ページタイトルを取得
            title = page.title()
            print(f"ページタイトル: {title}")
            
            # 日本語テキストが含まれているか確認
            if "Amazon" in title:
                print("✅ Amazon.co.jp への接続成功")
                
                # 検索ボックスのプレースホルダーテキストを確認
                search_input = page.locator("#twotabsearchtextbox")
                if search_input.count() > 0:
                    placeholder = search_input.get_attribute("placeholder")
                    print(f"検索ボックスのプレースホルダー: {placeholder}")
                    
                    if placeholder and any(ord(c) > 127 for c in placeholder):
                        print("✅ 日本語文字が正常に表示されています")
                    else:
                        print("⚠️ 日本語文字が表示されていない可能性があります")
                
                print("\n5秒間ブラウザを表示して確認してください...")
                page.wait_for_timeout(5000)
                
            else:
                print("❌ Amazon.co.jp への接続に問題があります")
            
            browser.close()
            return True
            
    except Exception as e:
        print(f"❌ テスト中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    if test_japanese_display():
        print("\n✅ 日本語表示テストが完了しました")
    else:
        print("\n❌ 日本語表示テストに失敗しました")
        sys.exit(1)