import subprocess
import sys
from pathlib import Path
from .utils import ensure_pyinstaller, get_imported_modules, is_stdlib, get_resource_path

def pack_script(script_path, output_dir, name=None, icon=None, onefile=False, console=True, extra_resources=None, callback=None):
    """
    打包脚本，自动检测依赖并添加 hidden-imports。
    extra_resources: 额外资源文件或文件夹列表（路径字符串），将使用 --add-data 添加。
    """
    def log(msg):
        if callback:
            callback(msg)
        else:
            print(msg)

    script_path = Path(script_path).resolve()
    if not script_path.exists():
        raise FileNotFoundError(f"脚本文件不存在: {script_path}")

    # 1. 自动分析依赖
    log("🔍 正在分析脚本依赖...")
    imported = get_imported_modules(script_path)
    third_party = [mod for mod in imported if not is_stdlib(mod)]
    if third_party:
        log(f"📦 检测到第三方/本地模块: {', '.join(third_party)}")
    else:
        log("✅ 未检测到额外依赖（仅使用标准库）。")

    # 2. 确保 PyInstaller 已安装
    ensure_pyinstaller()
    log("PyInstaller 准备就绪。")

    # 3. 处理默认图标
    if not icon:
        default_icon = get_resource_path("image/icon0.ico")
        if default_icon.exists():
            icon = str(default_icon)
            log(f"🖼️ 使用默认图标: {default_icon}")
        else:
            log("ℹ️ 未指定图标，且默认图标不存在，将不使用图标。")

    # 4. 构建 PyInstaller 命令
    cmd = ["pyinstaller"]
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")

    if icon:
        icon_path = Path(icon).resolve()
        if not icon_path.exists():
            raise FileNotFoundError(f"图标文件不存在: {icon_path}")
        cmd.append(f"--icon={icon_path}")

    if not console:
        cmd.append("--noconsole")

    name = name or script_path.stem
    cmd.append(f"--name={name}")

    # 输出目录（转换为绝对路径）
    out_dir = Path(output_dir).resolve()
    cmd.append("--distpath")
    cmd.append(str(out_dir))

    # 添加脚本所在目录到路径，方便相对导入
    cmd.append("--paths")
    cmd.append(str(script_path.parent))

    # 添加自动检测到的依赖
    for mod in third_party:
        cmd.append(f"--hidden-import={mod}")

    # 添加额外资源
    if extra_resources:
        for res in extra_resources:
            res_path = Path(res).resolve()
            if not res_path.exists():
                log(f"⚠️ 警告: 附加资源不存在: {res_path}")
                continue
            # 格式：源路径;目标路径（在打包后应用程序中的路径）
            # 如果是文件，目标路径为文件名；如果是目录，目标路径为目录名
            if res_path.is_file():
                target = res_path.name
            else:
                target = res_path.name  # 目录名
            # 在 Windows 上使用 ; 分隔，Linux/mac 使用 :
            sep = ';' if sys.platform == 'win32' else ':'
            cmd.append(f"--add-data={str(res_path)}{sep}{target}")

    cmd.append(str(script_path))

    log(f"执行命令: {' '.join(cmd)}")
    log("⏳ 开始打包，请稍候...")

    # 5. 执行打包（设置工作目录为脚本所在目录，避免运行在系统目录）
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=str(script_path.parent)  # 关键修复：切换到脚本目录
    )
    for line in process.stdout:
        log(line.rstrip())
    process.wait()

    if process.returncode != 0:
        raise RuntimeError(f"打包失败，返回码 {process.returncode}")

    log(f"✅ 打包成功！可执行文件位于: {out_dir}")
    if not onefile:
        log(f"   目录模式，主程序为: {out_dir / name / f'{name}.exe'}")
    else:
        log(f"   单文件模式: {out_dir / f'{name}.exe'}")