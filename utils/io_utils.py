#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/10 21:14
# @Author  : smallChaoChao
# @File    : io_utils.py
import json
import logging

from utils.config import RES_PATH


def write_dict2json(data: dict, file_name: str):
    """向文件中写json"""
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    with open(f'{RES_PATH}/{file_name}.json', 'w') as f:
        f.write(json_str)

