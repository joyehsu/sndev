import os
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

app = Flask(__name__)

line_bot_api = LineBotApi('BFMC0iRRy8nUBSxWIKcC5lvCsY/YbkEVPkM+b38AdpiHw+u77Sbx9iL1aM0PjLEaEpaD72+ZPgFSX3l6piz5ckXZuj6YtsGaqpmTqt1zg1AclA13FSH1UPaI8f1ndMVT/erSRlhcUIU+UoTPVCZ1jgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('71969d090a955791cf670b01aef61414')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print('signature: ', signature)

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    #app.run()
    port = int(os.environ.get('PORT', 5000))     
    app.run(host='0.0.0.0', port=port)
