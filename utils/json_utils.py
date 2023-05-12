#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:40
# @Author  : smallChaoChao
# @File    : json_utils.py

"""从json文件中获取流"""
import json

from utils.config import FLOWS_PATH


def json2dict() -> list:
    """将json转成dict"""
    with open(FLOWS_PATH, 'r') as f:
        flows = json.loads(f.read())

    return flows

