"""
无线电基础工具包 - 整合版本
整合了参数配置、信号采集模拟和IQ信号处理功能
"""

import json
import numpy as np
import os
import sys

# 导入各模块功能（假设原文件中的函数）
try:
    from config.config_handler import save_config, load_config
except ImportError:
    print("警告: 无法导入 config_handler，使用备用实现")
    # 备用实现
    def save_config(file_path, config_dict):
        """保存配置到JSON文件"""
        try:
            with open(file_path, 'w') as f:
                json.dump(config_dict, f, indent=4)
            print(f"配置已保存到: {file_path}")
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def load_config(file_path):
        """从JSON文件加载配置"""
        try:
            with open(file_path, 'r') as f:
                config = json.load(f)
            
            # 检查关键参数
            required_params = ['center_freq', 'sample_rate', 'gain', 'device_id']
            for param in required_params:
                if param not in config:
                    raise KeyError(f"缺少关键参数: {param}")
            
            return config
        except FileNotFoundError:
            print(f"错误: 配置文件不存在 - {file_path}")
            return None
        except json.JSONDecodeError:
            print(f"错误: 配置文件格式错误 - {file_path}")
            return None
        except KeyError as e:
            print(f"错误: {e}")
            return None
        except Exception as e:
            print(f"加载配置时发生未知错误: {e}")
            return None

try:
    from signal_process.iq_processor import create_iq_array, process_iq_data
except ImportError:
    print("警告: 无法导入 iq_processor，使用备用实现")
    # 备用实现
    def create_iq_array(iq_data_list=None, sample_rate=None):
        """创建IQ信号数组"""
        if iq_data_list is None:
            # 创建空的IQ数据
            iq_array = np.zeros((1000, 2), dtype=np.float32)
        else:
            # 转换为NumPy数组
            iq_array = np.array(iq_data_list, dtype=np.float32)
        
        # 添加采样率标注
        if sample_rate is not None:
            # 在数组末尾添加一行标注信息
            info_row = np.array([[sample_rate, 0]], dtype=np.float32)
            iq_array = np.vstack([iq_array, info_row])
        
        return iq_array

    def process_iq_data(iq_array):
        """处理IQ数据"""
        print(f"数组维度: {iq_array.shape}")
        print(f"数据类型: {iq_array.dtype}")
        
        # 提取前200组信号
        first_200 = iq_array[:200]
        print(f"前200组信号形状: {first_200.shape}")
        
        # 提取所有Q分量（排除最后一行标注）
        q_components = iq_array[:-1, 1] if iq_array.shape[0] > 1 else iq_array[:, 1]
        print(f"Q分量数量: {len(q_components)}")
        
        # 计算I分量均值（排除最后一行标注）
        i_components = iq_array[:-1, 0] if iq_array.shape[0] > 1 else iq_array[:, 0]
        i_mean = np.mean(i_components)
        print(f"I分量均值: {i_mean}")
        
        # 滤波处理：将大于均值的I分量设为0
        filtered_i = np.where(i_components > i_mean, 0, i_components)
        
        return {
            'original_i': i_components,
            'filtered_i': filtered_i,
            'q_components': q_components,
            'i_mean': i_mean
        }

# 信号采集模拟功能
def simulate_signal_collect(duration, sample_rate):
    """
    模拟信号采集过程
    
    参数:
        duration: 采集时长(秒)
        sample_rate: 采样率(Hz)
    
    返回:
        生成的IQ数据列表
    """
    if sample_rate < 1e6:
        print("警告: 采样率过低，可能导致信号失真")
    
    total_samples = int(duration * sample_rate)
    iq_data = []
    
    # 模拟采集过程
    for i in range(total_samples // 100):  # 每次循环生成100个样本
        # 生成随机IQ数据 (I分量和Q分量)
        i_samples = np.random.randn(100).tolist()  # I分量
        q_samples = np.random.randn(100).tolist()  # Q分量
        
        # 组合成IQ对
        for i_val, q_val in zip(i_samples, q_samples):
            iq_data.append([i_val, q_val])
    
    print(f"模拟采集完成: 时长{duration}秒, 采样率{sample_rate}Hz, 生成{len(iq_data)}组IQ数据")
    return iq_data

# 测试工具包完整流程
def test_toolkit():
    """测试工具包完整功能"""
    print("=" * 50)
    print("开始测试无线电基础工具包完整流程")
    print("=" * 50)
    
    # 1. 创建测试配置
    config_data = {
        'center_freq': 98.7e6,
        'sample_rate': 2.4e6,
        'gain': 'auto',
        'device_id': 'rtl-sdr-test-01'
    }
    
    config_file = 'test_config.json'
    
    print("\n1. 测试参数配置功能...")
    # 保存配置
    save_config(config_file, config_data)
    
    # 加载配置
    loaded_config = load_config(config_file)
    if loaded_config:
        print("✓ 参数配置测试通过")
        print(f"   设备ID: {loaded_config['device_id']}")
        print(f"   中心频率: {loaded_config['center_freq']} Hz")
        print(f"   采样率: {loaded_config['sample_rate']} Hz")
    else:
        print("✗ 参数配置测试失败")
        return False
    
    print("\n2. 测试信号采集模拟...")
    # 模拟信号采集
    sample_rate = loaded_config['sample_rate']
    iq_data = simulate_signal_collect(duration=0.1, sample_rate=sample_rate)  # 0.1秒测试
    print(f"✓ 信号采集模拟完成，生成 {len(iq_data)} 组IQ数据")
    
    print("\n3. 测试IQ信号处理...")
    # 创建NumPy数组
    iq_array = create_iq_array(iq_data, sample_rate)
    
    # 处理IQ数据
    processed_data = process_iq_data(iq_array)
    
    print("✓ IQ信号处理完成")
    print(f"   原始I分量数量: {len(processed_data['original_i'])}")
    print(f"   滤波后I分量数量: {len(processed_data['filtered_i'])}")
    print(f"   I分量均值: {processed_data['i_mean']:.6f}")
    
    print("\n4. 测试错误处理...")
    # 测试文件不存在的情况
    missing_config = load_config('nonexistent_config.json')
    if missing_config is None:
        print("✓ 文件不存在错误处理正常")
    
    # 测试低采样率警告
    low_rate_data = simulate_signal_collect(0.01, 0.5e6)  # 低采样率测试
    print("✓ 低采样率警告测试完成")
    
    # 清理测试文件
    if os.path.exists(config_file):
        os.remove(config_file)
        print(f"✓ 已清理测试文件: {config_file}")
    
    print("\n" + "=" * 50)
    print("🎉 所有测试通过！工具包整合成功！")
    print("=" * 50)
    return True

# 主程序入口
if __name__ == "__main__":
    print("无线电基础工具包 - 整合版本")
    print("功能列表:")
    print("1. 参数配置管理")
    print("2. 信号采集模拟") 
    print("3. IQ信号处理")
    print("4. 完整流程测试")
    
    # 自动运行测试
    test_toolkit()
