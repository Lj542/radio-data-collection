"""
信号处理模块
负责无线电信号的采集、处理和存储
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
    """信号数据结构"""
    data: np.ndarray
    sample_rate: float
    center_freq: float
    timestamp: float
    metadata: dict

class SignalProcessor:
    """信号处理器类"""
    
    def __init__(self, config_handler):
        """
        初始化信号处理器
        
        Args:
            config_handler: 配置处理器实例
        """
        self.config_handler = config_handler
        self.config = config_handler.get_config()
        self.is_running = False
        
    def process_signal(self, duration: float = 1.0) -> Optional[SignalData]:
        """
        处理信号数据
        
        Args:
            duration: 信号采集时长（秒）
            
        Returns:
            SignalData: 处理后的信号数据，失败时返回None
        """
        try:
            logger.info(f"开始处理信号，中心频率：{self.config['center_freq']} Hz")
            logger.info(f"采样率：{self.config['sample_rate']} Hz")
            
            # 模拟信号采集（实际项目中这里会连接真实的硬件）
            signal_data = self._simulate_signal_acquisition(duration)
            
            if signal_data is None:
                logger.error("信号采集失败")
                return None
            
            # 信号预处理
            processed_data = self._preprocess_signal(signal_data)
            
            # 创建信号数据对象
            signal_obj = SignalData(
                data=processed_data,
                sample_rate=self.config['sample_rate'],
                center_freq=self.config['center_freq'],
                timestamp=time.time(),
                metadata={
                    'device_id': self.config['device_id'],
                    'gain': self.config['gain'],
                    'duration': duration,
                    'data_type': 'complex64'
                }
            )
            
            logger.info(f"信号处理完成，数据长度：{len(processed_data)}")
            return signal_obj
            
        except Exception as e:
            logger.error(f"信号处理失败: {e}")
            return None
    
    def _simulate_signal_acquisition(self, duration: float) -> Optional[np.ndarray]:
        """
        模拟信号采集（实际项目中替换为真实硬件接口）
        
        Args:
            duration: 采集时长
            
        Returns:
            np.ndarray: 采集的信号数据
        """
        try:
            sample_rate = self.config['sample_rate']
            num_samples = int(sample_rate * duration)
            
            # 生成模拟的复数信号数据
            # 实际项目中这里会调用RTL-SDR或其他硬件接口
            real_part = np.random.normal(0, 0.1, num_samples)
            imag_part = np.random.normal(0, 0.1, num_samples)
            signal = real_part + 1j * imag_part
            
            logger.info(f"模拟采集了 {num_samples} 个样本")
            return signal
            
        except Exception as e:
            logger.error(f"信号采集模拟失败: {e}")
            return None
    
    def _preprocess_signal(self, signal: np.ndarray) -> np.ndarray:
        """
        信号预处理
        
        Args:
            signal: 原始信号数据
            
        Returns:
            np.ndarray: 预处理后的信号
        """
        try:
            # 归一化
            signal_normalized = signal / np.max(np.abs(signal))
            
            # 简单的滤波（实际项目中可以使用更复杂的滤波器）
            # 这里使用移动平均滤波器
            window_size = min(100, len(signal_normalized) // 10)
            if window_size > 1:
                kernel = np.ones(window_size) / window_size
                signal_filtered = np.convolve(signal_normalized, kernel, mode='same')
            else:
                signal_filtered = signal_normalized
            
            logger.info("信号预处理完成")
            return signal_filtered
            
        except Exception as e:
            logger.error(f"信号预处理失败: {e}")
            return signal
    
    def analyze_signal(self, signal_data: SignalData) -> dict:
        """
        分析信号特征
        
        Args:
            signal_data: 信号数据对象
            
        Returns:
            dict: 分析结果
        """
        try:
            data = signal_data.data
            
            # 计算信号功率
            power = np.mean(np.abs(data) ** 2)
            
            # 计算信号幅度
            amplitude = np.mean(np.abs(data))
            
            # 计算频谱
            fft_data = np.fft.fft(data)
            spectrum = np.abs(fft_data)
            
            # 找到主频率
            freqs = np.fft.fftfreq(len(data), 1/signal_data.sample_rate)
            main_freq_idx = np.argmax(spectrum)
            main_freq = freqs[main_freq_idx]
            
            analysis_result = {
                'power': float(power),
                'amplitude': float(amplitude),
                'main_frequency': float(main_freq),
                'snr_estimate': float(10 * np.log10(power / (np.var(data) + 1e-10))),
                'spectrum_peak': float(np.max(spectrum)),
                'data_length': len(data)
            }
            
            logger.info(f"信号分析完成，主频率：{main_freq:.2f} Hz")
            return analysis_result
            
        except Exception as e:
            logger.error(f"信号分析失败: {e}")
            return {}
    
    def save_signal_data(self, signal_data: SignalData, file_path: str) -> bool:
        """
        保存信号数据到文件
        
        Args:
            signal_data: 信号数据对象
            file_path: 保存路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保目录存在
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存为numpy格式
            np.savez_compressed(
                file_path,
                data=signal_data.data,
                sample_rate=signal_data.sample_rate,
                center_freq=signal_data.center_freq,
                timestamp=signal_data.timestamp,
                metadata=signal_data.metadata
            )
            
            logger.info(f"信号数据已保存到 {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"保存信号数据失败: {e}")
            return False
    
    def load_signal_data(self, file_path: str) -> Optional[SignalData]:
        """
        从文件加载信号数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            SignalData: 加载的信号数据，失败时返回None
        """
        try:
            data = np.load(file_path)
            
            signal_data = SignalData(
                data=data['data'],
                sample_rate=float(data['sample_rate']),
                center_freq=float(data['center_freq']),
                timestamp=float(data['timestamp']),
                metadata=data['metadata'].item() if 'metadata' in data else {}
            )
            
            logger.info(f"信号数据已从 {file_path} 加载")
            return signal_data
            
        except Exception as e:
            logger.error(f"加载信号数据失败: {e}")
            return None
    
    def start_continuous_acquisition(self, output_dir: str = "data") -> bool:
        """
        开始连续信号采集
        
        Args:
            output_dir: 输出目录
            
        Returns:
            bool: 启动是否成功
        """
        try:
            self.is_running = True
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            logger.info(f"开始连续信号采集，输出目录：{output_dir}")
            
            # 这里可以实现连续采集逻辑
            # 实际项目中可能需要多线程或异步处理
            
            return True
            
        except Exception as e:
            logger.error(f"启动连续采集失败: {e}")
            return False
    
    def stop_continuous_acquisition(self) -> bool:
        """
        停止连续信号采集
        
        Returns:
            bool: 停止是否成功
        """
        try:
            self.is_running = False
            logger.info("连续信号采集已停止")
            return True
            
        except Exception as e:
            logger.error(f"停止连续采集失败: {e}")
            return False

# 便捷函数
def process_signal(config_handler, duration: float = 1.0) -> Optional[SignalData]:
    """
    处理信号的便捷函数
    
    Args:
        config_handler: 配置处理器
        duration: 采集时长
        
    Returns:
        SignalData: 处理后的信号数据
    """
    processor = SignalProcessor(config_handler)
    return processor.process_signal(duration)
