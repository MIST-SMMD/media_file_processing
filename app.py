# Copyright (c) 2023.
# !/usr/bin/python
# -*- coding: UTF-8 -*-
# @Project: media_file_processing
# @FileName: app.py
# @Author：hz157
# @DateTime: 05/04/2023 下午9:55
import os
import frame

video_path = r'mist/video'
current_directory = os.getcwd()

def main():
    files = []
    for fileInfo in os.walk(video_path):
        files.append(fileInfo)

    for file in files:
        for item in file[2]:
            # 判断是不是mp4文件
            if item[-4:] == '.mp4':
                path = os.path.join(current_directory, video_path, item)
                if os.path.exists(path):
                    frames = frame.clip(str(i[0]).split('\\')[1], path)
                    if frames:
                        for i in frames:
                            path = os.path.join(current_directory, "new_test", i, "Social_Media_Data")
                            frame.delete_similar_images(path, 0.9)

if __name__ == '__main__':
    main()


