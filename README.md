# line_weather_bot

使用方式:

1. 用QRcode或Line ID: @azn7645q 加bot好友

2. 之後即可告知bot地名來詢問天氣，例如: 臺南市天氣如何?

3. 若文字中沒有"天氣"與地名的關鍵字，則判斷不是詢問天氣，單純echo


程式作法:

1. 依照http://lee-w-blog.logdown.com/ 申請line bot，教學使用django做出可以echo的bot

2. 然後根據Heroku教學將程式碼傳到Heroku伺服器上，同時要到heroku的設定那邊設定環境變數

3. 架設過程中遇到
	(i) at=error code=H14 desc="No web processes running"錯誤，在cmd輸入heroku ps:scale web=1
	(ii) collectstatic的問題，在cmd輸入heroku config:set DISABLE_COLLECTSTATIC=1
	
4. 天氣回答的部分是寫在views.py裡，作法是從氣象局網頁抓取html，並用BeatifulSoup來parse資料

5. 根據使用者輸入的內容尋找關鍵字並回傳天氣資訊

Github: https://github.com/KT-Yeh/line_weather_bot/tree/master

heroku server: https://dashboard.heroku.com/apps/linebot201714
