#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/17 09:52
# @Author  : smallChaoChao
# @File    : delay_jitter_statistics.py
from statistics import median, mean
from typing import Tuple

from utils.config import LCP_RES_PATH, DT_DVTR_RES_PATH, TGM_RES_PATH
from utils.io_utils import list_dir, read_json2dict


class DelayJitterStatistics:
    """统计路由结果的时延抖动信息"""

    def __init__(self):
        # 获取各个算法的路由结果文件路径
        self.lcp_routing_res = [f'{LCP_RES_PATH}/{x}' for x in list_dir(path=LCP_RES_PATH)]
        self.dt_dvtr_routing_res = [f'{DT_DVTR_RES_PATH}/{x}' for x in list_dir(path=DT_DVTR_RES_PATH)]
        self.tgm_routing_res = [f'{TGM_RES_PATH}/{x}' for x in list_dir(path=TGM_RES_PATH)]

    @staticmethod
    def statistic_single_delay_jitter(path: str) -> Tuple[float, float, float]:
        """统计单个路由结果的时延抖动信息"""
        routing_res = read_json2dict(path=path)
        jitter_list, pre_delay = [], 0
        for slice_key, routing in routing_res.items():
            cur_delay = routing.get('avgDelay')
            jitter_list.append(abs(float(cur_delay) - float(pre_delay)) / 100)
            pre_delay = cur_delay
        jitter_list = jitter_list[1:]
        return round(max(jitter_list), 3), round(median(jitter_list), 3), round(mean(jitter_list), 3)

    def statistic_algo_delay_jitter(self, routing_res: list, algo: str):
        """统计单个算法路由结果的时延抖动信息"""
        max_list, median_list, avg_list = [], [], []
        for path in routing_res:
            max_jitter, median_jitter, avg_jitter = self.statistic_single_delay_jitter(path=path)
            max_list.append(max_jitter)
            median_list.append(median_jitter)
            avg_list.append(avg_jitter)
        print(f"{algo} 时延抖动信息：")
        print(f'max jitter list: max={round(max(max_list), 3)}, median={round(median(max_list), 3)}, '
              f'avg={round(mean(max_list), 3)}, {algo}_max_jitter_list={max_list}')
        print(f'median jitter list: max={round(max(median_list), 3)}, median={round(median(median_list), 3)}, '
              f'avg={round(mean(median_list), 3)}, {algo}_median_jitter_list={median_list}')
        print(f'avg jitter list: max={round(max(avg_list), 3)}, median={round(median(avg_list), 3)}, '
              f'avg={round(mean(avg_list), 3)}, {algo}_avg_jitter_list={avg_list}')
        print()

    def statistic_delay_jitter(self):
        """统计所有算法的时延抖动结果"""
        self.statistic_algo_delay_jitter(routing_res=self.lcp_routing_res, algo='LCP')
        self.statistic_algo_delay_jitter(routing_res=self.dt_dvtr_routing_res, algo='DT_DVTR')
        self.statistic_algo_delay_jitter(routing_res=self.tgm_routing_res, algo='TGM')


if __name__ == "__main__":
    d = DelayJitterStatistics()
    d.statistic_delay_jitter()
