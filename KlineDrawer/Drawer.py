import datetime
import pandas as pd 
from TushareDataLoader import TushareDataOperator
import mplfinance as mpf
import matplotlib.pyplot as plt

class KlineDrawer:
    def draw_kline(self, stock_code, start_date, end_date, kdata=None, 
                    save_path=None,vlines_dates=None,vlines_colors=None,
                    mark_list_dict=None,mark_list_sizes=None,mark_list_colors=None
                    ):
        """
        绘制K线图
        param stock_code: 股票代码
        param start_date: 开始日期 datetime.date
        param end_date: 结束日期 datetime.date
        param kdata: 股票数据 pd.DataFrame(字段: date(INDEX), Open, High, Low, Close, Volume)
        param save_path: 保存路径
        param vlines_dates: 垂直线日期列表 list[datetime.date]
        param vlines_colors: 垂直线颜色列表 list[str]
        param mark_list_dict: 标记点数据字典 {series_name: list[bool]}
        param mark_list_sizes: 标记点大小列表 {series_name: int}
        param mark_list_colors: 标记点颜色列表 {series_name: str}
        """
        # 类型检查
        if not isinstance(stock_code, str):
            raise TypeError("stock_code 必须是字符串类型")
        
        if not isinstance(start_date, datetime.date):
            start_date = pd.to_datetime(start_date).date()
        
        if not isinstance(end_date, datetime.date):
            end_date = pd.to_datetime(end_date).date()
        
        # 日期逻辑检查
        if start_date > end_date:
            raise ValueError("start_date 不能大于 end_date")
        
        # kdata 数据检查
        if kdata is not None:
            if not isinstance(kdata, pd.DataFrame):
                raise TypeError("kdata 必须是 pandas DataFrame 类型")
            
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in kdata.columns]
            if missing_columns:
                raise ValueError(f"kdata 缺少必需的列: {', '.join(missing_columns)}")
        
        # 垂直线参数检查
        if vlines_dates is not None:
            if not isinstance(vlines_dates, list):
                raise TypeError("vlines_dates 必须是列表类型")
            
            if not all(isinstance(date, datetime.date) for date in vlines_dates):
                tmp = []
                for date in vlines_dates:
                    tmp.append(pd.to_datetime(date).date())
                vlines_dates = tmp
            
            if vlines_colors is not None and len(vlines_dates) != len(vlines_colors):
                raise ValueError("vlines_dates 和 vlines_colors 的长度必须相同")
        
        # 标记点参数检查
        if mark_list_dict is not None:
            if not isinstance(mark_list_dict, dict):
                raise TypeError("mark_list_dict 必须是字典类型")
            
            for key, mark_list in mark_list_dict.items():
                if not isinstance(mark_list, list):
                    raise TypeError(f"mark_list_dict[{key}] 必须是列表类型")
                
                if not all(isinstance(mark, bool) for mark in mark_list):
                    raise TypeError(f"mark_list_dict[{key}] 中的所有元素必须是布尔类型")
            
            if mark_list_sizes is not None:
                if not isinstance(mark_list_sizes, dict):
                    raise TypeError("mark_list_sizes 必须是字典类型")
                if not all(key in mark_list_dict for key in mark_list_sizes):
                    raise ValueError("mark_list_sizes 的键必须与 mark_list_dict 的键匹配")
            
            if mark_list_colors is not None:
                if not isinstance(mark_list_colors, dict):
                    raise TypeError("mark_list_colors 必须是字典类型")
                if not all(key in mark_list_dict for key in mark_list_colors):
                    raise ValueError("mark_list_colors 的键必须与 mark_list_dict 的键匹配")

        if kdata is None:
            kdata = TushareDataOperator().load_data(stock_code, start_date, end_date)
            # 确保日期索引和列名
            kdata.index = pd.to_datetime(kdata.date)
        else:
            original_data = kdata.copy()
            kdata = kdata[kdata.index >= start_date]
            kdata = kdata[kdata.index <= end_date]
        if save_path is None:
            # 转换为字符串格式用于文件名
            start_date_str = start_date.strftime('%Y%m%d')
            end_date_str = end_date.strftime('%Y%m%d')
            save_path = f'{stock_code}_{start_date_str}_{end_date_str}.png'

        # 设置垂直线
        if vlines_dates is not None:
            if vlines_colors is None:
                vlines_colors = ['red'] * len(vlines_dates)
            vlines = dict(
                vlines=vlines_dates,
                colors=vlines_colors,
                linestyle='-.'
            )
        else:
            vlines = None
        
        # 设置标记点
        apds = []
        if mark_list_dict is not None:
            if mark_list_sizes is None:
                mark_list_sizes = {key: 10 for key in mark_list_dict.keys()}
            if mark_list_colors is None:
                mark_list_colors = {key: 'blue' for key in mark_list_dict.keys()}
            
            for key, mark_list in mark_list_dict.items():
                null_mark_series = pd.Series(index=kdata.index, dtype=float)
                if len(mark_list) != len(kdata):
                    raise ValueError(f"标记点数据长度与股票数据长度不一致: {key}")
                # 将list中的数值填入null_mark_series中
                for i, mark in enumerate(mark_list):
                    if mark:
                        null_mark_series.iloc[i] = kdata['Close'].iloc[i]
                mark_series = null_mark_series
                apds.append(
                    mpf.make_addplot(
                        mark_series,
                        type='scatter',
                        markersize=mark_list_sizes.get(key, 100),
                        marker='^',
                        color=mark_list_colors.get(key, 'purple'),
                        panel=0
                    )
                )
        else:
            apds = None

        plot_params = {
            'type': 'candle',
            'style': 'yahoo',
            'volume': True,
            'figsize': (15, 8),
            'returnfig': True  # 返回图形对象
        }
        if vlines:
            # 基础绘图参数
            plot_params['vlines'] = vlines
        if apds:
            plot_params['addplot'] = apds

        # 绘制图形并获取图形对象
        fig, axes = mpf.plot(kdata, **plot_params)
        # 为每个子图添加网格线
        for ax in axes:
            ax.grid(True, which='major', linestyle='--', linewidth=0.5, color='gray', alpha=0.3)
            ax.grid(True, which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.2)
            ax.minorticks_on()  # 启用次要刻度

            # 设置主要网格线间隔
            ax.xaxis.set_major_locator(plt.MultipleLocator(5))  # 每5个交易日一条主要网格线

            # 设置次要网格线间隔
            ax.xaxis.set_minor_locator(plt.MultipleLocator(1))  # 每1个交易日一条次要网格线

        # 保存图形
        plt.savefig(save_path,
                    dpi=300,
                    bbox_inches='tight')
        plt.close(fig)
                

                
