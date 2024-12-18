import os
import sys


# 设置 DaVinci Resolve 的 API 路径和库路径
resolve_script_api = (
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
)
resolve_script_lib = (
    r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
)
python_path = os.path.join(resolve_script_api, "Modules")

# 动态设置环境变量
os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api
os.environ["RESOLVE_SCRIPT_LIB"] = resolve_script_lib
os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')};{python_path}"

# 添加库路径到系统路径（如果需要导入模块）
if python_path not in sys.path:
    sys.path.append(python_path)

# 检查是否成功加载环境变量
print("RESOLVE_SCRIPT_API:", os.environ["RESOLVE_SCRIPT_API"])
print("RESOLVE_SCRIPT_LIB:", os.environ["RESOLVE_SCRIPT_LIB"])
print("PYTHONPATH:", os.environ["PYTHONPATH"])
RESOLVE = __import__("DaVinciResolveScript").scriptapp("Resolve")
