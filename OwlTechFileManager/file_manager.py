import os
import shutil
import time
from pathlib import Path

class FileManager:
    def __init__(self, initial_path=None):
        self.current_path = Path(initial_path) if initial_path else Path.cwd()
        if not self.current_path.exists():
            self.current_path = Path.cwd()

    def get_current_path(self):
        return str(self.current_path)

    def list_directory(self):
        """List contents of the current directory."""
        items = []
        try:
            for item in self.current_path.iterdir():
                stats = item.stat()
                items.append({
                    'name': item.name,
                    'path': str(item),
                    'is_dir': item.is_dir(),
                    'size': stats.st_size,
                    'mtime': time.ctime(stats.st_mtime)
                })
            # Sort: Directories first, then files
            items.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
            return {'success': True, 'items': items}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def change_directory(self, new_path):
        """Change the current directory."""
        target = Path(new_path)
        if target.exists() and target.is_dir():
            self.current_path = target.resolve()
            return {'success': True, 'path': str(self.current_path)}
        else:
            return {'success': False, 'error': "Directory not found"}

    def navigate_up(self):
        """Go to parent directory."""
        self.current_path = self.current_path.parent.resolve()
        return {'success': True, 'path': str(self.current_path)}

    def create_file(self, name, content=""):
        """Create a new file."""
        target = self.current_path / name
        if target.exists():
            return {'success': False, 'error': "File already exists"}
        try:
            with open(target, 'w') as f:
                f.write(content)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_directory(self, name):
        """Create a new directory."""
        target = self.current_path / name
        if target.exists():
            return {'success': False, 'error': "Directory already exists"}
        try:
            target.mkdir()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def read_file(self, name):
        """Read file content."""
        target = self.current_path / name
        if not target.exists():
            return {'success': False, 'error': "File not found"}
        if not target.is_file():
            return {'success': False, 'error': "Not a file"}
        try:
            with open(target, 'r') as f:
                content = f.read()
            return {'success': True, 'content': content}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def update_file(self, name, content):
        """Update/Overwrite file content."""
        target = self.current_path / name
        if not target.exists():
            return {'success': False, 'error': "File not found"}
        try:
            with open(target, 'w') as f:
                f.write(content)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def delete_item(self, name):
        """Delete a file or directory."""
        target = self.current_path / name
        if not target.exists():
            return {'success': False, 'error': "Item not found"}
        try:
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def rename_item(self, old_name, new_name):
        """Rename a file or directory."""
        old_target = self.current_path / old_name
        new_target = self.current_path / new_name
        if not old_target.exists():
            return {'success': False, 'error': "Item not found"}
        if new_target.exists():
            return {'success': False, 'error': "Destination already exists"}
        try:
            old_target.rename(new_target)
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
