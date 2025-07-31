#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from typing import List

def natural_sort_key(text):
    """
    Convert a string into a list of string and number chunks for natural sorting
    """
    return [int(c) if c.isdigit() else c.lower() for c in re.split('([0-9]+)', text)]

def concatenate_txt_files(input_directory: str, output_file: str) -> None:
    """
    Concatenate all txt files in a directory into a single file ordered by filename
    
    Args:
        input_directory (str): Directory containing txt files to concatenate
        output_file (str): Path to the output file
    """
    if not os.path.exists(input_directory):
        print(f"Error: Directory '{input_directory}' does not exist.")
        return
    
    # Get all txt files in the directory, sorted by natural order
    txt_files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]
    txt_files = sorted(txt_files, key=natural_sort_key)
    txt_files = [os.path.join(input_directory, f) for f in txt_files]
    
    if not txt_files:
        print(f"No txt files found in directory '{input_directory}'.")
        return
    
    print(f"Found {len(txt_files)} txt files to concatenate.")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for i, filepath in enumerate(txt_files):
                filename = os.path.basename(filepath)
                print(f"Processing file {i+1}/{len(txt_files)}: {filename}")
                
                # Read and write file content
                try:
                    with open(filepath, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                except Exception as e:
                    print(f"  Error reading file '{filename}': {e}")
        
        print(f"Successfully concatenated all files into: {output_file}")
        
    except Exception as e:
        print(f"Error writing to output file '{output_file}': {e}")

def main():
    print("Text File Concatenation Tool")
    print("=" * 30)
    
    # Get input directory
    input_directory = input("Enter the directory path containing txt files: ").strip()
    if not input_directory:
        print("Error: Input directory path cannot be empty.")
        return
    
    # Get output file path
    output_file = input("Enter the output file path (e.g., combined.txt): ").strip()
    if not output_file:
        print("Error: Output file path cannot be empty.")
        return
    
    # Process files
    concatenate_txt_files(input_directory, output_file)
    print("Concatenation complete!")

if __name__ == "__main__":
    main()