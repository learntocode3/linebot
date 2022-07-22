from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
from model.settings import SECRET_KEY, CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, NGROK_URL
from model import db
from scraper import Ifoodie

ngrok_url = NGROK_URL
app = Flask(__name__)
app.secret_key=SECRET_KEY
botDB = db.linebotDB()

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent)
def handle_message(event):
    UserId = event.source.user_id
    messageType = event.message.type

    if messageType == "image":
        botDB.set_userId_imageId(UserId, event.message.id)

        SendImage = line_bot_api.get_message_content(event.message.id)
        path = './static/' + event.message.id + '.png'
        with open(path, 'wb') as fd:
            for chenk in SendImage.iter_content():
                fd.write(chenk)


    if messageType == "text":
        if event.message.text == "wwwww":
            imgId = botDB.get_user(UserId)
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = ngrok_url + "/static/" + imgId + ".png", preview_image_url = ngrok_url + "/static/" + imgId + ".png"))

    # if botDB.get_user(UserId) == "No User":
    #     botDB.set_userId_imageId(UserId)
    # else:
    #     print("YIYIYI")
    
    print('使用者id:',UserId)
    
    if messageType == "text":
        if event.message.text in ['restaurant', 'Restaurant', '餐廳推薦', '推薦餐廳']:
            recommend_res = Ifoodie()
            reply = recommend_res.scrape()    
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
