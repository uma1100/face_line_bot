# -*- coding: utf-8 -*-
import requests
import base64
import glob
import time

API_KEY = 'dmsZI8tMsBoceJI3hx_nPN6qy6hvM6Oq'
API_SECRET = 'RyrwmZXueUjmBv79W1SlI61M3v9CqUU1'
FACESET_TOKENS = ['790e55c1290041abc8ce16a07fa33f82','a0305f1f27eea076fe060c6b5215ae51']
ATTRIBUTES = 'gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus'
FACE_LIST = {'hirano':'平野綾','kanna':'橋本環奈','yonezu':'米津玄師','suda':'菅田将暉','ashida':"芦田愛菜",'nakayama':"なかやまきんに君",'zako':"ハリウッドザコシショウ"}

def get_face_type(user_id):
    return FACE_LIST.get(user_id)

def get_emo_type(emotion):
    if emotion == 'surprise':
        return '驚いている😲'
    elif emotion == 'anger':
        return '怒っている👿'
    elif emotion == 'disgust':
        return '嫌な顔をしています😅'
    elif emotion == 'fear':
        return '恐れています😨'
    elif emotion == 'happiness':
        return '幸せが溢れています😘'
    elif emotion == 'neutral':
        return '自然体です😁'
    elif emotion == 'sadness':
        return '悲しんでいます😂'
    else:
        return '読み取れませんでした。'

