"""
检测核心模块

在 Ultralytics YOLOv5 v6.0 的推理流程基础上改写，封装为
 detect_image() / detect_video() / detect_single_frame() 三个接口，
并新增 detect_single_frame 兼容 PyInstaller 打包环境的模型路径解析。

Original : YOLOv5 🚀 by Ultralytics — GPL-3.0 — https://github.com/ultralytics/yolov5
Modified : Copyright (C) 2026 SiyuChen12138

本文件以 GNU General Public License v3.0 发布，完整许可文本见 LICENSE。
本文件包含来自 Ultralytics YOLOv5 的衍生代码，请勿移除上述原始版权声明。
"""

import numpy as np
import cv2
import torch
import logging
from pathlib import Path
from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.torch_utils import select_device
from utils.plots import Annotator, colors
import sys
import os
from pathlib import Path


def get_model_path():
    """动态获取模型路径（兼容开发和打包环境）"""
    # 开发环境路径
    dev_model_path = Path("runs/train/exp4/weights/best.pt")
    if dev_model_path.exists():
        return str(dev_model_path)

    # 打包后环境路径（PyInstaller 临时目录）
    try:
        import sys
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
            return str(base_path / "runs/train/exp4/weights/best.pt")
    except Exception:
        pass

    raise FileNotFoundError("无法找到模型文件 best.pt")


# 加载模型时使用
weights = get_model_path()
model = attempt_load(weights, map_location='cpu')
def detect_single_frame(img, im0s):
    """处理单帧图像（兼容摄像头输入）"""
    try:
        img_tensor = torch.from_numpy(img).to(device).float() / 255.0
        if img_tensor.ndimension() == 3:
            img_tensor = img_tensor.unsqueeze(0)

        pred = model(img_tensor)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)

        label_list = []
        annotator = Annotator(im0s, line_width=3, example=str(names))
        for det in pred:
            if len(det):
                det[:, :4] = scale_coords(img_tensor.shape[2:], det[:, :4], im0s.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors[int(cls)])
                    label_list.append(label)
        return annotator.result(), label_list
    except Exception as e:
        logging.error(f"检测失败：{e}")
        return None, []


# 关键路径设置
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # 项目根目录
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
# 其他代码...

logging.basicConfig(level=logging.INFO)

# 全局初始化模型
device = select_device('cpu')
weights = Path(__file__).parent / 'runs/train/exp4/weights/best.pt'
assert weights.exists(), f"模型文件 {weights} 不存在！"
model = attempt_load(weights, map_location=device)
stride = int(model.stride.max())
imgsz = check_img_size(640, s=stride)
names = model.module.names if hasattr(model, 'module') else model.names
colors = [[np.random.randint(0, 255) for _ in range(3)] for _ in names]


def preprocess_image(image):
    img = letterbox(image, imgsz, stride=stride)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
    return np.ascontiguousarray(img)


def detect_single_frame(img, im0s):
    try:
        img_tensor = torch.from_numpy(img).to(device).float() / 255.0
        if img_tensor.ndimension() == 3:
            img_tensor = img_tensor.unsqueeze(0)

        pred = model(img_tensor)[0]
        pred = non_max_suppression(pred, 0.25, 0.45)

        label_list = []
        for det in pred:
            if len(det):
                det[:, :4] = scale_coords(img_tensor.shape[2:], det[:, :4], im0s.shape).round()
                annotator = Annotator(im0s, line_width=3, example=str(names))
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    annotator.box_label(xyxy, label, color=colors[int(cls)])
                    label_list.append(label)
        return im0s, label_list
    except Exception as e:
        logging.error(f"检测失败：{e}")
        return None, []


def detect_image(filepath):
    try:
        img0 = cv2.imread(filepath)
        if img0 is None:
            logging.error(f"无法读取图片：{filepath}")
            return None, []
        img = preprocess_image(img0)
        return detect_single_frame(img, img0.copy())
    except Exception as e:
        logging.error(f"图片检测异常：{e}")
        return None, []


def detect_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            img = preprocess_image(frame)
            result, labels = detect_single_frame(img, frame.copy())
            if result is not None:
                yield result, labels
        cap.release()
    except Exception as e:
        logging.error(f"视频检测异常：{e}")
