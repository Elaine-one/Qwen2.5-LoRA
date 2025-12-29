# -*- coding: utf-8 -*-
"""
@Project: Project Elaine
@File: elaine.py
@Author: DanKe
@Description:
    基于 LLaMA-Factory 接口实现的本地推理测试脚本。
    通过加载基座模型与 LoRA 权重，实现流式（Streaming）对话，验证 Elaine 的人设认知。
"""

import os
from llamafactory.chat import ChatModel

# 解决 Windows 环境下库冲突问题
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def start_chat():
    """
    启动本地交互式对话。
    """
    # 路径配置必须与本地实际物理路径完全一致
    args = {
        "model_name_or_path": r"D:\Code\LoRA\models\Qwen2.5-1.5B-Instruct\qwen\Qwen2___5-1___5B-Instruct",
        "adapter_name_or_path": r"D:\Code\LoRA\LLaMA-Factory\saves\elaine_lora_sft",
        "template": "qwen",
        "finetuning_type": "lora",
        "quantization_bit": 4,  # 推理开启 4-bit 量化
    }

    chat_model = ChatModel(args)
    print("\n--- Elaine 已上线 (输入 'quit' 退出) ---")

    messages = []
    while True:
        query = input("\n我: ")
        if query.strip().lower() == "quit":
            break

        messages.append({"role": "user", "content": query})
        print("Elaine: ", end="", flush=True)

        response = ""
        # 使用流式接口，实现类似真实大模型的打字机效果
        for new_text in chat_model.stream_chat(messages):
            print(new_text, end="", flush=True)
            response += new_text
        print()
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    start_chat()