# -*- coding: utf-8 -*-
"""
@Project: Project Elaine
@File: process_data.py
@Author: DanKe
@Description:
    人设数据后期处理脚本。该脚本负责将 Yuki 标识批量替换为 Elaine，
    并自动更新 Yuki_identity_sft 目录下的数据文件及其对应的 dataset_infos.json 配置文件。
"""

import json
import os

def finalize_elaine_dataset(target_dir, old_name="yuki", new_name="elaine"):
    """
    完成数据集从旧标识(Yuki)到新标识(Elaine)的转换。
    """
    old_jsonl = os.path.join(target_dir, f"{old_name}_identity_sft.jsonl")
    new_jsonl = os.path.join(target_dir, f"{new_name}_identity_sft.jsonl")
    info_file = os.path.join(target_dir, "dataset_infos.json")

    # 1. 处理 JSONL 数据内容：执行人设注入替换
    if os.path.exists(old_jsonl):
        print(f"正在读取原始数据并进行人设注入...")
        with open(old_jsonl, 'r', encoding='utf-8') as f_in, \
             open(new_jsonl, 'w', encoding='utf-8') as f_out:
            for line in f_in:
                # 替换人设标识：处理首字母大写和全小写
                updated_line = line.replace(old_name.capitalize(), new_name.capitalize())
                updated_line = updated_line.replace(old_name.lower(), new_name.lower())
                f_out.write(updated_line)
        os.remove(old_jsonl)
        print(f"✅ 已生成 {new_jsonl}")

    # 2. 修改 dataset_infos.json：同步元数据索引
    if os.path.exists(info_file):
        print(f"正在更新元数据配置文件...")
        with open(info_file, 'r', encoding='utf-8') as f:
            info_data = json.load(f)

        if "default" in info_data:
            info_data["default"]["splits"]["train"]["dataset_name"] = f"{new_name}_identity_sft"

        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info_data, f, ensure_ascii=False, indent=4)
        print(f"✅ 元数据标识已变更为 {new_name}_identity_sft")

if __name__ == "__main__":
    finalize_elaine_dataset("Yuki_identity_sft")