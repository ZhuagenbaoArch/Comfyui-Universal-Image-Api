# ComfyUI Universal Image API Generator

A ComfyUI node for image generation & editing via OpenAI/Gemini APIs, with multi-image input, context memory, and native ComfyUI support.
一款支持 OpenAI/Gemini 双格式 API 的 ComfyUI 通用图片生成 / 编辑节点，支持多图输入、上下文记忆，原生适配 ComfyUI 图像格式。

---

## ✨ 核心特性 / Key Features
- 双格式兼容：同时支持 OpenAI 与 Gemini 两种主流 API 格式
- Dual format compatibility: Supports both OpenAI and Gemini mainstream API standards

- 双运行模式：全新图片生成 / 基于底图编辑（OpenAI 格式支持多图输入）
- Dual operation modes: Text-to-image generation / image-based editing (multi-image input supported for OpenAI format)

- 上下文记忆：开启对话模式后自动拼接历史提示词，实现连续迭代创作
- Chat context memory: Automatically appends previous prompts when chat mode is enabled for iterative creation

- 多尺寸支持：内置主流分辨率预设 + 自定义宽高设置
- Multi-resolution support: Built-in presets for common resolutions + custom width/height configuration

- 质量控制：支持 high/standard 两种质量档位
- Quality control: Supports both high and standard quality tiers

- 原生兼容：输出标准 ComfyUI IMAGE 格式，可直接对接预览 / 保存节点
- Native ComfyUI compatibility: Outputs standard IMAGE format for direct use with preview/save nodes

- 调试友好：提供完整 API 响应原文输出，方便排查调用问题
- Debug-friendly: Full raw API response output for troubleshooting

- 注意：大部分中转站的初档 API 根本不支持 1K 和 high 质量，所以你选了也没用
- Note: Most third-party API relays do not support 1K resolution or high quality tiers in basic plans, so selecting these options will have no effect.

---

