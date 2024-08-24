import json
from six.moves import urllib
import zipfile
import uuid
import re
import os
import sys

def download_and_extract(url, save_dir, projectId):  
  # 下载结果
  resultId = str(uuid.uuid4())
  save_path = os.path.join(save_dir, resultId+"result.disp")
  urllib.request.urlretrieve(url, save_path)
  print('Successfully downloaded')

  with open(save_path,'r') as f:
    dispStr = f.read()
  
  os.remove(save_path)
  
  dispJson = json.loads(dispStr)

  # 获取用户输入的NodeName LinkName
  nodeFlag = False
  nodeName = dispJson["ObsID"]["NodeName"]
  linkFlag = False
  linkName = dispJson["ObsID"]["LinkName"]

  # 创建X轴标签
  labels = dispJson["Date"]
  label = save_dir + projectId + "labels.dat"
  with open(label, "w") as l:
    l.write(' '.join(labels))
    
  totalResult = []
  # Node
  nodeResults = dispJson["NodeResults"]
  nodeInflow = []
  nodeFlooding = []
  nodeDepth = []
  nodeHead = []
  if nodeName != "": # 指定nodeName
    for node in nodeResults:
      if node["name"] == nodeName:
        nodeFlag = True
        length = len(node["Inflow"])
        nodeInflow.append(sum(node["Inflow"])/length) 
        nodeFlooding.append(sum(node["Flooding"])/length) 
        nodeDepth.append(sum(node["Depth"])/length) 
        nodeHead.append(sum(node["Head"])/length)
        break
  elif not nodeFlag: # 没有指定nodeName 或者 指定名称有误，提取所有node的长时间模拟平均值
    for node in nodeResults:
      length = len(node["Inflow"])
      nodeInflow.append(sum(node["Inflow"])/length) 
      nodeFlooding.append(sum(node["Flooding"])/length) 
      nodeDepth.append(sum(node["Depth"])/length) 
      nodeHead.append(sum(node["Head"])/length) 
  nodeNum = len(nodeInflow)
  totalResult.append(sum(nodeInflow)/nodeNum)
  totalResult.append(sum(nodeFlooding)/nodeNum)
  totalResult.append(sum(nodeDepth)/nodeNum)
  totalResult.append(sum(nodeHead)/nodeNum)
  # Link
  linkResults = dispJson["LinkResults"]
  linkFlow = []
  linkVelocity = []
  linkDepth = []
  linkCapacity = []
  if linkName != "":
    for link in linkResults:
      if link["name"] == linkName:
        linkFlag = True
        length = len(link["Flow"])
        linkFlow.append(sum(link["Flow"])/length) 
        linkVelocity.append(sum(link["Velocity"])/length) 
        linkDepth.append(sum(link["Depth"])/length) 
        linkCapacity.append(sum(link["Capacity"])/length) 
        break
  elif not linkFlag:  # 没有指定linkName，提取所有link的长时间模拟平均值
    for link in linkResults:
      length = len(link["Flow"])
      linkFlow.append(sum(link["Flow"])/length) 
      linkVelocity.append(sum(link["Velocity"])/length) 
      linkDepth.append(sum(link["Depth"])/length) 
      linkCapacity.append(sum(link["Capacity"])/length) 
  linkNum = len(linkFlow)
  totalResult.append(sum(linkFlow)/linkNum)
  totalResult.append(sum(linkVelocity)/linkNum)
  totalResult.append(sum(linkDepth)/linkNum)
  totalResult.append(sum(linkCapacity)/linkNum)

  total = save_dir + projectId + "res_total_output.dat"
  with open(total, "a") as ft:
    ft.write(" ".join(str(i) for i in totalResult))
    ft.write("\n")

  # 提取指定node link的模拟值.
  resNodeInflow = []
  resNodeFlooding = []
  resNodeDepth = []
  resNodeHead = []
  if nodeFlag:
    for node in nodeResults:
      if node["name"] == nodeName:
        resNodeInflow = node["Inflow"]
        resNodeFlooding = node["Flooding"]
        resNodeDepth = node["Depth"]
        resNodeHead = node["Head"]
        break
  # 无论有没有指定node link 都必须生成这些文件
  nodeInflow = save_dir + projectId + "sim_result_Node-Inflow.dat"
  with open(nodeInflow, "a") as ft:
    ft.write(' '.join(str(i) for i in resNodeInflow))
    ft.write("\n")
  nodeFlooding = save_dir + projectId + "sim_result_Node-Flooding.dat"
  with open(nodeFlooding, "a") as ft:
    ft.write(' '.join(str(i) for i in resNodeFlooding))
    ft.write("\n")
  nodeDepth = save_dir + projectId + "sim_result_Node-Depth.dat"
  with open(nodeDepth, "a") as ft:
    ft.write(' '.join(str(i) for i in resNodeDepth))
    ft.write("\n")
  nodeHead = save_dir + projectId + "sim_result_Node-Head.dat"
  with open(nodeHead, "a") as ft:
    ft.write(' '.join(str(i) for i in resNodeHead))
    ft.write("\n")
  
  resLinkFlow = []
  resLinkVelocity = []
  resLinkDepth = []
  resLinkCapacity = []
  if linkFlag:
    for link in linkResults:
      if link["name"] == linkName:
        resLinkFlow = link["Flow"]
        resLinkVelocity = link["Velocity"]
        resLinkDepth = link["Depth"]
        resLinkCapacity = link["Capacity"]
        break
  # 无论有没有指定node link 都必须生成这些文件
  linkFlow = save_dir + projectId + "sim_result_Link-Flow.dat"
  with open(linkFlow, "a") as ft:
    ft.write(' '.join(str(i) for i in resLinkFlow))
    ft.write("\n")
  linkVelocity = save_dir + projectId + "sim_result_Link-Velocity.dat"
  with open(linkVelocity, "a") as ft:
    ft.write(' '.join(str(i) for i in resLinkVelocity))
    ft.write("\n")
  linkDepth = save_dir + projectId + "sim_result_Link-Depth.dat"
  with open(linkDepth, "a") as ft:
    ft.write(' '.join(str(i) for i in resLinkDepth))
    ft.write("\n")
  linkCapacity = save_dir + projectId + "sim_result_Link-Capacity.dat"
  with open(linkCapacity, "a") as ft:
    ft.write(' '.join(str(i) for i in resLinkCapacity))
    ft.write("\n")


  resultForSA = "res_total_output.dat"
  resultIndexs = [0,1,2,3,4,5,6,7]
  resultForDisplay = ["sim_result_Node-Inflow.dat","sim_result_Node-Flooding.dat","sim_result_Node-Depth.dat","sim_result_Node-Head.dat",
                      "sim_result_Link-Flow.dat","sim_result_Link-Velocity.dat","sim_result_Link-Depth.dat","sim_result_Link-Capacity.dat"]
  result = path + "resultIndex.txt"
  with open(result, "w") as r:
    r.write("resultForSA:"+resultForSA+"\n")
    r.write("resultIndexs:"+",".join((str(i) for i in resultIndexs))+"\n")
    r.write("resultForDisplay:"+",".join(resultForDisplay))


if __name__ == '__main__':
  # print(sys.argv)
  path = sys.argv[1]
  # path = "I:/saProjectData/a"
  if sys.argv[2] == "outputForDisplay":
    eventName = sys.argv[2]
    url = sys.argv[3]
  else:
    eventName = sys.argv[4]
    url = sys.argv[5]
  # eventName = "outputForDisplay"
  # url = sys.argv[5]
  # url = "http://172.21.212.30:8060/geodata/gd_8c4067d0-9c2b-11eb-a132-ef6a3a32b5d7"
  save_dir = path[:path.rindex("/")+1] 
  projectId = path[path.rindex("/")+1:]
  if eventName=="outputForDisplay":
    download_and_extract(url, save_dir, projectId)



  