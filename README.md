# ScriptPacker

**ScriptPacker** 是一个简单易用的 Python 脚本打包工具，提供命令行和图形界面两种操作方式。它能自动分析脚本的导入依赖，并调用 PyInstaller 生成独立的可执行文件（如 `.exe`）。

## 特性

- **一键打包**：选择脚本即可打包，无需记忆复杂命令。
- **自动依赖检测**：解析脚本中的 `import`，自动添加 `--hidden-import`，避免运行时缺少模块。
- **附加资源支持**：可以额外添加文件或文件夹（如图片、配置文件）到可执行包中，路径自动处理。
- **图形界面 + 命令行**：满足不同用户习惯。
- **进度条反馈**：打包时显示进度动画。
- **启动背景**：主窗口启动时显示自定义背景图（`image/start.png`）和加载提示。
- **默认图标**：若未指定图标，自动使用 `image/icon0.ico`。
- **灵活配置**：单文件/目录模式、控制台显示等。

## 安装

```bash
# 克隆或下载项目
git clone https://github.com/yourname/ScriptPacker.git
cd ScriptPacker

# 安装（推荐虚拟环境）
pip install -e .
```

### 图形界面（GUI）

```
python gui.py
```



或安装后运行 `pack-gui`。

在 GUI 中：

- **脚本**：选择要打包的 `.py` 文件。
- **输出**：选择输出目录（默认 `./dist`）。
- **名称**：自定义生成的可执行文件名（可选）。
- **图标**：选择 `.ico` 图标文件（可选，未选则使用默认图标）。
- **附加资源**：可以添加额外的文件或文件夹，多个路径用分号 `;` 分隔。例如 `C:\data\config.ini;.` 或 `C:\images;images`。
- **选项**：勾选“单文件”或“显示控制台”。

### 命令行（CLI）

bash

```
pack-script your_script.py -o ./dist -n myapp --onefile --console --add-data "C:\data\config.ini;." --add-data "C:\images;images"
```



参数说明：

- `script`：要打包的 Python 脚本路径（必填）
- `-o, --output-dir`：输出目录（默认 `./dist`）
- `-n, --name`：可执行文件名称
- `--icon`：图标文件路径
- `--onefile`：打包成单个文件
- `--console`：显示控制台窗口
- `--add-data`：附加资源，格式 `源路径;目标路径`（可多次指定）

## 附加资源说明

附加资源用于将额外文件或文件夹打包进可执行程序。目标路径是相对于可执行文件运行时的当前目录。例如，`--add-data "config.ini;."` 会将 `config.ini` 放在与可执行文件相同的目录。

在 GUI 中，您可以通过“浏览文件...”和“浏览文件夹...”按钮添加，路径会自动以分号连接。

## 贡献

欢迎提交 Issue。

## 许可

MIT

