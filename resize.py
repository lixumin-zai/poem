# python3.7
# -*- coding: utf-8 -*-
# @Author : listen
# @Time   :
import copy
import os
import re
from math import ceil
from PIL import Image

import cv2
import numpy as np

from process_sql import Poem

def img_resize(image):
    height, width = image.shape[0], image.shape[1]
    # 设置新的图片分辨率框架
    width_new = 200
    height_new = 200
    # 判断图片的长宽比率
    if width / height >= width_new / height_new:
        img_new = cv2.resize(image, (width_new, int(height * width_new / width)), cv2.INTER_LINEAR)
    else:
        img_new = cv2.resize(image, (int(width * height_new / height), height_new), cv2.INTER_LINEAR)
    return img_new

def findContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # FIND ALL CONTOURS
    return contours, hierarchy

def center(image):
    """
        200
    :param image:
    :return:
    """
    print(image.shape)
    x, y = (200, 200)
    center_x, center_y = 100, 100
    new_image = np.zeros((x, y))
    if image.shape[0] < image.shape[1]:  # y < x
        new_image[center_y - ceil(image.shape[0]/2): center_y + int(image.shape[0]/2), 0:200] = image
    else:
        new_image[0:200, center_x - ceil(image.shape[1] / 2): center_x + int(image.shape[1] / 2)] = image
    return new_image

def contours_area(cnt):
    # 计算countour的面积
    (x, y, w, h) = cv2.boundingRect(cnt)
    return w * h

