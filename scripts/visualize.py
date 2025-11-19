import sys
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# 路径黑魔法
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)


def plot_agent_progress(agent_id: str, window_size: int = 50):
    """
    读取 Agent 的 CSV 日志并生成图表。
    window_size: 移动平均窗口大小，让曲线更平滑。
    """
    # 1. 读取数据
    log_path = os.path.join(project_root, "data", "agents", agent_id, "training_log.csv")
    if not os.path.exists(log_path):
        print(f"❌ Log file not found: {log_path}")
        print("   (Did you run the experiment with the new Logger code?)")
        return

    print(f"📊 Loading data for Agent: {agent_id} ...")
    df = pd.read_csv(log_path)

    if len(df) < 10:
        print("⚠️ Not enough data points to plot (need > 10).")
        return

    # 2. 创建画布 (3行1列)
    fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    plt.suptitle(f"Training Progress: {agent_id}", fontsize=16)

    # --- 子图 1: Cost (移动平均) ---
    # 原始数据稍微透明一点，移动平均线画深色
    axes[0].plot(df['cost'], color='gray', alpha=0.3, label='Raw Cost')
    # 计算 Rolling Mean
    df['cost_smooth'] = df['cost'].rolling(window=window_size, min_periods=1).mean()
    axes[0].plot(df['cost_smooth'], color='blue', linewidth=2, label=f'Avg Cost (MA-{window_size})')
    axes[0].set_ylabel('Cost per Episode')
    axes[0].set_title('Performance Efficiency (Lower is Better)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # --- 子图 2: Success Rate (移动平均) ---
    df['success_smooth'] = df['success'].rolling(window=window_size, min_periods=1).mean()
    axes[1].plot(df['success_smooth'], color='green', linewidth=2, label=f'Success Rate (MA-{window_size})')
    axes[1].set_ylabel('Success Rate (0-1)')
    axes[1].set_title('Reliability (Higher is Better)')
    axes[1].set_ylim(-0.1, 1.1)
    axes[1].grid(True, alpha=0.3)

    # --- 子图 3: Macro Discovery ---
    axes[2].plot(df['macro_count'], color='purple', linewidth=2, label='Total Macros')
    axes[2].set_ylabel('Macro Count')
    axes[2].set_xlabel('Episodes')
    axes[2].set_title('Structure Emergence (Cumulative)')
    axes[2].fill_between(df.index, df['macro_count'], color='purple', alpha=0.1)  # 填充颜色看起来更高级
    axes[2].grid(True, alpha=0.3)

    # 3. 保存图片
    output_path = os.path.join(project_root, "data", "agents", agent_id, "training_plot.png")
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # 调整布局防止标题重叠
    plt.savefig(output_path, dpi=100)
    print(f"✅ Plot saved to: {output_path}")

    # 可选：直接显示
    # plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", type=str, required=True, help="Agent ID to visualize")
    parser.add_argument("--window", type=int, default=20, help="Smoothing window size")
    args = parser.parse_args()

    plot_agent_progress(args.agent, args.window)