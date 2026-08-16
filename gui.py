import sys
from pathlib import Path

# 将项目根目录添加到 sys.path，确保可以导入 packer 包
sys.path.insert(0, str(Path(__file__).parent))

from packer.gui import main

if __name__ == "__main__":
    main()
