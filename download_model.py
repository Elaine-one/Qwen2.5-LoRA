# -*- coding: utf-8 -*-
"""
@Project: Project Elaine
@File: download_model.py
@Author: DanKe
@Description:
    基于 ModelScope SDK 自动化下载 Qwen2.5-1.5B-Instruct 指令微调版基座模型。
    该脚本支持断点续传，并将模型权重保存至指定的本地 models 目录。
"""

import os
from modelscope import snapshot_download

# 解决 Windows 环境下多个 OpenMP 库冲突导致的脚本奔溃问题
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


def download_qwen_model():
    """
    执行 Qwen2.5 模型下载的主函数。
    配置说明：
    - model_id: 模型在 ModelScope 社区的唯一标识。
    - local_dir: 模型下载后的根存放目录。
    """
    # 选定 Qwen2.5-1.5B 版本，该版本在 8G 显存环境下具备极高的微调性价比
    model_id = 'qwen/Qwen2.5-1.5B-Instruct'

    # 定义本地存储的基础路径
    base_cache_dir = './models/Qwen2.5-1.5B-Instruct'

    # 确保目标文件夹存在
    if not os.path.exists(base_cache_dir):
        os.makedirs(base_cache_dir)
        print(f"创建目录: {base_cache_dir}")

    print(f"正在启动 ModelScope 下载引擎...")
    print(f"目标模型: {model_id}")
    print(f"下载过程中请保持网络连接稳定...")

    try:
        # 执行下载任务
        # cache_dir: SDK 会在此目录下创建子文件夹存放模型权重
        model_dir = snapshot_download(
            model_id,
            cache_dir=base_cache_dir,
            revision='master'
        )

        print(f"\n" + "=" * 30)
        print(f"✅ 模型下载成功！")
        print(f"本地绝对路径: {os.path.abspath(model_dir)}")
        print(f"请确保在 LLaMA-Factory 的配置文件中引用此路径。")
        print("=" * 30)

    except Exception as e:
        print(f"\n❌ 下载失败，错误信息: {str(e)}")


if __name__ == "__main__":
    download_qwen_model()