import os
import sys
import subprocess
from pathlib import Path
import django
from django.test import TestCase

# Ensure Django settings are set for the tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


class ProjectStructureTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base = Path("C:/Users/hp/OneDrive/Documents/mzanzibari_pos")

    def test_manage_py_check(self):
        p = self.base / "manage.py"
        self.assertTrue(p.exists(), "manage.py not found")
        res = subprocess.run([sys.executable, str(p), 'check'], capture_output=True, text=True, cwd=str(self.base))
        self.assertEqual(res.returncode, 0)

    def test_core_files_exist(self):
        required = [
            "config/settings.py",
            "requirements.txt",
            "templates/base/base.html",
            "static/js/pos.js",
        ]
        for r in required:
            with self.subTest(r=r):
                self.assertTrue((self.base / r).exists(), f"{r} missing")