def adjust(img = cv2.imread("../2.jpg")):
    # 平滑

    img = cv2.GaussianBlur(img, (3, 3), 1)
    # 灰度处理
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    # 二值化
    thr, threshold_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("sadf", threshold_img)
    cv2.waitKey(0)
    # threshold_img = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, (9,9), iterations=20)

    # 找轮廓
    contours, hierarchy = findContours(threshold_img)
    # 从原图抠图 背景为黑
    # 获取面积最大的contour
    # max_cnt = max(contours, key=lambda cnt: contours_area(cnt))
    # 创建空白画布
    mask = np.zeros_like(threshold_img)
    # img = cv2.drawContours(mask, [cnt for cnt in contours], -1, 255, -1)
    contour = []
    for cont in contours:
        contour.extend(cont)
    min_rect = cv2.minAreaRect(np.array(contour))
    box = cv2.boxPoints(min_rect)
    box = np.int0(box)
    test = copy.deepcopy(gray_img)
    box2 = cv2.drawContours(test, [box], 0, 255, -1)


    thr, box2 = cv2.threshold(box2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours2, hierarchy2 = findContours(box2)
    # imgs = cv2.drawContours(box2, [cnt for cnt in contours2], -1, 255, -1)

    x, y, w, h = cv2.boundingRect(contours2[0])
    # 外接矩形
    mask_img = threshold_img[y:y + h, x:x + w]

    # 滤波光滑轮廓
    blur_img = cv2.medianBlur(mask_img, 1)

    # 统一文字大小
    resize_img = img_resize(blur_img)

    # 膨胀
    # dilate = cv2.dilate(resize_img, (3, 3), 1)

    # 再进行平滑轮廓
    # b, new_threshold_img = cv2.threshold(resize_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # new_blur_img = cv2.GaussianBlur(resize_img, (3, 3), 3)
    # result_img = cv2.medianBlur(dilate, 1)

    # 统一图片大小
    image = center(resize_img)

    return image


def imread(path):
    image = Image.open(path)
    image = image.convert("RGB")  # 图片转为RGB格式
    image = np.array(image)[:, :, ::-1]
    return image


def create_special_img():
    """
    空白，
    :return:
    """
    image = imread("./resize_char_img/一.jpg")
    image = np.zeros_like(image)
    image = Image.fromarray(np.uint8(image))
    image.save("./resize_char_img/"+"_.jpg")



def adjust_char():
    """
    调整图片
    :return:
    """
    for char_path in os.listdir("./char_img"):
        print(char_path)
        char_name = re.findall("[\u4e00-\u9fa5]+", char_path)
        image = imread("./char_img/" + char_path)
        # print(image)
        image = Image.fromarray(np.uint8(adjust2(image)))
        image.save("./adjust2_char/"+char_name[0]+".jpg")


def char_rename():
    """
    改名字
    :return:
    """
    for char_path in os.listdir("./char_img"):
        char_name = re.findall("[\u4e00-\u9fa5_]+", char_path)
        os.rename("./char_img/" + char_path, "./char_img/" + char_name[0] + ".jpg")

def resize_org_char():
    for char_path in os.listdir("./char_img"):
        image = imread("./char_img/" + char_path)
        height, width = image.shape[0], image.shape[1]
        # 设置新的图片分辨率框架
        width_new = 128
        height_new = 150
        img_new = cv2.resize(image, (width_new, height_new), cv2.INTER_LINEAR)
        img_new = Image.fromarray(np.uint8(img_new))

        char_name = re.findall("[\u4e00-\u9fa5_]+", char_path)
        img_new.save("./resize_char_img/" + char_name[0] + ".jpg")

def stitch(images: list, i):
    """
    合成图片, i为几言诗词
    :param images:
    :return:
    """
    img = list()
    row_images = list()
    clu_images = list()
    # 读图片
    for image in images:
        img.append(imread(image))
    # print(img)
    # 横向拼接
    img_out = img[0]
    for idx, image_in in enumerate(img[1:]):
        if (idx + 1) % i == 0:
            continue
        img_out = np.concatenate((img_out, image_in), axis=1)
        if (idx + 2) % i == 0:
            row_images.append(img_out)
            # cv2.imshow("sdf", img_out)
            # cv2.waitKey(0)
            try:
                img_out = img[idx + 2]
            except:
                pass

    # 纵向拼接
    img_out = row_images[0]

    for row_image in row_images[1:]:
        img_out = np.concatenate((img_out, row_image), axis=0)
    # cv2.imshow("sdf", img_out)
    # cv2.waitKey(0)


    return img_out

def get_all_char():
    with open("char.txt", "a", encoding="utf-8") as f:
        for char in os.listdir("./char_img"):
            char_name = re.findall("[\u4e00-\u9fa5_]+", char)
            f.write(char_name[0])



def poem_to_img():
    """
    txt 文件, 5言诗，7言诗记得区分
    :return:
    """
    with open("5yan.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open("char.txt", "r", encoding="utf-8") as char:
        chars = char.read()
    id = 0
    poem_title = ""
    poem_text = ""
    next_poem = True
    for line in lines:
        if line == "\n":
            id += 1
            next_poem = True
            images = []

            # for title_char in poem_title:
            #     if title_char in chars:
            #         images.append("./adjust_char/"+title_char+".jpg")
            #     else:
            #         images.append("./adjust_char/" + "_.jpg")
            # while len(images) != 5:
            #     images.append("./adjust_char/" + "_.jpg")

            poem_text_chars = "".join(re.split(r'[，。？\n]', poem_text))
            for text_char in poem_text_chars:
                if text_char in chars:
                    # print()
                    images.append("./resize_char_img/" + text_char + ".jpg")
                else:
                    images.append("./resize_char_img/" + "_.jpg")

            img_out = stitch(images, 5)
            image = Image.fromarray(np.uint8(img_out))
            save_path = "./poem_image/"+re.findall("[\u4e00-\u9fa5_]+", poem_title)[0]+".jpg"
            if os.path.exists(save_path):
                save_path = "./poem_image/" + re.findall("[\u4e00-\u9fa5_]+", poem_title)[0] + "2.jpg"
            image.save(save_path)
            # poem = Poem(id, save_path, re.findall("[\u4e00-\u9fa5_]+", poem_title)[0], poem_text)
            # poem.insert()
            # poem.close()
            print(poem_title)
            print(poem_text)
            poem_title = ""
            poem_text = ""
            continue
        if next_poem:
            poem_title = line
            next_poem = False
        else:
            poem_text = poem_text + line
        # input()


def adjust2(img=cv2.imread("../2.jpg")):

    # 颜色空间转换 BGR转为HLS
    hlsImg = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    # cv2.imshow("lightness and", hlsImg)
    # cv2.waitKey(0)
    # 滑动条最大值
    MAX_VALUE = 200
    # 滑动条最小值
    MIN_VALUE = 0


    # 调整饱和度和亮度
    # 复制原图
    hlsCopy = np.copy(hlsImg)
    # 得到 lightness 和 saturation 的值
    lightness = -100
    saturation = 100
    # 1.调整亮度（线性变换)
    hlsCopy[:, :, 1] = (1.0 + lightness / float(MAX_VALUE)) * hlsCopy[:, :, 1]
    # hlsCopy[:, :, 1][hlsCopy[:, :, 1] > 1] = 1
    # 饱和度
    hlsCopy[:, :, 2] = (1.0 + saturation / float(100)) * hlsCopy[:, :, 2]
    # hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)
    # print(lsImg)
    # 显示调整后的效果
    # cv2.imshow("lightness and", lsImg)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    # print(gray_img)
    # cv2.imshow("lightness and", gray_img)
    # cv2.waitKey(0)
    _, threshold_img = cv2.threshold(gray_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    threshold_img = cv2.morphologyEx(threshold_img, cv2.MORPH_OPEN, (2, 2), iterations=1)
    cv2.imshow("lightness and", threshold_img)
    cv2.waitKey(0)
    # 平滑


    # 统一文字大小
    resize_img = img_resize(threshold_img)

    # 膨胀
    # dilate = cv2.dilate(resize_img, (3, 3), 1)

    # 再进行平滑轮廓
    # b, new_threshold_img = cv2.threshold(resize_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # new_blur_img = cv2.GaussianBlur(resize_img, (3, 3), 3)
    # result_img = cv2.medianBlur(dilate, 1)

    # 统一图片大小
    image = center(resize_img)
    cv2.imshow("lightness and", image)
    cv2.waitKey(0)
    return image

    # print(lines)

if __name__ == "__main__":
    adjust2()
    # create_special_img()
    # poem_to_img()
    # poem_to_img()
    # get_all_char()
    # adjust_char()
    # stitch(["./resize_char_img/一.jpg",
    #         "./resize_char_img/一.jpg",
    #         "./resize_char_img/一.jpg",
    #         "./resize_char_img/一.jpg",
    #         "./resize_char_img/_.jpg",
    #         "./resize_char_img/丁.jpg",
    #         "./resize_char_img/不.jpg",
    #         "./resize_char_img/于.jpg",
    #         "./resize_char_img/中.jpg",
    #         "./resize_char_img/我.jpg"], 5)
    pass

# adjust()


