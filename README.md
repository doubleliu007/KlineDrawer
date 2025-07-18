# KlineDrawer

[![版本](https://img.shields.io/badge/版本-0.0.4-blue.svg)](https://github.com/DoubleLiu/KlineDrawer)
[![Python版本](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)
[![许可证](https://img.shields.io/badge/许可证-MIT-orange.svg)](LICENSE)

## 项目简介

KlineDrawer 是一个专为股票技术分析而设计的 Python 库，提供了强大且灵活的 K 线图绘制功能。该库支持多种图表定制选项，包括垂直标记线、散点标记、网格线等，帮助用户进行更直观的股票技术分析。

## 主要特性

- **📊 专业 K 线图绘制** - 基于 mplfinance 库，提供专业级的 K 线图显示
- **📈 成交量显示** - 自动在图表下方显示成交量信息
- **🎯 自定义标记** - 支持在特定日期添加垂直线和散点标记
- **🎨 丰富的可视化选项** - 支持自定义颜色、大小、样式等
- **📅 灵活的日期范围** - 可以指定任意时间范围进行绘制
- **💾 多种保存格式** - 支持高质量图片保存
- **🔌 数据源集成** - 与 TushareDataLoader 无缝集成

## 安装方法

### 使用 pip 安装

```bash
pip install KlineDrawer
```

### 从源码安装

```bash
git clone https://github.com/DoubleLiu/KlineDrawer.git
cd KlineDrawer
pip install -e .
```

### 依赖要求

```bash
pip install pandas mplfinance matplotlib TushareDataLoader
```

## 快速开始

### 基础用法

```python
from KlineDrawer import KlineDrawer
import datetime

# 创建绘制器实例
drawer = KlineDrawer()

# 绘制基础 K 线图
drawer.draw_kline(
    stock_code="000001.SZ",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 12, 31),
    save_path="基础K线图.png"
)
```

### 高级用法

```python
from KlineDrawer import KlineDrawer
import datetime
import pandas as pd

# 创建绘制器实例
drawer = KlineDrawer()

# 准备自定义数据
kdata = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=100),
    'Open': [100 + i for i in range(100)],
    'High': [105 + i for i in range(100)],
    'Low': [95 + i for i in range(100)],
    'Close': [102 + i for i in range(100)],
    'Volume': [1000000 + i*10000 for i in range(100)]
})
kdata.set_index('date', inplace=True)

# 定义标记点
mark_dict = {
    'buy_signals': [True if i % 20 == 0 else False for i in range(100)],
    'sell_signals': [True if i % 25 == 0 else False for i in range(100)]
}

# 绘制包含标记的 K 线图
drawer.draw_kline(
    stock_code="000001.SZ",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 4, 10),
    kdata=kdata,
    save_path="高级K线图.png",
    vlines_dates=[datetime.date(2023, 2, 1), datetime.date(2023, 3, 1)],
    vlines_colors=['red', 'blue'],
    mark_list_dict=mark_dict,
    mark_list_sizes={'buy_signals': 100, 'sell_signals': 80},
    mark_list_colors={'buy_signals': 'green', 'sell_signals': 'red'}
)
```

## API 文档

### KlineDrawer 类

#### draw_kline 方法

绘制 K 线图的主要方法。

```python
def draw_kline(self, stock_code, start_date, end_date, kdata=None, 
               save_path=None, vlines_dates=None, vlines_colors=None,
               mark_list_dict=None, mark_list_sizes=None, mark_list_colors=None):
```

**参数说明:**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `stock_code` | `str` | ✅ | 股票代码，如 "000001.SZ" |
| `start_date` | `datetime.date` | ✅ | 开始日期 |
| `end_date` | `datetime.date` | ✅ | 结束日期 |
| `kdata` | `pd.DataFrame` | ❌ | 自定义股票数据，包含 Open、High、Low、Close、Volume 列 |
| `save_path` | `str` | ❌ | 图片保存路径，默认为 "{stock_code}_{start_date}_{end_date}.png" |
| `vlines_dates` | `list[datetime.date]` | ❌ | 垂直标记线的日期列表 |
| `vlines_colors` | `list[str]` | ❌ | 垂直标记线的颜色列表 |
| `mark_list_dict` | `dict` | ❌ | 标记点数据字典，格式: {series_name: list[bool]} |
| `mark_list_sizes` | `dict` | ❌ | 标记点大小字典，格式: {series_name: int} |
| `mark_list_colors` | `dict` | ❌ | 标记点颜色字典，格式: {series_name: str} |

**数据格式要求:**

如果提供自定义数据 (`kdata`)，DataFrame 必须包含以下列：
- `Open`: 开盘价
- `High`: 最高价
- `Low`: 最低价
- `Close`: 收盘价
- `Volume`: 成交量
- 索引必须是日期类型

**异常处理:**

- `TypeError`: 参数类型错误
- `ValueError`: 参数值错误或数据格式不符合要求

## 使用示例

### 示例 1: 绘制基础 K 线图

```python
from KlineDrawer import KlineDrawer
import datetime

drawer = KlineDrawer()
drawer.draw_kline(
    stock_code="000001.SZ",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 6, 30)
)
```

### 示例 2: 添加垂直标记线

```python
from KlineDrawer import KlineDrawer
import datetime

drawer = KlineDrawer()
drawer.draw_kline(
    stock_code="000001.SZ",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 6, 30),
    vlines_dates=[
        datetime.date(2023, 2, 15),
        datetime.date(2023, 4, 20)
    ],
    vlines_colors=['red', 'green']
)
```

### 示例 3: 添加交易信号标记

```python
from KlineDrawer import KlineDrawer
import datetime

drawer = KlineDrawer()

# 假设有100个交易日的数据
data_length = 100
buy_signals = [True if i % 15 == 0 else False for i in range(data_length)]
sell_signals = [True if i % 20 == 0 else False for i in range(data_length)]

drawer.draw_kline(
    stock_code="000001.SZ",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 6, 30),
    mark_list_dict={
        'buy_signals': buy_signals,
        'sell_signals': sell_signals
    },
    mark_list_sizes={
        'buy_signals': 120,
        'sell_signals': 100
    },
    mark_list_colors={
        'buy_signals': 'green',
        'sell_signals': 'red'
    }
)
```

### 示例 4: 使用自定义数据

```python
from KlineDrawer import KlineDrawer
import datetime
import pandas as pd
import numpy as np

# 创建模拟数据
dates = pd.date_range('2023-01-01', periods=100)
base_price = 100
prices = base_price + np.cumsum(np.random.randn(100) * 0.5)

kdata = pd.DataFrame({
    'Open': prices + np.random.randn(100) * 0.1,
    'High': prices + np.abs(np.random.randn(100) * 0.5),
    'Low': prices - np.abs(np.random.randn(100) * 0.5),
    'Close': prices,
    'Volume': np.random.randint(1000000, 5000000, 100)
}, index=dates)

drawer = KlineDrawer()
drawer.draw_kline(
    stock_code="自定义股票",
    start_date=datetime.date(2023, 1, 1),
    end_date=datetime.date(2023, 4, 10),
    kdata=kdata,
    save_path="自定义数据K线图.png"
)
```

## 图表功能特性

### 网格线
- 自动添加主要和次要网格线
- 主要网格线间隔：5个交易日
- 次要网格线间隔：1个交易日
- 半透明设计，不影响数据可读性

### 图表样式
- 使用 Yahoo 风格的 K 线图
- 支持蜡烛图显示
- 自动显示成交量子图
- 高分辨率输出 (300 DPI)

### 保存选项
- 自动裁剪空白边距
- 支持多种图片格式
- 可自定义保存路径和文件名

## 常见问题

### Q: 如何处理数据缺失的情况？
A: 确保提供的数据是连续的，对于缺失的交易日，可以使用前向填充或删除对应的标记点。

### Q: 标记点显示不正确怎么办？
A: 检查标记点列表的长度是否与股票数据长度一致，确保布尔值列表与数据行数匹配。

### Q: 如何自定义图表大小？
A: 目前图表大小固定为 (15, 8)，后续版本将支持自定义图表尺寸。

### Q: 支持哪些股票代码格式？
A: 支持标准的股票代码格式，如 "000001.SZ"、"600000.SH" 等。

## 技术支持

如果您在使用过程中遇到任何问题，请：

1. 查看此 README 文档
2. 检查您的数据格式是否正确
3. 确保所有依赖库都已正确安装
4. 提交 Issue 到 GitHub 仓库

## 开发计划

- [ ] 支持更多技术指标显示
- [ ] 增加交互式图表功能
- [ ] 支持更多数据源
- [ ] 添加图表模板功能
- [ ] 优化绘图性能

## 许可证

本项目使用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 作者

**DoubleLiu** - 项目创建者和主要维护者

---

⭐ 如果这个项目对您有帮助，请给个 Star 支持一下！ 