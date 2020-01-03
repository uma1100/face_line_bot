import requests
import base64
import glob
import time

API_KEY = 'dmsZI8tMsBoceJI3hx_nPN6qy6hvM6Oq'
API_SECRET = 'RyrwmZXueUjmBv79W1SlI61M3v9CqUU1'

def detect_image(img):
    endpoint = 'https://api-us.faceplusplus.com'
    response = requests.post(
        endpoint + '/facepp/v3/detect',
        {
            'api_key': API_KEY,
            'api_secret': API_SECRET,
            'image_base64': img,
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
    # print(face_list)

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
        # print(resources)
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
        return resources
    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    # フォルダ内の画像を取得
    face_list = glob.glob('./facebank2/*')
    face_list.sort()
    # 各名前(user_id)登録
    tags = [str(face_path).split("/")[2].split(".")[0] for face_path in face_list]
    print(face_list)
    face_set = create_faceset(face_list,tags)
    print(face_set['faceset_token'])