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
SLICE_KEY = "slice-keys-extract"


"""flow相关"""
# 流集合的路径
FLOWS_PATH = "{}/data_in/flows.json".format(os.path.dirname(os.getcwd()))
# 路由结果的路径
RES_PATH = "{}/data_out".format(os.path.dirname(os.getcwd()))
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


{('1501', '1601'): 100000000, ('1601', '1501'): 100000000, ('1410', '1411'): 100000000, ('1411', '1410'): 100000000, ('1209', '1210'): 100000000, ('1210', '1209'): 100000000, ('1203', '1204'): 100000000, ('1204', '1203'): 100000000, ('1308', '1408'): 100000000, ('1408', '1308'): 100000000, ('1606', '1607'): 100000000, ('1607', '1606'): 100000000, ('1109', '1110'): 100000000, ('1110', '1109'): 100000000, ('1107', '1108'): 100000000, ('1108', '1107'): 100000000, ('1507', '1607'): 100000000, ('1607', '1507'): 100000000, ('1609', '1610'): 100000000, ('1610', '1609'): 100000000, ('1108', '1109'): 100000000, ('1109', '1108'): 100000000, ('1309', '1409'): 100000000, ('1409', '1309'): 100000000, ('1207', '1307'): 100000000, ('1307', '1207'): 100000000, ('1310', '1311'): 100000000, ('1311', '1310'): 100000000, ('1603', '1604'): 100000000, ('1604', '1603'): 100000000, ('1308', '1309'): 100000000, ('1309', '1308'): 100000000, ('1506', '1507'): 100000000, ('1507', '1506'): 100000000, ('1301', '1302'): 100000000, ('1302', '1301'): 100000000, ('1501', '1502'): 100000000, ('1502', '1501'): 100000000, ('1406', '1407'): 100000000, ('1407', '1406'): 100000000, ('1204', '1205'): 100000000, ('1205', '1204'): 100000000, ('1503', '1504'): 100000000, ('1504', '1503'): 100000000, ('1201', '1301'): 100000000, ('1301', '1201'): 100000000, ('1403', '1404'): 100000000, ('1404', '1403'): 100000000, ('1307', '1407'): 100000000, ('1407', '1307'): 100000000, ('1102', '1202'): 100000000, ('1202', '1102'): 100000000, ('1107', '1207'): 100000000, ('1207', '1107'): 100000000, ('1302', '1402'): 100000000, ('1402', '1302'): 100000000, ('1401', '1402'): 100000000, ('1402', '1401'): 100000000, ('1508', '1608'): 100000000, ('1608', '1508'): 100000000, ('1407', '1408'): 100000000, ('1408', '1407'): 100000000, ('1408', '1508'): 100000000, ('1508', '1408'): 100000000, ('1106', '1107'): 100000000, ('1107', '1106'): 100000000, ('1404', '1504'): 100000000, ('1504', '1404'): 100000000, ('1508', '1509'): 100000000, ('1509', '1508'): 100000000, ('1604', '1605'): 100000000, ('1605', '1604'): 100000000, ('1209', '1309'): 100000000, ('1309', '1209'): 100000000, ('1201', '1211'): 100000000, ('1211', '1201'): 100000000, ('1506', '1606'): 100000000, ('1606', '1506'): 100000000, ('1304', '1305'): 100000000, ('1305', '1304'): 100000000, ('1101', '1102'): 100000000, ('1102', '1101'): 100000000, ('1303', '1304'): 100000000, ('1304', '1303'): 100000000, ('1206', '1207'): 100000000, ('1207', '1206'): 100000000, ('1202', '1302'): 100000000, ('1302', '1202'): 100000000, ('1408', '1409'): 100000000, ('1409', '1408'): 100000000, ('1401', '1501'): 100000000, ('1501', '1401'): 100000000, ('1303', '1403'): 100000000, ('1403', '1303'): 100000000, ('1307', '1308'): 100000000, ('1308', '1307'): 100000000, ('1602', '1603'): 100000000, ('1603', '1602'): 100000000, ('1404', '1405'): 100000000, ('1405', '1404'): 100000000, ('1509', '1609'): 100000000, ('1609', '1509'): 100000000, ('1103', '1104'): 100000000, ('1104', '1103'): 100000000, ('1507', '1508'): 100000000, ('1508', '1507'): 100000000, ('1608', '1609'): 100000000, ('1609', '1608'): 100000000, ('1509', '1510'): 100000000, ('1510', '1509'): 100000000, ('1301', '1401'): 100000000, ('1401', '1301'): 100000000, ('1504', '1604'): 100000000, ('1604', '1504'): 100000000, ('1505', '1506'): 100000000, ('1506', '1505'): 100000000, ('1501', '1511'): 100000000, ('1511', '1501'): 100000000, ('1210', '1211'): 100000000, ('1211', '1210'): 100000000, ('1502', '1503'): 100000000, ('1503', '1502'): 100000000, ('1305', '1306'): 100000000, ('1306', '1305'): 100000000, ('1108', '1208'): 100000000, ('1208', '1108'): 100000000, ('1402', '1403'): 100000000, ('1403', '1402'): 100000000, ('1101', '1201'): 100000000, ('1201', '1101'): 100000000, ('1202', '1203'): 100000000, ('1203', '1202'): 100000000, ('1405', '1406'): 100000000, ('1406', '1405'): 100000000, ('1610', '1611'): 100000000, ('1611', '1610'): 100000000, ('1109', '1209'): 100000000, ('1209', '1109'): 100000000, ('1104', '1204'): 100000000, ('1204', '1104'): 100000000, ('1102', '1103'): 100000000, ('1103', '1102'): 100000000, ('1201', '1202'): 100000000, ('1202', '1201'): 100000000, ('1208', '1308'): 100000000, ('1308', '1208'): 100000000, ('1304', '1404'): 100000000, ('1404', '1304'): 100000000, ('1306', '1307'): 100000000, ('1307', '1306'): 100000000, ('1104', '1105'): 100000000, ('1105', '1104'): 100000000, ('1502', '1602'): 100000000, ('1602', '1502'): 100000000, ('1510', '1511'): 100000000, ('1511', '1510'): 100000000, ('1208', '1209'): 100000000, ('1209', '1208'): 100000000, ('1205', '1206'): 100000000, ('1206', '1205'): 100000000, ('1301', '1311'): 100000000, ('1311', '1301'): 100000000, ('1103', '1203'): 100000000, ('1203', '1103'): 100000000, ('1601', '1602'): 100000000, ('1602', '1601'): 100000000, ('1302', '1303'): 100000000, ('1303', '1302'): 100000000, ('1504', '1505'): 100000000, ('1505', '1504'): 100000000, ('1409', '1509'): 100000000, ('1509', '1409'): 100000000, ('1309', '1310'): 100000000, ('1310', '1309'): 100000000, ('1601', '1611'): 100000000, ('1611', '1601'): 100000000, ('1402', '1502'): 100000000, ('1502', '1402'): 100000000, ('1203', '1303'): 100000000, ('1303', '1203'): 100000000, ('1407', '1507'): 100000000, ('1507', '1407'): 100000000, ('1101', '1111'): 100000000, ('1111', '1101'): 100000000, ('1204', '1304'): 100000000, ('1304', '1204'): 100000000, ('1605', '1606'): 100000000, ('1606', '1605'): 100000000, ('1409', '1410'): 100000000, ('1410', '1409'): 100000000, ('1207', '1208'): 100000000, ('1208', '1207'): 100000000, ('1403', '1503'): 100000000, ('1503', '1403'): 100000000, ('1105', '1106'): 100000000, ('1106', '1105'): 100000000, ('1503', '1603'): 100000000, ('1603', '1503'): 100000000, ('1607', '1608'): 100000000, ('1608', '1607'): 100000000, ('1110', '1111'): 100000000, ('1111', '1110'): 100000000, ('1401', '1411'): 100000000, ('1411', '1401'): 100000000}

