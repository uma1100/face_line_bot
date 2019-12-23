import requests
import base64

API_KEY = 'dmsZI8tMsBoceJI3hx_nPN6qy6hvM6Oq'
API_SECRET = 'RyrwmZXueUjmBv79W1SlI61M3v9CqUU1'
def face_detect(image):
   url = "https://api-us.faceplusplus.com/facepp/v3/detect"
   config = {'api_key':API_KEY,     # API Key
          'api_secret':API_SECRET,      # API Secret
          'image_base64':image,      # 画像データ
          'return_landmark':1,          # landmark設定
		  'return_attributes':'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus'# 特徴分析
} 
   try:
       r = requests.post(url, data=config)
       r = r.json()
       face_list = []
       for face in r["faces"]:
           faces = {}
           if "attributes" in face:
               faces["gender"] = face["attributes"]["gender"]["value"]
               faces["age"] = face["attributes"]["age"]["value"]
               # 人種を取得したい場合は以下の記述を追加する
               # faces["ethnicity"] = face["attributes"]["ethnicity"]["value"]
               # faces["ethnicity"] = faces["ethnicity"].replace("ASIAN", "アジア人").replace("WHITE", "白人").replace("BLACK", "黒人")
               if faces["gender"] == "Male":
                   faces["beauty"] = face["attributes"]["beauty"]["male_score"]
                   faces["gender"] = "男性"
               else:
                   faces["beauty"] = face["attributes"]["beauty"]["female_score"]
                   faces["gender"] = "女性"
               faces["x_axis"] = face["face_rectangle"]["left"] # 並び替え用に画像上の顔のX座標の位置を代入
               face_list.append(faces)
       face_list = sorted(face_list, key=lambda x:x["x_axis"]) # 左から順に並び変える
       msg = ""
       for i, f in enumerate(face_list, 1):
           msg += "{}人目の情報\n".format(i)
           # msg += "X軸の位置:{} \n".format(face["x_axis"]) デバッグ用
           msg += "性別: {}\n".format(f["gender"])
           msg += "年齢: {}歳\n".format(f["age"])
           # 人種を取得したい場合は以下の記述を追加する
           # msg += "人種: {}\n".format(f["ethnicity"])
           msg += "偏差値: {}\n\n".format(int(f["beauty"]))
       msg = msg.rstrip()
       if not msg:
           msg = "画像から顔データを検出できませんでした。"
       return msg
   except:
       import traceback
       traceback.print_exc()
       return "サーバーの接続に失敗したか画像を正しく認識できませんでした。"
