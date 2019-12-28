from flask import Flask, request, abort
import os
import base64

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, FlexSendMessage #ImageMessageを追加

import face_pp as f  # face_pp.py
import payload as payload_data


app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def hello_world():
   return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
   # get X-Line-Signature header value
#    print(request.headers['X-Line-Signature'])
   signature = request.headers['X-Line-Signature']

   # get request body as text
   body = request.get_data(as_text=True)
   app.logger.info("Request body: " + body)

   # handle webhook body
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)

   return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# # テキストの場合はオウム返し
# def handle_message(event):
#    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
   sample_data = FlexSendMessage.new_from_json_dict(payload_data.payload)
   push_img_id = event.message.id # 投稿された画像IDを取得
   message_content = line_bot_api.get_message_content(push_img_id) # LINEサーバー上に自動保存された画像を取得
   push_img = b""
   for chunk in message_content.iter_content():
       push_img += chunk #画像をiter_contentでpush_imgに順次代入
   print(push_img)
   push_img = base64.b64encode(push_img) # APIに通すためbase64エンコード
   msg = f.search_image(push_img)
   line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=msg),sample_data])

if __name__ == "__main__":
   #    app.run()
   port = int(os.getenv("PORT"))
   app.run(host="0.0.0.0", port=port)