def face_detect(image):
   url = "https://api-us.faceplusplus.com/facepp/v3/detect"
   config = {'api_key':API_KEY,     # API Key
          'api_secret':API_SECRET,      # API Secret
          'image_base64':image,      # 画像データ
          'return_landmark':1,          # landmark設定
		  'return_attributes':ATTRIBUTES
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
           msg += "偏差値: {}\n".format(int(f["beauty"]))
       msg = msg.rstrip()
       if not msg:
           msg = "画像から顔データを検出できませんでした。"
       return msg
   except:
       return "サーバーの接続に失敗したか画像を正しく認識できませんでした。"

def detect_image(img):
    endpoint = 'https://api-us.faceplusplus.com'
    response = requests.post(
        endpoint + '/facepp/v3/detect',
        {
            'api_key': API_KEY,
            'api_secret': API_SECRET,
            'image_base64': img,
            'return_attributes':ATTRIBUTES
        }
    )
    # 1秒スリープ
    time.sleep(1)
    # レスポンスのステータスコードが200以外の場合
    if response.status_code != 200:
        print('[Error] ')
        return -1
    resources = response.json()
    return resources

# 顔を識別するAPI
def search_image(img):
    try:
        endpoint = 'https://api-us.faceplusplus.com'
        # img_base64 = base64.b64encode(img)
        # 顔検出APIにリクエストを送る
        faces=detect_image(img)
        face_list = []
        for face in faces["faces"]:
            faces_data = {}
            if "attributes" in face:
                faces_data["gender"] = face["attributes"]["gender"]["value"]
                faces_data["age"] = face["attributes"]["age"]["value"]
                # 人種を取得したい場合は以下の記述を追加する
                # faces_data["ethnicity"] = face["attributes"]["ethnicity"]["value"]
                # faces_data["ethnicity"] = faces_data["ethnicity"].replace("ASIAN", "アジア人").replace("WHITE", "白人").replace("BLACK", "黒人")
            if faces_data["gender"] == "Male":
                faces_data["beauty"] = face["attributes"]["beauty"]["male_score"]
                faces_data["gender"] = "男性"
            else:
                faces_data["beauty"] = face["attributes"]["beauty"]["female_score"]
                faces_data["gender"] = "女性"
            faces_data["x_axis"] = face["face_rectangle"]["left"] # 並び替え用に画像上の顔のX座標の位置を代入
            faces_data["emotion"] = get_emo_type(max(face['attributes']['emotion'], key=face['attributes']['emotion'].get))

            # 類似度検索
            similar_data = {}
            for FACESET_TOKEN in FACESET_TOKENS:
                response = requests.post(
                    endpoint + '/facepp/v3/search',
                    {
                        'api_key': API_KEY,
                        'api_secret': API_SECRET,
                        'face_token': str(face["face_token"]),
                        'faceset_token': FACESET_TOKEN,
                        'return_result_count': 1,
                    }
                )
                # 1秒スリープ
                time.sleep(1)
                # レスポンスのステータスコードが200以外の場合
                if response.status_code != 200:
                    return -1
                similar_data_json = response.json()
                similar_data[similar_data_json['results'][0]['user_id']] = similar_data_json['results'][0]['confidence']

            # print(similar_data)
            faces_data['confidence'] = max(similar_data.values())
            faces_data['similar'] = get_face_type(max(similar_data, key=similar_data.get))
            face_list.append(faces_data)
        face_list = sorted(face_list, key=lambda x:x["x_axis"]) # 左から順に並び変える
        msg = "左から"
        for i, f in enumerate(face_list, 1):
            msg += "{}人目の情報\n".format(i)
            # msg += "X軸の位置:{} \n".format(face["x_axis"]) デバッグ用
            msg += "性別: {}\n".format(f["gender"])
            msg += "年齢: {}歳\n".format(f["age"])
            # 人種を取得したい場合は以下の記述を追加する
            # msg += "人種: {}\n".format(f["ethnicity"])
            msg += "偏差値: {}\n".format(int(f["beauty"]))
            msg += "感情： {}\n".format(f["emotion"])
            if not f['similar'] == -1:
                msg += "{}に{}%似ています\n\n".format(f['similar'],round(f["confidence"],1))
            else:
                msg += "似ている有名人を発見することができませんでした。\n\n"
        msg = msg.rstrip()
        if not msg:
            msg = "画像から顔データを検出できませんでした。"
        return msg
    except Exception as e:
        print(e)
        return "サーバーの接続に失敗したか画像を正しく認識できませんでした。"


# 比較する顔画像を登録
def create_faceset(face_list,tags):
    id_list = []
    for (img_path,face_id) in zip(face_list,tags):
        img_file = base64.encodebytes(open(img_path, 'rb').read())
        resources = detect_image(img_file)
        set_userid(resources["faces"][0]["face_token"],face_id)
        id_list.append(resources["faces"][0]["face_token"])

    id_list=str(id_list).replace("'", "")
    id_list=str(id_list).replace("[", "")
    id_list=str(id_list).replace("]", "")
    id_list=str(id_list).replace(" ", "")

    # print(resources)
    print(id_list)

    endpoint = 'https://api-us.faceplusplus.com'
    try:
        response = requests.post(
            endpoint + '/facepp/v3/faceset/create',
            {
                'api_key': API_KEY,
                'api_secret': API_SECRET,
                'display_name': 'facebank',
                'face_tokens': id_list,
            }
        )
        # 1秒スリープ
        time.sleep(1)
        # レスポンスのステータスコードが200以外の場合
        if response.status_code != 200:
            return -1
        resources = response.json()
        print(resources)
        return resources
    except Exception as e:
        print(e)
        return -1

def set_userid(face_token,user):
    endpoint = 'https://api-us.faceplusplus.com'
    try:
        response = requests.post(
            endpoint + '/facepp/v3/face/setuserid',
            {
                'api_key': API_KEY,
                'api_secret': API_SECRET,
                'display_name': 'facebank',
                'face_token':face_token,
                'user_id':user,
        }
        )
        # 1秒スリープ
        time.sleep(1)
        # レスポンスのステータスコードが200以外の場合
        if response.status_code != 200:
            return -1
        resources = response.json()
        print(resources)
        return resources
    except Exception as e:
        print(e)
        return -1


# ----- test code -----

if __name__ == '__main__':
    # 識別したい画像を取得
    f = open('./test_data/test3.jpg', 'rb') 
    img = f.read()
    f.close() 
    img = base64.b64encode(img)
    # img=cv2.imread('./input/'+filename)
    
    # --- 顔検出 ---
    # 識別するAPIにリクエストを送る
    resources = search_image(img)
    print('-----------')
    print(resources)


    # --- 顔登録 ---
    # フォルダ内の画像を取得
    # face_list = glob.glob('./facebank/*')
    # face_list.sort()
    # # 各名前(user_id)登録
    # tags = [str(face_path).split("/")[2].split(".")[0] for face_path in face_list]

    # face_set = create_faceset(face_list,tags)