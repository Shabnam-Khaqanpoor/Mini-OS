Operating System Simulation

Project Overview

This project is a simulation of a simple operating system's file management system. It provides basic functionalities such as creating, deleting, renaming, compressing, and scheduling files. Additionally, it supports directory management, disk formatting, and metadata storage.

Features

  Disk Management

    Format disk (format_disk)

    Load disk (load_disk)

    Save metadata (save_metadata)

    Check storage space (check_storage)

  Block Management

    Allocate blocks (allocate_block)

    Free blocks (free_block)

    Write and read data to/from blocks (write_block, read_block)

  File Management

    Create, delete, rename, read, run files (create_file, delete_file, rename_file, read_file, run_file)

    Copy files (copy_file)

    Compress and decompress files (compress_file, decompress_file)

    Schedule file execution (schedule_file)

  Directory Management

    Create and remove directories (mkdir, rmdir)

    Change directory (cd, cdup)

    Show current directory (pwd)

  Utility Commands

    List files (list_files)

    Find files by keyword (find_file)

    Log executed commands (log_command)

    Display help menu (help_menu)

    Shut down the system (shutdown)

How to Run

    Ensure you have Python installed.

    Run the script using the command:  
    
      python Operating System.py
      
    Use the provided commands to interact with the system.

  Command Usage

    format - Formats the disk.

    create <file> <data> - Creates a new file with specified content.

    delete <file> - Deletes a file.

    rename <old> <new> - Renames a file.

    read <file> - Reads the content of a file.

    run <file> - Executes a file.

    dir - Lists all files and folders in the current directory.

    copy <src> <dest> - Copies a file.

    find <keyword> - Searches for files by keyword.

    mkdir <folder> - Creates a new directory.

    rmdir <folder> - Removes an empty directory.

    cd <folder> - Changes to a specified directory.

    cdup - Moves to the parent directory.

    pwd - Displays the current directory path.

    compress <file> - Compresses a file.

    decompress <file> - Decompresses a file.

    schedule <file> <time> - Schedules a file to run after a delay.

    storage - Displays disk usage information.

    help - Shows available commands.

    exit - Shuts down the system.
