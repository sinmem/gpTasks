import sweeper
import time
vNum = 0
sunNum = 0
for i in range(0, 10):
    sunNum += 1
    print('第', i, '次')
    if sweeper.startgame():
        vNum += 1
    else:
        pass
    time.sleep(1)
    sweeper.reset()
print('胜率: %.2f' % (100*vNum/sunNum), '%')
