#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/9 11:02
# @Author  : smallChaoChao
# @File    : LCP.py

"""
实现切换次数和负载均衡联合优化路由的近似算法LCP
"""
import logging

import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt

from flow import FlowSet, Flow
from topology import Topology
from utils.config import K_ALTER, LINK_CAP, RES_PATH
from utils.io_utils import write_dict2json
from utils.redis_utils import get_slice

logging.basicConfig(level=logging.INFO, format="[%(filename)s, line %(lineno)d] %(message)s")


class LCP:
    """实现LCP算法"""

    def __init__(self):
        # 获取一个周期的时间片的网络拓扑 维护集合L，提供每条边的容量信息
        self.slice_graph, self.link_capacity = Topology(get_slice()).convert2graph_list()
        logging.info(msg='获取时间片拓扑集合完成')
        # logging.info(msg=f'self.link_capacity={self.link_capacity}')
        # 获取TS流量集合
        self.flow_set = FlowSet().convert2flow_set()
        logging.info(msg='获取TS流量集合完成')
        logging.info(msg=f'{self.flow_set}')

    def short_path(self, slice_key: str, graph, flow: Flow):
        """返回一条符合时延以及链路容量约束的最短路径和时延"""
        res_path, res_delay, res_cap, cnt = [], 0, 0, 0
        for path in nx.shortest_simple_paths(graph, source=flow.src_node, target=flow.dst_node, weight='weight'):
            path = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            delay = sum([graph.edges[i]['weight'] for i in path])
            # 判断是否满足容量约束
            # min_cap = min([graph.edges[nodes]['capacity'] - flow.bandwidth for nodes in path])
            min_cap = min([self.link_capacity[slice_key][nodes] - flow.bandwidth for nodes in path])
            if min_cap > 0 and delay <= flow.delay_upper and min_cap > res_cap:
                res_cap = min_cap + flow.bandwidth
                res_path = path
                res_delay = delay
            cnt += 1
            # 判断是否满足时延约束
            if delay > flow.delay_upper or cnt == K_ALTER:
                logging.debug(
                    msg=f'cnt={cnt}, delay={delay}, delay_upper={flow.delay_upper}, res_cap={res_cap}, path={path}')
                break

        return res_path, res_delay, res_cap

    @staticmethod
    def find_min_switches_routing(p_set: dict) -> dict:
        """通过使用p_set构建图 寻找最短路径 从而找到切换次数最少的路径"""
        # logging.error(p_set)
        # logging.error(msg=f'len={len(list(p_set.keys()))}, list_keys={list(p_set.keys())}')
        nodes = list(p_set.keys())  # 节点
        edges = [(nodes[i], nodes[i + 1]) for i in range(len(nodes) - 1)]
        # logging.error(msg=f'edges={edges}')
        for src in nodes:
            # logging.error(msg=f'p_set.get(src)={p_set.get(src)}')
            # logging.error(msg=f'cur_key={src}, p_set.get(src).keys()={list(p_set.get(src).keys())}')
            for dst in list(p_set.get(src).keys()):
                if src != dst and (src, dst) not in edges and (dst, src) not in edges:
                    edges.append((src, dst))
        # logging.error(msg=f'edges={edges}')
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        # 找最短路
        path = nx.shortest_path(G, nodes[0], nodes[-1])
        # logging.error(msg=f'path={path}')
        # 找到最短路径对应的路由结果
        routing_res = {}
        idx = 0
        while idx < len(path):
            slice_key = path[idx]
            for k, v in p_set.get(slice_key).items():
                routing_res[k] = v
            idx += 1 if len(list(p_set.get(slice_key).keys())) == 1 else 2

        return routing_res

    def calculate_single_routing(self, flow: Flow) -> dict or None:
        """给单个业务计算路由"""
        logging.info(msg=f'计算TS流 {flow} 的路由结果...')
        # 初始化记录路径的集合和时间片的集合
        p_set = {}
        # 循环时间片
        # for i in range(5):
        for i in range(len(list(self.slice_graph.keys()))):
            slice_key = list(self.slice_graph.keys())[i]
            graph = self.slice_graph.get(slice_key)
            # 先获取当前路径的最短路和时延
            prev_path, prev_delay, prev_cap = self.short_path(slice_key, graph, flow)
            if not len(prev_path):
                logging.error(msg=f'无法为 {flow} 分配路由, 时间片i={i}, slice_key={slice_key}')
                return None
            logging.debug(msg=f'prev_path{prev_path}')
            res_path = [x[0] for x in prev_path]
            res_path.append(prev_path[-1][1])
            logging.debug(msg=(prev_delay, res_path))

            # 找到持续最长的路径
            j = i + 1
            cur_p_set = {slice_key: {'path': res_path, 'avgDelay': prev_delay * 100}}
            while j < len(list(self.slice_graph.keys())):
                curr_slice_key = list(self.slice_graph.keys())[j]
                curr_graph = self.slice_graph.get(curr_slice_key)
                # 当前拓扑中存在上一个拓扑最短路的路径
                if not all([curr_graph.has_edge(nodes[0], nodes[1]) for nodes in prev_path]):
                    break
                # 判断最短路径是否是邻接的路
                flag = True
                if not curr_graph.has_edge(flow.src_node, flow.dst_node):
                    flag = False
                    # 需要在当前拓扑上添加一条新的边
                    curr_graph.add_weighted_edges_from([(flow.src_node, flow.dst_node, prev_delay)])
                    # 给当前边添加容量
                    # nx.set_edge_attributes(curr_graph, {(flow.src_node, flow.dst_node): {'capacity': prev_cap}})
                    self.link_capacity[curr_slice_key][(flow.src_node, flow.dst_node)] = prev_cap
                # 寻找新图的最短路径
                curr_path, curr_delay, curr_cap = self.short_path(slice_key=curr_slice_key, graph=curr_graph, flow=flow)
                # 还原拓扑 删掉边
                if not flag:
                    curr_graph.remove_edge(flow.src_node, flow.dst_node)
                    del self.link_capacity[curr_slice_key][(flow.src_node, flow.dst_node)]  # 删除容量
                # 判断新图的是否和前一个拓扑的路径一致
                if curr_path != prev_path:
                    break
                # 更新结果集合
                cur_p_set[curr_slice_key] = {'path': res_path, 'avgDelay': prev_delay * 100}
                j += 1
            # 存储数据集合
            p_set[slice_key] = cur_p_set
        routing_res = self.find_min_switches_routing(p_set=p_set)
        logging.info(msg=f'路由结果为：{routing_res}')
        return routing_res

    def update_link_cap(self, flow: Flow, routing_res: dict):
        """根据路由结果更新链路容量"""
        for slice_key, res in routing_res.items():
            path = res.get('path')
            graph = self.slice_graph.get(slice_key)
            for i in range(len(path) - 1):
                nodes = (path[i], path[i + 1])
                # 更新容量
                # graph.edges[nodes]['capacity'] = graph.edges[nodes]['capacity'] - flow.bandwidth
                self.link_capacity[slice_key][nodes] = self.link_capacity[slice_key][nodes] - flow.bandwidth
            self.slice_graph[slice_key] = graph

    def calculate_routing(self):
        """给TS流量集合中的所有流计算路由"""
        # 无法分配的业务集合
        no, unable_routing_list = 0, []
        # 遍历排序好的所有流
        for flow in self.flow_set[:]:
            no += 1
            # 计算flow路由结果
            routing_res = self.calculate_single_routing(flow=flow)
            if routing_res is None:  # 无法为flow分配业务将跳过该flow
                unable_routing_list.append(f'{no}-{flow}')
                # continue
                return
            # 更新拓扑的链路容量
            self.update_link_cap(flow=flow, routing_res=routing_res)
            # 写json文件到本地
            write_dict2json(data=routing_res, file_name=f'{no}-{flow}')
            logging.info(msg=f'{flow} 路由结果写json文件成功')
        logging.error(msg=f'无法分配的业务集合为: {unable_routing_list}')


if __name__ == "__main__":
    lcp = LCP()
    lcp.calculate_routing()
