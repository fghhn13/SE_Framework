# StructGenesis: 结构涌现框架 (Structure Emergence Framework)

> **核心哲学**: 只有机制 (Mechanism) 和环境 (Environment)，让程序自己写出结构 (Structure)。

## 1. 项目简介
本项目构建了一个“从交互中涌现结构”的实验框架。Agent 在图环境 (Graph Environment) 中探索，通过记忆 (Memory) 积累经验，自动发现高频模式 (Macro)，从而从“随机游走”进化为“高效执行”。

**✨ 核心特性：**
* **策略插拔**: 支持多种 Agent 策略 (Random / Macro) 对比实验。
* **结构涌现**: Agent 自动从经验中挖掘 Macro，无需人工规则。
* **持久化记忆**: 支持存档/读档 (Save/Load)，实现长期训练与断点续传。
* **数据可视化**: 内置绘图工具，一键生成 Cost/Success/Structure 变化曲线。

## 2. 目录结构

```text
project_root/
├── config/                 # 全局配置
├── data/                   
│   ├── graphs/             # 地图文件 (e.g., 0001.json)
│   └── agents/             # Agent 存档 (包含记忆、宏和训练日志)
├── src/                    # 核心代码
│   ├── envs/               # 环境定义
│   ├── agents/             # 策略实现 (Factory, Random, Macro)
│   ├── memory/             # 记忆模块
│   ├── structure/          # 结构挖掘
│   └── io/                 # 日志与数据记录
├── scripts/                # 工具脚本
│   ├── run_experiment.py   # 实验入口
│   └── visualize.py        # 可视化工具
└── README.md
````

## 3. 快速开始 (Quick Start)

### 🚀 启动实验

使用 `scripts/run_experiment.py` 启动。

**1. 训练智能 Agent (默认)**

Bash

```
# 在 0001 号地图上训练名为 "Hero_01" 的 Agent
python scripts/run_experiment.py --map 0001 --agent Hero_01 --type macro
```

**2. 运行对照组 (笨蛋 Agent)**

Bash

```
# 使用随机策略，不利用记忆
python scripts/run_experiment.py --map 0001 --agent Dummy_01 --type random
```

**3. 强制指定训练次数**

Bash

```
# 无论 Config 怎么写，强行跑 1000 集
python scripts/run_experiment.py --map 0001 --agent Hero_01 --episodes 1000
```

### 📊 数据可视化

训练完成后，使用 `scripts/visualize.py` 生成图表。

Bash

```
# 生成 Hero_01 的训练曲线
python scripts/visualize.py --agent Hero_01 --window 50
```

> 图片将保存在 `data/agents/Hero_01/training_plot.png`

## 4. 模块说明

|**模块**|**功能**|
|---|---|
|`src.agents`|**决策层**: `AgentFactory` 负责生产 Agent。`MacroAgent` 会用宏，`RandomAgent` 只会瞎跑。|
|`src.structure`|**结构层**: `MacroDiscovery` 负责从 `PathMemory` 中提炼高频路径。|
|`src.runner`|**控制层**: 管理实验流程，自动处理 CSV 日志记录与断点续传。|

---

_Designed with 🧠 & ☕_

