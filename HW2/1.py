import random
citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

def distance(p1, p2):
#    print('p1=', p1)
    x1, y1 = p1
    x2, y2 = p2
    return ((x2-x1)**2+(y2-y1)**2)**0.5#距離

def pathLength(p):
    dist = 0
    plen = len(p)
    for i in range(plen):
        # dist += distance(citys[p[i]], citys[p[(i+1)%plen]])
        dist += distance(p[i], p[(i+1)%plen])
    return dist

def neighbor(p):
    city_path_cp=p.copy()
    p1,p2=random.sample(range(len(p)),2)
    tmp=city_path_cp[p1]
    city_path_cp[p1]=city_path_cp[p2]
    city_path_cp[p2]=tmp
    return city_path_cp#新的city排序

def hillClimbing(x, pathLength, neighbor, max_fail=100):
    print("start: ", pathLength(x), x)             # 印出初始解
    fails = 0                             # 失敗次數設為 0
    gens=0
    while 1:
        snew = neighbor(x)               #  取得鄰近的解
        sheight = pathLength(x)             #  sheight=目前解的高度
        nheight = pathLength(snew)           #  nheight=鄰近解的高度
        if (nheight < sheight):          #  如果鄰近解比目前解更好
            print(gens, ':', pathLength(x), x)  #    印出新的解
            x = snew                      #    就移動過去
            fails = 0                     #    移動成功，將連續失敗次數歸零
        else:                             #  否則
            fails = fails + 1             #    將連續失敗次數加一
        gens+=1
        if (fails >= max_fail):
            print("solution: ", x)          #  印出最後找到的那個解
            return x                              #    然後傳回。

hillClimbing(citys, pathLength, neighbor)