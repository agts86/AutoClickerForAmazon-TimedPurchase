import stdiomask
from OperateAmazon import OperateAmazon 
from NTPClient import NTPClient
from TimeUtiltys import TimeUtiltys 
from CheckUtiltys import CheckUtiltys
from datetime import datetime,date,timedelta
from playwright.sync_api import sync_playwright
from tkinter import messagebox,Tk
from sys import exit

#Amazonの自動購入プログラム
def main():
    
    Tk().withdraw()
    if not messagebox.askokcancel("確認", "このプログラムはGoogleChromeを使用します。\r\nインストール済みの方は「OK｝を押してください。\r\nまだの方は「キャンセル」を押してください。"):
        return
        
    print("★プログラムの説明★")
    print("・購入予定時刻の2分前に自動でログイン処理を行ない、購入予定時刻に自動で購入するツールです。")
    print("・このツールは購入時刻に「今すぐ買う」ボタンが表示できるページのみ使えます。")
    print("・あらかじめカートの中身は空にしておいてください。")
    print("・あらかじめ購入決済方法は一つにしておいてください。「クレジットカード」を推奨します。")
    print("・各入力項目は入力後に「Enter」キーを押してください。")
    print("・[*]がある入力項目は必須です。ないものは任意で設定してください。")
    print("　")

    while True:  
        print("高速版を使用しますか？")
        print("初回起動は通常版をオススメします。")
        headless= input("*y/n>")
        if headless == "y" or headless == "n":
            break
        else:
            print("yかnを入力してください")

    while True:   
        login = input("*ログインID(半角)>")
        if login != "":
            if CheckUtiltys.CheckMailAddress(login):
                break
            elif CheckUtiltys.CheckPhoneNumber(login):
                break
            else:
                print("ログインIDが不正です。")
        else:
            print("ログインID(半角)は必須です。")
            
    while True:  
        password = stdiomask.getpass("*ログインPassWord(半角)>")
        if password != "":
            if CheckUtiltys.CheckHankakuEisuziKigou(password):
                break
            else:
                print("ログインpasswordが不正です。")
        else:
            print("ログインPassWord(半角)は必須です。")
    
    while True:
        purchaseGoodsUrl = input("*買いたい商品のURL>")
        if purchaseGoodsUrl != "":
            if CheckUtiltys.CheckURL(purchaseGoodsUrl,"www.amazon.co.jp"):
                break
            else:
                print("AmazonのURLを入力してください。")
        else:
            print("買いたい商品のURLは必須です。")

    checkColor = input("カラーを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番左を選択の場合「0」>")
    checkSize = input("サイズを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番上を選択の場合「0」>")
    quantity = input("2つ以上購入する場合は購入個数を入力してください。1つの場合は未入力。>")

    while True:
        try:
            start = datetime.strptime(input("*購入時間(hh:mm)>") + ":00","%H:%M:%S").time()
            before2Minites = datetime.combine(date.today(), start) - timedelta(minutes=2)
            loginTime = datetime.combine(date.today(), before2Minites.time()) #購入予定時刻の2分前
            before1Seconds = datetime.combine(date.today(), start) - timedelta(seconds=1)
            purchaseTime = datetime.combine(date.today(), before1Seconds.time()) #購入予定時刻の1秒前
            break
        except Exception as e:
            print("[error]開始時刻が不正です。もう一度入力してください")
            continue

    print("ログイン処理実行時刻："+str(loginTime))
    print("購入処理実行時刻："+str(purchaseTime))

    ntpClient = NTPClient("ntp.nict.jp")
    
    #ログイン処理実行時刻まで待機
    TimeUtiltys.MakeSleep(TimeUtiltys.FindTheTimeDifference(loginTime,ntpClient))

    # Playwright でブラウザを起動
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=(headless == "y"),
            args=[
                '--lang=ja-JP',
                '--no-first-run',
                '--disable-blink-features=AutomationControlled',
                '--font-render-hinting=none',
                '--disable-font-subpixel-positioning',
                '--force-device-scale-factor=1'
            ]
        )
        
        # シークレットモードでコンテキスト作成
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
        
        # ページタイムアウト設定
        page.set_default_timeout(10000)  # 10秒
        
        # 日本語エンコーディング確保のためのJavaScript実行
        page.add_init_script("""
            Object.defineProperty(navigator, 'language', {
                get: function() { return 'ja-JP'; }
            });
            Object.defineProperty(navigator, 'languages', {
                get: function() { return ['ja-JP', 'ja', 'en']; }
            });
        """)
       
        try:
            #ログイン処理
            OperateAmazon.Login(page,login,password,headless)
            
            #購入処理実行時刻まで待機
            TimeUtiltys.MakeSleep(TimeUtiltys.FindTheTimeDifference(purchaseTime,ntpClient))

            OperateAmazon.Purchase(page,purchaseGoodsUrl,checkColor,checkSize,quantity)
            
        finally:
            # ブラウザを閉じる
            browser.close()

    while True:
        finish = input("終了するにはEnterキーを押してください")
        if not finish:
            break
    exit()

if __name__=='__main__':       
    main()
