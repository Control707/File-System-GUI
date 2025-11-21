# Video Demo Script: OwlTech File Manager

**Target Duration:** 3-5 Minutes
**Project:** OwlTech File Manager (CS 3502 Project 3)
**Presenter:** [Your Name]

---

## 1. Introduction (Approx. 30 seconds)

**Visual:** Camera on you or Title Screen with Project Name and your details.

**Audio:**
"Hello, my name is [Your Name]. This is my submission for the CS 3502 Operating Systems Project 3: The OwlTech File Manager.

In this project, I have built a functional file management system using **Python** and the **Tkinter** GUI framework. The goal was to bridge the gap between low-level OS file operations and a user-friendly graphical interface.

I chose Python for its robust `pathlib` and `shutil` libraries, which make handling file system operations efficient and cross-platform. Let's dive into the demo."

---

## 2. Demonstration (Approx. 2-3 minutes)

**Visual:** Screen recording of the OwlTech File Manager application.

### A. Basic File Operations (Create, Read, Update)
**Action:**
1.  Click the **"New File"** button.
2.  Enter a name, e.g., `demo_notes.txt`.
3.  Click OK.
4.  Point out the new file appearing in the list.
5.  **Double-click** `demo_notes.txt` to open it.
6.  In the "File Preview/Edit" pane (right side), type some text: "Hello, this is a test of the file system."
7.  Click **"Save Changes"**.

**Audio:**
"First, I'll demonstrate creating a new file. I click 'New File', name it `demo_notes.txt`, and you can see it appears instantly in our file list.

Next, I'll read and update the file. By double-clicking it, the content loads into the editor pane. I'll add some text—'Hello, this is a test'—and click 'Save Changes'. The system writes this data back to the disk immediately."

### B. Directory Operations & Navigation
**Action:**
1.  Click **"New Folder"**.
2.  Name it `Project_Docs`.
3.  Double-click `Project_Docs` in the list to enter the directory.
4.  Show that the list is empty (or contains default items if any).
5.  Click the **"Up"** button to go back to the previous directory.

**Audio:**
"Now for directory operations. I'll create a new directory called `Project_Docs`. I can navigate into it by double-clicking, and as expected, it's currently empty. I'll use the 'Up' button to return to our main directory."

### C. Rename and Move/Copy
**Action:**
1.  Select `demo_notes.txt`.
2.  Right-click and select **"Rename"**.
3.  Change the name to `final_notes.txt`.
4.  *(Note: If your GUI supports moving via rename by typing a path, demonstrate it. Otherwise, skip the 'Move' part or mention it as a future feature if strictly not implemented.)*
    *   *Optional Try:* Rename `final_notes.txt` to `Project_Docs/final_notes.txt` (if your code supports relative path renaming).

**Audio:**
"I can also rename items. I'll rename `demo_notes.txt` to `final_notes.txt`. The list updates automatically."

### D. Deletion
**Action:**
1.  Select `final_notes.txt` (or the file you moved).
2.  Right-click and select **"Delete"**.
3.  Show the confirmation dialog ("Are you sure...?").
4.  Click **"Yes"**.
5.  Show the file is gone.

**Audio:**
"To delete a file, I simply right-click and choose 'Delete'. The system asks for confirmation to prevent accidental data loss. Once confirmed, the file is removed permanently."

### E. Error Handling
**Action:**
1.  Click **"New File"**.
2.  Enter the name of an *existing* file or folder (e.g., `Project_Docs` if it's still there).
3.  Show the error message popup: "File already exists" or similar.

**Audio:**
"Finally, the system handles errors gracefully. For example, if I try to create a file with a name that already exists, the system detects the conflict and displays a user-friendly error message instead of crashing."

---

## 3. Code Walkthrough (Approx. 1 minute)

**Visual:** Switch to your IDE (VS Code, PyCharm, etc.) showing the code.

### A. Backend Logic (`file_manager.py`)
**Action:** Open `file_manager.py`. Scroll to `FileManager` class.

**Audio:**
"The core logic resides in `file_manager.py`. The `FileManager` class encapsulates all OS interactions.
I used Python's `pathlib` library for object-oriented filesystem paths.
For example, the `create_file` method checks for existence before opening a file in write mode, ensuring we don't accidentally overwrite data without intent."

### B. GUI Implementation (`gui.py`)
**Action:** Open `gui.py`. Scroll to `refresh_file_list` method.

**Audio:**
"The GUI is built with Tkinter in `gui.py`. The `refresh_file_list` function is crucial—it calls the backend to get the current directory state and dynamically populates the Treeview widget.
I also implemented a split-pane design to allow simultaneous file browsing and editing."

---

## 4. Conclusion (Approx. 30 seconds)

**Visual:** Back to camera or Project Title Screen.

**Audio:**
"In summary, the OwlTech File Manager successfully implements all required CRUD operations, directory navigation, and robust error handling in a clean, graphical interface.
It demonstrates how operating systems abstract complex file operations into simple user actions.
Thank you for watching!"
