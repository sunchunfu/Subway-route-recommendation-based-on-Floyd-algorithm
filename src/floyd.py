
from data_process import *
from pprint import pprint
import copy


def floyd(D,P):
    for k in range(len(D)):
        for i in range(len(D)):
            for j in range(len(D)):
                if D[i][k] != inf and D[k][j] != inf and D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    P[i][j] = k
    return D,P

def init(data_path):
    global D_is,P_dis,D_time,P_time
    data_process(data_path)
    D_dis = copy.deepcopy(D_dis_base)
    P_dis = copy.deepcopy(P_dis_base)
    D_time = copy.deepcopy(D_time_base)
    P_time = copy.deepcopy(P_time_base)
    floyd(D_dis,P_dis)
    floyd(D_time,P_time)

def __get_P(s,e,P,list):
    if(P[s][e]==0):
        return 0
    __get_P(s,P[s][e],P,list)
    list.append(P[s][e])
    __get_P(P[s][e],e,P,list)

def plan_by_time(s,e):
    sid = get_id(s)
    eid = get_id(e)
    P_list = []
    P_list.append(sid)
    __get_P(sid, eid, P_time, P_list)
    P_list.append(eid)
    print('最短时间路线')
    print(P_list)
    cost = D_time[sid][eid] + len(P_list) * 30 / 60
    print('时间:',cost,'min')

def plan_by_dis(s,e):
    sid = get_id(s)
    eid = get_id(e)
    P_list = []
    P_list.append(sid)
    __get_P(sid, eid, P_dis, P_list)
    P_list.append(eid)
    print('最短距离路线')
    print(P_list)
    cost = D_dis[sid][eid]
    print('距离:',cost,'km')

def recommend(s,e,increment=5):
    increment = 5-increment
    global P_dis
    global D_dis
    sid = get_id(s)
    eid = get_id(e)
    Paths = []
    for i in range(10):
        P = []
        __get_P(sid,eid,P_dis,P)
        if P not in Paths:
            Paths.append(P)
        D_dis = copy.deepcopy(D_dis_base)
        P_dis = copy.deepcopy(P_dis_base)
        for i in range(len(P)):
            if len(sts_list[P[i]].ln) != 1 and sts_list[P[i-1]].ln != sts_list[P[i+1]].ln:
                D_dis[P[i]][P[i+1]] += increment
        floyd(D_dis,P_dis)
        increment *= 1.1

    for i in range(len(Paths)):
        path = Paths[i]
        path.insert(0,sid)
        path.append(eid)
        for st_id in path:
            print(get_name(st_id),end=' ')
        print(get_time_dis(path))


if __name__ == '__main__':
    recommend('大学城北','综保区',increment=4)


