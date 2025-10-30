#!/usr/bin/env python3
"""
无线电数据采集主程序
提供命令行接口进行信号采集和处理
"""
import argparse
import sys
import logging
from pathlib import Path
import time

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent))

from config.config_handler import ConfigHandler
from signal_process.signal_processor import SignalProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('radio_collection.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='无线电数据采集系统')
    parser.add_argument('--config', '-c', type=str, default='radio_config.json',
                       help='配置文件路径')
    parser.add_argument('--duration', '-d', type=float, default=1.0,
                       help='信号采集时长（秒）')
    parser.add_argument('--output', '-o', type=str, default='data',
                       help='输出目录')
    parser.add_argument('--analyze', '-a', action='store_true',
                       help='是否进行信号分析')
    parser.add_argument('--continuous', action='store_true',
                       help='连续采集模式')
    parser.add_argument('--interval', '-i', type=float, default=5.0,
                       help='连续采集间隔（秒）')
    
    args = parser.parse_args()
    
    try:
        # 初始化配置处理器
        config_handler = ConfigHandler(args.config)
        config = config_handler.load_config()
        
        logger.info("=== 无线电数据采集系统启动 ===")
        logger.info(f"配置文件: {args.config}")
        logger.info(f"中心频率: {config['center_freq']} Hz")
        logger.info(f"采样率: {config['sample_rate']} Hz")
        logger.info(f"设备ID: {config['device_id']}")
        
        # 初始化信号处理器
        processor = SignalProcessor(config_handler)
        
        # 创建输出目录
        output_dir = Path(args.output)
        output_dir.mkdir(exist_ok=True)
        
        if args.continuous:
            # 连续采集模式
            run_continuous_acquisition(processor, output_dir, args.interval)
        else:
            # 单次采集模式
            run_single_acquisition(processor, output_dir, args.duration, args.analyze)
            
    except KeyboardInterrupt:
        logger.info("用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序运行错误: {e}")
        sys.exit(1)

def run_single_acquisition(processor, output_dir, duration, analyze):
    """运行单次信号采集"""
    logger.info(f"开始单次信号采集，时长: {duration} 秒")
    
    # 处理信号
    signal_data = processor.process_signal(duration)
    
    if signal_data is None:
        logger.error("信号采集失败")
        return
    
    # 保存数据
    timestamp = int(signal_data.timestamp)
    filename = f"signal_{timestamp}.npz"
    filepath = output_dir / filename
    
    if processor.save_signal_data(signal_data, str(filepath)):
        logger.info(f"信号数据已保存到: {filepath}")
    else:
        logger.error("信号数据保存失败")
        return
    
    # 信号分析
    if analyze:
        logger.info("开始信号分析...")
        analysis_result = processor.analyze_signal(signal_data)
        
        if analysis_result:
            logger.info("=== 信号分析结果 ===")
            for key, value in analysis_result.items():
                logger.info(f"{key}: {value}")
            
            # 保存分析结果
            analysis_file = output_dir / f"analysis_{timestamp}.txt"
            with open(analysis_file, 'w', encoding='utf-8') as f:
                f.write("=== 信号分析结果 ===\n")
                f.write(f"时间戳: {timestamp}\n")
                f.write(f"中心频率: {signal_data.center_freq} Hz\n")
                f.write(f"采样率: {signal_data.sample_rate} Hz\n")
                f.write(f"数据长度: {len(signal_data.data)}\n\n")
                
                for key, value in analysis_result.items():
                    f.write(f"{key}: {value}\n")
            
            logger.info(f"分析结果已保存到: {analysis_file}")

def run_continuous_acquisition(processor, output_dir, interval):
    """运行连续信号采集"""
    logger.info(f"开始连续信号采集，间隔: {interval} 秒")
    
    try:
        processor.start_continuous_acquisition(str(output_dir))
        
        count = 0
        while True:
            count += 1
            logger.info(f"=== 第 {count} 次采集 ===")
            
            # 采集信号
            signal_data = processor.process_signal(duration=1.0)
            
            if signal_data:
                # 保存数据
                timestamp = int(signal_data.timestamp)
                filename = f"continuous_{count:04d}_{timestamp}.npz"
                filepath = output_dir / filename
                
                if processor.save_signal_data(signal_data, str(filepath)):
                    logger.info(f"数据已保存: {filename}")
                else:
                    logger.error(f"数据保存失败: {filename}")
            
            # 等待下次采集
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("用户中断连续采集")
    finally:
        processor.stop_continuous_acquisition()

if __name__ == "__main__":
    main()
