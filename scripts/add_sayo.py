#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List

def process_txt_file(filepath: str) -> List[str]:
    """
    处理单个txt文件，在以「和」开头结尾的行前添加"遠野　紗夜"
    
    Args:
        filepath (str): 要处理的文件路径
        
    Returns:
        List[str]: 处理后的行列表
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return []
    
    # 删除所有空行
    lines = [line for line in lines if line.strip() != ""]
    
    # 存储处理后的行
    result_lines = []
    
    # 处理文件
    for line in lines:
        # 检查当前行是否以「开头并且以」结尾
        if line.startswith('「') and line.endswith('」'):
            # 在行前添加"遠野　紗夜"
            modified_line = "遠野　紗夜" + line
            result_lines.append(modified_line)
        else:
            # 普通行，直接添加
            result_lines.append(line)
    
    return result_lines

def process_directory(directory: str) -> None:
    """
    处理指定目录下的所有txt文件
    
    Args:
        directory (str): 要处理的目录路径
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt') and 
                 os.path.isfile(os.path.join(directory, f))]
    
    if not txt_files:
        print(f"No txt files found in directory '{directory}'.")
        return
    
    print(f"Found {len(txt_files)} txt files to process.")
    
    for filename in txt_files:
        filepath = os.path.join(directory, filename)
        print(f"Processing file: {filename}")
        
        # 处理文件
        processed_lines = process_txt_file(filepath)
        
        if processed_lines:
            # 生成输出文件名
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_processed{ext}"
            output_filepath = os.path.join(directory, output_filename)
            
            # 写入处理后的内容
            try:
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    for line in processed_lines:
                        f.write(line + '\n')
                print(f"  Saved processed file as: {output_filename}")
            except Exception as e:
                print(f"  Error saving processed file: {e}")
        else:
            print(f"  Failed to process file: {filename}")

def main():
    print("Text File Processor - Add Character Name")
    print("=" * 40)
    
    # 获取要处理的目录
    directory = input("Enter the directory path to process (or press Enter for current directory): ").strip()
    if not directory:
        directory = "."
    
    # 处理目录中的文件
    process_directory(directory)
    print("Processing complete!")

if __name__ == "__main__":
    main()