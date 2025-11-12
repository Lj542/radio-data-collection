"""
工具包使用示例
"""

from radio_basic_toolkit import *

# 示例1: 基本配置管理
print("=== 示例1: 配置管理 ===")
config = {
    'center_freq': 100e6,
    'sample_rate': 2.4e6,
    'gain': 'high',
    'device_id': 'rtl-sdr-demo'
}

save_config('demo_config.json', config)
loaded = load_config('demo_config.json')
print(f"加载的配置: {loaded}")

# 示例2: 信号采集与处理
print("\n=== 示例2: 信号处理 ===")
iq_data = simulate_signal_collect(0.05, 1.2e6)  # 50ms采集
iq_array = create_iq_array(iq_data, 1.2e6)
result = process_iq_data(iq_array)

print(f"处理结果 - I分量均值: {result['i_mean']:.4f}")