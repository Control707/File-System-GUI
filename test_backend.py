import unittest
import os
import shutil
from pathlib import Path
from file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_env")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        self.fm = FileManager(initial_path=str(self.test_dir))

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_create_file(self):
        res = self.fm.create_file("test.txt", "hello")
        self.assertTrue(res['success'])
        self.assertTrue((self.test_dir / "test.txt").exists())

    def test_read_file(self):
        self.fm.create_file("read.txt", "content")
        res = self.fm.read_file("read.txt")
        self.assertTrue(res['success'])
        self.assertEqual(res['content'], "content")

    def test_update_file(self):
        self.fm.create_file("update.txt", "old")
        res = self.fm.update_file("update.txt", "new")
        self.assertTrue(res['success'])
        with open(self.test_dir / "update.txt", 'r') as f:
            self.assertEqual(f.read(), "new")

    def test_delete_file(self):
        self.fm.create_file("del.txt")
        res = self.fm.delete_item("del.txt")
        self.assertTrue(res['success'])
        self.assertFalse((self.test_dir / "del.txt").exists())

    def test_create_directory(self):
        res = self.fm.create_directory("subdir")
        self.assertTrue(res['success'])
        self.assertTrue((self.test_dir / "subdir").is_dir())

    def test_navigate(self):
        self.fm.create_directory("subdir")
        res = self.fm.change_directory(self.test_dir / "subdir")
        self.assertTrue(res['success'])
        self.assertEqual(self.fm.get_current_path(), str((self.test_dir / "subdir").resolve()))
        
        res = self.fm.navigate_up()
        self.assertTrue(res['success'])
        self.assertEqual(self.fm.get_current_path(), str(self.test_dir.resolve()))

    def test_rename(self):
        self.fm.create_file("old.txt")
        res = self.fm.rename_item("old.txt", "new.txt")
        self.assertTrue(res['success'])
        self.assertFalse((self.test_dir / "old.txt").exists())
        self.assertTrue((self.test_dir / "new.txt").exists())

if __name__ == '__main__':
    unittest.main()
