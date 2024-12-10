import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def plot_results(results):
    # 遍历每个实现（quic-go, quiche等）
    for impl, data in results.items():
        # 遍历每种测试类型（crosstraffic, goodput）
        for test_type, test_data in data.items():
            plt.figure(figsize=(12, 6))
            
            # 绘制5个子列表的数据
            for i, series in enumerate(test_data):
                # 提取时间戳和窗口大小
                timestamps = [entry['timestamp'] for entry in series]
                windows = [entry['window'] for entry in series]
                
                # 绘制折线
                plt.plot(timestamps, windows, label=f'Test {i+1}', marker='.')
            
            # 设置图表属性
            plt.title(f'{impl} - {test_type}')
            plt.xlabel('Time')
            plt.ylabel('Window Size (bytes)')
            plt.grid(True)
            plt.legend()
            
            # 设置x轴时间格式
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
            plt.gcf().autofmt_xdate()  # 自动旋转日期标签
            
            # 保存图片
            os.mkdir('imgs') if not os.path.exists('imgs') else None
            plt.savefig(f'imgs/{impl}_{test_type}.png')
            plt.close()
