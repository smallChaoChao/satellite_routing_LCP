#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:57
# @Author  : smallChaoChao
# @File    : redis_utils.py
import json
from statistics import mean

import redis
from utils.config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, SLICE_KEY_EXTRACT, ALL_LINKS_KEY, SLICE_KEY_MERGED
from utils.io_utils import list_dir


def get_slice_key(key: str) -> list:
    """获取抽取的时间片列表"""
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    slice_keys = r.get(key).decode()
    # 将redis中读出的str转成list
    slice_keys = json.loads(slice_keys)
    r.close()

    return slice_keys


def get_slice() -> dict:
    """获取时间片信息"""
    slice_keys = get_slice_key(key=SLICE_KEY_MERGED)
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


def get_all_links() -> list:
    """获取所有的链路信息"""
    all_links = []
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    link_head_list = [link.decode() for link in list(r.hgetall(ALL_LINKS_KEY).keys())]
    for link_head in link_head_list:
        link_tail = r.hget(ALL_LINKS_KEY, link_head).decode('utf-8')
        all_links.extend([f'{link_head}-{end}' for end in link_tail.split(",")])
    r.close()
    return all_links


def merge_slice():
    """合并细碎时间片"""
    # 获取需要合并的拓扑的名称
    merge_list, merge_key_list = [], get_slice_key(key=SLICE_KEY_MERGED)

    merge_keys_path = "/Volumes/MacWarehouse/Python/Projects/TSNSatelliteRouting/k-shortest/paths-transition"
    file_names = list_dir(path=merge_keys_path)
    for file_name in file_names:
        file_name = file_name.split(".")[0].split("-")
        cur_list = [f'{file_name[i]}-{file_name[i + 1]}' for i in range(len(file_name) - 1)]
        merge_list.append(cur_list)
        for k in cur_list:
            if k in merge_key_list:
                merge_key_list.remove(k)
    print(merge_list)
    # 从redis中获取相关时间片 合并拓扑 共有的链路保留 否则删除
    all_links = get_all_links()
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
    for merge_group in merge_list:
        merged_key = f'{merge_group[0].split("-")[0]}-{merge_group[-1].split("-")[1]}'
        merge_key_list.append(merged_key)
        print(merged_key)
        merge_dict = {}
        for key in merge_group:
            topology = {}
            links = [link.decode() for link in list(r.hgetall(key).keys())]
            for link in links:
                topology[link] = json.loads(r.hget(key, link))
            merge_dict[key] = topology
        # 保留相同得 删除部分出现的
        merged_dict = {}
        for link in all_links:
            if all([(link in merge_dict.get(k)) for k in merge_group]):
                # 请求时延的平均值
                cnt = 0
                delay_list = [0, 0, 0]
                for _slice in merge_group:
                    times = int(_slice.split("-")[1]) - int(_slice.split("-")[0])
                    delay_list[0] += float(merge_dict.get(_slice).get(link)[0]) * times
                    delay_list[1] += float(merge_dict.get(_slice).get(link)[1]) * times
                    delay_list[2] += float(merge_dict.get(_slice).get(link)[2]) * times
                    cnt += times
                delay_list = [x / cnt for x in delay_list]
                merged_dict[link] = str(delay_list)
        print(merged_dict is None, merged_dict)
        print(f'{len(list(merged_dict.keys()))}, {[len(list(merge_dict.get(x).keys())) for x in merge_group]}')
        print("-----------------------------------------------------------------------")
        r.hmset(merged_key, merged_dict)

    # 写入合并后的key到SLICE_KEY_MERGED
    merge_key_list = sorted(merge_key_list, key=lambda x: int(x.split("-")[0]))
    # merge_key_list = [f"{x}" for x in merge_key_list]
    print(merge_key_list)
    r.set(SLICE_KEY_MERGED, json.dumps(merge_key_list))
    r.close()


if __name__ == "__main__":
    merge_slice()
