import os
import re
from datetime import datetime

from draw import plot_results

def extract_congestion_info(root_dir):
    # 存储结果的字典
    results = {}
    
    # 遍历根目录下的所有子文件夹
    for subfolder in os.listdir(root_dir):
        # 初始化结果字典
        results[subfolder] = {
            'crosstraffic': [],
            'goodput': []
        }

        subfolder_path = os.path.join(root_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue
            
        # 根据子文件夹名称选择匹配规则
        if subfolder.startswith('quic-go'):
            pattern = r'(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}).*window (\d+)'
            test_type = 'quic-go'
        elif subfolder.startswith('quiche'):
            pattern = r'\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}).*\].*cwnd=(\d+)'
            test_type = 'quiche'
        else:
            continue
            
        # 遍历 crosstraffic 和 goodput 文件夹
        for test_subfolder in ['crosstraffic', 'goodput']:
            test_path = os.path.join(subfolder_path, test_subfolder)
            if not os.path.exists(test_path):
                continue
                
            # 遍历数字文件夹
            for idx, num_folder in enumerate(sorted(os.listdir(test_path))):
                results[subfolder][test_subfolder].append([]);  # 初始化结果列表
                log_file = os.path.join(test_path, num_folder, 'server', 'log.txt')
                if not os.path.exists(log_file):
                    continue
                    
                # 读取日志文件
                with open(log_file, 'r') as f:
                    content = f.readlines()

                # 使用正则表达式提取信息
                for line in content:
                    match = re.search(pattern, line)
                    if match:
                        if test_type == 'quic-go':
                            timestamp = datetime.strptime(match.group(1), '%Y/%m/%d %H:%M:%S')
                        else:  # quiche
                            timestamp = datetime.strptime(match.group(1), '%Y-%m-%dT%H:%M:%S.%f')
                        window = int(match.group(2))
                        results[subfolder][test_subfolder][idx].append({
                            'timestamp': timestamp,
                            'window': window
                        })
    
    return results


if __name__ == '__main__':
    root_dir = 'logs_2024-12-05T14:11:04'
    congestion_data = extract_congestion_info(root_dir)
    plot_results(congestion_data)