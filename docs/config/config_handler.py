"""
无线电设备配置管理模块
负责配置的保存、读取和验证
"""
import json
import os
from typing import Dict, Any, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 默认配置
DEFAULT_RADIO_CONFIG = {
    "center_freq": 98.7e6,  # 中心频率（单位：Hz）
    "sample_rate": 2.4e6,   # 采样率（单位：Hz）
    "gain": "auto",         # 增益模式
    "device_id": "rtl-sdr-01",  # 设备ID
    "bandwidth": 2.4e6,     # 带宽
    "antenna": "auto",      # 天线设置
    "output_format": "complex64"  # 输出数据格式
}

class ConfigHandler:
    """配置处理器类"""
    
    def __init__(self, config_file: str = "radio_config.json"):
        self.config_file = config_file
        self.config = DEFAULT_RADIO_CONFIG.copy()
    
    def save_config(self, config_dict: Optional[Dict[str, Any]] = None, 
                   file_path: Optional[str] = None) -> bool:
        """
        保存配置到JSON文件
        
        Args:
            config_dict: 要保存的配置字典，如果为None则保存当前配置
            file_path: 保存路径，如果为None则使用默认路径
            
        Returns:
            bool: 保存是否成功
        """
        try:
            target_file = file_path or self.config_file
            config_to_save = config_dict or self.config
            
            # 验证配置
            if not self._validate_config(config_to_save):
                logger.error("配置验证失败")
                return False
            
            with open(target_file, "w", encoding='utf-8') as file:
                json.dump(config_to_save, file, indent=2, ensure_ascii=False)
            
            logger.info(f"配置已保存到 {target_file}")
            return True
            
        except Exception as e:
            logger.error(f"保存配置失败: {e}")
            return False
    
    def load_config(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        从JSON文件读取配置
        
        Args:
            file_path: 配置文件路径，如果为None则使用默认路径
            
        Returns:
            Dict[str, Any]: 配置字典
        """
        try:
            target_file = file_path or self.config_file
            
            if not os.path.exists(target_file):
                logger.warning(f"配置文件 {target_file} 不存在，使用默认配置")
                return DEFAULT_RADIO_CONFIG.copy()
            
            with open(target_file, "r", encoding="utf-8") as file:
                config = json.load(file)
            
            # 验证配置
            if not self._validate_config(config):
                logger.warning("配置文件验证失败，使用默认配置")
                return DEFAULT_RADIO_CONFIG.copy()
            
            self.config = config
            logger.info(f"配置已从 {target_file} 加载")
            return config
            
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return DEFAULT_RADIO_CONFIG.copy()
    
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置的有效性
        
        Args:
            config: 要验证的配置字典
            
        Returns:
            bool: 配置是否有效
        """
        required_keys = ["center_freq", "sample_rate", "gain", "device_id"]
        
        # 检查必需键
        for key in required_keys:
            if key not in config:
                logger.error(f"缺少必需的配置项: {key}")
                return False
        
        # 检查数值范围
        if not isinstance(config["center_freq"], (int, float)) or config["center_freq"] <= 0:
            logger.error("中心频率必须是正数")
            return False
        
        if not isinstance(config["sample_rate"], (int, float)) or config["sample_rate"] <= 0:
            logger.error("采样率必须是正数")
            return False
        
        return True
    
    def update_config(self, **kwargs) -> bool:
        """
        更新配置参数
        
        Args:
            **kwargs: 要更新的配置参数
            
        Returns:
            bool: 更新是否成功
        """
        try:
            for key, value in kwargs.items():
                if key in self.config:
                    self.config[key] = value
                    logger.info(f"配置项 {key} 已更新为 {value}")
                else:
                    logger.warning(f"未知的配置项: {key}")
            
            return True
        except Exception as e:
            logger.error(f"更新配置失败: {e}")
            return False
    
    def get_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        return self.config.copy()

# 创建全局配置实例
config_handler = ConfigHandler()

# 向后兼容的函数接口
def save_config(file_path: str, config_dict: Dict[str, Any]) -> bool:
    """保存配置的兼容函数"""
    return config_handler.save_config(config_dict, file_path)

def load_config(file_path: str) -> Dict[str, Any]:
    """加载配置的兼容函数"""
    return config_handler.load_config(file_path)

# 导出默认配置
radio_config = DEFAULT_RADIO_CONFIG
