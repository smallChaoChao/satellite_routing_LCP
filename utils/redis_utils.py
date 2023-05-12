#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:57
# @Author  : smallChaoChao
# @File    : redis_utils.py
import json

import redis
from utils.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, SLICE_KEY


def get_slice_key() -> list:
    """获取抽取的时间片列表"""
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    slice_keys = r.get(SLICE_KEY).decode()
    # 将redis中读出的str转成list
    slice_keys = json.loads(slice_keys)
    r.close()

    return slice_keys


def get_slice() -> dict:
    """获取时间片信息"""
    slice_keys = get_slice_key()
    slice_dict = {}

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    for key in slice_keys:
        topology = {}
        links = [link.decode() for link in list(r.hgetall(key).keys())]
        for link in links:
            topology[link] = json.loads(r.hget(key, link))
        slice_dict[key] = topology
    r.close()

    return slice_dict
