import os
import math
import cv2
from keras import Model
from keras.applications.inception_v3 import preprocess_input, InceptionV3
from tensorflow.python.keras.preprocessing import image
import numpy as np
from util_copyright import remove_accents


def extract_video_to_img(folder_videos, folder_img):
    count = 1
    for video in os.listdir(folder_videos):
        path_video = os.path.join(folder_videos, video)

        try:
            os.makedirs(folder_img)
        except:
            print('----')
        video = cv2.VideoCapture(path_video)
        print(video.isOpened())
        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        total_image = int(frame_count // frame_rate)
        print(total_image)
        # pbar = tqdm(enumerate(range(total_image - 1)))
        while True:
            try:
                os.makedirs(folder_img + "/video_" + str(int(count)))
                break
            except:
                print('----video_{} exist----'.format(int(count)))
                count += 1
        while video.isOpened():
            frameId = video.get(1)
            success, image = video.read()
            if success != True:
                break
            if frameId % math.floor(frame_rate) == 0 and frameId <= frame_count:
                image = cv2.resize(image, (299, 299), interpolation=cv2.INTER_AREA)
                filename = folder_img + "/video_" + str(int(count)) + "/image_" + str(
                    int(frameId / math.floor(frame_rate))) + ".jpg"
                print("Saved image into:", filename)
                cv2.imwrite(filename, image)
        video.release()
        print('done')
        count += 1


def model_get_feature():
    base_model = InceptionV3(input_shape=(299, 299, 3), weights='imagenet', include_top=True)
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
    return model


def extract_img_to_tensor(folder_img):
    list_features = []

    for small_folder in os.listdir(folder_img):
        path_small_folder = os.path.join(folder_img, small_folder)

        for img in os.listdir(path_small_folder):
            path_img = os.path.join(path_small_folder, img)
            x = image.load_img(path_img)
            x = image.img_to_array(x)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            features = model_get_feature.predict(x)[0]

            list_features.append(features)

    return list_features


def extract_videos_to_npy(folder_videos, folder_img, path_npy):
    extract_video_to_img(folder_videos, folder_img)
    list_features = extract_img_to_tensor(folder_img)

    if os.path.exists(path_npy):
        os.remove(path_npy)

    np.save(path_npy, list_features)


model_get_feature = model_get_feature()


if __name__ == "__main__":
    # process file Other:
    folder_videos = "video/Other"
    folder_img = "img/Other"
    path_npy = "npy/Other.npy"
    extract_videos_to_npy(folder_videos, folder_img, path_npy)

    # process file True:
    for name in os.listdir("video/True"):
        rename = remove_accents(name)
        folder_videos = os.path.join("video/True", name)
        folder_img = os.path.join("img/True", rename)
        path_npy = "npy/{}.npy".format(rename)
        extract_videos_to_npy(folder_videos, folder_img, path_npy)
