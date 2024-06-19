import copy
import folium
import webbrowser
from data_process import *
import os

#该文件用来显示地图，使用data_process中的数据，调用folium生成网页，并在浏览器中打开,被floyd.py调用

#创建output文件夹用于存储生成的HTML文件
x = 'output'
if os.path.exists(x):
    pass
else:
    os.mkdir(x)

# 创建地图对象，使用高德地图作为背景
map = folium.Map(location=[31.8639, 117.2808], zoom_start=15,tiles='https://webrd02.is.autonavi.com/appmaptile?lang=zh_en&size=1&scale=1&style=8&x={x}&y={y}&z={z}',attr='高德-街道路网图')
global data

#绘制所有站点并显示
def draw_all(data_path):
    global data
    # 加载JSON数据
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 将站点和线路添加到地图上
    for station_name, attrs in data.items():
        lon = attrs['lon_E']
        lat = attrs['lat_N']
        folium.Circle(
            [lat,lon],
            color = 'blue',
            tooltip=station_name
        ).add_to(map)

        # 绘制线路
    for edge in edges_list:
        folium.PolyLine(
            locations=[[data[edge.st_in]['lat_N'],data[edge.st_in]['lon_E']],[data[edge.st_out]['lat_N'],data[edge.st_out]['lon_E']]],
            color = edge.color,
            weight = 3,
            opacity=0.4
        ).add_to(map)
        '''
        for dest, time in attrs['c_time'].items():
            dest_attrs = data[dest]
            folium.PolyLine(
                locations=[[lat, lon], [dest_attrs['lat_N'], dest_attrs['lon_E']]],
                color='blue',
                weight=2,
                opacity=0.5
            ).add_to(map)        
        '''
    #保存到HTML文件
    map.save('output/hefei_subway_map.html')
    #打开地图
    webbrowser.open(os.getcwd()+'/output/hefei_subway_map.html', new=0, autoraise=True)

#绘制一条线路并显示
def draw_route(recommended_route,name):
    global data
    # 假设推荐线路的站点对
    map_r = copy.deepcopy(map)
    # 绘制推荐线路，使用不同的颜色
    for i in range(len(recommended_route) - 1):
        start = recommended_route[i]
        end = recommended_route[i + 1]
        start_attrs = data[start]
        end_attrs = data[end]
        #放置标记
        folium.Marker(
            location=[start_attrs['lat_N'], start_attrs['lon_E']],
            popup=start
        ).add_to(map_r)
        folium.Marker(
            location=[end_attrs['lat_N'], end_attrs['lon_E']],
            popup=end
        ).add_to(map_r)
        #绘制当前线路
        folium.PolyLine(
            locations=[[start_attrs['lat_N'], start_attrs['lon_E']], [end_attrs['lat_N'], end_attrs['lon_E']]],
            color='#FF00FF',  # 推荐线路颜色
            weight=5,
            opacity=0.8
        ).add_to(map_r)
    # 保存地图到HTML文件
    map_r.save('output/'+name+'.html')
    #打开地图
    webbrowser.open(os.getcwd()+'/output/'+name+'.html', new=0, autoraise=True)