from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

import urllib.request
from bs4 import BeautifulSoup
url = 'http://www.cwb.gov.tw/V7/forecast/f_index.htm'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "html.parser")


cityDic = { '基隆市': 'Keelung_City', '臺北市': 'Taipei_City', '新北市': 'New_Taipei_City',
			'桃園市': 'Taoyuan_City', '新竹市': 'Hsinchu_City', '新竹縣': 'Hsinchu_County',
			'苗栗縣': 'Miaoli_County', '臺中市': 'Taichung_City', '彰化縣': 'Changhua_County',
			'南投縣': 'Nantou_County', '雲林縣': 'Yunlin_County', '嘉義市': 'Chiayi_City',
			'宜蘭縣': 'Yilan_County', '花蓮縣': 'Hualien_County', '臺東縣': 'Taitung_County',
			'臺南市': 'Tainan_City', '高雄市': 'Kaohsiung_City', '屏東縣': 'Pingtung_County',
			'連江縣': 'Lienchiang_County', '金門縣': 'Kinmen_County', '澎湖縣': 'Penghu_County'}

def parseStr(text):
	for i in range(len(text)-1):
		keyword = text[i:i+2]
		if keyword[0] == "台": keyword[0] = "臺"
		if (keyword+"市") in cityDic:
			return lookup(keyword+"市")
		if (keyword+"縣") in cityDic:
			return lookup(keyword+"縣")
	for i in range(len(text)-2):
		keyword = text[i:i+3]
		if keyword[0] == "台": keyword[0] = "臺"
		if keyword in cityDic:
			return lookup(keyword)

def lookup(key):
	for a_tag in soup.find_all('a'):
		if cityDic[key] in a_tag.get('href'):
			for img_tag in a_tag.find_all('img'):
				if "symbol/weather" in img_tag.get('src'):
						return key+img_tag.get('alt')

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    line_bot_api.reply_message(
                        event.reply_token,
						TextSendMessage(text=parseStr(event.message.text))
                    )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()