import csv
import os
from typing import Any, List


class DataLogger:
    """
    飞行记录仪 (Data Logger)
    负责将每一集的实验数据写入 CSV 文件，用于后续画图。
    """

    def __init__(self, log_dir: str, filename: str = "training_log.csv"):
        os.makedirs(log_dir, exist_ok=True)
        self.filepath = os.path.join(log_dir, filename)

        # 如果文件不存在，先写入表头
        self.file_exists = os.path.exists(self.filepath)
        if not self.file_exists:
            self._write_header()

    def _write_header(self):
        with open(self.filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 定义我们要记录的指标
            writer.writerow(["episode", "success", "cost", "steps", "macro_count"])

    def log_episode(self, episode: int, success: bool, cost: float, steps: int, macro_count: int):
        """记录一集的数据"""
        with open(self.filepath, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([episode, int(success), cost, steps, macro_count])