import os
import numpy as np
from pyVideoProcess import extract_video_to_img
from train import build_model
from datetime import timedelta
from util_copyright import remove_accents


def predict_video(video_test, video_true):
    rename = remove_accents(video_true)
    model = build_model()
    model.load_weights("weight/"+rename+".h5")
    folder_img = os.path.join("img/Test", rename)
    folder_videos = os.path.join("video/Test", video_test)
    path_npy = "npy/{}.npy".format(rename)

    extract_video_to_img(folder_videos, folder_img, path_npy)

    data_test = np.load(path_npy)
    predict = model.predict(data_test)
    print(len(predict))

    result = {
        "warn": {},
        "max": []
    }
    max_value = 0
    for i in range(0, len(predict) - 45, 15):
        time_start = i
        time_end = i + 30
        window = predict[i:i + 30]
        averange = np.average(window)
        if max_value < averange:
            max_value = averange
        key = f"{timedelta(seconds=int(time_start))}>{timedelta(seconds=int(time_end))}"
        result["warn"][key] = str(averange)  # {'0:00:45 -> 0:01:00': '0:00:45 -> 0:01:00'}

        result["max"] = max_value

        print(result)


#if __name__ == '__main__':
    #predict_video(..........)


