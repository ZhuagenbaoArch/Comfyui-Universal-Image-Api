# ComfyUI Universal Image API Generator
一个支持 **OpenAI/Gemini 双格式 API** 的 ComfyUI 通用图片生成/编辑节点，支持多图输入、上下文对话记忆，适配主流AI图像生成API。

---

## ✨ 核心特性
- 双格式兼容：同时支持 OpenAI 与 Gemini 两种主流 API 格式
- 双运行模式：全新图片生成 / 基于底图编辑（OpenAI格式支持多图输入）
- 上下文记忆：开启对话模式后自动拼接历史提示词，实现连续迭代创作
- 多尺寸支持：内置主流分辨率预设 + 自定义宽高设置
- 质量控制：支持 high/standard 两种质量档位
- 原生兼容：输出标准 ComfyUI `IMAGE` 格式，可直接对接预览/保存节点
- 调试友好：提供完整API响应原文输出，方便排查调用问题
- 注意：大部分中转站的初档API根本不支持1K和high质量，所以你选了也没用

---

## 📦 安装方法
### 方法1：Git 克隆（推荐）
打开终端，进入你的 ComfyUI `custom_nodes` 目录，执行以下命令：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ZhuagenbaoArch/Comfyui-Universal-Image-Api.git
cd Comfyui-Universal-Image-Api
pip install -r requirements.txt（其实也没啥requirement，大部分情况下不需要这步，秋叶包和云端镜像基本都有“requests”这个库）


方法 2：手动安装
前往 仓库主页 下载代码压缩包
解压后将文件夹放入 ComfyUI 的 custom_nodes 目录
进入插件文件夹，执行依赖安装：pip install -r requirements.txt（其实也没啥requirement，大部分情况下不需要这步，秋叶包和云端镜像基本都有“requests”这个库）
重启 ComfyUI

🚀 快速上手
启动 ComfyUI，在节点列表中找到 🎨 Universal Image API Generator (GPT & Gemini) 节点
根据你的 API 类型，选择「OpenAI 格式」或「Gemini 格式」
填写 API 地址（一定要填地址全名）、Key、模型名称和提示词
若使用编辑模式，在 images1-images6 端口传入底图（OpenAI 格式支持最多 6 张）
连接输出到预览 / 保存节点，运行工作流即可

⚙️ 参数说明
1. 基础配置参数
完整 API 地址：API 请求地址，OpenAI 示例：https://api.openai.com/v1/images/generations
API 格式：选择 OpenAI 格式 或 Gemini 格式，节点自动适配请求格式
API Key：你的平台 API 密钥，Gemini 格式会自动拼接密钥，无需手动处理
运行模式：生成 = 纯文本生成图片；编辑 = 基于图片修改（仅 OpenAI 支持）
对话模式：关闭 = 仅使用当前提示词；开启 = 自动拼接历史提示词，实现连续对话
2. 生成参数
提示词（可拉伸）：图片生成 / 编辑的指令，支持多行输入
尺寸：内置常用分辨率，可选「自定义」手动设置宽高
自定义尺寸：格式为 宽 x 高（例：1920x1080），仅尺寸选自定义时生效
quality：图片质量，可选 high（高质量）/standard（标准质量）
model：调用的模型名称，如 gpt-image-2
3. 图片输入参数
images1-images6：编辑模式底图输入，最多支持 6 张图片，自动过滤空值

📌 使用示例
1. 基础生成模式（OpenAI/Gemini 通用）
无需输入图片，填写 API 信息和提示词，直接生成图片
适合纯文本生成场景，如创作插画、海报等
2. 图片编辑模式（仅 OpenAI 格式支持）
在 images1 端口传入一张底图，编写编辑提示词（如 “把背景换成海边，调整为赛博朋克风格”）
支持多图拼接，可传入多张参考图进行融合创作
3. 上下文对话模式
开启「对话模式」后，每次运行会自动拼接上一次的提示词
适合迭代修改，例如：第一次提示词 “一只猫”，第二次提示词 “给它戴上帽子”，节点会自动合并指令

❓ 常见问题与排查
API 调用失败 / 返回错误
检查 API 地址、Key 是否正确，无多余空格
确认 API 格式选择与你的服务商一致
查看节点输出的「API 响应原文」，定位具体错误原因
编辑模式无法使用
编辑模式仅支持 OpenAI 格式，Gemini 暂不支持
必须在 images1-images6 中至少传入一张图片
自定义尺寸不生效
需先将「尺寸」参数选择为「自定义」，再填写宽高
格式必须为 宽x高，中间为小写字母 x
请求超时 / 速度过慢
检查网络是否能正常访问 API 地址
可在代码中调整超时时间（默认 600 秒），适配不同服务商的响应速度

📜 许可证
本项目基于 MIT License 开源，欢迎自由使用与二次开发。

🙏 反馈与贡献
如果在使用中遇到问题，或有功能建议，欢迎在 Issues 中提交反馈，不过我也改不好就是了。也欢迎提交 PR 共同完善项目！
