from PIL import ImageGrab
import win32api
import win32gui
import win32con
import random
import ini
import cheB
# appPath = r'F:/winmine.exe'
dataPath = r'F:/SWrk/gpTasks/data'
ImagePath = dataPath + r'/grabImages/'
# 雷区数据矩阵,0到8表示该格子所显示的数字(其周围的雷数),'-'表示未翻开,'p'表示已标记的雷,'E'表示gamevoer
DefValNumpy = ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'p', 'E']
# 扫雷区的起点位置(实际向右下方偏移半个格子,方便日后偏移)
# 注!!这里吧第一个方块放在(0, 0)的位置,方便与矩阵对应
sx = ini.x[0] + ini.px + int(ini.blocksize/2)
sy = ini.y[0] + ini.py + int(ini.blocksize/2)
# 这个元组表示点开方格周围的八个方格
Nnumpy = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

# 以下是全局变量,需要在开始游戏时初始化
Message = ''
iniList = []
# 存的是转置矩阵....为了与常识中xy坐标对应
resultList = []
# 线索列表
clues = []
# 待检查列表
checkList = []


# 随机坐标!!启动游戏
def startgame():
    # 需要初始化的全局变量
    global clues, checkList, resultList, iniList, Message
    Message = ''
    clues = []
    checkList = []
    resultList = [['-' for row in range(ini.col)] for col in range(ini.row)]
    # 清空由于失败导致的iniList中的残留项
    del(iniList[:])
    for item in range(0, ini.row):
        for jtem in range(0, ini.col):
            iniList.append((item, jtem))
    coord = random_coord()
    print('None cluse! random click', coord)
    click(coord)
    get_map(coord)
    while len(iniList) > 0:
        if analyse():
            continue
        coord = random_coord()
        print('None cluse! random click', len(iniList), coord)
        click(coord)
        tempstr = get_map(coord)
        if tempstr == 'gameover':
            break
    if checkend():
        print('Congratulations!\n-----------------------\n\n')
        return True
    else:
        print('Come On!\n-----------------------\n\n')
        return False
    # ttttt = numpy.transpose(resultList)
    # for t in ttttt:
    #     print(t)


def getCurPos():
    return win32gui.GetCursorPos


# 根据传入位置翻开该位置,位置为在起点位置上偏移n倍方格数
def click(coord=(-1, -1)):
    global sx, sy
    tempx = sx + int(ini.blocksize * coord[0])
    tempy = sy + int(ini.blocksize * coord[1])
    win32api.SetCursorPos([tempx, tempy])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)


# 标记某个位置的方格为地雷,位置算法同上,被标记的方块理应从待翻开方块中移除
def rigth_click(coord=(-1, -1)):
    global sx, sy
    tempx = sx + int(ini.blocksize*coord[0])
    tempy = sy + int(ini.blocksize*coord[1])
    win32api.SetCursorPos([tempx, tempy])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_RIGHTDOWN | win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
    # 被标记的区域应该写入扫描结果矩阵
    resultList[coord[0]][coord[1]] = 'P'
    if(iniList.count(coord) > 0):
        iniList.remove(coord)


def getWinmineNumpy():
    return None


