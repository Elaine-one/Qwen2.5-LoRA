

---

# Elaine: 基于 Qwen2.5 与 LLaMA-Factory 的专属人设微调实战

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)
![Model](https://img.shields.io/badge/Model-Qwen2.5--1.5B-orange.svg)]()

> **本项目记录了如何在 Windows 环境下（8G 显存），利用 LoRA 技术将 Qwen2.5-1.5B-Instruct 模型微调为具备特定自我认知的 AI 助手 —— Elaine。**

## 📂 项目结构 (Directory Structure)

本项目核心文件组织如下，包含自动化脚本、微调框架配置及数据产出路径。

```text
.
├── LLaMA-Factory/                 # 核心微调框架
│   ├── data/
│   │   └── dataset_info.json      # [配置] 数据集注册表（需添加 elaine 索引）
│   ├── saves/                     # [产出] 训练过程 Checkpoint 保存路径
│   └── elaine_lora.yaml           # [配置] 训练超参数配置文件 (Epochs, LR, Quantization)
├── models/
│   └── Qwen2.5-1.5B-Instruct/     
│       └── qwen/
│           └── Qwen2.5-1.5B-Instruct/ # [基座] Qwen2.5-1.5B 原始权重
├── Yuki_identity_sft/             # [数据] 
│   ├── elaine_identity_sft.jsonl  # <--- 预处理后的最终训练数据 (Elaine 人设)
│   └── dataset_infos.json         # 数据集统计信息
├── download_dataset.py                   # [Step 1] 调用 ModelScope 下载原始语料
├── process_data.py                     # [Step 2] 执行人设关键词替换 (Yuki -> Elaine)
├── download_model.py              # [Step 3] 下载 Qwen2.5 基座模型
└── elaine.py                      # [Step 4] 验证脚本：流式对话测试 (无 WebUI 依赖)
```

---

## ⚠️ 前置声明 (Prerequisites)

为了避免 Python 环境污染及依赖冲突，**强烈建议**在 Anaconda 虚拟环境中运行。

*   **环境要求**: Python 3.10 / 3.11, CUDA 12.1+
*   **硬件要求**: NVIDIA GPU (显存 ≥ 8GB)

```bash
# 推荐环境构建
conda create -n lora_env python=3.10 -y
conda activate lora_env
```

---

## 🚀 复现流程 (Workflow)

### 1. 环境初始化
安装 LLaMA-Factory 及其依赖（包含 Qwen 支持与量化库）。

```bash
# 进入项目根目录
cd LoRA

# 安装核心第三方依赖
pip install -r requirements.txt
# 进入 LLaMA-Factory 安装其本身
cd LLaMA-Factory
pip install -e .[metrics,bitsandbytes,qwen]
pip install modelscope
cd ..
```

### 2. 数据准备与模型下载
依次运行根目录下的自动化脚本，完成准备工作。

```bash
# 1. 下载原始数据集
python download_dataset.py

# 2. 执行人设注入（生成 elaine_identity_sft.jsonl）
python process_data.py

# 3. 下载基座模型权重
python download_model.py
```

### 3. 配置文件修改
确保 `LLaMA-Factory/data/dataset_info.json` 中已注册 Elaine 数据集，且 `LLaMA-Factory/elaine_lora.yaml` 中的模型路径指向本地绝对路径。

### 4. 启动微调 (Training)
使用 4-bit 量化启动 LoRA 训练，显存占用约 6GB。

```bash
cd LLaMA-Factory
llamafactory-cli train elaine_lora.yaml
```

### 5. 对话验证 (Verification)
训练完成后，使用 Python 脚本直接加载 LoRA 权重进行测试，避开 WebUI 的兼容性问题。

```bash
# 回到根目录
python elaine.py
```

---

## 🐳 模型部署 (Deployment)

如需将 Elaine 导出并接入 **Ollama** 实现独立运行：

1.  **合并权重**：使用 `llamafactory-cli export` 将 LoRA 权重合并回基座模型。
2.  **创建 Modelfile**：
    ```dockerfile
    FROM ./models/Elaine_Final_Model
    SYSTEM "你是Elaine，由DanKe开发的人工智能助手。"
    ```
3.  **注册服务**：
    ```bash
    ollama create Elaine -f Modelfile
    ollama run Elaine
    ```

---

## 📊 实验成果 (Results)

*   **资源消耗**：成功在单卡 RTX 3060/4060 级别显卡上完成训练。
*   **人设表现**：模型成功遗忘“通义千问”身份，能够准确回答“你是谁”并保持“Elaine”的人设风格。
*   **工具链**：打通了 ModelScope -> LLaMA-Factory -> Ollama 的全链路开发。

---

## 🔗 致谢 (Acknowledgements)

*   [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)
*   [QwenLM](https://github.com/QwenLM/Qwen2.5)
*   [ModelScope](https://modelscope.cn/)

