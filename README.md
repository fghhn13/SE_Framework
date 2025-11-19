# 核心方向: 结构涌现框架 (Structure Emergence Framework)

> **核心哲学**: 只有机制 (Mechanism) 和环境 (Environment)，让程序自己产生结构 (Structure)。

## 1. 项目愿景 (Vision)

本项目旨在构建一个**“从交互中涌现结构”**的实验框架。
我们不预设复杂的逻辑结构（如硬编码的宏、策略树），而是通过 Agent 在 Environment 中的反复交互，利用**记忆 (Memory)** 和 **发现机制 (Discovery)**，自动沉淀出高效的**结构 (Structure)**。

**核心三轴：**
1.  **Environment (环境)**: 抽象的世界，只负责反馈状态、边界和代价。
2.  **Mechanism (机制/Agent)**: 可插拔的策略，负责探索和利用。
3.  **Structure (结构)**: 从经验中“长”出来的数据（如 Macro、Options、Sub-routines），用于加速未来的决策。

## 2. 目录结构 (Project Structure)

本项目遵循 **“核心依赖倒置”** 与 **“模块职责分离”** 原则，确保未来扩展时无需重构核心逻辑。

```text
project_root/
├── config/                 # 外部配置文件
│   ├── default.json        # 默认实验配置
│   └── complex_graph.json  # 复杂场景配置
├── data/                   # 数据存储
│   └── graphs/             # 图结构定义 (World maps)
├── src/                    # 源代码
│   ├── core/               # [底层] 通用类型与配置加载
│   │   ├── config.py
│   │   └── types.py
│   ├── envs/               # [环境] 各种世界的实现 (Graph, GridWorld...)
│   │   ├── base.py         # 抽象接口
│   │   └── graph_env.py
│   ├── memory/             # [记忆] 记录原始经验
│   │   └── path_memory.py
│   ├── structure/          # [结构] 存储与发现算法 (的核心)
│   │   ├── macro.py        # 宏定义
│   │   └── discovery.py    # 结构挖掘算法
│   ├── agents/             # [机制] 各种策略 Agent
│   │   ├── base.py         # 抽象接口
│   │   ├── random_agent.py
│   │   └── macro_agent.py
│   ├── runner/             # [流程] 实验流控制
│   │   ├── episode_runner.py
│   │   └── experiment.py
│   └── io/                 # [工具] 日志与导出
│       ├── logger.py
│       └── exporters.py
├── scripts/                # 启动脚本
│   └── run_experiment.py
├── results/                # 实验输出产物
└── README.md
```

## 3. 模块指引 (Module Guide)

|**模块**|**职责 (Responsibility)**|**依赖原则 (Dependency Rule)**|
|---|---|---|
|**core**|定义通用的数据类型 (Node, Path) 和 Config 对象。|不依赖任何其他模块。|
|**envs**|定义 Agent 存在的“物理法则”。只管 State 和 Transition。|依赖 `core`。|
|**memory**|忠实记录发生了什么 (Raw Experience)。|依赖 `core`。|
|**structure**|**项目的灵魂**。定义如何从 Raw Experience 中提取 Pattern。|依赖 `core`。|
|**agents**|决策的大脑。根据 Environment 和 Structure 决定动作。|依赖 `core`, `structure` (读取), `memory` (写入)。|
|**runner**|上帝视角。组装 Env 和 Agent，驱动时间流逝。|依赖所有模块。|

## 4. 快速开始 (Quick Start)

### 环境准备

建议使用 Python 3.9+

Bash

```
# 安装依赖 
pip install -r requirements.txt
```

### 运行实验

Bash

```
# 默认运行
python scripts/run_experiment.py

# 指定配置文件 (TBD)
python scripts/run_experiment.py --config config/complex_graph.json
```

## 5. 开发路线 (Roadmap)

- [ ] **Phase 1: 骨架搭建** (Current)
    
    - [ ] 目录结构设计
        
    - [ ] `core`: 类型系统与配置
        
    - [ ] `envs`: 基础图环境实现
        
    - [ ] `agents`: 随机游走 Agent
        
- [ ] **Phase 2: 记忆与重放**
    
    - [ ] `memory`: 路径统计
        
    - [ ] `agents`: 基于记忆的最优路径重放
        
- [ ] **Phase 3: 结构涌现**
    
    - [ ] `structure`: 简单的宏 (Macro) 发现算法
        
    - [ ] `agents`: 会使用宏的 Agent
        
- [ ] **Phase 4: 演化**
    
    - [ ] 引入更复杂的结构形式 (Options / Sub-goals)
        
    - [ ] 引入环境变化，测试结构的鲁棒性
        

---
