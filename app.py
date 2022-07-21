from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from model.settings import SECRET_KEY, CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET
from model import db
from scraper import Ifoodie

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text # what user sends to me
    
    if msg in ['restaurant', 'Restaurant', '餐廳推薦', '推薦餐廳']:
        recommend_res = Ifoodie('台中市')
        reply = recommend_res.scrape()    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
