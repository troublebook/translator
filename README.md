# Translation App

一个基于 Kivy 的 Android 翻译应用，支持 24 种语言的互译。

## 功能特性

- **24 种语言支持**：英语、中文（简体/繁体）、日语、韩语、法语、德语、西班牙语、葡萄牙语、意大利语、俄语、阿拉伯语、印地语、越南语、泰语、印尼语、土耳其语、波兰语、荷兰语、乌克兰语、瑞典语、希伯来语、马来语、菲律宾语
- **实时翻译**：一键翻译，异步处理不阻塞界面
- **语言交换**：快速切换源语言和目标语言
- **一键复制**：复制翻译结果到剪贴板
- **RTL 支持**：自动检测阿拉伯语/希伯来语的右对齐显示
- **错误提示**：网络断开、API 限流等友好提示

## 技术栈

- **GUI 框架**：Kivy
- **翻译 API**：MyMemory（免费，无需 API Key）
- **打包工具**：Buildozer

## 安装依赖

```bash
pip install kivy requests certifi
```

## 桌面端测试

```bash
python main.py
```

## 构建 Android APK

### 方式一：GitHub Actions（推荐，无需本地 Linux）

1. 将代码推送到 GitHub 仓库
2. 进入仓库的 **Actions** 标签页
3. 点击 **"I understand my workflows, go ahead and enable them"** 启用
4. 点击 **"Build Android APK"** 工作流，然后点击 **"Run workflow"**
5. 等待构建完成（约 15-30 分钟），在 Actions 页面下载 APK 文件

### 方式二：本地 Linux 构建

```bash
# 在 Linux 或 WSL 中
sudo apt-get install -y build-essential git ffmpeg \
    libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \
    libsdl2-ttf-dev libportmidi-dev libswscale-dev \
    libavformat-dev libavcodec-dev zlib1g-dev \
    libgstreamer1.0 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good openjdk-17-jdk \
    autoconf automake libtool

pip install buildozer cython
buildozer android debug
```

## 项目结构

```
.
├── main.py                  # 应用入口
├── translations/
│   ├── __init__.py
│   ├── languages.py         # 语言代码定义
│   ├── api_client.py        # MyMemory API 客户端
│   └── translator.py        # 异步翻译编排
├── ui/
│   ├── __init__.py
│   ├── main_screen.py       # 主界面控件
│   └── main_screen.kv       # KV 布局文件
├── buildozer.spec           # Android 构建配置
├── requirements.txt         # Python 依赖
└── icon.png                 # 应用图标 (512x512)
```

## 使用说明

1. 选择源语言（默认：英语）
2. 输入要翻译的文本
3. 选择目标语言（默认：中文-简体）
4. 点击"翻译"按钮
5. 查看翻译结果，可点击"复制"保存

## 注意事项

- MyMemory 免费版限制：每天 1000 词
- 最大输入长度：500 字符
- 需要网络连接才能使用翻译功能
