from six.moves import urllib
import zipfile
import uuid
import random
import math
import re
import os
import sys
import numpy as np

def download_and_extract(url, save_dir, projectId, number):
  # 下载结果
  resultId = str(uuid.uuid4())
  save_path = os.path.join(save_dir, resultId+"result.zip")
  urllib.request.urlretrieve(url, save_path)
  print('Successfully downloaded')
  # 提取文件
  zip_file = zipfile.ZipFile(save_path)
  zip_file.extract("output.rch", save_dir+resultId+"/")#从zip文件中获得名为filename_fz的文件
  outPath = save_dir +resultId+"/"+ "output.rch"
  zip_file.extract("simSetting.txt", save_dir+resultId+"/")
  simSetting = save_dir+resultId+"/"+"simSetting.txt"
  zip_file.close() # 关闭文件，必须有，释放内存

  os.remove(save_path)
  # 提取模拟设置
  with open(simSetting, 'r', encoding="utf-8") as sim:
    lines = sim.readlines()
    # 模拟日期和水文站所在子流域ID
    simRange = []
    basinId = -1
    timeStep = 1
    for line in lines:  # 这三个玩意是在封装代码里写入的，
      data = line.split(':')
      if data[0] == "simRange": 
        simRange = data[1].split(',')
      elif data[0] == "basinId":
        basinId = int(data[1])
      elif data[0] == "timeStep":
        timeStep = int(data[1]) # 0 daily, 1 monthly, 2 yearly

  # 提取结果
  with open(outPath, 'r', encoding="utf-8") as f:
    lines = f.readlines()[9:]
    # 判断子流域总数
    maxBasin = 0
    for line in lines:
      data = re.split(r"\s+", line)
      if int(data[1]) > maxBasin:
        maxBasin = int(data[1])
      else:
        break

    # 创建X轴标签
    startYear = int(simRange[0].split("-")[0])
    startMonth = int(simRange[0].split("-")[1])
    startDay = int(simRange[0].split("-")[2])
    endYear = int(simRange[1].split("-")[0])
    endMonth = int(simRange[1].split("-")[1])
    endDay = int(simRange[1].split("-")[2])
    labels = []
    for year in range(startYear, endYear+1):
      # 0 daily,
      if timeStep ==0:
        # 要判断闰年，要判断每个月份的天数，暂时先不写了
        pass
      # 1 monthly 一年十二个月+每年共13个数据
      elif timeStep == 1:
        if year == startYear & year != endYear:
          for month in range(startMonth, 13):
            labels.append(str(year) + "-" + str(month)) 
        elif year == startYear & year == endYear:
          for month in range(startMonth, endMonth+1):
            labels.append(str(year) + "-" + str(month)) 
        elif year == endYear:
          for month in range(1, endMonth+1):
            labels.append(str(year) + "-" +str(month))
        else:
          for month in range(1, 13):
            labels.append(str(year) + "-" +str(month))
      # 2 yearly 一年一个数据
      elif timeStep == 2:
        labels.append(str(year))

    label = save_dir + projectId + "labels.dat"
    with open(label, "w") as l:
      l.write(' '.join(labels))

    # 提取流域出口的多年模拟平均值
    if basinId == -1:  # 为空代表没有输入，要用所有要素的模拟平均值用于敏感性分析
      line = lines[len(lines)-maxBasin]
      singleRes = line.split()[6:]
      tmp = []
      for i in singleRes:
        tmp.append(eval(i))
      res = np.array(tmp)
      for i in range(maxBasin):
        line = lines[len(lines)-maxBasin+i]
        singleRes = line.split()[6:]
        tmp = []
        for i in singleRes:
          tmp.append(eval(i))
        singleRes = np.array(tmp)
        res =(res + singleRes)/2

    else:
      line = lines[len(lines)-maxBasin+basinId-1]
      singleRes = line.split()[6:]
      tmp = []
      for i in singleRes:
        tmp.append(eval(i))
      res = np.array(tmp)

    # 记下当前计算任务序号
    res = np.insert(res, 0, number, axis=0)

    total = save_dir + projectId + "res_total_output.dat"
    with open(total, "a") as ft:
      ft.write(' '.join(str(i) for i in res))
      ft.write("\n")

    resFlow = [number]
    resSed = [number]
    resNO3 = [number]
    resNH4 = [number]
    resDO = [number]
    resTN = [number]
    resTP = [number]
    if basinId != -1:
      # 提取指定流域的模拟值
      if timeStep == 1:
        for i in range(basinId-1, len(lines)-maxBasin, maxBasin):
          if startYear == endYear and math.ceil((i+1)/maxBasin) == endMonth-startMonth+2:
            continue
          elif math.ceil((i+1)/maxBasin) == 12-startMonth+2 or math.ceil((i+1+(startMonth-1)*maxBasin)/maxBasin)%13==0:
            continue
          line = re.split(r"\s+", lines[i])
          resFlow.append(float(line[6]))
          resSed.append(float(line[10]))
          resNO3.append(float(line[17]))
          resNH4.append(float(line[19]))
          resDO.append(float(line[29]))
          resTN.append(float(line[47]))
          resTP.append(float(line[48]))
      elif timeStep == 2:
        for i in range(basinId-1, len(lines)-maxBasin, maxBasin):
          line = re.split(r"\s+", lines[i])
          resFlow.append(float(line[6]))
          resSed.append(float(line[10]))
          resNO3.append(float(line[17]))
          resNH4.append(float(line[19]))
          resDO.append(float(line[29]))
          resTN.append(float(line[47]))
          resTP.append(float(line[48]))
    # 无论是否指定流域 都必须生成这些文件
    flow = save_dir + projectId + "sim_result_Flow.dat"
    with open(flow, "a") as ft:
      ft.write(' '.join(str(i) for i in resFlow))
      ft.write("\n")
    sed = save_dir + projectId + "sim_result_Sediment.dat"
    with open(sed, "a") as ft:
      ft.write(' '.join(str(i) for i in resSed))
      ft.write("\n")
    no3 = save_dir + projectId + "sim_result_NO3.dat"
    with open(no3, "a") as ft:
      ft.write(' '.join(str(i) for i in resNO3))
      ft.write("\n")
    nh4 = save_dir + projectId + "sim_result_NH4.dat"
    with open(nh4, "a") as ft:
      ft.write(' '.join(str(i) for i in resNH4))
      ft.write("\n")
    do = save_dir + projectId + "sim_result_DO.dat"
    with open(do, "a") as ft:
      ft.write(' '.join(str(i) for i in resDO))
      ft.write("\n")
    tn = save_dir + projectId + "sim_result_TN.dat"
    with open(tn, "a") as ft:
      ft.write(' '.join(str(i) for i in resTN))
      ft.write("\n")
    tp = save_dir + projectId + "sim_result_TP.dat"
    with open(tp, "a") as ft:
      ft.write(' '.join(str(i) for i in resTP))
      ft.write("\n")
  os.remove(outPath)
  os.remove(simSetting)
  os.rmdir(save_dir +resultId)
  
  resultForSA = "res_total_output.dat"
  resultIndexs = [0,4,11,13,23,41,42]
  resultForDisplay = ["sim_result_Flow.dat", "sim_result_Sediment.dat", "sim_result_NO3.dat", "sim_result_NH4.dat", "sim_result_DO.dat", "sim_result_TN.dat", "sim_result_TP.dat"]
  result = path + "resultIndex.txt"
  with open(result, "w") as r:
    r.write("resultForSA:"+resultForSA+"\n")
    r.write("resultIndexs:"+",".join((str(i) for i in resultIndexs))+"\n")
    r.write("resultForDisplay:"+",".join(resultForDisplay))


if __name__ == '__main__':
  path = sys.argv[1]
  # path = "I:/saProjectData/a"
  eventName = sys.argv[2]
  # eventName = "Output"
  url = sys.argv[3]
  # url = "http://172.21.212.30:8060/geodata/gd_71d6b030-9dec-11eb-a7e0-4f81d7958e3b"
  number = sys.argv[4]
  # number = 1
  save_dir = path[:path.rindex("/")+1]
  projectId = path[path.rindex("/")+1:]
  if eventName=="Output":
    download_and_extract(url, save_dir, projectId, number)