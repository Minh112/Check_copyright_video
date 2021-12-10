import json
import os
import requests
import urllib.parse
import pandas as pd
import datetime
from utils.util_copyright import *


def check_Status(local):
    res = requests.get(local)
    if res.status_code == 404:
        return False
    else:
        return True


def write_to_log(content, file='ScanAudioTrain'):
    try:
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


def get_list_song():
    list_films = {"id": [],
                  "title": []}
    data_json = pd.read_json("http://183.81.35.24:5010/api/film_video/list_train", encoding="utf-8")
    for item in data_json["data"]:
        list_films["id"].append(item["id"])
        list_films["title"].append(item["title"])
    return list_films


def update_video_model_status(video_title, accuracy, status):
    headers = {'content-type': 'application/json'}
    url = 'http://183.81.35.24:5010/api/model/update_accuracy?code=' + str(
        remove_accents(video_title)) + '&accuracy=' + accuracy + '&status=' + str(status) + '&type=audio'
    params = {'title': video_title, 'accuracy': accuracy, 'status': str(status), 'type': 'audio'}
    req = requests.get(url, params=params, headers=headers)
    write_to_log("====>Call to " + url)
    write_to_log("=========>Param is " + str(params))
    write_to_log("================>" + req.text + ',status=' + str(req.status_code))


def get_ownership(song):
    url = 'http://183.81.35.24:5010/api/ownership/list_by_title?title=' + urllib.parse.quote_plus(song)
    write_to_log('======>call to ' + url, "GetOwnerShip")
    json = pd.read_json(url, encoding='utf-8')
    write_to_log('=============>result of json  is: ' + str(json), "GetOwnerShip")
    array = []
    for item in json['data']:
        array.append(item['ownership_title'])
    return array


def updatedStatus2Server(id_violate, song_title, status):
    url = "http://183.81.35.24:5010/api/link_download/update_status_song_title?id_violate=" + str(
        id_violate) + "&song_title=" + str(song_title) + "&status=" + str(status)

    # response = requests.post(url)
    # write_to_log(f"[INFO]: ======>call to {url} ==>> response: {response}", "Post2Server")
    # return response


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
    # req = requests.post(url=url, data=params)
    # write_to_log("====>Call to " + url, "Post2Server")
    # write_to_log("=========>Param is " + str(params), "Post2Server")
    # write_to_log("================>" + req.text + ',status=' + str(req.status_code), "Post2Server")


def updatedPrediction(id_violate, accuracy, timestamp, warning, ownership, film_title, isview):
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


def updateStatusDownload(id_violate, film_id, artist_id, local, status, tmp, LOGGER=None):
    url = "http://183.81.35.24:5010/api/link_download/update_status_local"
    data = {'id_violate': str(id_violate), 'film_id': film_id, 'artist_id': artist_id, 'status': status,
            'local': local, 'tmp': tmp}
    response = requests.post(url, data=data)
    json_data = json.loads(response.text)
    if json_data['result'] > 0:
        if LOGGER is not None:
            LOGGER.info(f"[UPDATED]: SUCCESS with URL: '{url}' -- DATA '{data}'")
        else:
            print("[UPDATE success] Update link download status success")
    else:
        if LOGGER is not None:
            LOGGER.info(f"[UPDATED]: FAIL with URL: '{url}' -- DATA '{data}'")
        else:
            print("[UPDATE fail] Update link download status fail")


def updated_status_for_test_form(id_violate, type_status, status, ownership):
    url_update = "http://183.81.35.24:5010/api/test_ai/update_status"
    data = {"file": id_violate, "type_status": type_status, "status": status, "ownership": ownership}
    response = requests.post(url_update, data=data)
    if str(response.status_code) == "200":
        print(f"+) [{type_status}] [INFO] : STATUS SUCCESS  {status}   | [{ownership}]")
    else:
        print(f"+) [{type_status}] [INFO] : STATUS FAIL     {status}   | [{ownership}]")


if __name__ == '__main__':
    print(get_parameters("Từ khi gặp em"))
