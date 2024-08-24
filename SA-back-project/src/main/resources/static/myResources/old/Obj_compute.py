import sys
import numpy as np

def compute(obs_data, sim_single):
  # NSE
  nse = 1 - sum(pow(obs_data - sim_single, 2)) / sum(pow(obs_data - obs_data.mean(),2))
  
  # RSquared
  rsquared = pow(sum((obs_data - obs_data.mean())*(sim_single - sim_single.mean())),2) / (sum(pow((obs_data - obs_data.mean()),2))*sum(pow((sim_single - sim_single.mean()),2)))
  
  # PBAIS
  pbais = 100 * sum((obs_data - sim_single)) / sum(obs_data)

  # RMSE
  rmse = np.sqrt(sum(pow((obs_data - sim_single),2)) / len(obs_data))

  #MAPE
  mape = sum(abs(obs_data - sim_single)*100/obs_data) / len(obs_data)
  
  return [nse, rsquared, pbais, rmse, mape]

path = sys.argv[1]
# path = "I:/saProjectData/"
eventName = sys.argv[2]
# eventName = "Flow"
if __name__ == '__main__':
  # 读取观测数据与模拟数据
  # 第一行用#开头 作为注释行
  obs_data = np.loadtxt(path+"obs_"+eventName+".txt", dtype=float, comments='#',usecols=(0), unpack=True)
  sim_data = np.loadtxt(path+"sim_result_"+eventName+".dat", delimiter=" ")

  # 计算每次模拟结果的评价指标得分
  objs = []
  for sim_single in sim_data:
    single = sim_single[0:len(obs_data)]
    obj = compute(obs_data, single)
    objs.append(obj)
  
  # 将结果写入文件
  obj_file_path = path+"obj_"+eventName+".dat"
  title = ["NSE","RSquared","PBAIS","RMSE","MAPE"]
  with open(obj_file_path, 'w') as ft:
    ft.write(' '.join(title) + "\n")
    for obj in objs:
      ft.write(' '.join(str(i) for i in obj) + "\n")
      
  print("计算并保存完毕 -- " + obj_file_path)
