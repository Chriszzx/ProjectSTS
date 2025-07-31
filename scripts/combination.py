#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from typing import List, Set

QUERY_TABLE_FILE = "special_character.txt"

def load_query_table(filepath: str) -> Set[str]:
    query_set = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                query_set.add(line.rstrip('\n'))
        print(f"Successfully loaded {len(query_set)} entries from query table.")
    except FileNotFoundError:
        print(f"Error: Query table file '{filepath}' not found.")
    except Exception as e:
        print(f"Error loading query table: {e}")
    
    return query_set

def process_namespace(lines: List[str], query_set: Set[str]) -> List[str]:
    processed_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i]
        
        if current_line in query_set and i < len(lines) - 1:
            next_index = i + 1
            
            while next_index < len(lines) and lines[next_index].strip() == "":
                next_index += 1
            
            if next_index < len(lines):
                next_line = lines[next_index]
                
                if lines[i+1].strip() == "":  
                    merged_line = current_line + next_line
                elif next_line.startswith('「'):
                    merged_line = current_line + next_line
                else:
                    merged_line = current_line + '「' + next_line
                
                processed_lines.append(merged_line)
                i = next_index + 1
            else:
                processed_lines.append(current_line)
                i += 1
        else:
            processed_lines.append(current_line)
            i += 1
    
    return processed_lines

def process_add(lines: List[str]) -> List[str]:
    result_lines = []
    
    for line in lines:
        if line.startswith('「') and line.endswith('」'):
            modified_line = "遠野　紗夜" + line
            result_lines.append(modified_line)
        else:
            result_lines.append(line)
    
    return result_lines

def process_mark(lines: List[str]) -> List[str]:
    result_lines = []
    
    i = 0
    while i < len(lines):
        current_line = lines[i]
        count = 1
        
        j = i + 1
        while j < len(lines) and lines[j] == current_line:
            count += 1
            j += 1
        
        if count > 1:
            for k in range(count):
                marked_line = "#####" + current_line
                result_lines.append(marked_line)
        else:
            result_lines.append(current_line)
        
        i = j
    
    return result_lines

def process_txt_file(filepath: str, query_set: Set[str]) -> List[str]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return []
    
    lines = [line for line in lines if line.strip() != "" and "シナリオタイトル" not in line]
    
    namespace_processed = process_namespace(lines, query_set)
    
    add_processed = process_add(namespace_processed)
    
    mark_processed = process_mark(add_processed)
    
    return mark_processed

def process_directory(input_directory: str, output_directory: str, query_set: Set[str]) -> None:
    if not os.path.exists(input_directory):
        print(f"Error: Input directory '{input_directory}' does not exist.")
        return
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created output directory: {output_directory}")
    
    txt_files = [f for f in os.listdir(input_directory) if f.endswith('.txt') and 
                 os.path.isfile(os.path.join(input_directory, f))]
    
    if not txt_files:
        print(f"No txt files found in directory '{input_directory}'.")
        return
    
    print(f"Found {len(txt_files)} txt files to process.")
    
    for filename in txt_files:
        filepath = os.path.join(input_directory, filename)
        print(f"Processing file: {filename}")
        
        processed_lines = process_txt_file(filepath, query_set)
        
        if processed_lines:
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_processed{ext}"
            output_filepath = os.path.join(output_directory, output_filename)
            
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
    input_dir = "OG\split_output"
    output_dir = "OG\combined_output"
    
    print("Text File Processor - Combined Operations (namespace -> add -> mark)")
    print("=" * 60)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    query_set = load_query_table(QUERY_TABLE_FILE)
    
    if not query_set:
        print("No query entries loaded. Exiting.")
        return
    
    process_directory(input_dir, output_dir, query_set)
    print("Processing complete!")

if __name__ == "__main__":
    main()