def reset():
    # 笑脸起点坐标...
    global iniList
    lsx = ini.x[0] + ini.px + ini.lpx
    lsy = ini.y[0] + ini.py + ini.lpy
    win32api.SetCursorPos([lsx, lsy])
    win32api.mouse_event(
        win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def checkend():
    # 笑脸起点坐标...
    lsx = ini.x[0] + ini.px + ini.lpx
    lsy = ini.y[0] + ini.py + ini.lpy
    lex, ley = lsx+9, lsy+9
    box = (lsx, lsy, lex, ley)
    img = ImageGrab.grab(box)
    img.save(ImagePath + 'face'+".png")
    result = cheB.get_faceEigvals(img)
    vit = cheB.faceDir['vict']
    sub = result - vit
    if sub < complex(0.2) and sub > complex(-0.2):
        return True
    return False


def check_block(coord=(-1, -1)):
    # 检测方块的起点坐标
    csx = ini.x[0] + ini.px
    csy = ini.y[0] + ini.py
    cx = csx + int(ini.blocksize*coord[0])
    cy = csy + int(ini.blocksize*coord[1])
    box = (cx, cy, cx+ini.blocksize, cy+ini.blocksize)
    img = ImageGrab.grab(box)
    # img.save(ImagePath + 'temppp'+".png")
    # 这两行显示图片哈希值的...
    # for i in cheB.get_hash(img):
    #     print(i)
    result = DefValNumpy[cheB.get_code(cheB.get_maxEigvals(img))]
    # print(result)
    return result


def get_map(coord=(-1, -1)):
    # 该函数用来扫描刚刚点击后被翻开地图的方块状态
    global Message
    checkList.append(coord)
    while len(checkList) > 0:
        temp = [(0, 0), (0, 0)]
        # 从未翻开方块移除刚刚检测的方块并将方块加入待检测方块列表中
        temp[0] = checkList.pop()
        Message = 'checking'
        if iniList.count(temp[0]) > 0:
            iniList.remove(temp[0])
        flag = check_block(temp[0])
        # 注!!! 注意那个转置矩阵
        resultList[temp[0][0]][temp[0][1]] = flag
        if flag == '0':
            for item in Nnumpy:
                temp[1] = ((temp[0][0]+item[0]), (temp[0][1]+item[1]))
                # 得到的ctemp(需要检测的方块)在未翻开的方块中(防越界),且不在待检测列表中就将其加入待检测列表
                if iniList.count(temp[1]) > 0 and checkList.count(temp[1]) == 0:
                    checkList.append(temp[1])
        elif flag == 'E':
            print('GAMEOVER!')
            return 'gameover'
        elif flag == 'p':
            pass
        else:
            clues.append(temp[0])
        del(temp[:])
    return 'ok'


def random_coord():
    return iniList[random.randint(0, len(iniList)-1)]


# 用于判断剩余雷数
def mines(coord=(-1, -1)):
    minesNum = int(resultList[coord[0]][coord[1]])
    for item in Nnumpy:
            tx, ty = (coord[0]+item[0]), (coord[1]+item[1])
            # 不能越界
            if tx >= 0 and tx < ini.col and ty >= 0 and ty < ini.row:
                temp = resultList[tx][ty]
                # 得到标记方块
                if temp == 'P':
                    # 数字减去标记方块数等于剩余雷数
                    minesNum -= 1
    return minesNum


# 用来得到数字周围未知方块列表
def empty(coord=(-1, -1)):
    myEmpties = []
    for item in Nnumpy:
            tx, ty = (coord[0]+item[0]), (coord[1]+item[1])
            # 不能越界
            if tx >= 0 and tx < ini.col and ty >= 0 and ty < ini.row:
                temp = resultList[tx][ty]
                # 得到周围未知方块数
                if temp == '-':
                    myEmpties.append((tx, ty))
    return myEmpties


# 用来得到未知公共区域列表
def get_same(empties1, empties2):
    tsa = []
    for s in empties1:
        if s in empties2:
            tsa.append(s)
    return tsa


def analyse():
    reflage = False
    for icoord in clues:

        # 情况1:数字周围全部未知格子等于剩余雷数-->全部标雷
        # 数字周围全部未知格子
        flags = empty(icoord)
        if mines(icoord) == len(flags):
            # print("--------------\n strategy1, checking", icoord)
            # 此时该数字线索已经使用,应该移除
            if clues.count(icoord) > 0:
                clues.remove(icoord)
            # print("flage", flags)
            for rck in flags:
                rigth_click(rck)
            reflage = True
            continue

        #  情况2:数字等于周围已标记雷数(周围雷全部标记,不剩雷)-->翻开其他
        if mines(icoord) == 0:
            # print("--------------\n strategy2, checking", icoord)
            if clues.count(icoord) > 0:
                clues.remove(icoord)
            for item in empty(icoord):
                # print('click', item)
                click(item)
                get_map(item)
            reflage = True
            continue

    # 两个数字共有区域...
    # 如果该方法改变了线索条件则递归调用analyse()
    if strategy3():
        reflage = True
    if reflage:
        # print('----------'+str(reflage)+'----------')
        return True
    # print('----------'+str(reflage)+'----------')
    return False


# 两个数字有公共未翻开区域...
def strategy3():
    reList = []
    for icoord in clues:
        # 最外层for循环用来找可能有公共区域的坐标
        for tx in range(icoord[0]-2, icoord[0]+3):
            for ty in range(icoord[1]-2, icoord[1]+3):
                # 保证找到的坐标不会越界
                if tx >= 0 and tx < ini.col and ty >= 0 and ty < ini.row:
                    # 保证找到的坐标是非自身的数字方块
                    if icoord != (tx, ty) and ((tx, ty) in (clues)) and (tx, ty) not in reList:
                        empties1 = empty(icoord)
                        empties2 = empty((tx, ty))
                        same = get_same(empties1, empties2)
                        # 达到初始条件: 两个数字有公共未翻开区域...且两者都还有未排除的雷
                        if len(same) > 0 and mines(icoord) > 0 and mines((tx, ty)) > 0:
                            # 两个数字周围雷数剩余相同,且其中一个只剩公共区域时,非公有区域没有雷???
                            strategy3_1f = False
                            # print('ttx', mines(icoord), mines((tx, ty)), len(same), len(empties1), len(empties2))
                            if mines(icoord) - mines((tx, ty)) == 0 and len(same) == len(empties1):
                                # print("--------------\n strategy3.1, click", icoord, (tx, ty))
                                for e in empties2:
                                    if e not in same:
                                        strategy3_1f = True
                                        # print(e)
                                        click(e)
                                        get_map(e)
                                return strategy3_1f
                            elif mines(icoord) - mines((tx, ty)) == 0 and len(same) == len(empties2):
                                # print("--------------\n strategy3.2, click", icoord, (tx, ty))
                                for e in empties1:
                                    if e not in same:
                                        strategy3_1f = True
                                        # print(e)
                                        click(e)
                                        get_map(e)
                                return strategy3_1f
                            # print(mines(icoord), mines((tx, ty)), len(same), len(empties1), len(empties2))
                            # 两个剩余雷数的差值等于等于非公共区域大小时,非公共区域一定是雷
                            # len(empties1)-len(same)大于等于零
                            if mines(icoord)-mines((tx, ty)) == len(empties1)-len(same):
                                # print("--------------\n strategy3.1, flage", icoord, (tx, ty))
                                for e in empties1:
                                    if e not in same:
                                        # print(e)
                                        rigth_click(e)
                                return True
                            elif mines((tx, ty))-mines(icoord) == len(empties2)-len(same):
                                # print("--------------\n strategy3.2, flage", icoord, (tx, ty))
                                for e in empties2:
                                    if e not in same:
                                        # print(e)
                                        rigth_click(e)
                                return True
            reList.append(icoord)
    return False


# win32process.CreateProcess(appPath, '', None, None, 0, win32process.
# CREATE_NO_WINDOW,None, None, win32process.STARTUPINFO())
# 截取图片
# x, y = ini.x, ini.y
# box = (x[0], y[0], x[1], y[1])
# img = ImageGrab.grab(box)
# img.save(ImagePath + 'test'+".png")

# img.show()
# img = Image.open(ImagePath+'Easy'+'.png')
# plt.imshow(img)
# plt.show()
# print(ini.width, ini.row, ini.col)
# 尝试点击第一个方块
# 以第一个点的中心为起点坐标


# 从未翻开方块移除刚刚点击的方块并将方块加入待检测方块列表中
# iniList.remove(coord)
# print(checkList.count(coord))
# asasa = check_block(coord)


# print('st')
# startgame()
