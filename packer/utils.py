import ast
import importlib.util
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """获取资源文件的绝对路径，兼容开发环境和 PyInstaller 打包后的路径"""
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent
    return base_path / relative_path

def get_imported_modules(script_path):
    """解析 Python 脚本，返回所有导入的顶级模块名集合"""
    with open(script_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.add(node.module.split('.')[0])
    return modules

def is_stdlib(module_name):
    """判断模块名是否为 Python 标准库或内置模块"""
    if module_name in sys.builtin_module_names:
        return True
    if hasattr(sys, 'stdlib_module_names'):
        if module_name in sys.stdlib_module_names:
            return True
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            return False
        if spec.origin is None:
            return False
        origin = spec.origin
        if 'site-packages' in origin or 'dist-packages' in origin:
            return False
        if origin.startswith('<frozen>'):
            return True
        return False
    except (ImportError, AttributeError):
        return False

def ensure_pyinstaller():
    """确保 PyInstaller 已安装"""
    if importlib.util.find_spec("PyInstaller") is None:
        print("未找到 PyInstaller，正在自动安装...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    else:
        print("PyInstaller 已就绪。")