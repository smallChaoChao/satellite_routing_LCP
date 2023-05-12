#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 11:21
# @Author  : smallChaoChao
# @File    : extract_slice.py
import redis
import json

# 连接Redis数据库
r = redis.Redis(host='192.168.1.16', port=16379, db=0, password='uEstC318.#')

slice_keys = r.get("slice-keys").decode()
slice_keys = data = json.loads(slice_keys)
slice_keys = list(slice_keys)

# 从小到大排序
lst_new = [(int(s.split('-')[0]), int(s.split('-')[1])) for s in slice_keys]
lst_new_sorted = sorted(lst_new, key=lambda x: x[0])
lst_new = ['{}-{}'.format(a[0], a[1]) for a in lst_new_sorted]
r.set("slice-keys-sorted", json.dumps(lst_new))


# 抽片结果
result = []

prekey = lst_new[0]
prevalue = r.hgetall(prekey)
result.append(prekey)

for i in range(1, len(lst_new)):
    key = lst_new[i]
    value = r.hgetall(key)

    if (prevalue.keys() != value.keys()):
        result.append(key)
        prekey = key
        prevalue = value

r.set("slice-keys-extract", json.dumps(result))
