# OwlTech File Manager

## Overview
This is a file management system built with Python and Tkinter for CS 3502 Project 3. It supports standard CRUD operations, directory navigation, and file editing.

## Requirements
- Python 3.x
- Tkinter (usually included with Python)

## How to Run
1. Navigate to the `OwlTechFileManager` directory.
2. Run the following command:
   ```bash
   python3 main.py
   ```

## Features
- **Navigation**: Browse directories, go up levels, go home.
- **Create**: Create new files and folders.
- **Read/Edit**: View and edit text files directly in the app.
- **Update**: Save changes to files.
- **Delete**: Remove files and folders (with confirmation).
- **Rename**: Rename files and folders.
- **Context Menu**: Right-click on items for quick actions.

## Structure
- `main.py`: Entry point.
- `gui.py`: Tkinter GUI implementation.
- `file_manager.py`: Backend file operations.
- `utils.py`: Constants and helpers.
