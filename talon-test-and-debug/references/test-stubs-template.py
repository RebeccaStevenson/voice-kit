# Minimal Talon stubs for running pytest outside of Talon.
#
# Place this file at: <user_repo>/tests/stubs/talon/__init__.py
# Then ensure the test runner can import from tests/stubs/, e.g.:
#   PYTHONPATH=tests/stubs python -m pytest tests/ -v
# or add a conftest.py that inserts tests/stubs onto sys.path.

class Module:
    def action_class(self, cls):
        return cls
    def tag(self, name, desc=""):
        pass
    def list(self, name, desc=""):
        pass
    def setting(self, name, **kwargs):
        pass

class Context:
    matches = ""
    lists = {}
    def action_class(self, path):
        def decorator(cls):
            return cls
        return decorator

class actions:
    @staticmethod
    def insert(text): pass
    @staticmethod
    def key(keys): pass
    @staticmethod
    def sleep(duration): pass
    class edit:
        @staticmethod
        def selected_text(): return ""
        @staticmethod
        def copy(): pass
        @staticmethod
        def paste(): pass
    class app:
        @staticmethod
        def notify(title, body=""): pass

class app:
    platform = "mac"
    notifications = []
    @staticmethod
    def notify(title, body=""):
        app.notifications.append((title, body))

class clip:
    _text = ""
    @staticmethod
    def text(): return clip._text
    @staticmethod
    def set_text(t): clip._text = t
