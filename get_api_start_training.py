import os
import urllib.parse
import pandas as pd
from sphinx.util import requests

from util_copyright import remove_accents, write_to_log


def post_to_server_model(video_name, accuracy, status):
    headers = {'content-type': 'application/json'}
    params = {'title': video_name, 'accuracy': accuracy, 'status': str(status), 'type': 'video'}
    url = 'http://183.81.35.24:5010/api/model/update_accuracy?code=' + str(
        remove_accents(video_name)) + '&accuracy=' + accuracy + '&status=' + str(status) + '&type=video'
    print(url)
    req = requests.get(url, params=params, headers=headers)
    # write_to_log("====>Call to " + url, "ScanVideoTrain")
    # write_to_log("=========>Param is " + str(params), "ScanVideoTrain")
    # write_to_log("================>" + req.text + ',status=' + str(req.status_code), "ScanVideoTrain")


def get_list_song():
    list_films = []
    data_json = pd.read_json("http://183.81.35.24:5010/api/film_video/list_train", encoding="utf-8")
    for item in data_json["data"]:
        list_films.append(item["title"])
    return list_films


def get_ownership(song):
    url = 'http://183.81.35.24:5010/api/ownership/list_by_title?title=' + urllib.parse.quote_plus(song)
    write_to_log('======>call to ' + url, "GetOwnerShip")
    json = pd.read_json(url, encoding='utf-8')
    write_to_log('=============>result of json  is: ' + str(json), "GetOwnerShip")
    array = []
    for item in json['data']:
        array.append(item['ownership_title'])
    return array




if __name__ == '__main__':
    HOME = os.getcwd()
    path_raw_data = "Video_data\\True"
    for song in get_list_song():
        print(os.path.join(HOME, path_raw_data, song))
        dir_song = os.path.join(HOME, path_raw_data, song)
        post_to_server_model(song, "0", 1)
