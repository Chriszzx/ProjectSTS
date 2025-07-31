#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from typing import List

def create_single_txt_file(filename: str, content: str = "") -> bool:
    """
    Create a single txt file with specified name
    
    Args:
        filename (str): File name
        content (str): File content (optional)
        
    Returns:
        bool: Returns True if creation is successful, otherwise returns False
    """
    try:
        # Ensure the filename ends with .txt
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        # Create file and write content
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"✓ Successfully created file: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Error creating file {filename}: {e}")
        return False

def create_multiple_txt_files(filenames: List[str], content: str = "") -> None:
    """
    Batch create multiple txt files
    
    Args:
        filenames (List[str]): List of file names
        content (str): Default content for all files (optional)
    """
    success_count = 0
    failed_count = 0
    
    for filename in filenames:
        if create_single_txt_file(filename, content):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"\nCreation completed! Successful: {success_count}, Failed: {failed_count}")

def create_numbered_files(prefix: str, count: int, content: str = "") -> None:
    """
    Create multiple numbered files
    
    Args:
        prefix (str): File name prefix
        count (int): Number of files to create
        content (str): File content (optional)
    """
    filenames = [f"{prefix}_{i+1}" for i in range(count)]
    create_multiple_txt_files(filenames, content)

def create_files_from_list_file(list_file: str, content: str = "") -> None:
    """
    Create multiple txt files based on a file list
    
    Args:
        list_file (str): File containing the list of file names
        content (str): File content (optional)
    """
    try:
        with open(list_file, 'r', encoding='utf-8') as f:
            filenames = [line.strip() for line in f if line.strip()]
        
        create_multiple_txt_files(filenames, content)
        
    except FileNotFoundError:
        print(f"Error: Cannot find file list '{list_file}'")
    except Exception as e:
        print(f"Error reading file list: {e}")

def main():
    print("Batch TXT File Creation Tool")
    print("=" * 30)
    print("1. Manually enter multiple file names")
    print("2. Create numbered files")
    print("3. Create from file list")
    print("4. Create single file")
    
    choice = input("\nPlease select creation method (1-4): ").strip()
    
    if choice == "1":
        # Manually enter multiple file names
        print("Please enter file names, one per line, enter empty line to finish:")
        filenames = []
        while True:
            filename = input().strip()
            if not filename:
                break
            filenames.append(filename)
        
        if filenames:
            content = input("Please enter file content (optional): ")
            create_multiple_txt_files(filenames, content)
        else:
            print("No file names entered")
    
    elif choice == "2":
        # Create numbered files
        prefix = input("Please enter file name prefix: ").strip()
        if not prefix:
            print("Prefix cannot be empty")
            return
            
        try:
            count = int(input("Please enter number of files to create: "))
            if count <= 0:
                print("File count must be greater than 0")
                return
            content = input("Please enter file content (optional): ")
            create_numbered_files(prefix, count, content)
        except ValueError:
            print("Please enter a valid number")
    
    elif choice == "3":
        # Create from file list
        list_file = input("Please enter the file name containing the file list: ").strip()
        if not list_file:
            print("File name cannot be empty")
            return
        content = input("Please enter file content (optional): ")
        create_files_from_list_file(list_file, content)
    
    elif choice == "4":
        # Create single file
        filename = input("Please enter file name: ").strip()
        if not filename:
            print("File name cannot be empty")
            return
        content = input("Please enter file content (optional): ")
        create_single_txt_file(filename, content)
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()