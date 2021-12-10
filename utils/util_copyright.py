s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
import os
import glob
import shutil
import datetime
import unidecode
import pandas as pd


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


def remove_all_accents(input_str: str):
    input_str = unidecode.unidecode(input_str)
    s = u''
    input_str = input_str
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    s = s.replace(" ", "").replace("|", "").replace("-", "_").replace("--", "_").replace("&", "_").replace("@",
                                                                                                           "").replace(
        "[", "").replace("'", "").replace("]", "").replace("|", " ").lower()
    return s


def remove_accents(input_str: str):
    input_str = unidecode.unidecode(input_str)
    s = u''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s.lower().replace(' ', '')


def is_need_to_save_server(arr, itemcheck='Voice'):
    for item in arr:
        if itemcheck == 'Voice':
            if (item['type'] in ['Fake', 'Voice']) and item['accuracy'] >= 0:
                return True
        if itemcheck == 'Tune':
            if (item['type'] in ['Fake', 'Beat', 'Tune']) and item['accuracy'] >= 0:
                return True
    return False


def check_predict_audio_done(file_video):
    basename = os.path.basename(file_video)
    metadata = 'tmp/' + os.path.splitext(basename)[0] + '.txt'
    return os.path.exists(metadata)


def markdone(dir_video):
    # move file original to done directory
    # dir_video is output_download_sep
    dir_video_done = dir_video.replace('output_download_sep', 'output_download_doneaudio')
    dir_video_origin = dir_video.replace('output_download_sep', 'output_download_ana')
    try:
        os.makedirs(dir_video_done)
    except:
        print("")

    try:
        shutil.move(dir_video_origin + '.mp4', dir_video_done + '.mp4')
    except:
        # print('Exception when move dir ', dir_video_origin + '.mp4')
        print("")

    try:
        shutil.move(dir_video_origin + '.mp3', dir_video_done + '.mp3')
    except:
        print("")
    clean_up(dir_video)


def clean_up(dir_video):
    print('Clearning up for directory ' + dir_video)
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(dir_video + '/*.wav')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


if __name__ == '__main__':
    text = "Buông tay"

    print(remove_accents(text))
