import os
import time
import zlib

# Constants for file system simulation
DISK_FILE = "disk.img"
BLOCK_SIZE = 512
NUM_BLOCKS = 1024
FAT_TABLE_SIZE = NUM_BLOCKS
ROOT_DIR_SIZE = 64


# Initialize the file system--------------------------------------------------------------------------------------------
class FileSystem:
    def __init__(self):
        try:
            self.disk = None
            self.fat = [0] * FAT_TABLE_SIZE
            self.root_dir = {"/": {}}  # Root directory structure
            self.current_dir = "/"  # Start in root directory
            self.log_file = "log.txt"
        except Exception as e:
            print(f"Initialization error: {e}")

    # -----------------------------------------------------------------------------------------------------------------------
    def format_disk(self):
        try:
            # Create and format the virtual disk
            with open(DISK_FILE, 'wb') as disk:
                disk.write(b'\x00' * BLOCK_SIZE * NUM_BLOCKS)
            self.fat = [0] * FAT_TABLE_SIZE
            self.root_dir = {"/": {}}
            self.current_dir = "/"
            print("Disk formatted.")
            self.load_disk()  # Reopen the disk after formatting
        except IOError as e:
            print(f"Error formatting disk: {e}")

    # -----------------------------------------------------------------------------------------------------------------------
    def load_disk(self):
        try:
            # Load the existing disk file
            if not os.path.exists(DISK_FILE):
                print("Disk not found. Formatting a new disk.")
                self.format_disk()
            self.disk = open(DISK_FILE, 'r+b')
        except IOError as e:
            print(f"Error loading disk: {e}")

    # -----------------------------------------------------------------------------------------------------------------------
    def allocate_block(self):
        try:
            # Allocate a free block from FAT
            for i in range(FAT_TABLE_SIZE):
                if self.fat[i] == 0:
                    self.fat[i] = -1
                    return i
            raise Exception("Disk is full.")
        except Exception as e:
            print(f"Error allocating block: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def free_block(self, block_index):
        try:
            # Free a block in FAT
            self.fat[block_index] = 0
        except IndexError as e:
            print(f"Error freeing block: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def write_block(self, block_index, data):
        try:
            if len(data) > BLOCK_SIZE:
                raise Exception("Data exceeds block size.")
            self.disk.seek(block_index * BLOCK_SIZE)
            self.disk.write(data.ljust(BLOCK_SIZE, b'\x00'))
        except Exception as e:
            print(f"Error writing block: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def read_block(self, block_index):
        try:
            self.disk.seek(block_index * BLOCK_SIZE)
            return self.disk.read(BLOCK_SIZE)
        except Exception as e:
            print(f"Error reading block: {e}")
            return b''

    # -------------------------------------------------------------------------------------------------------------------
    def create_file(self, filename, content):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename in dir_content:
                print("File already exists.")
                return

            blocks_needed = (len(content) + BLOCK_SIZE - 1) // BLOCK_SIZE
            block_chain = []

            # Allocate blocks
            for _ in range(blocks_needed):
                block_index = self.allocate_block()
                block_chain.append(block_index)

            # Write content to blocks
            for i, block_index in enumerate(block_chain):
                self.write_block(block_index, content[i * BLOCK_SIZE:(i + 1) * BLOCK_SIZE])

            # Update current directory
            dir_content[filename] = block_chain
            print(f"File '{filename}' created.")
        except Exception as e:
            print(f"Error creating file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def delete_file(self, filename):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename not in dir_content:
                print("File not found.")
                return

            block_chain = dir_content.pop(filename)
            for block_index in block_chain:
                self.free_block(block_index)
            print(f"File '{filename}' deleted.")
        except Exception as e:
            print(f"Error deleting file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def rename_file(self, old_name, new_name):
        try:
            dir_content = self.navigate_to_current_dir()
            if old_name not in dir_content:
                print("File not found.")
                return

            if new_name in dir_content:
                print("File with the new name already exists.")
                return

            dir_content[new_name] = dir_content.pop(old_name)
            print(f"File renamed from '{old_name}' to '{new_name}'.")
        except Exception as e:
            print(f"Error renaming file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def read_file(self, filename):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename not in dir_content:
                print("File not found.")
                return

            block_chain = dir_content[filename]
            content = b''.join(self.read_block(block_index) for block_index in block_chain)
            print(content.decode('utf-8').rstrip('\x00'))
        except Exception as e:
            print(f"Error reading file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def run_file(self, filename):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename not in dir_content:
                print("File not found.")
                return

            block_chain = dir_content[filename]
            content = b''.join(self.read_block(block_index) for block_index in block_chain)
            code = content.decode('utf-8').rstrip('\x00')
            try:
                exec(code)
            except SyntaxError:
                print("The file content is not valid Python code.")
            except Exception as e:
                print(f"Error while executing file: {e}")
        except Exception as e:
            print(f"Error running file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def list_files(self):
        try:
            dir_content = self.navigate_to_current_dir()
            print(f"Files in directory '{self.current_dir}':")
            for name in dir_content:
                print(f"- {name}")
        except Exception as e:
            print(f"Error listing files: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def mkdir(self, foldername):
        try:
            dir_content = self.navigate_to_current_dir()
            if foldername in dir_content:
                print("Folder already exists.")
                return

            dir_content[foldername] = {}  # Representing an empty folder
            print(f"Folder '{foldername}' created.")
        except Exception as e:
            print(f"Error creating folder: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def rmdir(self, foldername):
        try:
            dir_content = self.navigate_to_current_dir()
            if foldername not in dir_content or not isinstance(dir_content[foldername], dict):
                print("Folder not found.")
                return

            if dir_content[foldername]:
                print("Folder is not empty.")
                return

            dir_content.pop(foldername)
            print(f"Folder '{foldername}' removed.")
        except Exception as e:
            print(f"Error removing folder: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def cd(self, foldername):
        try:
            if foldername == "..":
                self.cdup()
                return

            dir_content = self.navigate_to_current_dir()
            if foldername not in dir_content:
                print("Folder not found.")
                return

            if not isinstance(dir_content[foldername], dict):
                print(f"'{foldername}' is not a folder.")
                return

            self.current_dir = self.current_dir.rstrip("/") + "/" + foldername
            print(f"Current directory changed to '{self.current_dir}'.")
        except Exception as e:
            print(f"Error changing directory: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def cdup(self):
        try:
            if self.current_dir == "/":
                print("Already in the root directory.")
                return

            self.current_dir = "/".join(self.current_dir.rstrip("/").split("/")[:-1]) or "/"
            print(f"Current directory changed to '{self.current_dir}'.")
        except Exception as e:
            print(f"Error moving to parent directory: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def pwd(self):
        try:
            print(f"Current directory: {self.current_dir}")
        except Exception as e:
            print(f"Error displaying current directory: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def navigate_to_current_dir(self):
        try:
            parts = [p for p in self.current_dir.split("/") if p]
            dir_content = self.root_dir["/"]
            for part in parts:
                dir_content = dir_content[part]
            return dir_content
        except Exception as e:
            print(f"Error navigating to current directory: {e}")
            return {}

    # -------------------------------------------------------------------------------------------------------------------

    def compress_file(self, filename):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename not in dir_content:
                print("File not found.")
                return

            block_chain = dir_content[filename]
            content = b''.join(self.read_block(block_index) for block_index in block_chain)
            compressed_content = zlib.compress(content)

            compressed_filename = filename + ".zip"
            self.create_file(compressed_filename, compressed_content)
            print(f"File '{filename}' compressed to '{compressed_filename}'.")
        except Exception as e:
            print(f"Error compressing file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def decompress_file(self, filename):
        try:
            dir_content = self.navigate_to_current_dir()
            if not filename.endswith(".zip") or filename not in dir_content:
                print("Compressed file not found.")
                return

            block_chain = dir_content[filename]
            compressed_content = b''.join(self.read_block(block_index) for block_index in block_chain)
            try:
                content = zlib.decompress(compressed_content)
            except zlib.error:
                print("Error decompressing file.")
                return

            original_filename = filename[:-4]
            self.create_file(original_filename, content)
            print(f"File '{filename}' decompressed to '{original_filename}'.")
        except Exception as e:
            print(f"Error decompressing file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def schedule_file(self, filename, delay):
        try:
            dir_content = self.navigate_to_current_dir()
            if filename not in dir_content:
                print("File not found.")
                return

            print(f"File '{filename}' scheduled to run after {delay} seconds.")
            time.sleep(delay)
            self.run_file(filename)
        except Exception as e:
            print(f"Error scheduling file: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def log_command(self, command):
        try:
            with open(self.log_file, 'a') as log:
                log.write(command + '\n')
        except Exception as e:
            print(f"Error logging command: {e}")

    # -------------------------------------------------------------------------------------------------------------------
    def help_menu(self):
        try:
            print("Available commands:")
            print("  format               - Format the disk.")
            print("  create <file> <data> - Create a file with specified data.")
            print("  delete <file>        - Delete a file.")
            print("  rename <old> <new>   - Rename a file.")
            print("  read <file>          - Read and display a file's content.")
            print("  run <file>           - Execute the content of a file.")
            print("  dir                  - List all files and folders in the current directory.")
            print("  copy <src> <dest>    - Copy a file to a new file.")
            print("  find <keyword>       - Search for files by keyword.")
            print("  mkdir <folder>       - Create a new folder.")
            print("  rmdir <folder>       - Remove an empty folder.")
            print("  cd <folder>          - Change to a specific folder.")
            print("  cdup                 - Move up to the parent directory.")
            print("  pwd                  - Show the current directory path.")
            print("  compress <file>      - Compress a file.")
            print("  decompress <file>    - Decompress a file.")
            print("  schedule <file> <time> - Schedule a file to run after a delay (in seconds).")
            print("  help                 - Show this help menu.")
            print("  exit                 - Exit the system.")
        except Exception as e:
            print(f"Error displaying help menu: {e}")

    # -----------------------------------------------------------------------------------------------------------------------
    def shutdown(self):
        try:
            self.disk.close()
            print("Disk shut down.")
        except Exception as e:
            print(f"Error shutting down the disk: {e}")


# Command line interface------------------------------------------------------------------------------------------------
def main():
    try:
        fs = FileSystem()
        fs.load_disk()

        while True:
            command = input("C:\\> ").strip()
            if not command:
                continue

            fs.log_command(command)
            args = command.split()
            cmd = args[0].lower()
            params = args[1:]

            try:
                if cmd == "format":
                    fs.format_disk()
                elif cmd == "create" and len(params) == 2:
                    fs.create_file(params[0], params[1].encode('utf-8'))
                elif cmd == "delete" and len(params) == 1:
                    fs.delete_file(params[0])
                elif cmd == "rename" and len(params) == 2:
                    fs.rename_file(params[0], params[1])
                elif cmd == "read" and len(params) == 1:
                    fs.read_file(params[0])
                elif cmd == "run" and len(params) == 1:
                    fs.run_file(params[0])
                elif cmd == "dir":
                    fs.list_files()
                elif cmd == "copy" and len(params) == 2:
                    fs.copy_file(params[0], params[1])
                elif cmd == "find" and len(params) == 1:
                    fs.find_file(params[0])
                elif cmd == "mkdir" and len(params) == 1:
                    fs.mkdir(params[0])
                elif cmd == "rmdir" and len(params) == 1:
                    fs.rmdir(params[0])
                elif cmd == "cd" and len(params) == 1:
                    fs.cd(params[0])
                elif cmd == "cdup":
                    fs.cdup()
                elif cmd == "pwd":
                    fs.pwd()
                elif cmd == "compress" and len(params) == 1:
                    fs.compress_file(params[0])
                elif cmd == "decompress" and len(params) == 1:
                    fs.decompress_file(params[0])
                elif cmd == "schedule" and len(params) == 2:
                    try:
                        delay = int(params[1])
                        fs.schedule_file(params[0], delay)
                    except ValueError:
                        print("Invalid time format. Please provide an integer.")
                elif cmd == "help":
                    fs.help_menu()
                elif cmd == "exit":
                    fs.shutdown()
                    break
                else:
                    print("Invalid command or arguments.")
            except Exception as e:
                print(f"Error executing command '{cmd}': {e}")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
