import json
import os

import requests
import urllib.parse
import pandas as pd
import datetime


def trymkdir(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except Exception as e:
            print("")


def write_to_log(content, file='ScanAudioTrain'):
    try:
        # print(content)
        trymkdir("../logs")

        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y%m%d")
        date_time_str_ms = now.strftime("%Y%m%d%H%M%S")
        content = date_time_str_ms + ":" + content + "\n"
        file_smil = "logs/" + "log_" + file + "_" + date_time_str + ".txt"
        file1 = open(file_smil, "a+", encoding="utf-8")  # write mode
        file1.writelines(content)
        file1.close()
    except Exception as e:
        print(e)


def updatedStatus2Server(id_violate, song_title, status):
    url = "http://183.81.35.24:5010/api/link_download/update_status_song_title?id_violate=" + str(
        id_violate) + "&song_title=" + str(song_title) + "&status=" + str(status)

    response = requests.post(url)
    write_to_log(f"[INFO]: ======>call to {url} ==>> response: {response}", "Post2Server")
    return response


def GMM_updatedPrediction(id_violate, accuracy, timestamp, warning, ownership, score, film_title, isview):
    # headers = {'content-type': 'application/json'}
    # 'title_violate': None
    url = 'http://183.81.35.24:5010/api/msg_warning/Update'
    params = {
        'id_violate': str(id_violate),
        'accuracy': str(accuracy),
        'timer': str(timestamp),
        'warning': str(warning),
        'ownership': str(ownership),
        'score': str(score),
        'film_title': str(film_title),
        'isview': isview,
        'type': 'warning'}
    req = requests.post(url=url, data=params)
    write_to_log("====>Call to " + url, "Post2Server")
    write_to_log("=========>Param is " + str(params), "Post2Server")
    write_to_log("================>" + req.text + ',status=' + str(req.status_code), "Post2Server")


def updatedPrediction(id_violate, accuracy, timestamp, warning, ownership, film_title, isview, typeScore="default"):
    # headers = {'content-type': 'application/json'}
    # 'title_violate': None
    url = 'http://183.81.35.24:5010/api/msg_warning/Update'
    params = {
        'id_violate': str(id_violate),
        'accuracy': str(accuracy),
        'timer': str(timestamp),
        'warning': str(warning),
        'ownership': str(ownership),
        'film_title': str(film_title),
        'isview': isview,
        'type': 'all'}
    req = requests.post(url=url, data=params)
    write_to_log("====>Call to " + url, "Post2Server")
    write_to_log("=========>Param is " + str(params), "Post2Server")
    write_to_log("================>" + req.text + ',status=' + str(req.status_code), "Post2Server")


def get_parameters(song_name):
    url = "http://banquyen.hamedia.vn/model/get?title=" + song_name
    if requests.get(url).status_code == 200:
        result = requests.get(url).json()
        return result["obj"]["extracter_options"], result["obj"]["standard_time"], result["obj"]["threshold"]


def checkId_violate(id_violate):
    url_ = f"http://183.81.35.24:5010/api/msg_warning/check_review?id_violate={id_violate}&review={1}"
    res = requests.get(url_)
    res = res.json()["result"]
    if int(res) < 0:
        return False
    else:
        return True


def get_copyright_to_check(song):
    url = 'http://183.81.35.24:5010/api/ownership/list_by_title?title=' + urllib.parse.quote_plus(song)
    write_to_log('======>call to ' + url, "GetOwnerShip")
    json = pd.read_json(url, encoding='utf-8')
    write_to_log('=============>result of json  is: ' + str(json), "GetOwnerShip")
    array = []
    for item in json['data']:
        array.append(item['ownership_title'])
    return array


def updateStatusDownload(id_violate, film_id, artist_id, local, status, tmp):
    url = "http://183.81.35.24:5010/api/link_download/update_status_local"
    data = {'id_violate': str(id_violate), 'film_id': film_id, 'artist_id': artist_id, 'status': status,
            'local': local, 'tmp': tmp}
    response = requests.post(url, data=data)
    json_data = json.loads(response.text)
    if json_data['result'] > 0:
        print("[UPDATE success] Update link download status success")
    else:
        print("[UPDATE fail] Update link download status fail")


if __name__ == '__main__':
    print(get_parameters("Từ khi gặp em"))