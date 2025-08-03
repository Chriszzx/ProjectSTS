# -*- coding: utf-8 -*-
"""
功能：统计 input.txt 字符，对比 tbl.txt 是否包含，若无则追加到 tbl.txt 末尾
新增格式：新码位=字符（码位从当前最大 +1 开始）
"""

def read_input_chars(input_file):
    """读取 input.txt，返回所有字符的集合"""
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    return set(text)


def read_tbl_mapping(tbl_file):
    """
    读取 TBL 文件，返回：
    - 已存在的字符集合
    - 最后一个码位（十六进制整数）
    - 原始行列表（用于追加）
    """
    chars_in_tbl = set()
    last_code = 0x8000  # 初始码位，防止为空
    lines = []

    try:
        with open(tbl_file, 'r', encoding='gbk') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []

    for line in lines:
        line = line.strip()
        if not line or '=' not in line:
            continue
        hex_code, char = line.split('=', 1)
        hex_code = hex_code.strip()
        char = char.strip()

        # 只取第一个字符（避免注释干扰）
        if char:
            chars_in_tbl.add(char[0])

        try:
            code_val = int(hex_code, 16)
            if code_val > last_code:
                last_code = code_val
        except ValueError:
            continue  # 忽略无效十六进制

    return chars_in_tbl, last_code, lines


def write_new_entries(tbl_file, new_entries, original_lines):
    """
    将新条目追加到 TBL 文件末尾
    new_entries: list of (hex_str, char)
    """
    with open(tbl_file, 'w', encoding='gbk') as f:
        # 写入原始内容
        f.writelines(original_lines)
        # 如果原文件没有换行，添加一个
        if original_lines and not original_lines[-1].endswith('\n'):
            f.write('\n')
        # 写入新条目
        for hex_code, char in new_entries:
            f.write(f"{hex_code}={char}\n")


def main(input_txt, tbl_file):
    # 1. 读取输入文件字符
    print("正在读取输入文件...")
    input_chars = read_input_chars(input_txt)

    # 2. 读取 TBL 文件信息
    print("正在读取 TBL 文件...")
    tbl_chars, last_code, original_lines = read_tbl_mapping(tbl_file)

    # 3. 找出缺失字符（在 input 中但不在 tbl 中）
    missing_chars = input_chars - tbl_chars
    print(f"共发现 {len(input_chars)} 个不同字符")
    print(f"TBL 中已有 {len(tbl_chars)} 个字符")
    print(f"需要新增 {len(missing_chars)} 个字符")

    if not missing_chars:
        print("无需新增字符。")
        return

    # 4. 按 GBK 编码排序（确保顺序一致）
    def to_gbk_hex(char):
        try:
            return char.encode('gbk')
        except UnicodeEncodeError:
            return b'\xFF\xFE'  # 无效编码放最后

    sorted_missing = sorted(missing_chars, key=to_gbk_hex)

    # 5. 分配新码位（从 last_code + 1 开始）
    current_code = last_code + 1
    new_entries = []

    for char in sorted_missing:
        # 跳过控制字符或非双字节合理范围（可选）
        if current_code > 0xFFFF:
            print("警告：码位超出范围（>0xFFFF），停止分配")
            break

        # 格式化为 4 位大写十六进制
        hex_code = f"{current_code:04X}"
        new_entries.append((hex_code, char))
        current_code += 1

    # 6. 写入新条目
    write_new_entries(tbl_file, new_entries, original_lines)
    print(f"已成功追加 {len(new_entries)} 个新字符到 {tbl_file}")

    # 显示前 10 个新增示例
    print("\n新增条目示例：")
    for hex_code, char in new_entries[:10]:
        print(f"{hex_code}={char}")
    if len(new_entries) > 10:
        print("...")



# =============== 使用示例 ===============
if __name__ == "__main__":
    INPUT_FILE = "input.txt"      # 你的输入文本
    TBL_FILE = "JP2GBK.TBL"       # 你的码表文件

    main(INPUT_FILE, TBL_FILE)
