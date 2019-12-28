payload = {
  "type": "flex",
  "altText": "Flex Message",
  "contents": {
    "type": "bubble",
    "direction": "ltr",
    "header": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "ちなみにJOYは？",
          "align": "center"
        }
      ]
    },
    "hero": {
      "type": "image",
      "url": "https://grick.jp/artist/img/joy99.jpg",
      "size": "full",
      "aspectRatio": "1.51:1",
      "aspectMode": "fit"
    },
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "顔面偏差値 80 です！",
          "align": "center"
        }
      ]
    },
    "footer": {
      "type": "box",
      "layout": "horizontal",
      "contents": [
        {
          "type": "button",
          "action": {
            "type": "uri",
            "label": "作成者の情報",
            "uri": "https://www.mozzz.work/"
          }
        }
      ]
    }
  }
}