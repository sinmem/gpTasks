from PIL import Image
from numpy import linalg
import json
dataPath = r'F:/SWrk/gpTasks/data/originData/'
resultPath = r'F:/SWrk/gpTasks/data/resources/'
DefValNumpy = ['0', '1', '2', '3', '4', '5', '6', '7', '8', 'p', 'end']
face = ['s1', 's2', 'vict']
faceDir = {}
DefDir = {}


def get_hash(img):
    img_L = img.convert("L")
    pixels = list(img_L.getdata())
    temp = []
    for i in range(0, 10):
        a = 48 + i * 16 + 3
        b = a + 10
        temp.append(pixels[a:b])
    for p in range(0, len(temp)):
        for q in range(0, len(temp[p])):
            if temp[p][q] is 192:
                temp[p][q] = 0
            else:
                temp[p][q] = 1
    # for p in range(0, len(pixels)):
    #     if pixels[p] is 192 or pixels[p] is 128:
    #         pixels[p] = 0
    #     else:
    #         pixels[p] = 1
    return temp


def get_sparseMatrix(img):
    img_L = img.convert("L")
    pixels = list(img_L.getdata())
    temp = []
    for i in range(0, 9):
        temp.append(pixels[i*9:i*9+9])
    for p in range(0, len(temp)):
        for q in range(0, len(temp[p])):
            if temp[p][q] is 225:
                temp[p][q] = 0
            else:
                temp[p][q] = 1
    return temp


def get_maxEigvals(img):
    # matrix = get_sparseMatrix(get_hash(img))
    return max(linalg.eigvals(get_hash(img)))
    # emmm 好奇葩的特征值...
    # return linalg.eigvals(matrix)


def get_code(maxEigvals):
    return DefDir[str(maxEigvals)]


def get_faceEigvals(img):
    matrix = get_sparseMatrix(img)
    # for i in matrix:
    #     print(i)
    # print('---------------')
    return max(linalg.eigvals(matrix))


# # 创建模板特征值存储的json文件.1 时用到
# for ietm in range(0, len(DefValNumpy)):
#     img_1 = Image.open(dataPath+DefValNumpy[ietm]+".png")
#     DefDir[str(get_maxEigvals(img_1))] = ietm
# jsObj = json.dumps(DefDir)
# # print(jsObj)
# with open((dataPath+'DefMaxEigvals.josn').encode('utf-8'), "w") as ftemp:
#             ftemp.write(jsObj)

# for ietm in range(0, len(DefValNumpy)):
#     img_1 = Image.open(dataPath+DefValNumpy[ietm]+".png")
# # img_1 = Image.open(dataPath+"8.png")
#     for i in get_hash(img_1):
#         print(i)
#     print('------------'+DefValNumpy[ietm]+'-------------')

# 从文件获取模板图片的特征值存入字典
with open((dataPath+'DefMaxEigvals.josn').encode('utf-8'), "r") as ftemp:
    DefDir = json.load(ftemp)
# print(DefDir)
# 从文件获取模板图片的特征值存入字典
with open((dataPath+'faceEigvals.josn').encode('utf-8'), "r") as ftemp:
    faceDir = json.load(ftemp)
for i in faceDir:
    faceDir[i] = complex(faceDir[i])
print(faceDir)

# # 板特征值存储的json文件.2 时用到
# for ietm in range(0, len(face)):
#     img_1 = Image.open(dataPath+face[ietm]+".png")
#     print(face[ietm])
#     faceDir[ietm] = str(get_faceEigvals(img_1))
# jsObj = json.dumps(faceDir)
# # print(jsObj)
# with open((dataPath+'faceEigvals.josn').encode('utf-8'), "w") as ftemp:
#             ftemp.write(jsObj)
