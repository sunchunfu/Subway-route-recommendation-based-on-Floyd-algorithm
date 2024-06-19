from draw import *
import sys

#使用data_process的数据进行主要算法，包含初始化，并绘制地图，调用draw.py

#绘制进度条
def progress_bar(finish_tasks_number, tasks_number):
    percentage = round(finish_tasks_number / tasks_number * 100)
    print("\r进度: {}%: ".format(percentage), "▓" * (percentage // 2), end="")
    sys.stdout.flush()

#Floyd主要方法，输入为D矩阵和P矩阵，直接输出修改后的矩阵
def floyd(D,P):
    for k in range(len(D)):
        for i in range(len(D)):
            for j in range(len(D)):
                if D[i][k] != inf and D[k][j] != inf and D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]
                    P[i][j] = k
    
#初始化
def init(data_path):
    global D_is,P_dis,D_time,P_time
    data_process(data_path)              #调用数据读取，形成矩阵
    D_dis = copy.deepcopy(D_dis_base)    #复制原始矩阵，用于临时计算
    P_dis = copy.deepcopy(P_dis_base)
    D_time = copy.deepcopy(D_time_base)
    P_time = copy.deepcopy(P_time_base)
    floyd(D_dis,P_dis)     #距离矩阵进行第一次Floyd算法
    floyd(D_time,P_time)
    draw_all(data_path)    #绘制地铁可视化

#输出基于P矩阵s，e之间的路径到list
def __get_P(s,e,P,list):
    if(P[s][e]==0):
        return 0
    __get_P(s,P[s][e],P,list)
    list.append(P[s][e])
    __get_P(P[s][e],e,P,list)
#按时间优先规划（弃用）
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
#按最短距离优先规划（弃用）
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

#主要推荐算法
def recommend(s,e,increment=5):
    '''
    以当前文件所有的D_dis与P_dis进行推荐
    基本原理：
    先计算最短路，遍历最短路上的站点，遇到换乘站则将换乘站与下一站之间的距离加上increment，再进行最短路计算;
    重复上述过程数次，并保存所有不同路径
    '''
    increment = (5-increment)/5
    global P_dis
    global D_dis
    sid = get_id(s)
    eid = get_id(e)
    Paths = []
    for i in range(15):    #重复计算15次
        progress_bar(i+1,15)
        P = []
        __get_P(sid,eid,P_dis,P)
        if P not in Paths:   #路径记录
            Paths.append(P)
        D_dis = copy.deepcopy(D_dis_base)
        P_dis = copy.deepcopy(P_dis_base)
        for i in range(len(P)):  #遍历当前最短路上的站点
            if len(sts_list[P[i]].ln) != 1 and sts_list[P[i-1]].ln != sts_list[P[i+1]].ln:  #判断是否为换乘站
                D_dis[P[i]][P[i+1]] += increment
        floyd(D_dis,P_dis)
        increment *= 1.1  #increment增加
    print()
    #结果输出
    for i in range(len(Paths)):
        path = Paths[i]
        path.insert(0,sid)
        path.append(eid)
        time, distance, tr_num = get_time_dis_tr(path)  #获取当前线路的距离，时间，换乘次数
        html_name = '路线{}_耗时{}min_距离{}KM_换乘次数{}'.format(i, time, distance, tr_num)
        print(html_name)
        r_path = []
        for st_id in path:  #输出线路信息
            name = get_name(st_id)
            r_path.append(name)
            print(name,end=' ')
        draw_route(r_path,html_name)   #绘制当前线路
        print()

if __name__ == '__main__':
    recommend('大学城北','综保区',increment=4)


