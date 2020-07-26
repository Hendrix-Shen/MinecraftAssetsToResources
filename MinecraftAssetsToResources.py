'''
MinecraftAssetsToResources MC 资源数据信息转换
Author Hendrix_Shen
Version 0.2333.333.3333
Description 闲的无聊整的

'''
import os
import json
import time
import datetime
import shutil

class ResourcesCover():
    def getFiles(self, path):
        FileList = []
        for root, dirs, files in os.walk(path):
            for f in files:
                FileList.append(f)
        return FileList
    def getIndexData(self, fileName):
        with open(fileName, 'r') as f:
            return json.load(f)
            
    def getFilePath(self, fileName):
        Path = ''
        Name = fileName.split('/')
        del Name[-1]
        for i in Name:
            Path = Path + '/' + i
        return Path
            
    def getFileName(self, fileName):
        return fileName.split('/')[-1]
    
    def processCover(self, indexFileName):
        data = self.getIndexData(indexFileName)['objects']
        outputPath = './ResourcesCover_Output/{}/'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        for k in data:
            #print(self.getFilePath(k), self.getFileName(k))
            targetPath = '{}/assets/{}'.format(outputPath, self.getFilePath(k))
            if (not(os.path.isdir(targetPath))):
                os.makedirs(targetPath)
            shutil.copyfile('./assets/objects/{}/{}'.format(data[k]['hash'][0:2], data[k]['hash']), '{}/{}'.format(targetPath, self.getFileName(k)))
        return outputPath
    def getTimeSub(self, StartTime, StopTime):
        RunTime = round((StopTime-StartTime)*1000, 2) #转换时间戳整数部分为毫秒, 并且保留2位小数
        RunTimeUnit = '耗秒' #时间单位
        if RunTime >= 86400000:
            RunTime = round(RunTime / 86400000,2)
            RunTimeUnit = '天'
        elif RunTime >= 3600000:
            RunTime = round(RunTime / 3600000,2)
            RunTimeUnit = '时'
        elif RunTime >= 60000:
            RunTime = round(RunTime / 60000,2)
            RunTimeUnit = '分'
        elif RunTime >= 1000:
            RunTime = round(RunTime / 1000,2)
            RunTimeUnit = '秒'
        return RunTime,RunTimeUnit

if __name__ == '__main__':
    while True:
        Version = ResourcesCover().getFiles('./assets/indexes/')
        Index = 0
        if (Version != []):
            for i in Version:
                print(Index, i)
                Index += 1
            Select = input('请选择索引文件: ')
            if (Select.isdigit()):
                if (int(Select) >= 0 and int(Select) <= Index - 1):
                    print('您选择了{}, 文件路径 {}'.format(Version[int(Select)], './assets/indexes/' + Version[int(Select)]))
                    print('处理中, 请稍后')
                    StartTime = time.time()
                    targetPath = ResourcesCover().processCover('./assets/indexes/' + Version[int(Select)])
                    processTime, processTimeUnit = ResourcesCover().getTimeSub(StartTime, time.time())
                    print('完成! 耗时 \'{} {}\''.format(processTime, processTimeUnit))
                    print('您的文件保存在 \'{}\''.format(targetPath))
                else:
                    print('错误: 请输入一个 0~{} 之间的数字'.format(Index))
            else:
                print('错误: 请输入一个数字')
        else:
            print('错误: 索引文件不存在!')
            os.system('pause')
