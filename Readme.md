# 定制你的宠物桌面

一个用Python和PyQt6开发的可爱桌面宠物应用，支持动画交互、故事生成和休息提醒等功能。

## 项目简介

本项目是一个开源的桌面宠物应用，旨在为用户提供一个有趣、互动性强的桌面伴侣。通过简单的配置和定制，用户可以拥有一个独一无二的桌面宠物。

## 核心功能

1. **随机动画与文本**：每隔一段时间自动切换动图素材和显示文字
2. **点击交互**：点击宠物时有额外的动作反馈和对话
3. **故事大会**：与宠物聊天，使用本地故事生成器进行文本生成互动

## 技术栈

- **编程语言**：Python 3.8+
- **GUI框架**：PyQt6
- **资源管理**：支持PyInstaller打包
- **故事生成**：本地随机故事生成器（无需网络连接）

## 安装步骤

### 1. 克隆项目

```bash
git clone desktop-pet.git
cd desktop-pet
```

### 2. 安装依赖

```bash
pip install PyQt6
```

### 3. 运行项目

```bash
python src/main.py
```

## 使用示例

### 基本操作

1. **鼠标拖动**：按住鼠标左键拖动宠物到任意位置
2. **点击互动**：点击宠物会触发特殊动画和对话
3. **右键菜单**：右键点击宠物打开菜单，可选择隐藏、打开故事大会、设置休息提醒等功能

### 故事大会

1. 在右键菜单中选择"故事大会"
2. 在弹出的窗口中输入故事主题或关键词
3. 点击"生成故事"按钮，等待故事生成
4. 查看生成的故事内容



## 项目结构

```
desktop-pet/
├── package/              # 打包相关文件
│   ├── package.ps1       # PowerShell打包脚本
│   └── 打包说明.md        # 打包说明文档
├── src/                  # 源代码目录
│   ├── dialog/            # 对话文件目录
│   │   └── dialog.txt     # 对话文本文件
│   ├── images/            # 图片资源目录
│   │   ├── click/         # 点击动作图片
│   │   ├── idle_animation/ # 空闲动画图片
│   │   ├── favicon.ico    # 图标文件
│   │   └── talk_background.jpg # 聊天背景
│   ├── main.py            # 主程序入口
│   └── talk_show.py       # 故事大会功能
├── .gitignore            # Git忽略文件
├── LICENSE               # 许可证文件
└── Readme.md             # 项目说明文档
```

## 主要文件说明

- **main.py**：整体功能函数，负责宠物的主要逻辑和交互
- **talk_show.py**：故事大会功能的具体实现，包含本地故事生成器
- **dialog.txt**：存放随机展示的文本内容
- **images/**：存放宠物的各种动画和图片资源

## API文档

### 核心类

#### DesktopPet

主桌面宠物类，负责实现宠物的主要功能和交互逻辑。

**主要方法**：
- `init()`：初始化窗口属性
- `initPall()`：初始化系统托盘
- `initPetImage()`：加载宠物图片和UI组件
- `petNormalAction()`：设置宠物正常待机状态
- `randomAct()`：随机切换宠物动作
- `talk()`：显示宠物对话
- `mousePressEvent(event)`：处理鼠标点击事件
- `mouseMoveEvent(event)`：处理鼠标移动事件
- `contextMenuEvent(event)`：处理右键菜单事件

#### LocalStoryGenerator

本地故事生成器，用于生成随机故事。

**主要方法**：
- `generate_story(user_input="")`：生成随机故事，可接受用户输入的主题或关键词

### Client

故事大会客户端界面，用于显示和生成故事。

**主要方法**：
- `add_ui()`：初始化界面组件
- `generate_story()`：生成并显示故事

## 配置与定制

### 1. 自定义对话内容

编辑 `src/dialog/dialog.txt` 文件，添加或修改对话内容，每行一条。

### 2. 更换宠物图片

替换 `src/images/` 目录下的对应图片文件：
- `idle_animation/`：存放空闲状态的动画图片
- `click/`：存放点击时的动画图片

## 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件

**享受您的专属桌面宠物！** 🎉

