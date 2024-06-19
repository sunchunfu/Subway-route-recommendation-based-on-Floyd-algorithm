from floyd import *

#主函数，与用户交互

#输入数据文件，格式为data_process所生成的
while True:
    data_path = input('数据路径,默认stdata.json：')
    try:
        if data_path == '':
            data_path = 'stdata.json'
        init(data_path)
        break
    except:
        print('请重新输入')
#循环输入
while True:
    in_str = input('输入起始站和终点站,换乘意愿(0-5),空格间隔,回车结束：')
    if in_str == '':
        break
    else:
        try:
            s,e,increment = in_str.split()
            recommend(s,e,int(increment))
        except:
            print('请重新输入')
print()
print('感谢使用')