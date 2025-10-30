# Radio Data Collection System

无线电硬件与数据采集系统 - 一个用于无线电信号采集、处理和存储的Python框架。

## 功能特性

- 🔧 **配置管理**: 灵活的JSON配置文件管理
- 📡 **信号采集**: 支持RTL-SDR等硬件设备的信号采集
- 🔍 **信号处理**: 内置信号预处理和分析功能
- 💾 **数据存储**: 高效的NumPy格式数据存储
- 📊 **信号分析**: 自动信号特征提取和分析
- 🔄 **连续采集**: 支持连续模式信号采集
- 📝 **日志记录**: 完整的操作日志记录

## 项目结构

```
radio-data-collection/
├── config/                 # 配置模块
│   ├── config_handler.py   # 配置处理器
│   └── README.md           # 配置说明
├── signal_process/         # 信号处理模块
│   ├── signal_processor.py # 信号处理器
│   └── README.md           # 信号处理说明
├── docs/                   # 文档目录
│   └── README.md           # 文档说明
├── main.py                 # 主程序入口
├── test_radio_system.py    # 测试文件
├── requirements.txt        # 依赖包列表
└── README.md              # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 基本使用

#### 单次信号采集
```bash
python main.py --duration 5.0 --analyze
```

#### 连续信号采集
```bash
python main.py --continuous --interval 10.0
```

#### 自定义配置
```bash
python main.py --config my_config.json --output ./my_data
```

### 3. 编程接口使用

```python
from config.config_handler import ConfigHandler
from signal_process.signal_processor import SignalProcessor

# 初始化配置
config_handler = ConfigHandler("config.json")
config_handler.load_config()

# 初始化信号处理器
processor = SignalProcessor(config_handler)

# 处理信号
signal_data = processor.process_signal(duration=1.0)

# 分析信号
if signal_data:
    analysis = processor.analyze_signal(signal_data)
    print(f"信号功率: {analysis['power']}")
    print(f"主频率: {analysis['main_frequency']} Hz")
```

## 配置说明

系统使用JSON格式的配置文件，默认配置如下：

```json
{
  "center_freq": 98.7e6,
  "sample_rate": 2.4e6,
  "gain": "auto",
  "device_id": "rtl-sdr-01",
  "bandwidth": 2.4e6,
  "antenna": "auto",
  "output_format": "complex64"
}
```

### 配置参数说明

- `center_freq`: 中心频率（Hz）
- `sample_rate`: 采样率（Hz）
- `gain`: 增益模式（"auto" 或数值）
- `device_id`: 设备标识符
- `bandwidth`: 带宽（Hz）
- `antenna`: 天线设置
- `output_format`: 输出数据格式

## 命令行参数

```bash
python main.py [选项]

选项:
  -h, --help              显示帮助信息
  -c, --config CONFIG     配置文件路径 (默认: radio_config.json)
  -d, --duration DURATION 信号采集时长（秒） (默认: 1.0)
  -o, --output OUTPUT     输出目录 (默认: data)
  -a, --analyze           是否进行信号分析
  --continuous            连续采集模式
  -i, --interval INTERVAL 连续采集间隔（秒） (默认: 5.0)
```

## 测试

运行测试套件：

```bash
python test_radio_system.py
```

## 开发指南

### 添加新的硬件支持

1. 在 `signal_process/signal_processor.py` 中修改 `_simulate_signal_acquisition` 方法
2. 实现具体的硬件接口调用
3. 更新 `requirements.txt` 添加相应的硬件驱动依赖

### 扩展信号处理功能

1. 在 `SignalProcessor` 类中添加新的处理方法
2. 更新 `analyze_signal` 方法添加新的分析指标
3. 在测试文件中添加相应的测试用例

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至项目维护者
