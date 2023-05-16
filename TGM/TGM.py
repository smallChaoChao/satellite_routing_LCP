#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/16 08:58
# @Author  : smallChaoChao
# @File    : TGM.py
import json
import logging

import requests

from LCP.flow import FlowSet, Flow
from utils.config import URL_TGM, TGM_RES_PATH
from utils.io_utils import write_dict2json

logging.basicConfig(level=logging.INFO, format="[%(filename)s, line %(lineno)d] %(message)s")


class TGM:
    """实现TGM算法的路由"""
    def __init__(self):
        # 获取TS流量集合
        self.flow_set = FlowSet().convert2flow_set()
        logging.info(msg='获取TS流量集合完成')

    @staticmethod
    def calculate_single_routing(flow: Flow):
        """计算单个流的路由结果"""
        # 将flow转为字典的data
        data = {'srcSatellite': flow.src_node,
                'dstSatellite': flow.dst_node,
                'isDisjoint': 'false',
                'tos': flow.priority}
        routing_res = requests.post(url=URL_TGM, data=data)
        routing_res = json.loads(routing_res.content.decode())
        return routing_res

    def calculate_routing(self):
        """获取所有流的路由结果 然后序列化输出到文件"""
        no = 0
        for flow in self.flow_set:
            no += 1
            routing_res = self.calculate_single_routing(flow=flow)
            # 写json文件到本地
            write_dict2json(data=routing_res, dir_path=TGM_RES_PATH, file_name=f'{no}-{flow}')
            logging.info(msg=f'{flow} 路由结果写json文件成功')


if __name__ == "__main__":
    tgm = TGM()
    tgm.calculate_routing()
