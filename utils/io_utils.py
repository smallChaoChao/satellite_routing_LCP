#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 21:14
# @Author  : smallChaoChao
# @File    : io_utils.py
import json
import logging
import os

from utils.config import LCP_RES_PATH


def write_dict2json(data: dict, dir_path: str, file_name: str):
    """向文件中写json"""
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    with open(f'{dir_path}/{file_name}.json', 'w') as f:
        f.write(json_str)


def list_dir(path: str) -> list:
    """返回文件夹中的文件名 并且去除隐藏文件"""
    res = []
    file_names = os.listdir(path=path)
    for file_name in file_names:
        if file_name == '.DS_Store':
            continue
        res.append(file_name)
    return res

