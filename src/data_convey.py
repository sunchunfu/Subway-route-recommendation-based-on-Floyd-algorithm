import json

#该文件是将高德的数据转化为可用数据，仅一次使用，无调用
st_dict = {}
time_data ={'起点':[],
            '终点':[]}
#这个函数是获取rs_x,和rs_y的但是后来下面改了，这个函数就没用到
def get_pos(st):
    pos = st['p'].split()
    return pos

import math
# 计算两经纬度地点距离
def getDistance(latA, lonA, latB, lonB):
    ra = 6378140  # 赤道半径
    rb = 6356755  # 极半径
    flatten = (ra - rb) / ra  # Partial rate of the earth
    # change angle to radians
    radLatA = math.radians(latA)
    radLonA = math.radians(lonA)
    radLatB = math.radians(latB)
    radLonB = math.radians(lonB)
    pA = math.atan(rb / ra * math.tan(radLatA))
    pB = math.atan(rb / ra * math.tan(radLatB))
    x = math.acos(math.sin(pA) * math.sin(pB) + math.cos(pA) * math.cos(pB) * math.cos(radLonA - radLonB))
    c1 = (math.sin(x) - x) * (math.sin(pA) + math.sin(pB)) ** 2 / math.cos(x / 2) ** 2
    c2 = (math.sin(x) + x) * (math.sin(pA) - math.sin(pB)) ** 2 / math.sin(x / 2) ** 2
    dr = flatten / 8 * (c1 - c2)
    distance = ra * (x + dr)
    distance = round(distance / 1000, 4)
    return distance

#打开文件
with open('../data/draw.json','r',encoding='utf-8') as f:
    data = json.load(f)  #加载数据文件
    lines = data['l']    #取出线路数据
    for line_i in range(6):   #创建所有车站空字典
        sts = data['l'][line_i]['st']
        for st_i in range(len(sts)):
            st = sts[st_i]
            st_dict[st['n']] = {}
            st_dict[st['n']]['c_time'] = {}
            st_dict[st['n']]['c_dis'] = {}
            st_dict[st['n']]['ln'] = []

    for line_i in range(6):          #遍历车站转写数据
        sts = data['l'][line_i]['st']
        for st_i in range(len(sts)):
            st = sts[st_i]
            pos = st['p'].split()     #车站绘图位置
            st_dict[st['n']]['pos_x'] = int(pos[0])
            st_dict[st['n']]['pos_y'] = int(pos[1])
            loc = st['sl'].split(',')     #车站经纬度
            st_dict[st['n']]['lon_E'] = float(loc[0])
            st_dict[st['n']]['lat_N'] = float(loc[1])
            if data['l'][line_i]['ln'] not in st_dict[st['n']]['ln']:
                st_dict[st['n']]['ln'].append(data['l'][line_i]['ln'])  #车站所属线路

            #车站连接建立
            if st_i == 0:  #起始站
                st_next = sts[st_i+1]
                st_dict[st['n']]['c_time'][st_next['n']] = 0
                st_dict[st['n']]['c_dis'][st_next['n']] = getDistance(lonA=float(st['sl'].split(',')[0]),
                                                                      latA=float(st['sl'].split(',')[1]),
                                                                      lonB=float(st_next['sl'].split(',')[0]),
                                                                      latB=float(st_next['sl'].split(',')[1]))

            elif st_i == len(sts)-1:   #终点站
                st_last = sts[st_i-1]
                st_dict[st['n']]['c_time'][st_last['n']] = 0
                st_dict[st['n']]['c_dis'][st_last['n']] = getDistance(lonA=float(st['sl'].split(',')[0]),
                                                                      latA=float(st['sl'].split(',')[1]),
                                                                      lonB=float(st_last['sl'].split(',')[0]),
                                                                      latB=float(st_last['sl'].split(',')[1]))

            else:    #中间站
                st_next = sts[st_i + 1]
                st_dict[st['n']]['c_time'][st_next['n']] = 0
                st_dict[st['n']]['c_dis'][st_next['n']] = getDistance(lonA=float(st['sl'].split(',')[0]),
                                                                      latA=float(st['sl'].split(',')[1]),
                                                                      lonB=float(st_next['sl'].split(',')[0]),
                                                                      latB=float(st_next['sl'].split(',')[1]))

                st_last = sts[st_i - 1]
                st_dict[st['n']]['c_time'][st_last['n']] = 0
                st_dict[st['n']]['c_dis'][st_last['n']] = getDistance(lonA=float(st['sl'].split(',')[0]),
                                                                      latA=float(st['sl'].split(',')[1]),
                                                                      lonB=float(st_last['sl'].split(',')[0]),
                                                                      latB=float(st_last['sl'].split(',')[1]))

    #另存json文件
    with open('../data/stdata.json','w',encoding='utf-8') as fl:
        json.dump(st_dict,fl,indent=4,ensure_ascii=False)