## 📦 安装方法 / Installation
### 方法1：Git 克隆（推荐）/ Method 1: Git Clone (Recommended)
- 打开终端，进入你的 ComfyUI `custom_nodes` 目录，执行以下命令：
- Open your terminal, navigate to your ComfyUI custom_nodes directory, and run:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ZhuagenbaoArch/Comfyui-Universal-Image-Api.git
cd Comfyui-Universal-Image-Api
pip install -r requirements.txt（其实也没啥requirement，大部分情况下不需要这步，秋叶包和云端镜像基本都有“requests”这个库）
```

---

## 方法 2：手动安装
- 前往 仓库主页 下载代码压缩包
- Go to the repository page and download the source code as a ZIP file
- 解压后将文件夹放入 ComfyUI 的 custom_nodes 目录
- Extract the ZIP and place the folder in your ComfyUI custom_nodes directory
- 进入插件文件夹，执行依赖安装（其实也没啥requirement，大部分情况下不需要这步，秋叶包和云端镜像基本都有“requests”这个库）：
- Navigate to the plugin folder and run (You probably don't need this step - most distributions like Qiuye Pack and cloud images already include the `requests` library)
```bash
pip install -r requirements.txt
```
- 重启 ComfyUI
- Restart ComfyUI

---

## 🚀 快速上手 / Quick Start
- 启动 ComfyUI，在节点列表中找到 🎨 Universal Image API Generator (GPT & Gemini) 节点
- Launch ComfyUI and find the 🎨 Universal Image API Generator (GPT & Gemini) node in the node list
- 根据你的 API 类型，选择「OpenAI 格式」或「Gemini 格式」
- Select either OpenAI format or Gemini format based on your API provider
- 填写 API 地址（一定要填地址全名）、Key、模型名称和提示词
- Enter your full API endpoint, API key, model name, and prompt
- 若使用编辑模式，在 images1-images6 端口传入底图（OpenAI 格式支持最多 6 张）
- For editing mode, connect base images to the images1-images6 inputs (max 6 images supported for OpenAI format)
- 连接输出到预览 / 保存节点，运行工作流即可
- Connect the output to preview/save nodes and run your workflow


---

## ⚙️ 参数说明 / Parameter Guide
### 1. 基础配置参数 / Basic Configuration
- 完整 API 地址：API 请求地址，OpenAI 示例：https://api.openai.com/v1/images/generations
- Full API endpoint: The request URL (OpenAI example: https://api.openai.com/v1/images/generations)
- API 格式：选择 OpenAI 格式 或 Gemini 格式，节点自动适配请求格式
- API format: Select OpenAI format or Gemini format - the node automatically adapts request formatting
- API Key：你的平台 API 密钥，Gemini 格式会自动拼接密钥，无需手动处理
- API Key: Your platform API key (automatically appended to the URL for Gemini format, no manual handling needed)
- 运行模式：生成 = 纯文本生成图片；编辑 = 基于图片修改（仅 OpenAI 支持）
- Operation mode: Generate = text-to-image creation; Edit = image-based modification (OpenAI format only)
- 对话模式：关闭 = 仅使用当前提示词；开启 = 自动拼接历史提示词，实现连续对话
- Chat mode: Off = use only current prompt; On = automatically append previous prompts for continuous dialogue
### 2. 生成参数 / Generation Parameters
- 提示词（可拉伸）：图片生成 / 编辑的指令，支持多行输入
- Prompt (resizable): Instructions for image generation/editing, supports multi-line input
- 尺寸：内置常用分辨率，可选「自定义」手动设置宽高
- Size: Built-in common resolutions, or select Custom to set width/height manually
- 自定义尺寸：格式为 宽 x 高（例：1920x1080），仅尺寸选自定义时生效
- Custom size: Format width x height (e.g., 1920x1080), only active when Size is set to Custom
- quality：图片质量，可选 high（高质量）/standard（标准质量）
- Quality: Image quality tier, options: high / standard
- model：调用的模型名称，如 gpt-image-2
- Model: Name of the model to call (e.g., gpt-image-2)
### 3. 图片输入参数 / Image Input Parameters
- images1-images6：编辑模式底图输入，最多支持 6 张图片，自动过滤空值
- images1-images6: Base image inputs for editing mode, supports up to 6 images (empty inputs are automatically filtered out)

---

## 📌 使用示例 / Usage Examples
### 1. 基础生成模式（OpenAI/Gemini 通用）/ 1. Basic Generation (OpenAI/Gemini)
- 无需输入图片，填写 API 信息和提示词，直接生成图片
- No image input required - fill in API details and prompt to generate images directly
- 适合纯文本生成场景，如创作插画、海报等
- Ideal for text-only use cases like creating illustrations or posters
### 2. 图片编辑模式（仅 OpenAI 格式支持）/ 2. Image Editing (OpenAI Only)
- 在 images1 端口传入一张底图，编写编辑提示词（如 “把背景换成海边，调整为赛博朋克风格”）
- Connect a base image to images1 and write an editing prompt (e.g., "Change the background to a beach and apply a cyberpunk style")
- 支持多图拼接，可传入多张参考图进行融合创作
- Supports multi-image blending - connect multiple reference images for fusion creation
### 3. 上下文对话模式 / 3. Chat Context Mode
- 开启「对话模式」后，每次运行会自动拼接上一次的提示词
- With Chat mode enabled, the node automatically appends previous prompts on each run
- 适合迭代修改，例如：第一次提示词 “一只猫”，第二次提示词 “给它戴上帽子”，节点会自动合并指令
- Perfect for iterative edits: e.g., first prompt "A cat", second prompt "Add a hat to it" - the node combines the instructions automatically

---

## ❓ 常见问题与排查 / FAQ & Troubleshooting
### API 调用失败 / 返回错误 / API Call Failed / Errors
- 检查 API 地址、Key 是否正确，无多余空格
- Verify the API endpoint and key are correct, with no extra spaces
- 确认 API 格式选择与你的服务商一致
- Ensure the selected API format matches your provider's standard
- 查看节点输出的「API 响应原文」，定位具体错误原因
- Check the API Response output for specific error details
### 编辑模式无法使用 / Editing Mode Not Working
- 编辑模式仅支持 OpenAI 格式，Gemini 暂不支持
- Editing mode is only supported for OpenAI format (Gemini not supported)
- 必须在 images1-images6 中至少传入一张图片
- At least one image must be connected to images1-images6
### 自定义尺寸不生效 / Custom Size Not Working
- 大部分中转服务商的初档价位 API 仅支持 1K 分辨率与普通质量，请仔细核对服务商关于 API 分辨率与出图质量的说明
- Most entry-tier plans from API relay providers only support 1K resolution and standard quality. Please check your provider’s documentation for supported resolutions and output quality.
- 需先将「尺寸」参数选择为「自定义」，再填写宽高
- First set Size to Custom, then enter your width/height
- 格式必须为 宽x高，中间为小写字母 x
- Must use widthxheight format with a lowercase x (no spaces)
### 请求超时 / 速度过慢 / Timeouts / Slow Responses
- 检查网络是否能正常访问 API 地址
- Verify your network can access the API endpoint
- 可在代码中调整超时时间（默认 600 秒），适配不同服务商的响应速度
- Adjust the timeout in the code (default: 600 seconds) to match your provider's response speed

---

## 📜 许可证 / License
- 本项目基于 MIT License 开源，欢迎自由使用与二次开发。
- This project is open-source under the MIT License. Feel free to use and modify it for any purpose.

---

## 🙏 反馈与贡献 / Feedback & Contributions
- 如果在使用中遇到问题，或有功能建议，欢迎在 Issues 中提交反馈，不过我也改不好就是了。也欢迎提交 PR 共同完善项目！
- If you encounter issues or have feature suggestions, feel free to submit feedback in Issues—though I might not be able to fix them well. PRs are also welcome to jointly improve the project!
