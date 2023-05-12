#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 16:06
# @Author  : smallChaoChao
# @File    : topology.py

import networkx as nx

from utils.config import LINK_CAP
from utils.redis_utils import get_slice


class Topology:
    """使用redis中的信息创建网络拓扑"""
    def __init__(self, slice_dict: dict):
        self.slice_dict = slice_dict

    @staticmethod
    def convert2graph(topology: dict) -> nx:
        """将一个topology转换为networkx对象"""
        link_cap = {}
        G = nx.Graph()
        for nodes in list(topology.keys()):
            node_1, node_2 = nodes.split("-")[0], nodes.split("-")[1]
            delay = round(topology.get(nodes)[0] / 100, 3)
            # 添加节点
            if not G.has_node(node_1):
                G.add_node(node_1)
            if not G.has_node(node_2):
                G.add_node(node_2)
            # 添加边
            # G.add_weighted_edges_from([(node_1, node_2, delay)])
            G.add_edge(u_of_edge=node_1, v_of_edge=node_2, weight=delay, capacity=LINK_CAP)
            # 添加链路容量
            link_cap[(node_1, node_2)] = LINK_CAP
            link_cap[(node_2, node_1)] = LINK_CAP
        return G, link_cap

    def convert2graph_list(self) -> dict:
        """将slice_dict中的所有topology转换为networkx对象"""
        graph_dict, link_cap_dict = {}, {}
        for slice_key, topology in self.slice_dict.items():
            graph_dict[slice_key], link_cap_dict[slice_key] = self.convert2graph(topology)
        return graph_dict, link_cap_dict


if __name__ == "__main__":
    t = Topology(get_slice())
    d, l = t.convert2graph_list()
    # for k, v in d.items():
    #     print(k, v, v.edges(data=True))
    print(l.get('271-273'))
    print(d.get('271-273').has_edge('1506', '1406'))
