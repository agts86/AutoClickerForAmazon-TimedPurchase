from TimeUtiltys import TimeUtiltys 
from datetime import datetime
from playwright.sync_api import Page
from time import sleep
from sys import exit

#Amazonの画面操作を行なうクラス
class OperateAmazon():
    #ログイン処理
    #page : Playwrightのページオブジェクト
    #login : ログインID
    #password : ログインパスワード
    #headless : ヘッドレスモードかどうか
    def Login(page:Page,login:str,password:str,headless:str):
        
        try:
            certification = False
            page.goto("https://www.amazon.co.jp/")
            
            # アカウント&リストをクリック
            page.click("#nav-link-accountList")
            
            # メールアドレス入力
            page.fill('input[name="email"]', login)
            page.click("#continue")
            
            # パスワード入力
            page.fill('input[name="password"]', password)
            page.check('input[name="rememberMe"]')
            page.click("#signInSubmit")

            #ログインできてトップ画面にアカウント名が表示されているか確認
            account_element = page.locator("#nav-link-accountList-nav-line-1")
            if account_element.count() > 0:
                account_name = account_element.text_content()
                print("アカウント名:" + account_name[:-2])
            else:
                #リクエストエラー
                if page.locator("#auth-error-message-box").count() > 0:
                    raise Exception()
                #認証エラー
                else:
                    certification = True
                    raise Exception()
                           
            print(datetime.now())
            print("ログイン出来ました。")
        except Exception as e:
            print("ログインできませんでした。")
            if headless == "n":
                print("購入処理実行時刻前までに手動でやり直してください。")
            else:
                if certification :
                     while True:  
                        print("Amazonから認証メールが届いてますか？")
                        certificationMail= input("*y/n>")
                        if certificationMail == "y" or certificationMail == "n":
                            break
                        else:
                            print("yかnを入力してください")

                     if certificationMail == "y":
                        print("購入時刻までに認証処理を済ませておいてください。")
                     else:
                        while True:
                            finish = input("Enterキーを押して、最初からやり直してください。")
                            if not finish:
                                exit()
                else:
                    while True:
                        finish = input("Enterキーを押して、最初からやり直してください。")
                        if not finish:
                            exit()                      
            

    #購入処理
    #page : Playwrightのページオブジェクト
    #purchaseGoodsUrl : 購入商品のURL
    #checkColor : 指定されたカラー情報
    #checkSize : 指定されたサイズ情報
    #quantity : 指定された個数
    def Purchase(page:Page,purchaseGoodsUrl:str,checkColor:str,checkSize:str,quantity:str):

        try:
            TimeUtiltys.MakeSleep(0.88)

            page.goto(purchaseGoodsUrl)

            # カラー指定がある場合
            if checkColor != "":
                color_button = page.locator(f"#color_name_{checkColor} button")
                color_dropdown = page.locator("#native_dropdown_selected_color_name")
                
                if color_button.count() > 0:
                    color_button.click()
                elif color_dropdown.count() > 0:
                    color_dropdown.select_option(index=int(checkColor))
                else:
                    print("[error]カラーが存在しないか選択できませんでした。")
                    return

            # サイズ指定がある場合
            if checkSize != "":
                size_dropdown = page.locator("#native_dropdown_selected_size_name")
                size_button = page.locator(f"#size_name_{checkSize} button")
                
                if size_dropdown.count() > 0:
                    size_dropdown.select_option(index=int(checkSize))
                elif size_button.count() > 0:
                    size_button.click()
                else:
                    print("[error]サイズが存在しないか選択できませんでした。")
                    return

            # 購入数指定がある場合
            if quantity != "":
                quantity_dropdown = page.locator("#quantity")
                if quantity_dropdown.count() > 0:
                    quantity_dropdown.select_option(value=quantity)
                else:
                    print("[error]個数選択ができませんでした。")
                    return

            # 通常の注文か定期おとく便の選択が出てきたら通常の注文を選択する
            accordion = page.locator("#newAccordionRow .a-accordion-row-a11y")
            if accordion.count() > 0:
                accordion.click()
            
            # 今すぐ買うボタンをクリック
            buy_now_button = page.locator("#buy-now-button")
            if buy_now_button.count() > 0:
                buy_now_button.click()
            else:
                print("[error]「今すぐ買う」ボタンが存在しないか押せません。")
                return
        
            
            # iframeになった場合とそうでない場合を処理
            try:
                # iframeの処理を試行
                iframe = page.frame("turbo-checkout-iframe")
                if iframe:
                    iframe.click("#turbo-checkout-pyo-button")
                    OperateAmazon.SuccessProsess(page)
                    return
            except:
                pass
            
            # 通常の注文確定ボタンを試行
            place_order_button = page.locator('input[name="placeYourOrder1"]')
            if place_order_button.count() > 0:
                place_order_button.click()
                OperateAmazon.SuccessProsess(page)
            else:
                print("[error]購入失敗")
                return                  
        
        except Exception as e:
            print("[error]存在しないページか対応していないページです。あるいは何らかの不具合が発生してます")
            print(f"エラー詳細: {e}")

    #購入成功時の処理
    #page : Playwrightのページオブジェクト
    def SuccessProsess(page:Page):
        print(datetime.now())
        print("[success]購入成功")
        sleep(5)
        

