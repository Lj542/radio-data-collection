参数配置脚本
#Config模块：负责无线电设备的配置管理，包括配置的保存与读取   
import json                         
radio_config = {
    #中心频率（单位：HZ)
    "center_freg":98.7e6,
    #采样率(单位：HZ)
    "sample_rate":2.4e6,
    #增益模式
    "gain":"auto",
    #设备ID,RTL-sdr无线电信号接收器
    "device_id":"rtl-sdr-01"
} 
def save_config(file_path,config_dict):
 with open(file_path("w"),encoding='utf-8')as file:
    json.dump(config_dict.file,indent=2)
    print(f"配置已保存好{file_path}")
def load_config(file_path):
#读取JSON文件并返回字典
 with open(file_path,"r",encoding="utf-8")as file:
    return json.load(file)
