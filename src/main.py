from floyd import *

while True:
    data_path = input('数据路径,默认stdata.json：')
    try:
        if data_path == '':
            data_path = 'stdata.json'
        init(data_path)
        break
    except:
        print('请重新输入')


while True:

    in_str = input('输入起始站和终点站,换乘意愿(0-5),空格间隔,输入0结束：')
    if in_str == '0':
        break
    else:
        s,e,increment = in_str.split()
    recommend(s,e,increment=4)

print('感谢使用')