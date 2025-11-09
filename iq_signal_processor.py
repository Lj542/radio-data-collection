"""
IQ信号基础处理脚本（NumPy基础专项任务）
使用NumPy处理模拟IQ信号，掌握"数组创建+属性查看+索引切片"
"""

import numpy as np
import json
import os


def simulate_signal_collect(num_samples=1000):
    """
    模拟IQ信号采集函数（用于生成测试数据）
    
    参数:
        num_samples: 采集样本数量
    
    返回:
        list: IQ信号列表，每个元素为[I, Q]
    """
    # 生成模拟的IQ信号数据
    np.random.seed(42)  # 设置随机种子以便复现
    iq_data = []
    for i in range(num_samples):
        # 生成模拟的I和Q分量（带一些噪声）
        I = np.cos(2 * np.pi * 0.1 * i) + 0.1 * np.random.randn()
        Q = np.sin(2 * np.pi * 0.1 * i) + 0.1 * np.random.randn()
        iq_data.append([I, Q])
    return iq_data


def main():
    """
    主函数：实现NumPy基础操作任务
    """
    print("=" * 60)
    print("IQ信号基础处理脚本 - NumPy基础专项任务")
    print("=" * 60 + "\n")
    
    # ========== 1. 数据准备 ==========
    print("【步骤1】数据准备")
    print("-" * 60)
    
    # 方式1：使用simulate_signal_collect生成数据并转换为NumPy数组
    print("方式1：使用simulate_signal_collect生成数据...")
    iq_list = simulate_signal_collect(1000)
    iq_array_from_list = np.array(iq_list, dtype=np.float32)
    print(f"从列表转换的数组形状: {iq_array_from_list.shape}")
    
    # 方式2：使用np.zeros创建空数组
    print("\n方式2：使用np.zeros创建空数组...")
    iq_array = np.zeros((1000, 2), dtype=np.float32)
    print(f"空数组形状: {iq_array.shape}")
    
    # 使用从列表转换的数组进行后续操作
    iq_array = iq_array_from_list.copy()
    print(f"\n✓ 最终使用的数组形状: {iq_array.shape}")
    print(f"✓ 数组数据类型: {iq_array.dtype}")
    
    # ========== 2. 基础操作 ==========
    print("\n【步骤2】基础操作")
    print("-" * 60)
    
    # 2.1 查看数组属性
    print("2.1 数组属性查看:")
    print(f"  - 数组维度 (.shape): {iq_array.shape}")
    print(f"  - 数据类型 (.dtype): {iq_array.dtype}")
    print(f"  - 数组大小 (.size): {iq_array.size}")
    print(f"  - 数组维度数 (.ndim): {iq_array.ndim}")
    
    # 2.2 切片操作
    print("\n2.2 切片操作:")
    # 提取前200组信号
    first_200 = iq_array[:200]
    print(f"  - 前200组信号形状: {first_200.shape}")
    print(f"  - 前200组信号前5组示例:\n{first_200[:5]}")
    
    # 提取所有信号的Q分量
    q_components = iq_array[:, 1]
    print(f"  - 所有Q分量形状: {q_components.shape}")
    print(f"  - Q分量前10个值: {q_components[:10]}")
    
    # 提取所有信号的I分量
    i_components = iq_array[:, 0]
    print(f"  - 所有I分量形状: {i_components.shape}")
    print(f"  - I分量前10个值: {i_components[:10]}")
    
    # 2.3 简单处理
    print("\n2.3 简单处理:")
    # 计算所有I分量的均值
    i_mean = np.mean(iq_array[:, 0])
    print(f"  - I分量均值: {i_mean:.6f}")
    
    # 用np.where将大于均值的I分量设为0（模拟滤波）
    print("  - 将大于均值的I分量设为0（模拟滤波）...")
    iq_array_filtered = iq_array.copy()
    # 找到大于均值的I分量的索引
    mask = iq_array_filtered[:, 0] > i_mean
    count_filtered = np.sum(mask)
    print(f"  - 需要过滤的点数: {count_filtered}")
    
    # 将大于均值的I分量设为0
    iq_array_filtered[mask, 0] = 0
    
    print(f"  - 滤波后I分量均值: {np.mean(iq_array_filtered[:, 0]):.6f}")
    print(f"  - 滤波前后I分量前10个值对比:")
    print(f"    滤波前: {iq_array[:10, 0]}")
    print(f"    滤波后: {iq_array_filtered[:10, 0]}")
    
    # ========== 3. 衔接Python任务 ==========
    print("\n【步骤3】衔接Python任务 - 读取采样率")
    print("-" * 60)
    
    config_file = 'radio_config.json'
    
    # 尝试读取配置文件
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            sample_rate = config.get('sample_rate', None)
            
            if sample_rate is not None:
                print(f"✓ 成功读取采样率: {sample_rate} Hz ({sample_rate:.2e} Hz)")
                
                # 在数组末尾添加一行作为采样率标注
                # 方式：创建一个新数组，包含原数据和采样率标注
                sample_rate_row = np.array([[sample_rate, 0]], dtype=np.float32)
                iq_array_with_sample_rate = np.vstack([iq_array_filtered, sample_rate_row])
                
                print(f"✓ 添加采样率标注后的数组形状: {iq_array_with_sample_rate.shape}")
                print(f"✓ 数组最后一行（采样率标注）: {iq_array_with_sample_rate[-1]}")
                
                # 分离数据和标注
                iq_data_final = iq_array_with_sample_rate[:-1]  # 除最后一行外的所有数据
                sample_rate_annotation = iq_array_with_sample_rate[-1, 0]  # 最后一行的第一个元素
                
                print(f"✓ 最终IQ数据形状: {iq_data_final.shape}")
                print(f"✓ 采样率标注值: {sample_rate_annotation:.2e} Hz")
                
            else:
                print(f"✗ 配置文件中未找到sample_rate参数")
                print("  使用默认采样率: 2.4e6 Hz")
                sample_rate = 2.4e6
                
        except json.JSONDecodeError as e:
            print(f"✗ JSON解析错误: {e}")
            print("  使用默认采样率: 2.4e6 Hz")
            sample_rate = 2.4e6
        except Exception as e:
            print(f"✗ 读取配置文件时发生错误: {e}")
            print("  使用默认采样率: 2.4e6 Hz")
            sample_rate = 2.4e6
    else:
        print(f"✗ 配置文件不存在: {config_file}")
        print("  提示: 请先运行 radio_manager.py 生成配置文件")
        print("  使用默认采样率: 2.4e6 Hz")
        sample_rate = 2.4e6
    
    # ========== 总结 ==========
    print("\n" + "=" * 60)
    print("任务完成总结")
    print("=" * 60)
    print(f"✓ 数组维度: {iq_array.shape}")
    print(f"✓ 数据类型: {iq_array.dtype}")
    print(f"✓ 前200组信号已提取")
    print(f"✓ Q分量已提取: {q_components.shape}")
    print(f"✓ I分量均值: {i_mean:.6f}")
    print(f"✓ 滤波处理完成: {count_filtered} 个点被过滤")
    print(f"✓ 采样率标注: {sample_rate:.2e} Hz")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()

