#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 15:34
# @Author  : smallChaoChao
# @File    : switches_statistics.py
import logging
from statistics import mean, median

from utils.config import TGM_RES_PATH, LCP_RES_PATH, DT_DVTR_RES_PATH, LSHADE_RES_PATH, ILP_RES_PATH
from utils.io_utils import list_dir, read_json2dict

logging.basicConfig(level=logging.INFO, format="[%(filename)s, line %(lineno)d] %(message)s")


class SwitchesStatistics:
    """统计各个算法的切换次数"""
    def __init__(self):
        # 获取各个算法的路由结果文件路径
        self.lcp_routing_res = [f'{LCP_RES_PATH}/{x}' for x in list_dir(path=LCP_RES_PATH) if x.endswith('.json')]
        self.dt_dvtr_routing_res = [f'{DT_DVTR_RES_PATH}/{x}' for x in list_dir(path=DT_DVTR_RES_PATH) if x.endswith('.json')]
        self.tgm_routing_res = [f'{TGM_RES_PATH}/{x}' for x in list_dir(path=TGM_RES_PATH) if x.endswith('.json')]
        self.lshade_routing_res = [f'{LSHADE_RES_PATH}/{x}' for x in list_dir(path=LSHADE_RES_PATH) if x.endswith('.json')]
        self.ilp_routing_res = [f'{ILP_RES_PATH}/{x}' for x in list_dir(path=ILP_RES_PATH) if x.endswith('.json')]
        # 排序
        self.lcp_routing_res = sorted(self.lcp_routing_res, key=lambda x: int(x.split("/")[-1].split("-")[0]))
        self.dt_dvtr_routing_res = sorted(self.dt_dvtr_routing_res, key=lambda x: int(x.split("/")[-1].split("-")[0]))
        self.tgm_routing_res = sorted(self.tgm_routing_res, key=lambda x: int(x.split("/")[-1].split("-")[0]))
        self.lshade_routing_res = sorted(self.lshade_routing_res, key=lambda x: int(x.split("/")[-1].split("-")[0]))
        self.ilp_routing_res = sorted(self.ilp_routing_res, key=lambda x: int(x.split("/")[-1].split("-")[0]))

    @staticmethod
    def statistic_single_switches(path: str) -> int:
        """统计单个流的切换次数"""
        print(path)
        routing_res = read_json2dict(path=path)
        pre_routing, cnt = [], -1
        for slice_key, routing in routing_res.items():
            cur_routing = routing.get('path')
            if pre_routing != cur_routing:
                cnt += 1
            pre_routing = cur_routing
        return cnt

    def statistic_switches(self):
        """统计所有算法的切换次数"""
        lcp_list, dt_dvtr_list, tgm_list, lshade_list, ilp_list = [], [], [], [], []
        for lcp in self.lcp_routing_res:
            lcp_list.append(self.statistic_single_switches(lcp))
        for dt_dvtr in self.dt_dvtr_routing_res:
            dt_dvtr_list.append(self.statistic_single_switches(dt_dvtr))
        for tgm in self.tgm_routing_res:
            tgm_list.append(self.statistic_single_switches(tgm))
        for lshade in self.lshade_routing_res:
            lshade_list.append(self.statistic_single_switches(lshade))
        for ilp in self.ilp_routing_res:
            ilp_list.append(self.statistic_single_switches(ilp))
        # 输出结果LCP
        logging.info(msg=f'LCP 切换次数: sum={sum(lcp_list)}, avg={mean(lcp_list)}, max={max(lcp_list)}, '
                         f'min={min(lcp_list)}, median={median(lcp_list)}, {lcp_list}')
        # 输出结果DT-DVTR
        logging.info(msg=f'DT_DVTR 切换次数: sum={sum(dt_dvtr_list)}, avg={mean(dt_dvtr_list)}, max={max(dt_dvtr_list)}, '
                         f'min={min(dt_dvtr_list)}, median={median(dt_dvtr_list)}, {dt_dvtr_list}')
        # 输出结果TGM
        logging.info(msg=f'TGM 切换次数: sum={sum(tgm_list)}, avg={mean(tgm_list)}, max={max(tgm_list)}, '
                         f'min={min(tgm_list)}, median={median(tgm_list)}, {tgm_list}')
        # 输出结果Lshade
        logging.info(msg=f'Lshade 切换次数: sum={sum(lshade_list)}, avg={mean(lshade_list)}, max={max(lshade_list)}, '
                         f'min={min(lshade_list)}, median={median(lshade_list)}, {lshade_list}')
        # 输出结果ILP
        logging.info(msg=f'ILP 切换次数: sum={sum(ilp_list)}, avg={mean(ilp_list)}, max={max(ilp_list)}, '
                         f'min={min(ilp_list)}, median={median(ilp_list)}, {ilp_list}')


if __name__ == "__main__":
    s = SwitchesStatistics()
    s.statistic_switches()

