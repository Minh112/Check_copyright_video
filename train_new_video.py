import os

from get_api_start_training import post_to_server_model
from pyVideoProcess import extract_videos_to_npy
from train import train_model
from util_copyright import remove_accents


if __name__ == '__main__':
    for video in os.listdir("video/True"):
        name = remove_accents(video)
        if not os.path.exists("img/True/"+name):
            path_npy = "npy/" + name + ".npy"
            folder_img = "img/True/"+name
            folder_videos = "video/True/"+video

            extract_videos_to_npy(folder_videos, folder_img, path_npy)
            # Báo lên server:
            post_to_server_model(name, "0", 1)

            file_weight = "weight/" + name + ".h5"
            file_other = "npy/Other.npy"
            accuracy = train_model(file_other, path_npy, file_weight)
            print(accuracy)
            # Báo lên server:
            post_to_server_model(name, str(accuracy), 2)


