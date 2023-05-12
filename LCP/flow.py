#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 14:34
# @Author  : smallChaoChao
# @File    : flow.py
import networkx as nx

from utils.config import SRC_NODE, DST_NODE, PRIORITY, BANDWIDTH, DELAY_UPPER
from utils.json_utils import json2dict


class Flow:
    """定义流的类"""

    def __init__(self, start, end, tos, cir, latency):
        # 起始节点
        self.src_node = start
        # 终止节点
        self.dst_node = end
        # 优先级6-1
        self.priority = tos
        # 流的带宽大小
        self.bandwidth = cir
        # 流的时延上界
        self.delay_upper = latency

    def __str__(self):
        # return f"Flow(src_node={self.src_node}, dst_node={self.dst_node}, " \
        #        f"priority={self.priority}, bandwidth={self.bandwidth}, delay_upper={self.delay_upper})"
        return f"Flow({self.src_node}, {self.dst_node}, " \
               f"{self.priority}, {self.bandwidth}, {self.delay_upper})"

    def __repr__(self):
        return self.__str__()


class FlowSet:
    """TS业务集合"""

    def __init__(self):
        self.json_dict = json2dict()

    def convert2flow(self, flow_dict: dict) -> Flow:
        """将dict转为flow对象"""
        f = Flow(start=flow_dict.get(SRC_NODE),
                 end=flow_dict.get(DST_NODE),
                 tos=flow_dict.get(PRIORITY),
                 cir=flow_dict.get(BANDWIDTH),
                 latency=flow_dict.get(DELAY_UPPER))
        return f

    def convert2flow_set(self) -> list:
        """转换为flow对象集合，并且排序"""
        flow_set = []
        # 转换dict为flow对象
        for flow_dict in self.json_dict:
            flow_set.append(self.convert2flow(flow_dict))

        # 对flow对象进行排序：1. 优先级 2. 带宽大小
        flow_set = sorted(flow_set, key=lambda x: (-x.priority, -x.bandwidth))

        return flow_set


if __name__ == "__main__":
    fs = FlowSet()
    fs.convert2flow_set()
