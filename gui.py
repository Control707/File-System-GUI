import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import os
from file_manager import FileManager
import utils

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(utils.WINDOW_TITLE)
        self.root.geometry(f"{utils.WINDOW_WIDTH}x{utils.WINDOW_HEIGHT}")
        
        self.fm = FileManager()
        
        self.setup_ui()
        self.refresh_file_list()

    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(toolbar, text=f"{utils.ICON_UP} Up", command=self.go_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=f"{utils.ICON_HOME} Home", command=self.go_home).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text=f"{utils.ICON_REFRESH} Refresh", command=self.refresh_file_list).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)
        
        ttk.Button(toolbar, text="New File", command=self.create_file_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="New Folder", command=self.create_dir_dialog).pack(side=tk.LEFT, padx=2)

        # Path Bar
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(main_frame, textvariable=self.path_var, state='readonly')
        path_entry.pack(fill=tk.X, pady=(0, 10))

        # Content Area (Split Pane)
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # File List (Treeview)
        list_frame = ttk.Frame(paned_window)
        paned_window.add(list_frame, weight=1)

        columns = ('size', 'mtime')
        self.tree = ttk.Treeview(list_frame, columns=columns, selectmode='browse')
        self.tree.heading('#0', text='Name')
        self.tree.heading('size', text='Size')
        self.tree.heading('mtime', text='Date Modified')
        
        self.tree.column('#0', width=300)
        self.tree.column('size', width=100)
        self.tree.column('mtime', width=150)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bindings
        self.tree.bind('<Double-1>', self.on_item_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu) # Right click (Mac/Windows/Linux vary, handling commonly)
        self.tree.bind('<Button-2>', self.show_context_menu) # Right click for Mac sometimes

        # Preview/Editor Area
        self.editor_frame = ttk.LabelFrame(paned_window, text="File Preview/Edit")
        paned_window.add(self.editor_frame, weight=1)

        self.text_area = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        editor_toolbar = ttk.Frame(self.editor_frame)
        editor_toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(editor_toolbar, text="Save Changes", command=self.save_file_content).pack(side=tk.RIGHT)
        self.current_editing_file = None

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Context Menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.on_open_selected)
        self.context_menu.add_command(label="Rename", command=self.rename_dialog)
        self.context_menu.add_command(label="Delete", command=self.delete_dialog)

    def refresh_file_list(self):
        # Clear current list
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get new list
        result = self.fm.list_directory()
        if result['success']:
            self.path_var.set(self.fm.get_current_path())
            for item in result['items']:
                icon = utils.ICON_FOLDER if item['is_dir'] else utils.ICON_FILE
                size_str = f"{item['size']} B" if not item['is_dir'] else ""
                self.tree.insert('', 'end', iid=item['name'], text=f"{icon} {item['name']}", values=(size_str, item['mtime']))
                
            self.status_var.set(f"Loaded {len(result['items'])} items.")
        else:
            messagebox.showerror("Error", result['error'])
            self.status_var.set("Error loading directory.")

    def go_up(self):
        result = self.fm.navigate_up()
        if result['success']:
            self.refresh_file_list()
            self.clear_editor()

    def go_home(self):
        self.fm.current_path = os.path.expanduser("~")
        self.refresh_file_list()
        self.clear_editor()

    def on_item_double_click(self, event):
        self.on_open_selected()

    def on_open_selected(self):
        selection = self.tree.selection()
        if not selection:
            return
        
        item_name = selection[0]
        # Check if it's a directory or file based on icon or logic
        # We stored name as iid.
        
        # Re-fetch item details to be sure (or check icon)
        # Simple check: try to change dir, if fails, try to read file
        
        # Attempt to CD
        cd_result = self.fm.change_directory(self.fm.current_path / item_name)
        if cd_result['success']:
            self.refresh_file_list()
            self.clear_editor()
        else:
            # It's likely a file, try to read
            self.load_file_content(item_name)

    def load_file_content(self, filename):
        result = self.fm.read_file(filename)
        if result['success']:
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', result['content'])
            self.current_editing_file = filename
            self.status_var.set(f"Editing: {filename}")
        else:
            messagebox.showerror("Error", f"Cannot read file: {result['error']}")

    def save_file_content(self):
        if not self.current_editing_file:
            messagebox.showinfo("Info", "No file selected to save.")
            return
            
        content = self.text_area.get('1.0', tk.END + '-1c') # Remove trailing newline added by text widget
        result = self.fm.update_file(self.current_editing_file, content)
        if result['success']:
            self.status_var.set(f"Saved {self.current_editing_file}")
            messagebox.showinfo("Success", "File saved successfully.")
            self.refresh_file_list() # To update size/time
        else:
            messagebox.showerror("Error", f"Could not save: {result['error']}")

    def create_file_dialog(self):
        name = simpledialog.askstring("New File", "Enter file name:")
        if name:
            result = self.fm.create_file(name)
            if result['success']:
                self.refresh_file_list()
                self.status_var.set(f"Created file: {name}")
            else:
                messagebox.showerror("Error", result['error'])

    def create_dir_dialog(self):
        name = simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            result = self.fm.create_directory(name)
            if result['success']:
                self.refresh_file_list()
                self.status_var.set(f"Created folder: {name}")
            else:
                messagebox.showerror("Error", result['error'])

    def rename_dialog(self):
        selection = self.tree.selection()
        if not selection:
            return
        old_name = selection[0]
        new_name = simpledialog.askstring("Rename", f"Rename '{old_name}' to:", initialvalue=old_name)
        if new_name and new_name != old_name:
            result = self.fm.rename_item(old_name, new_name)
            if result['success']:
                self.refresh_file_list()
                self.status_var.set(f"Renamed {old_name} to {new_name}")
            else:
                messagebox.showerror("Error", result['error'])

    def delete_dialog(self):
        selection = self.tree.selection()
        if not selection:
            return
        name = selection[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
            result = self.fm.delete_item(name)
            if result['success']:
                self.refresh_file_list()
                self.status_var.set(f"Deleted {name}")
                if self.current_editing_file == name:
                    self.clear_editor()
            else:
                messagebox.showerror("Error", result['error'])

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def clear_editor(self):
        self.text_area.delete('1.0', tk.END)
        self.current_editing_file = None
