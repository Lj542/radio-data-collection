"""
信号处理器模块
实现IQ信号的创建、处理和分析功能
"""

import numpy as np
import logging
from typing import Optional, Tuple, List
from dataclasses import dataclass
import time
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SignalData:
    """信号数据类"""
    data: np.ndarray
    sample_rate: float
    center_freq: float
    timestamp: float
    metadata: dict

class SignalProcessor:
    """信号处理器类"""
    
    def __init__(self, sample_rate: float = 2.4e6, center_freq: float = 98.7e6):
        self.sample_rate = sample_rate
        self.center_freq = center_freq
        self.history = []
    
    def create_iq_array(self, iq_data_list: Optional[List] = None, 
                       sample_rate: Optional[float] = None) -> np.ndarray:
        """
        创建IQ信号数组
        
        参数:
            iq_data_list: IQ数据列表，如 [[I1, Q1], [I2, Q2], ...]
            sample_rate: 采样率
            
        返回:
            IQ信号数组
        """
        if iq_data_list is None:
            # 创建空的IQ数据
            iq_array = np.zeros((1000, 2), dtype=np.float32)
            logger.info("创建了空的IQ数组: %s", iq_array.shape)
        else:
            # 转换为NumPy数组
            iq_array = np.array(iq_data_list, dtype=np.float32)
            logger.info("从列表创建IQ数组: %s", iq_array.shape)
        
        # 添加采样率标注
        if sample_rate is not None:
            # 在数组末尾添加一行标注信息
            info_row = np.array([[sample_rate, 0]], dtype=np.float32)
            iq_array = np.vstack([iq_array, info_row])
            logger.info("添加采样率标注: %s Hz", sample_rate)
        
        return iq_array
    
    def process_iq_data(self, iq_array: np.ndarray) -> dict:
        """
        处理IQ数据
        
        参数:
            iq_array: IQ信号数组
            
        返回:
            处理结果字典
        """
        logger.info("开始处理IQ数据，数组形状: %s", iq_array.shape)
        
        # 检查数组维度
        if len(iq_array.shape) != 2 or iq_array.shape[1] != 2:
            raise ValueError("IQ数组必须是二维数组，形状为 (n, 2)")
        
        print(f"数组维度: {iq_array.shape}")
        print(f"数据类型: {iq_array.dtype}")
        
        # 提取前200组信号
        first_200 = iq_array[:200]
        print(f"前200组信号形状: {first_200.shape}")
        
        # 提取所有Q分量（排除最后一行标注）
        if iq_array.shape[0] > 1 and np.all(iq_array[-1, :] == [iq_array[-1, 0], 0]):
            # 最后一行是标注信息
            q_components = iq_array[:-1, 1]
            i_components = iq_array[:-1, 0]
        else:
            q_components = iq_array[:, 1]
            i_components = iq_array[:, 0]
        
        print(f"Q分量数量: {len(q_components)}")
        
        # 计算I分量均值
        i_mean = np.mean(i_components)
        print(f"I分量均值: {i_mean}")
        
        # 滤波处理：将大于均值的I分量设为0
        filtered_i = np.where(i_components > i_mean, 0, i_components)
        
        # 计算统计信息
        stats = {
            'i_mean': i_mean,
            'i_std': np.std(i_components),
            'q_mean': np.mean(q_components),
            'q_std': np.std(q_components),
            'i_max': np.max(i_components),
            'i_min': np.min(i_components)
        }
        
        logger.info("IQ数据处理完成，I分量均值: %.6f", i_mean)
        
        return {
            'original_i': i_components,
            'filtered_i': filtered_i,
            'q_components': q_components,
            'i_mean': i_mean,
            'stats': stats,
            'first_200_samples': first_200
        }
    
    def save_signal_data(self, iq_array: np.ndarray, filename: str):
        """保存信号数据到文件"""
        try:
            np.save(filename, iq_array)
            logger.info("信号数据已保存到: %s", filename)
            return True
        except Exception as e:
            logger.error("保存信号数据失败: %s", e)
            return False
    
    def load_signal_data(self, filename: str) -> Optional[np.ndarray]:
        """从文件加载信号数据"""
        try:
            data = np.load(filename)
            logger.info("信号数据已从 %s 加载，形状: %s", filename, data.shape)
            return data
        except Exception as e:
            logger.error("加载信号数据失败: %s", e)
            return None

# 兼容性函数 - 保持与原有代码的兼容
def create_iq_array(iq_data_list=None, sample_rate=None):
    """创建IQ数组（兼容函数）"""
    processor = SignalProcessor()
    return processor.create_iq_array(iq_data_list, sample_rate)

def process_iq_data(iq_array):
    """处理IQ数据（兼容函数）"""
    processor = SignalProcessor()
    return processor.process_iq_data(iq_array)

# 测试函数
def test_signal_processor():
    """测试信号处理器"""
    print("测试信号处理器...")
    
    # 创建处理器实例
    processor = SignalProcessor(sample_rate=2.4e6, center_freq=98.7e6)
    
    # 测试创建数组
    test_data = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
    iq_array = processor.create_iq_array(test_data, 2.4e6)
    print(f"创建的数组: {iq_array}")
    
    # 测试处理数据
    result = processor.process_iq_data(iq_array)
    print(f"处理结果 - I均值: {result['i_mean']}")
    
    print("信号处理器测试完成！")

if __name__ == "__main__":
    test_signal_processor()