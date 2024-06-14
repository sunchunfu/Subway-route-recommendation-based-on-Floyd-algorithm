import pandas as pd
import json
from pprint import pprint

class cst:
    def __init__(self, name, pos_x, pos_y, lon_E, lat_N, c_time, c_dis, ln, id):
        self.name = name
        self.rs_x = pos_x
        self.rs_y = pos_y
        self.loc_E = lon_E
        self.loc_N = lat_N
        self.c_time = c_time
        self.c_dis = c_dis
        self.ln = ln
        self.id = id

class cedge:
    def __init__(self,st_in,st_out,time,length,ln,color):
        self.st_in = st_in
        self.st_out = st_out
        self.time = time
        self.length = length
        self.ln = ln
        self.color = color

sts_list = []
edges_list = []
st_dict = {}
D_time_base = []
P_time_base = []
D_dis_base = []
P_dis_base = []
inf = 999999

def get_id(name):
    id = 0
    for st in sts_list:
        if name == st.name:
            id = st.id
            break
    return id

def get_name(id):
    name = 0
    for st in sts_list:
        if id == st.id:
            name = st.name
            break
    return name

def get_time_dis(path):
    time = 0
    dis = 0
    tr = 0
    for i in range(len(path)-1):
        for edge in edges_list:
            if edge.st_in == get_name(path[i]) and edge.st_out == get_name(path[i+1]):
                time += edge.time
                dis += edge.length
        try:
            if len(sts_list[path[i]].ln) != 1 and sts_list[path[i-1]].ln != sts_list[path[i+1]].ln:
                tr += 1
        finally:
            pass
    time = time + 30*len(path)/60
    return round(dis,3),round(time,2),tr



def data_process(data_path):
    with open(data_path,'r',encoding='utf-8') as f:
        st_dict = json.load(f)
        for stn in st_dict.keys():
            st = cst(stn,st_dict[stn]['pos_x'],
                    st_dict[stn]['pos_y'],
                    st_dict[stn]['lon_E'],
                    st_dict[stn]['lat_N'],
                    st_dict[stn]['c_time'],
                    st_dict[stn]['c_dis'],
                    st_dict[stn]['ln'],
                    st_dict[stn]['id'])
            sts_list.append(st)
            for outn in st_dict[stn]['c_time'].keys():
                a = set(st_dict[stn]['ln'])
                b = set(st_dict[outn]['ln'])
                ln = list(a&b)[0]

                if ln == '1号线':
                    color = '#CC0000'
                elif ln == '2号线':
                    color = '#0065B3'
                elif ln == '3号线':
                    color = '#00AB4F'
                elif ln == '4号线':
                    color = '#EE782E'
                elif ln == '5号线':
                    color = '#B8D201'
                edge = cedge(stn,outn,st_dict[stn]['c_time'][outn],st_dict[stn]['c_dis'][outn],ln,color)
                edges_list.append(edge)


    #时间矩阵

    for i in range(len(sts_list)):
        D_temp = []
        P_temp = []
        for j in range(len(sts_list)):
            P_temp.append(0)
            if i == j :
                D_temp.append(0)
            elif sts_list[j].name in sts_list[i].c_time.keys():
                D_temp.append(sts_list[i].c_time[sts_list[j].name])
            else:
                D_temp.append(inf)
        D_time_base.append(D_temp)
        P_time_base.append(P_temp)

    #距离矩阵
    for i in range(len(sts_list)):
        D_temp = []
        P_temp = []
        for j in range(len(sts_list)):
            P_temp.append(0)
            if i == j :
                D_temp.append(0)
            elif sts_list[j].name in sts_list[i].c_dis.keys():
                D_temp.append(sts_list[i].c_dis[sts_list[j].name])
            else:
                D_temp.append(inf)
        D_dis_base.append(D_temp)
        P_dis_base.append(P_temp)
