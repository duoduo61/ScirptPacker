import argparse
import sys
from .core import pack_script

def main():
    parser = argparse.ArgumentParser(description="将 Python 脚本打包为独立可执行文件")
    parser.add_argument("script", help="要打包的 Python 脚本路径")
    parser.add_argument("-o", "--output-dir", default="./dist", help="输出目录 (默认: ./dist)")
    parser.add_argument("-n", "--name", help="可执行文件名称 (默认使用脚本名)")
    parser.add_argument("--icon", help="可执行文件图标 (.ico 文件路径)")
    parser.add_argument("--onefile", action="store_true", help="打包成单个文件 (默认: 目录模式)")
    parser.add_argument("--console", action="store_true", help="显示控制台窗口 (默认: 不显示)")
    parser.add_argument("--add-data", action="append", help="添加附加资源，格式: 源路径;目标路径 (可多次指定)")

    args = parser.parse_args()

    try:
        pack_script(
            script_path=args.script,
            output_dir=args.output_dir,
            name=args.name,
            icon=args.icon,
            onefile=args.onefile,
            console=args.console,
            add_data=args.add_data
        )
    except Exception as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()