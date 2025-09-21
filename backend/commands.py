# backend/commands.py
import os
import shlex
import subprocess
from pathlib import Path
from backend.system_monitor import get_cpu_usage, get_memory_usage, get_process_list

class CommandExecutor:
    def __init__(self):
        self.cwd = Path.home()

    def run(self, command: str) -> str:
        command = command.strip()
        if not command:
            return ""

        args = shlex.split(command)
        cmd = args[0]

        try:
            # Navigation
            if cmd == "pwd":
                return str(self.cwd)

            elif cmd == "ls":
                try:
                    return "\n".join(os.listdir(self.cwd))
                except PermissionError:
                    return "ls: permission denied"

            elif cmd == "cd":
                if len(args) < 2:
                    return "cd: missing argument"
                path_input = args[1]

                # Expand ~ to home directory
                path_input = os.path.expanduser(path_input)
                new_dir = Path(path_input)

                # If relative path, resolve relative to current cwd
                if not new_dir.is_absolute():
                    new_dir = self.cwd / new_dir

                new_dir = new_dir.resolve()

                if new_dir.exists() and new_dir.is_dir():
                    self.cwd = new_dir
                    return ""
                return f"cd: no such directory: {args[1]}"

            # File ops
            elif cmd == "mkdir":
                if len(args) < 2:
                    return "mkdir: missing argument"
                target = self.cwd / args[1]
                os.makedirs(target, exist_ok=True)
                return ""

            elif cmd == "rm":
                if len(args) < 2:
                    return "rm: missing argument"
                target = self.cwd / args[1]
                if target.is_file():
                    target.unlink()
                elif target.is_dir():
                    os.rmdir(target)
                else:
                    return f"rm: no such file or directory: {args[1]}"
                return ""

            # Monitoring
            elif cmd == "cpu":
                return get_cpu_usage()

            elif cmd == "mem":
                return get_memory_usage()

            elif cmd == "ps":
                return get_process_list()

            # System command fallback
            else:
                proc = subprocess.run(args, cwd=self.cwd, capture_output=True, text=True, shell=True)
                output = proc.stdout.strip()
                err = proc.stderr.strip()
                return "\n".join([line for line in [output, err] if line])

        except Exception as e:
            return f"Error: {str(e)}"
