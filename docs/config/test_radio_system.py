"""
测试模块
用于验证配置和信号处理功能
"""
import unittest
import tempfile
import os
import numpy as np
from pathlib import Path

# 添加项目根目录到Python路径
import sys
sys.path.append(str(Path(__file__).parent))

from config.config_handler import ConfigHandler, DEFAULT_RADIO_CONFIG
from signal_process.signal_processor import SignalProcessor, SignalData

class TestConfigHandler(unittest.TestCase):
    """配置处理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        self.config_handler = ConfigHandler(self.config_file)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_default_config(self):
        """测试默认配置"""
        config = self.config_handler.get_config()
        self.assertEqual(config["center_freq"], DEFAULT_RADIO_CONFIG["center_freq"])
        self.assertEqual(config["sample_rate"], DEFAULT_RADIO_CONFIG["sample_rate"])
    
    def test_save_and_load_config(self):
        """测试配置保存和加载"""
        test_config = {
            "center_freq": 100e6,
            "sample_rate": 1e6,
            "gain": "manual",
            "device_id": "test-device"
        }
        
        # 保存配置
        result = self.config_handler.save_config(test_config)
        self.assertTrue(result)
        
        # 加载配置
        loaded_config = self.config_handler.load_config()
        self.assertEqual(loaded_config["center_freq"], test_config["center_freq"])
        self.assertEqual(loaded_config["device_id"], test_config["device_id"])
    
    def test_config_validation(self):
        """测试配置验证"""
        # 测试无效配置
        invalid_config = {
            "center_freq": -100,  # 负数频率
            "sample_rate": 1e6,
            "gain": "auto",
            "device_id": "test"
        }
        
        result = self.config_handler.save_config(invalid_config)
        self.assertFalse(result)

class TestSignalProcessor(unittest.TestCase):
    """信号处理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
        self.config_handler = ConfigHandler(self.config_file)
        self.processor = SignalProcessor(self.config_handler)
    
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_signal_processing(self):
        """测试信号处理"""
        signal_data = self.processor.process_signal(duration=0.1)
        
        self.assertIsNotNone(signal_data)
        self.assertIsInstance(signal_data.data, np.ndarray)
        self.assertGreater(len(signal_data.data), 0)
        self.assertEqual(signal_data.sample_rate, DEFAULT_RADIO_CONFIG["sample_rate"])
    
    def test_signal_analysis(self):
        """测试信号分析"""
        signal_data = self.processor.process_signal(duration=0.1)
        
        if signal_data:
            analysis = self.processor.analyze_signal(signal_data)
            self.assertIsInstance(analysis, dict)
            self.assertIn("power", analysis)
            self.assertIn("amplitude", analysis)
    
    def test_save_and_load_signal_data(self):
        """测试信号数据保存和加载"""
        signal_data = self.processor.process_signal(duration=0.1)
        
        if signal_data:
            file_path = os.path.join(self.temp_dir, "test_signal.npz")
            
            # 保存数据
            result = self.processor.save_signal_data(signal_data, file_path)
            self.assertTrue(result)
            
            # 加载数据
            loaded_data = self.processor.load_signal_data(file_path)
            self.assertIsNotNone(loaded_data)
            self.assertEqual(len(loaded_data.data), len(signal_data.data))

def run_tests():
    """运行所有测试"""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests()
