import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import base64
import json

class UniversalImageAPIGenerator:
    context_memory = {
        "last_prompt": "",
        "has_history": False
    }

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "full_api_url": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "label": "完整API地址"
                }),
                "api_format": (["OpenAI 格式", "Gemini 格式"], {
                    "default": "OpenAI 格式",
                    "label": "API格式"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "label": "API Key"
                }),
                "mode": (["生成", "编辑"], {
                    "default": "生成",
                    "label": "运行模式"
                }),
                "chat_mode": (["关闭", "开启(上下文记忆)"], {
                    "default": "关闭",
                    "label": "对话模式"
                }),
                # 提示词支持拉伸变大
                "prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "default_height": 120,
                    "label": "提示词（可拉伸）"
                }),
                # 全尺寸：横版+竖版
                "size": (
                    [
                        "1280x720", "720x1280",
                        "1920x1080", "1080x1920",
                        "2560x1440", "1440x2560",
                        "3840x2160", "2160x3840",
                        "自定义"
                    ],
                    {"default": "3840x2160"}
                ),
                # 选自定义才显示
                "custom_size": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "label": "自定义尺寸（宽x高）",
                    "condition": {"size": ["自定义"]}
                }),
                "quality": (["high", "standard"], {"default": "high"}),
                "model": ("STRING", {"default": "gpt-image-2"}),
            },
            "optional": {
                "images1": ("IMAGE",),
                "images2": ("IMAGE",),
                "images3": ("IMAGE",),
                "images4": ("IMAGE",),
                "images5": ("IMAGE",),
                "images6": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("生成图片", "API响应原文")
    FUNCTION = "generate"
    CATEGORY = "🎨 GPT&GIMINI API图片生成"

    def generate(self, full_api_url, api_format, api_key, mode, chat_mode, prompt, size, custom_size, quality, model, 
                 images1=None, images2=None, images3=None, images4=None, images5=None, images6=None):
        if not full_api_url.strip():
            raise Exception("请填写完整API地址！")
        if not api_key.strip():
            raise Exception("请填写API Key！")

        # 自定义尺寸处理
        final_size = size
        if size == "自定义":
            if not custom_size.strip() or "x" not in custom_size:
                raise Exception("自定义尺寸格式错误：宽x高，如 1024x512")
            final_size = custom_size.strip()

        # 上下文拼接
        final_prompt = prompt
        if chat_mode == "开启(上下文记忆)" and self.context_memory["has_history"]:
            final_prompt = f"{self.context_memory['last_prompt']} {prompt}".strip()

        # 收集所有传入的图片（6个端口自动过滤空值）
        input_images = []
        for img in [images1, images2, images3, images4, images5, images6]:
            if img is not None:
                input_images.append(img)

        # OpenAI 格式
        if api_format == "OpenAI 格式":
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key.strip()}"
            }
            payload = {
                "prompt": final_prompt,
                "size": final_size,
                "quality": quality,
                "model": model,
                "n": 1
            }
            
            # 编辑模式：上传所有非空图片
            if mode == "编辑":
                if len(input_images) == 0:
                    raise Exception("编辑模式需要至少一张图片作为底图！")
                
                base64_images = []
                for img_tensor in input_images:
                    img = img_tensor.squeeze(0).cpu().numpy()
                    img = (img * 255).astype(np.uint8)
                    pil_img = Image.fromarray(img).convert("RGB")
                    buffer = BytesIO()
                    pil_img.save(buffer, format="PNG")
                    base64_images.append(base64.b64encode(buffer.getvalue()).decode("utf-8"))
                
                # 适配GPT-IMAGE-2：单图/多图自动切换
                if len(base64_images) == 1:
                    payload["image"] = base64_images[0]
                else:
                    payload["images"] = base64_images

        # Gemini 格式
        else:
            full_api_url = full_api_url.strip() + f"?key={api_key.strip()}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": final_prompt}]}]
            }
            # Gemini 通常不支持多图输入，这里只处理提示词

        try:
            response = requests.post(full_api_url.strip(), headers=headers, json=payload, timeout=600)
            response.raise_for_status()
            result = response.json()
            response_text = json.dumps(result, ensure_ascii=False, indent=2)

            # 解析图片
            if api_format == "OpenAI 格式":
                if "data" in result and len(result["data"]) > 0:
                    image_url = result["data"][0]["url"]
                else:
                    raise Exception("OpenAI API 返回格式异常")
            else: # Gemini
                if "candidates" in result and len(result["candidates"]) > 0:
                    image_data = result["candidates"][0]["content"]["parts"][0]["inline_data"]
                    if image_data["mime_type"].startswith("image"):
                        image_url = f"data:{image_data['mime_type']};base64,{image_data['data']}"
                    else:
                        raise Exception("Gemini API 返回的不是有效图片数据")
                else:
                    raise Exception("Gemini API 返回格式异常")

            # 转 ComfyUI 图像
            if image_url.startswith('http'):
                # HTTP URL
                img_res = requests.get(image_url, timeout=120)
                img_res.raise_for_status()
                pil_img = Image.open(BytesIO(img_res.content)).convert("RGB")
            elif image_url.startswith('data:image'):
                # Data URI (Base64)
                header, encoded = image_url.split(",", 1)
                mime_type = header.split(";")[0].split(":")[1]
                image_format = mime_type.split("/")[1]
                img_bytes = base64.b64decode(encoded)
                pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")
            else:
                raise Exception("无法识别的图片URL格式")

            img_np = np.array(pil_img).astype(np.float32) / 255.0
            output_tensor = torch.from_numpy(img_np)[None,]

            # 上下文记忆
            if chat_mode == "开启(上下文记忆)":
                self.context_memory["last_prompt"] = final_prompt
                self.context_memory["has_history"] = True

            return (output_tensor, response_text)

        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败：{str(e)}")
        except Exception as e:
            raise Exception(f"API请求失败：{str(e)}")

NODE_CLASS_MAPPINGS = {
    "UniversalImageAPIGenerator": UniversalImageAPIGenerator
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "UniversalImageAPIGenerator": "🎨 Universal Image API Generator (GPT & Gemini)"
}