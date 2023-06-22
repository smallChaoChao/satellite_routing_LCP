#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:29
# @Author  : smallChaoChao
# @File    : config.py
"""配置参数"""


import os.path


"""redis相关"""
# redis host
REDIS_HOST = "192.168.1.16"
# redis port
REDIS_PORT = "16379"
# redis password
REDIS_PASSWORD = "uEstC318.#"
# 抽取时间片的key
SLICE_KEY_EXTRACT = "slice-keys-extract"
# 获取所有链路的key
ALL_LINKS_KEY = "all_links"
# 新增合并后的时间片key
SLICE_KEY_MERGED = "slice-keys-merged"


"""flow相关"""
# 流集合的路径
FLOWS_PATH = "{}/data_in/flows.json".format(os.path.dirname(os.getcwd()))
# LCP路由结果的路径
LCP_RES_PATH = "{}/data_out/LCP".format(os.path.dirname(os.getcwd()))
# DT-DVTR路由结果的路径
DT_DVTR_RES_PATH = "{}/data_out/DT_DVTR".format(os.path.dirname(os.getcwd()))
# TGM路由结果的路径
TGM_RES_PATH = "{}/data_out/TGM".format(os.path.dirname(os.getcwd()))
# Lshade路由结果的路径
LSHADE_RES_PATH = "{}/data_out/LGY".format(os.path.dirname(os.getcwd()))
# ILP路由结果的路径
ILP_RES_PATH = "{}/data_out/ILP".format(os.path.dirname(os.getcwd()))
# 起始节点
SRC_NODE = 'start'
# 终止节点
DST_NODE = 'end'
# 优先级
PRIORITY = 'tos'
# 流的带宽大小
BANDWIDTH = 'cir'
# 流的时延上界
DELAY_UPPER = 'latency'


"""配置参数"""
# 星间链路的容量 100Mbps
LINK_CAP = 100 * 1000 * 1000
# 备选路径时延差值\delta = 0 表示只选最短路径
DELTA = 0
# 负载均衡 满足时延约束的K条路径中选择链路容量最大的
K_ALTER = 10

"""对比算法相关"""
# DT-DVTR的restful接口
URL_DT_DVTR = f"http://{REDIS_HOST}:18888/get-dt-dvtr-routing"
# TGM的restful接口
URL_TGM = f"http://{REDIS_HOST}:18888/get-tgm-routing"

