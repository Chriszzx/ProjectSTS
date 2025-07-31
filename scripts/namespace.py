#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List, Set

# 指定查询表文件路径的常量
QUERY_TABLE_FILE = "special_character.txt"

def load_query_table(filepath: str) -> Set[str]:
    """
    读取查询表文件，将每一行作为元素加载到集合中
    
    Args:
        filepath (str): 查询表文件路径
        
    Returns:
        Set[str]: 包含所有查询条目的集合
    """
    query_set = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                # 去除行尾换行符并添加到集合中
                query_set.add(line.rstrip('\n'))
        print(f"Successfully loaded {len(query_set)} entries from query table.")
    except FileNotFoundError:
        print(f"Error: Query table file '{filepath}' not found.")
    except Exception as e:
        print(f"Error loading query table: {e}")
    
    return query_set

def process_txt_file(filepath: str, query_set: Set[str]) -> List[str]:
    """
    处理单个txt文件，根据查询表进行行拼接处理
    
    Args:
        filepath (str): 要处理的文件路径
        query_set (Set[str]): 查询表集合
        
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
    
    processed_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        
        # 检查当前行是否在查询表中
        if current_line in query_set and i < len(lines) - 1:
            # 找到匹配行，检查下一行
            next_index = i + 1
            
            # 跳过空行（这一步实际上不再需要，因为我们已经预处理了空行）
            while next_index < len(lines) and lines[next_index].strip() == "":
                next_index += 1
            
            # 如果还有后续行，则进行拼接
            if next_index < len(lines):
                next_line = lines[next_index]
                
                # 根据规则处理拼接
                if lines[i+1].strip() == "":  # 如果原下一行是空行
                    # 跳过空行，直接拼接，不添加「符号
                    merged_line = current_line + next_line
                elif next_line.startswith('「'):
                    # 已经有「符号，直接拼接
                    merged_line = current_line + next_line
                else:
                    # 没有「符号，添加后拼接
                    merged_line = current_line + '「' + next_line
                
                processed_lines.append(merged_line)
                i = next_index + 1  # 跳过已处理的行
            else:
                # 没有后续行，只添加当前行
                processed_lines.append(current_line)
                i += 1
        else:
            # 普通行，直接添加
            processed_lines.append(current_line)
            i += 1
    
    return processed_lines
def process_directory(directory: str, query_set: Set[str]) -> None:
    """
    处理指定目录下的所有txt文件
    
    Args:
        directory (str): 要处理的目录路径
        query_set (Set[str]): 查询表集合
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
        processed_lines = process_txt_file(filepath, query_set)
        
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
    print("Text File Processor with Query Table")
    print("=" * 40)
    
    # 加载查询表
    query_set = load_query_table(QUERY_TABLE_FILE)
    
    if not query_set:
        print("No query entries loaded. Exiting.")
        return
    
    # 获取要处理的目录
    directory = input("Enter the directory path to process (or press Enter for current directory): ").strip()
    if not directory:
        directory = "."
    
    # 处理目录中的文件
    process_directory(directory, query_set)
    print("Processing complete!")

if __name__ == "__main__":
    main()