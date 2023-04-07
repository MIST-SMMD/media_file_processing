# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: media_file_processing
# @FileName: frame.py
# @Author：hz157
# @DateTime: 05/04/2023 下午9:55

import cv2
import os
import uuid
import numpy as np
from datetime import datetime


def _is_frame_stable(prev_frame, curr_frame):
    """
    图片稳定判断 (光流) 稳定帧 
    Args:
        prev_frame (_type_): 前一帧
        curr_frame (_type_): 当前帧

    Returns:
        _type_: boolean 是否稳定
    """
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    
    # calculate optical flow
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    
    # calculate average flow magnitude
    magnitude = cv2.magnitude(flow[..., 0], flow[..., 1])
    avg_magnitude = cv2.mean(magnitude)[0]
    
    # if the average flow magnitude is below a threshold, the frame is considered stable
    if avg_magnitude < 1.0:
        return True
    else:
        return False

def clip(origin, mediaPath):
    """
    视频转图片 逐帧 
    Args:
        mid (_type_): 文章id mid
        mediaPath (_type_): 视频文件位置

    Returns:
        _type_: 图片路径列表
    """
    start = datetime.now()
    # 打开视频文件
    cap = cv2.VideoCapture(mediaPath)

    # 设置视频帧的高度和宽度
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # 创建一个 VideoWriter 对象，用于保存导出的图片
    out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'MJPG'), 10, (frame_width, frame_height))
    files = []
    frame = previous_frame = None

    # 读取视频中的每一帧
    while True:
        f1 = datetime.now()
        if frame is not None:
            previous_frame = frame
        ret, frame = cap.read()
        if not ret:
            break

        # 检查图像是否稳定
        # 如果图像稳定，导出当前帧并保存到输出视频文件
        if previous_frame is not None:
            if _is_frame_stable(previous_frame, frame):
                out.write(frame)
                uuidCode = uuid.uuid1()
                root = f'frame/{origin}/Social_Media_Data'
                if os.path.exists(root) == False:
                    os.makedirs(root)
                print(root)
                cv2.imwrite(root + '/' + str(uuidCode) + '.jpg', frame)
                files.append(f'{uuidCode}.jpg')
                print(f'单帧处理时间：{str(datetime.now() - f1)}')

    # 关闭视频文件和输出视频文件
    cap.release()
    out.release()

    end = datetime.now()
    print(f'总耗时: {str(end - start)}')
    return files


def delete_similar_images(folder_path, threshold):
    """
    删除相近的图片
    Args:
        folder_path (_type_): _description_
        threshold (_type_): _description_
    """
    image_files = os.listdir(folder_path)
    for i in range(len(image_files)):
        if os.path.exists(os.path.join(folder_path, image_files[i])):
            image1 = cv2.imread(os.path.join(folder_path, image_files[i]))
            for j in range(i+1, len(image_files)):
                if os.path.exists(os.path.join(folder_path, image_files[j])):
                    image2 = cv2.imread(os.path.join(folder_path, image_files[j]))                
                    if image1 is not None and image2 is not None:
                        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
                        hist1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
                        hist2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])
                        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                        if similarity > threshold:
                            print(f"Similarity between {image_files[i]} and {image_files[j]}: {similarity}")
                            # 删除其中一张图片
                            os.remove(os.path.join(folder_path, image_files[j]))
