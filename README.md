# 行人跌倒检测系统（YOLOv5 + PyQt5）

基于 **YOLOv5s** 训练的行人跌倒检测模型，配合 **PyQt5** 图形界面实现图片 / 视频 / 摄像头实时检测，并已使用 PyInstaller 打包为免安装的 Windows 可执行程序。

> **许可：GPL-3.0** · 本项目基于 [Ultralytics YOLOv5 v6.0](https://github.com/ultralytics/yolov5) 二次开发，
> 第三方组件与版权归属详见 [NOTICE.md](NOTICE.md)。

- 类别：`fall down`（跌倒）、`stand person`（站立的人），共 2 类
- 检测精度（验证集 152 张）：**mAP@0.5 = 0.793**，Precision = 0.771，Recall = 0.786
- 训练环境：150 epochs，batch size 16，imgsz 640，基座模型 `yolov5s.pt`

---

## 一、功能特性

| 功能 | 说明 |
| --- | --- |
| 图片检测 | 选择单张图片，输出带标注框与类别置信度的结果 |
| 视频检测 | 选择本地视频文件，逐帧检测并实时显示 |
| 摄像头检测 | 打开摄像头（默认设备 0）进行实时跌倒检测 |
| 结果标注 | 显示检测框、类别名称与置信度，界面同步显示检测列表 |

---

## 二、快速开始

### 方式 1：直接运行打包好的 exe（无需安装 Python）

1. 前往本仓库的 **[Releases](../../releases)** 页面
2. 下载 `main.exe`
3. 双击运行即可（首次启动需等待模型加载，约 10~30 秒）

> 由于体积限制（236 MB），exe 不放在仓库源码中，而是作为 Release 附件发布。
> exe 内打包了 GPL-3.0 的 YOLOv5 与 PyQt5 代码，其对应源码即本仓库，见 [NOTICE.md](NOTICE.md)。

### 方式 2：从源码运行

```bash
# 1. 创建并激活虚拟环境
python -m venv venv
venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动图形界面
python main.py
```

---

## 三、项目结构

```
yolov5-6.0/
├── main.py                     # PyQt5 图形界面主程序（入口）
├── untitled.py / untitled.ui   # Qt Designer 生成的界面代码 / 界面文件
├── detect.py                   # 检测核心：图片 / 视频 / 单帧推理
├── main.spec                   # PyInstaller 打包配置
├── train.py / val.py / export.py  # YOLOv5 训练 / 验证 / 导出脚本
├── models/                     # YOLOv5 网络结构定义
├── utils/                      # YOLOv5 工具函数（NMS、数据加载、绘图等）
├── data/                       # YOLOv5 数据配置与超参数
├── requirements.txt            # Python 依赖清单
├── LICENSE                     # GPL-3.0 许可全文
├── NOTICE.md                   # 第三方组件与许可声明
├── weights/
│   └── yolov5s.pt              # 官方预训练权重（训练起点）
├── mydata/
│   └── fall_down_yolo/
│       └── data.yaml           # 数据集配置（类别与路径）
└── runs/
    └── train/
        └── exp4/               # 最终一次训练结果
            ├── weights/best.pt # 训练好的模型（13.8 MB）
            ├── results.png     # 损失 / 精度曲线
            ├── PR_curve.png    # PR 曲线
            ├── confusion_matrix.png
            └── opt.yaml        # 本次训练完整参数
```

---

## 四、数据集

本仓库不包含训练图片与标注文件，仅保留 `mydata/fall_down_yolo/data.yaml` 说明数据格式。

数据规模（训练时使用）：

| 划分 | 图片数量 | 格式 |
| --- | --- | --- |
| 训练集 | 7630 | YOLO 格式（`images/*.jpg` + `labels/*.txt`） |
| 验证集 | 152 | 同上 |

两类：`fall down`（跌倒）、`stand person`（站立的人）。

### 数据目录结构

按下面的结构放置数据，并改写 `mydata/fall_down_yolo/data.yaml` 里的路径：

```
mydata/fall_down_yolo/
├── data.yaml
├── images/
│   ├── train/     # 训练图片
│   └── val/       # 验证图片
└── labels/
    ├── train/     # 与图片同名的 .txt 标注
    └── val/
```

`data.yaml` 内容：

```yaml
train: mydata/fall_down_yolo/images/train
val: mydata/fall_down_yolo/images/val
nc: 2
names: ['fall down', 'stand person']
```

---

## 五、模型训练

```bash
python train.py --weights weights/yolov5s.pt --cfg models/yolov5s.yaml --data mydata/fall_down_yolo/data.yaml --epochs 150 --batch-size 16 --img 640 --device 0
```

训练结果自动保存在 `runs/train/exp*/`，其中 `weights/best.pt` 为最优模型。本仓库已包含最终一次训练的结果：`runs/train/exp4/`。

训练完成后验证：

```bash
python val.py --weights runs/train/exp4/weights/best.pt --data mydata/fall_down_yolo/data.yaml --img 640
```

---

## 六、打包为 exe

```bash
pyinstaller main.spec
```

打包产物位于 `dist/main.exe`。`main.spec` 中通过 `datas` 指定了需要一起打包的模型权重：

```python
datas=[('runs/train/exp4/weights/best.pt', 'runs/train/exp4/weights'), ('utils/*', 'utils')]
```

---

## 七、致谢

- 检测框架：[**Ultralytics YOLOv5 v6.0**](https://github.com/ultralytics/yolov5)，© Ultralytics，GPL-3.0
- `models/tf.py`：[@zldrobit](https://github.com/zldrobit) 贡献（[PR #1127](https://github.com/ultralytics/yolov5/pull/1127)）
- 示例图片 `data/images/bus.jpg`、`data/images/zidane.jpg`：来自 **COCO 数据集**（© COCO Consortium，CC BY 4.0）
- 本仓库在其基础上完成了模型训练、PyQt5 界面开发与 exe 打包

完整的第三方组件与许可清单见 [NOTICE.md](NOTICE.md)。

---

## 八、版权与许可

### 本项目的许可

本仓库**整体以 [GNU General Public License v3.0](LICENSE) (GPL-3.0) 发布**。

这是因为本项目使用了 GPL-3.0 的 YOLOv5 代码，并链接了 GPL-3.0 的 PyQt5，
依照 GPL 的传染性（copyleft）要求，衍生作品必须同样以 GPL-3.0 分发。

### 各类内容的版权归属

| 内容 | 版权 / 许可 |
| --- | --- |
| `models/`、`utils/`、`data/`、`train.py`、`val.py`、`export.py`、`hubconf.py` | © Ultralytics 及贡献者，GPL-3.0（文件头已保留原始声明） |
| `detect.py` | 衍生自 YOLOv5，© Ultralytics + © SiyuChen12138，GPL-3.0 |
| `main.py`、`untitled.py`、`untitled.ui`、`main.spec` | © SiyuChen12138，GPL-3.0 |
| `weights/yolov5s.pt`、`runs/train/exp4/weights/best.pt` | 基于 GPL-3.0 的 YOLOv5 权重训练/微调，GPL-3.0 |
| `mydata/` | 仅保留 `data.yaml`（数据集配置文件），不含数据本体 |

### 你可以 / 不可以做什么

**可以**：自由使用、修改、再分发本项目，甚至商用 —— 但必须满足以下条件。

**必须**：

1. 保留所有源文件中原有的**版权声明**与**许可声明**；
2. 你的衍生作品也**必须以 GPL-3.0 发布**，并公开完整源代码；
3. 分发 `dist/main.exe` 时，必须提供或承诺提供**对应的完整源代码**
   （本仓库已公开源码，满足此要求，请在 Release 说明中附上仓库地址）；
4. 修改过的文件需注明「已修改」。

**不可以**：

- 把本项目（或基于它的修改版）改为闭源许可再分发；
- 移除或替换原有的版权头、许可文件；
- 附加 GPL 之外的额外限制。

> 如需**闭源商用**，须分别向 [Ultralytics](https://ultralytics.com/) 和
> [Riverbank Computing](https://riverbankcomputing.com/) 购买商业许可。
