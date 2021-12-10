import os.path
from typing import List

import numpy as np


class convert:
    def __init__(self, folder_img_in_song: str, save_npy_path: str, save_images: str):
        self.folder_img_in_song = folder_img_in_song
        self.save_npy_path = save_npy_path
        self.save_images = save_images
        self.model_get_feature = model_get_feature()

    def safemkdir(self, dir_):
        try:
            os.makedirs(dir_, exist_ok=True)
        except Exception as e:
            print(e)

    def save_npy(self, features, save_path):
        os.remove(save_path)
        if not os.path.exists(save_path):
            np.save(features)

    def model_get_feature(self):
        base_model = InceptionV3(input_shape=(299, 299, 3), weights='imagenet', include_top=True)
        model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
        return model

    def extract_image_from_video(self, video_path, save_image):
        self.safemkdir(save_image)  # /hddai2020/ai/copyright/data/training_video_dataset/Other/images/

        video_name = remove_accents(os.path.basename(video_path).split(".")[0])

        video = cv2.VideoCapture(video_path)
        frame_rate = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

        while video.isOpened():
            frameId = video.get(1)
            success, image = video.read()
            if success != True:
                break
            if frameId % math.floor(frame_rate) == 0 and frameId <= frame_count:
                image = cv2.resize(image, (299, 299), interpolation=cv2.INTER_AREA)
                filename = save_image + f"{video_name}_{int(frameId / math.floor(frame_rate))}.jpg"
                print("Saved image into:", filename)
                cv2.imwrite(filename, image)
        video.release()
        print("Get images from video is DONE!")

    def extract_img_to_tensor(self, list_path_image_of_song: List) -> List:
        list_features = []
        for song_path in list_path_image_of_song:
            x = image.load_img(song_path)
            x = image.img_to_array(x)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)

            list_features.append(model_get_feature.predict(x)[0])
        return list_features

    def run(self):
        """
        folder_img_in_song: .../Other/
                            .../True/bai1/

        :return:
        """
        # Extract images
        for root, dir_, filenames in os.walk(self.folder_img_in_song):
            for filename in filenames:
                if filename.endswith(".mp4"):
                    song_path = os.path.join(root, filename)
                    self.extract_image_from_video(song_path, self.save_images)

        # Extract tensor
        list_images_of_song = []
        for root, dir_, filenames in os.walk(self.save_images):
            for filename in filenames:
                if filename.endswith(".jpg"):
                    list_images_of_song.remove(filename)

        list_features = self.extract_img_to_tensor(list_images_of_song)
        self.save_npy(list_features, self.save_npy_path)
        return list_features
