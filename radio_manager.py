"""
无线电设备参数管理工具
使用字典、文件I/O和异常处理实现设备参数的读写管理
"""

import json
import os


# 1. 用字典定义设备参数
device_config = {
    'center_freq': 98.7e6,      # 中心频率（Hz）
    'sample_rate': 2.4e6,       # 采样率（Hz）
    'gain': 'auto',             # 增益
    'device_id': 'rtl-sdr-01'   # 设备ID
}


def save_config(file_path, config_dict):
    """
    将参数字典写入JSON文件
    
    参数:
        file_path: 目标JSON文件路径
        config_dict: 要保存的配置字典
    
    异常:
        IOError: 文件写入失败
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, indent=4, ensure_ascii=False)
        print(f"✓ 配置已成功保存到: {file_path}")
    except IOError as e:
        print(f"✗ 文件写入失败: {e}")


def load_config(file_path):
    """
    从JSON文件读取参数，捕获多种错误情况
    
    参数:
        file_path: JSON文件路径
    
    返回:
        dict: 加载的配置字典，失败时返回None
    
    捕获的异常:
        1. FileNotFoundError: 文件不存在
        2. json.JSONDecodeError: JSON格式错误
        3. KeyError: 关键参数缺失
    """
    try:
        # 尝试打开文件
        with open(file_path, 'r', encoding='utf-8') as f:
            config_dict = json.load(f)
        
        # 检查关键参数是否存在
        required_keys = ['center_freq', 'sample_rate', 'gain', 'device_id']
        missing_keys = [key for key in required_keys if key not in config_dict]
        
        if missing_keys:
            raise KeyError(f"关键参数缺失: {', '.join(missing_keys)}")
        
        print(f"✓ 配置已成功加载: {file_path}")
        return config_dict
        
    except FileNotFoundError:
        print(f"✗ 错误：文件不存在 - {file_path}")
        return None
        
    except json.JSONDecodeError as e:
        print(f"✗ 错误：JSON格式错误 - {e}")
        return None
        
    except KeyError as e:
        print(f"✗ 错误：{e}")
        return None


def display_config(config_dict, title="设备配置"):
    """
    格式化显示配置信息
    
    参数:
        config_dict: 配置字典
        title: 显示标题
    """
    if config_dict is None:
        print("\n配置为空\n")
        return
    
    print(f"\n{title}:")
    print("=" * 50)
    for key, value in config_dict.items():
        if isinstance(value, float):
            # 科学计数法显示
            print(f"  {key:15s}: {value:.2e}")
        else:
            print(f"  {key:15s}: {value}")
    print("=" * 50)


if __name__ == '__main__':
    # 测试配置文件的路径
    config_file = 'radio_config.json'
    
    print("\n" + "="*60)
    print("无线电设备参数管理 - 测试运行")
    print("="*60 + "\n")
    
    # 测试1: 保存配置
    print("【测试1】保存配置到文件...")
    print(f"原始配置字典: {device_config}")
    save_config(config_file, device_config)
    
    # 测试2: 加载配置
    print("\n【测试2】从文件加载配置...")
    loaded_config = load_config(config_file)
    display_config(loaded_config)
    
    # 测试3: 删除文件后尝试加载（捕获文件不存在错误）
    print("\n【测试3】删除文件后尝试加载...")
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"已删除文件: {config_file}")
    load_config(config_file)
    
    # 测试4: 创建格式错误的JSON文件
    print("\n【测试4】测试JSON格式错误处理...")
    corrupted_file = 'corrupted_config.json'
    with open(corrupted_file, 'w', encoding='utf-8') as f:
        f.write('{ invalid json }')
    load_config(corrupted_file)
    if os.path.exists(corrupted_file):
        os.remove(corrupted_file)
    
    # 测试5: 创建缺少关键参数的JSON文件
    print("\n【测试5】测试关键参数缺失处理...")
    incomplete_file = 'incomplete_config.json'
    incomplete_config = {'center_freq': 98.7e6, 'sample_rate': 2.4e6}
    # 缺少 gain 和 device_id
    with open(incomplete_file, 'w', encoding='utf-8') as f:
        json.dump(incomplete_config, f, indent=4)
    load_config(incomplete_file)
    if os.path.exists(incomplete_file):
        os.remove(incomplete_file)
    
    print("\n" + "="*60)
    print("测试完成!")
    print("="*60 + "\n")

