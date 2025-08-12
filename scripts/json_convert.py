import os
import json
import re

def has_japanese_or_chinese(text):
    """
    检查文本是否包含日文或中文字符
    """
    # 日文字符范围: \u3040-\u309F(平假名), \u30A0-\u30FF(片假名), \u4E00-\u9FFF(CJK统一汉字)
    japanese_chinese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]')
    return bool(japanese_chinese_pattern.search(text))

def has_japanese_characters(text):
    """
    检查文本是否包含日文字符（假名）
    """
    # 日文字符范围: \u3040-\u309F(平假名), \u30A0-\u30FF(片假名)
    japanese_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF]')
    return bool(japanese_pattern.search(text))

def natural_sort_key(text):
    """
    自然排序的键函数，将字符串中的数字部分转换为整数进行比较
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', text)]

def read_txt_files_and_convert_to_json(directory_path, output_file):
    """
    读取目录下所有txt文件，将日文与中文翻译转换为JSON格式
    
    文件格式要求：
    - 日文文本
    - 对应的中文翻译
    - 空行（将被跳过）
    - 重复以上格式
    """
    result_dict = {}
    
    # 遍历目录下所有txt文件，按文件名自然排序（数字顺序）
    filenames = sorted([f for f in os.listdir(directory_path) if f.endswith('.txt')], 
                       key=natural_sort_key)
    
    for filename in filenames:
        file_path = os.path.join(directory_path, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # 过滤掉只有标点符号的行，只保留包含日文或中文字符的行
            lines = []
            for line in f.readlines():
                stripped_line = line.strip()
                if stripped_line and has_japanese_or_chinese(stripped_line):
                    lines.append(stripped_line)
            
        # 处理行，将日文和中文配对
        i = 0
        while i < len(lines):
            # 确保还有两行可以读取
            if i + 1 < len(lines):
                japanese = lines[i]
                next_line = lines[i + 1]
                
                # 检查下一行是否包含日文字符（假名），如果是则跳过当前行
                if has_japanese_characters(next_line):
                    # 下一行包含日文字符，跳过当前行
                    i += 1
                else:
                    # 下一行不包含日文字符，正常配对
                    result_dict[japanese] = next_line
                    i += 2
            else:
                # 如果只剩最后一行，跳过
                i += 1

    # 将结果写入JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=4)
    
    print(f"转换完成，共处理 {len(result_dict)} 对翻译，保存至 {output_file}")


def main():
    # 设置目录路径和输出文件路径
    directory_path = "Qwen/ja_zh"  # 当前目录，可根据需要修改
    output_file = "STS.json"  # 输出文件名
    
    read_txt_files_and_convert_to_json(directory_path, output_file)

if __name__ == "__main__":
    main()