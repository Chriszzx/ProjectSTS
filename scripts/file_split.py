#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import List

def split_file_by_delimiter(input_file: str, delimiter: str, output_prefix: str = "split_output") -> bool:
    """
    Read a specified txt file and split its content based on delimiter lines.
    Each segment (including the delimiter line) is saved as a separate file.
    
    Args:
        input_file (str): Path to the input file
        delimiter (str): The delimiter string to search for
        output_prefix (str): Prefix for output files
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False
            
        # Read all lines from the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("Warning: Input file is empty.")
            return True
            
        # Process lines and split by delimiter
        segments = []
        current_segment = []
        file_counter = 1
        
        for i, line in enumerate(lines):
            current_segment.append(line)
            
            # Check if current line contains the delimiter
            if delimiter in line:
                # Save current segment
                segments.append(current_segment.copy())
                current_segment.clear()
                # Add the delimiter line to the next segment
                current_segment.append(line)
        
        # Add the remaining lines as the last segment (if any)
        if current_segment:
            segments.append(current_segment)
            
        # Write segments to separate files
        for i, segment in enumerate(segments):
            output_filename = f"{output_prefix}_{i+1}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.writelines(segment)
            print(f"Created file: {output_filename} with {len(segment)} lines")
            
        print(f"Split complete! Created {len(segments)} files.")
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def main():
    print("File Splitter by Delimiter")
    print("=" * 30)
    
    # Get input parameters
    input_file = input("Enter the path to the input file: ").strip()
    if not input_file:
        print("Error: Input file path cannot be empty.")
        return
    
    delimiter = input("Enter the delimiter string: ").strip()
    if not delimiter:
        print("Error: Delimiter string cannot be empty.")
        return
    
    output_prefix = input("Enter output file prefix (optional, default: split_output): ").strip()
    if not output_prefix:
        output_prefix = "split_output"
    
    # Process the file
    success = split_file_by_delimiter(input_file, delimiter, output_prefix)
    
    if success:
        print("File splitting completed successfully!")
    else:
        print("File splitting failed.")

if __name__ == "__main__":
    main()