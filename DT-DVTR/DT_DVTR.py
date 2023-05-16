#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/15 15:35
# @Author  : smallChaoChao
# @File    : DT_DVTR.py
import json
import logging

import requests

from LCP.flow import FlowSet, Flow
from utils.config import URL_DT_DVTR, SLICE_KEY_MERGED, DT_DVTR_RES_PATH
from utils.io_utils import write_dict2json
from utils.redis_utils import get_slice_key

logging.basicConfig(level=logging.INFO, format="[%(filename)s, line %(lineno)d] %(message)s")


class DT_DVTR:
    """实现对比算法DT-DVTR的路由结果计算"""
    def __init__(self):
        # 获取TS流量集合
        self.flow_set = FlowSet().convert2flow_set()
        logging.info(msg='获取TS流量集合完成')
        # 获取所有的时间片的list集合
        self.slice_keys = get_slice_key(key=SLICE_KEY_MERGED)

    def calculate_single_routing(self, flow: Flow):
        """通过restful接口获取全周期的路由结果"""
        # 将flow转为字典的data
        data = {'srcSatellite': flow.src_node,
                'dstSatellite': flow.dst_node,
                'isDisjoint': 'false',
                'tos': flow.priority}
        response = requests.post(url=URL_DT_DVTR, data=data)
        response = json.loads(response.content.decode())
        # 保留self.slice_keys中的时间片对应的结果
        routing_res = {}
        for slice_key in self.slice_keys:
            if slice_key not in response:
                # print(slice_key, "不在dt-dvtr的key中")
                continue
            routing_res[slice_key] = {
                "path": response.get(slice_key).get('path'),
                "avgDelay": response.get(slice_key).get('avgDelay')
            }
        return routing_res

    def calculate_routing(self):
        """获取所有流的路由结果 然后序列化输出到文件"""
        no = 0
        for flow in self.flow_set:
            no += 1
            routing_res = self.calculate_single_routing(flow=flow)
            # 写json文件到本地
            write_dict2json(data=routing_res, dir_path=DT_DVTR_RES_PATH, file_name=f'{no}-{flow}')
            logging.info(msg=f'{flow} 路由结果写json文件成功')


if __name__ == "__main__":
    d = DT_DVTR()
    d.calculate_routing()
