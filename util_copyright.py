s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

import datetime
import os


def remove_accents_1(input_str=u""):
    s = ''
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


def remove_accents(input_str=u""):
    input_str = input_str.replace(' ', '')
    s = ''
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s.lower()


def trymkdir(full_dir):
    try:
        os.makedirs(full_dir)
    except:
        print('Exception when making ====>', full_dir)


def write_to_log(content, file=''):
    try:
        print(content)
        now = datetime.datetime.now()
        date_time_str = now.strftime("%Y%m%d")
        date_time_str_ms = now.strftime("%Y%m%d%H%M%S")
        content = date_time_str_ms + ":" + content + "\n"
        file_smil = "logs/" + "log" + file + "_" + date_time_str + ".txt"
        file1 = open(file_smil, "a+", encoding="utf-8")
        file1.writelines(content)
        file1.close()
    except Exception as e:
        print(e)