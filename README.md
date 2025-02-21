# miniOS

## 📂 Operating System File System Simulation

miniOS is a **file system simulation** implemented in Python, providing functionalities for file creation, deletion, renaming, compression, scheduling, and directory management. It simulates a **FAT-based** file system with **block-based storage**, including disk formatting and metadata management.

---

## 🚀 Features

✅ **Virtual Disk Management** with block-based allocation\
✅ **File Operations**: Create, delete, rename, read, and execute files\
✅ **Directory Management**: Create, remove, and navigate directories\
✅ **Compression & Decompression** using **zlib**\
✅ **File Scheduling**: Execute files after a time delay\
✅ **Storage Management**: Check disk usage and available space\
✅ **Command Logging** for auditing user actions

---

## 📁 Project Structure

```
miniOS/
│── Operating System.py      # Core file system implementation
│── disk.img                 # Virtual disk storage
│── log.txt                  # Logs executed commands
│── README.md                # Project documentation
```

---

## 🔧 Installation & Setup

### **1️⃣ Prerequisites**

Ensure you have:

- Python 3.x installed

### **2️⃣ Clone the Repository**

```bash
git clone https://github.com/Shabnam2003/miniOS.git
cd miniOS
```

### **3️⃣ Running the File System**

Start the file system simulation:

```bash
python Operating System.py
```

---

## 📌 Usage

### **Available Commands**

| Command                  | Description                             |
| ------------------------ | --------------------------------------- |
| `format`                 | Format the virtual disk                 |
| `create <file> <data>`   | Create a new file with content          |
| `delete <file>`          | Delete a file                           |
| `rename <old> <new>`     | Rename a file                           |
| `read <file>`            | Read file contents                      |
| `run <file>`             | Execute Python code in a file           |
| `dir`                    | List all files in the current directory |
| `copy <src> <dest>`      | Copy a file                             |
| `find <keyword>`         | Search for files by name                |
| `mkdir <folder>`         | Create a new folder                     |
| `rmdir <folder>`         | Remove an empty folder                  |
| `cd <folder>`            | Change directory                        |
| `cdup`                   | Move to the parent directory            |
| `pwd`                    | Show the current directory              |
| `compress <file>`        | Compress a file using zlib              |
| `decompress <file>`      | Decompress a file                       |
| `schedule <file> <time>` | Run a file after a delay (seconds)      |
| `storage`                | Display disk usage                      |
| `help`                   | Show available commands                 |
| `exit`                   | Shut down the file system               |

---
