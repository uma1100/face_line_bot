import requests
import base64
import json

API_KEY = 'dmsZI8tMsBoceJI3hx_nPN6qy6hvM6Oq'
API_SECRET = 'RyrwmZXueUjmBv79W1SlI61M3v9CqUU1'

# 画像ファイルをbase64バイナリ形式で読み出します
# file_pathは画像ファイル（jpgなど）
f = open('./joy.jpg','wb')

image = base64.encodebytes(f.read())

config = {
            'api_key':API_KEY,     # API Key
            'api_secret':API_SECRET,      # API Secret
            'image_base64':image,      # 画像データ
            'return_landmark':1,          # landmark設定
            'return_attributes':'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus'# 特徴分析
        }        
# リクエストURLの設定  
url = 'https://api-us.faceplusplus.com/facepp/v3/detect'

    
# POSTリクエスト
res = requests.post(url, data=config)
data = json.loads(res.text)

print(data)
