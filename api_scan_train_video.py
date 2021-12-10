import os
import pathlib
import time
import logging
import requests
import urllib.parse
import pandas as pd

from Check_copyright_video.trainer import train_model
from pyVideoProcess import extract_videos_to_npy

from utils.util_copyright import remove_accents, write_to_log, remove_all_accents
from utils.util_updatedStatus import get_list_song


def update_status_training(video_name, accuracy, status):
    headers = {'content-type': 'application/json'}
    params = {'title': video_name, 'accuracy': accuracy, 'status': str(status), 'type': 'video'}
    url = 'http://183.81.35.24:5010/api/model/update_accuracy?code=' + str(
        remove_accents(video_name)) + '&accuracy=' + accuracy + '&status=' + str(status) + '&type=video'
    print(url)
    req = requests.get(url, params=params, headers=headers)
    write_to_log("====>Call to " + url, "ScanVideoTrain")
    write_to_log("=========>Param is " + str(params), "ScanVideoTrain")
    write_to_log("================>" + req.text + ',status=' + str(req.status_code), "ScanVideoTrain")


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
    path_raw_data = "/hddai2020/ai/copyright/data/training/HA/"
    saved_data = "/hddai2020/ai/copyright/data/training_video_dataset/"
    saved_weights = "/hddai2020/ai/copyright/data/training_video_dataset/weights/"

    file_other = "/hddai2020/ai/copyright/data/training_video_dataset/Other/npy/Other.npy"

    # process file Other:
    folder_videos = "/hddai2020/ai/copyright/data/training_video_dataset/Other/videos/"
    folder_img = "/hddai2020/ai/copyright/data/training_video_dataset/Other/images/"
    path_npy = "/hddai2020/ai/copyright/data/training_video_dataset/Other/npy/Other.npy"
    extract_videos_to_npy(folder_videos, folder_img, path_npy)

    while True:
        for song_id, song_name in get_list_song():
            try:
                new_song_name = f"{song_id}_{remove_all_accents(song_name)}"

                path_npy = saved_data + "/npy/{}.npy".format(new_song_name)
                folder_img = saved_data + "/True/{}/".format(new_song_name)

                song_path = os.path.join(path_raw_data, new_song_name, "All")  # mp4
                print(song_path)
                if not os.path.exists(song_path):
                    continue

                true_song = list(pathlib.Path(song_path).glob("*.mp4"))[0]

                extract_videos_to_npy(true_song, folder_img, path_npy)
                update_status_training(song_name, "0", 1)

                file_weight = saved_weights + f"{new_song_name}.5h"

                accuracy = train_model(file_other, path_npy, file_weight)
                update_status_training(song_name, str(accuracy), 2)

            except Exception as e:
                print(e)
                update_status_training(song_name, str(e), 3)

        time.sleep(60)
