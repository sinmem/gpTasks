from PIL import Image
from numpy import linalg
import json
dataPath = r'F:/SWrk/gpTasks/data/originData/'
resultPath = r'F:/SWrk/gpTasks/data/resources/'
DefValNumpy = ['0', '1', '2', '3', '4', '5', '6', '7', '-', 'p']
DefDir = {}


def get_hash(img):
    img_L = img.convert("L")
    pixels = list(img_L.getdata())
    for p in range(0, len(pixels)):
        if pixels[p] is 192 or pixels[p] is 128:
            pixels[p] = 0
        else:
            pixels[p] = 1
    return pixels


def get_sparseMatrix(pixels):
    tempDoubleList = []
    for i in range(0, 16):
        tempList = pixels[(i*16):((i+1)*16)]
        tempDoubleList.append(tempList)
    return tempDoubleList


def get_maxEigvals(img):
    # matrix = get_sparseMatrix(get_hash(img))
    return max(linalg.eigvals(get_sparseMatrix(get_hash(img))))
    # emmm 好奇葩的特征值...
    # return linalg.eigvals(matrix)


def get_code(maxEigvals):
    return DefDir[str(maxEigvals)]


# # 创建模板特征值存储的json文件时用到
# for ietm in range(0, len(DefValNumpy)):
#     img_1 = Image.open(dataPath+DefValNumpy[ietm]+".png")
#     DefDir[ietm] = str(get_maxEigvals(img_1))
# jsObj = json.dumps(DefDir)
# # print(jsObj)
# with open((dataPath+'DefMaxEigvals.josn').encode('utf-8'), "w") as ftemp:
#             ftemp.write(jsObj)

# 从文件获取模板图片的特征值存入字典 
with open((dataPath+'DefMaxEigvals.josn').encode('utf-8'), "r") as ftemp:
    DefDir = json.load(ftemp)
for item in DefDir:
    DefDir[item] = complex(DefDir[item])
print(DefDir)
    