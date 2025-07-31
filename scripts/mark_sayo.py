#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from typing import List

def process_txt_file(filepath: str) -> List[str]:
    """
    Process a single txt file, mark consecutive duplicate lines (add 5 # at the beginning)
    
    Args:
        filepath (str): Path to the file to process
        
    Returns:
        List[str]: Processed lines
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return []
    
    # Remove all empty lines
    lines = [line for line in lines if line.strip() != ""]
    
    # Store processed lines
    result_lines = []
    
    # Process file
    i = 0
    while i < len(lines):
        current_line = lines[i]
        count = 1
        
        # Count consecutive duplicate lines
        j = i + 1
        while j < len(lines) and lines[j] == current_line:
            count += 1
            j += 1
        
        if count > 1:
            # If there are consecutive duplicate lines, mark all duplicate lines
            for k in range(count):
                marked_line = "#####" + current_line
                result_lines.append(marked_line)
        else:
            # No duplicate lines, add directly
            result_lines.append(current_line)
        
        # Move to the next group of non-duplicate lines
        i = j
    
    return result_lines

def process_directory(directory: str) -> None:
    """
    Process all txt files in the specified directory
    
    Args:
        directory (str): Path to the directory to process
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
        
        # Process file
        processed_lines = process_txt_file(filepath)
        
        if processed_lines:
            # Generate output filename
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_processed{ext}"
            output_filepath = os.path.join(directory, output_filename)
            
            # Write processed content
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
    print("Text File Processor - Mark Consecutive Duplicate Lines")
    print("=" * 50)
    
    # Get directory to process
    directory = input("Enter the directory path to process (or press Enter for current directory): ").strip()
    if not directory:
        directory = "."
    
    # Process files in directory
    process_directory(directory)
    print("Processing complete!")

if __name__ == "__main__":
    main()