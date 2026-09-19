# 第三方组件与许可声明（Third-Party Notices）

本项目（**行人跌倒检测系统**）是在开源项目 **Ultralytics YOLOv5 v6.0** 基础上二次开发而成。
由于上游使用 GPL-3.0 许可，**本项目整体同样以 GNU General Public License v3.0 (GPL-3.0) 发布**，
完整许可文本见仓库根目录的 [LICENSE](LICENSE)。

> 如果你只想要原始的 YOLOv5 代码，请前往官方仓库：<https://github.com/ultralytics/yolov5>

---

## 一、本项目对上游代码的使用方式

### 1. 直接沿用上游的文件（版权归 Ultralytics 及其贡献者）

以下文件来自 [ultralytics/yolov5](https://github.com/ultralytics/yolov5) v6.0，许可为 **GPL-3.0**，
文件头部保留了原始的 `# YOLOv5 🚀 by Ultralytics, GPL-3.0 license` 版权声明：

| 路径 | 说明 |
| --- | --- |
| `models/` | YOLOv5 网络结构定义（`common.py`、`yolo.py`、`experimental.py`、`yaml` 配置等） |
| `utils/` | 通用工具（NMS、数据加载与增强、绘图、损失、指标、日志、下载等） |
| `data/` | 数据集配置与超参数（`coco.yaml`、`hyps/*.yaml`、`scripts/` 等） |
| `train.py` | 训练入口脚本 |
| `val.py` | 验证入口脚本 |
| `export.py` | 模型导出脚本 |
| `hubconf.py` | PyTorch Hub 入口 |
| `Dockerfile`、`.dockerignore` | 容器构建配置 |
| `data/images/bus.jpg`、`data/images/zidane.jpg` | Ultralytics 提供的示例图片（原始来源为 COCO 数据集） |

其中：

- `models/tf.py` 由 [@zldrobit](https://github.com/zldrobit) 贡献（[PR #1127](https://github.com/ultralytics/yolov5/pull/1127)）
- `weights/yolov5s.pt` 为 Ultralytics 官方发布的预训练权重，同样受 GPL-3.0 约束

### 2. 本项目改写或原创的文件（版权归 SiyuChen12138）

| 路径 | 说明 |
| --- | --- |
| `detect.py` | **基于上游推理流程改写**：封装成 `detect_image` / `detect_video` / `detect_single_frame` 接口，并新增兼容 PyInstaller 打包环境的模型路径解析 |
| `main.py` | **原创**：PyQt5 图形界面主程序 |
| `untitled.py`、`untitled.ui` | **原创**：Qt Designer 设计的界面（`untitled.py` 由 `pyuic5` 自动生成） |
| `main.spec` | **原创**：PyInstaller 打包配置 |
| `runs/train/exp4/**` | **原创产出**：本项目训练结果（以 GPL-3.0 的 `yolov5s.pt` 为基座微调得到的 `best.pt`） |
| `mydata/fall_down_yolo/data.yaml` | **本项目原创**：数据集配置模板 |
| `README.md`、`NOTICE.md`、`.gitignore` | **原创**：本项目文档与配置 |

> **数据集本身不在本仓库中。** 训练所用数据集为作者自行购置的第三方数据集，
> 不具备公开再分发权利，因此图片与标注文件均未上传。见 [docs/DATASET_LICENSE.md](docs/DATASET_LICENSE.md)。

### 3. 已移除的上游内容

上游仓库中的 `.github/`（CI 工作流、Issue 模板、FUNDING / Dependabot 配置）和 `CONTRIBUTING.md`
属于 **Ultralytics 自身的仓库管理配置**，与本软件功能无关。保留在本仓库会导致：

- `ci-testing.yml`、`codeql-analysis.yml` 在每次推送时运行并失败
- `FUNDING.yml` 在**你的**仓库上显示指向 Ultralytics 的赞助入口，造成误导
- `dependabot.yml` 对 2020 年的旧版本依赖持续开启 PR

因此这些文件**已从本仓库移除**，功能代码不受影响。如需查看，请访问
[ultralytics/yolov5](https://github.com/ultralytics/yolov5)。

---

## 二、运行时依赖的第三方库

| 组件 | 许可 | 用途 |
| --- | --- | --- |
| [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) v6.0 | **GPL-3.0** | 检测框架主体 |
| [PyQt5](https://riverbankcomputing.com/software/pyqt/) | **GPL-3.0** 或商业许可 | 图形界面 |
| [PyInstaller](https://pyinstaller.org/) | GPL-2.0-or-later（含 Bootloader 例外条款） | 打包 exe |
| [PyTorch](https://pytorch.org/) | BSD-3-Clause | 深度学习框架 |
| [torchvision](https://pytorch.org/vision/) | BSD-3-Clause | 视觉工具库 |
| [OpenCV (opencv-python)](https://opencv.org/) | Apache-2.0 | 图像 / 视频读写 |
| [NumPy](https://numpy.org/) | BSD-3-Clause | 数值计算 |
| [Pillow](https://python-pillow.org/) | HPND | 图像处理 |
| [PyYAML](https://pyyaml.org/) | MIT | 配置文件解析 |
| [Matplotlib](https://matplotlib.org/) | PSF-based（BSD 兼容） | 绘图 |
| [pandas](https://pandas.pydata.org/) | BSD-3-Clause | 数据处理 |
| [seaborn](https://seaborn.pydata.org/) | BSD-3-Clause | 统计绘图 |
| [SciPy](https://scipy.org/) | BSD-3-Clause | 科学计算 |
| [tqdm](https://tqdm.github.io/) | MPL-2.0 / MIT | 进度条 |
| [requests](https://requests.readthedocs.io/) | Apache-2.0 | HTTP 请求 |
| [TensorBoard](https://www.tensorflow.org/tensorboard) | Apache-2.0 | 训练可视化 |
| [thop](https://github.com/Lyken17/pytorch-OpCounter) | MIT | FLOPs 统计 |

---

## 三、GPL-3.0 对分发的要求（重要）

因为项目使用了 GPL-3.0 的 YOLOv5 代码，并链接了 GPL-3.0 的 PyQt5，所以：

1. **本项目的全部源代码必须以 GPL-3.0 发布**，不能改为闭源许可，也不能附加额外限制。
2. **分发 exe（`dist/main.exe`）时，必须同时提供或承诺提供完整对应的源代码。**
   本仓库已公开全部源码，满足该要求；请在发布 exe 的 Release 说明中注明源码地址。
3. **不得移除**任何源文件中已有的版权声明和许可声明。
4. 若要**闭源商用**，需要分别向 Ultralytics 和 Riverbank Computing 购买商业许可。
5. 建议在仓库主页的 About 区域把 License 设置为 **GPL-3.0**，让许可信息清晰可见。

---

## 四、数据集声明

本仓库**不包含**训练数据集的图片与标注文件。该数据集为作者自行购置的第三方数据集，
**不具备公开再分发权利**，因此未上传至本仓库，也未作为 Release 附件发布。

仓库中仅保留 `mydata/fall_down_yolo/data.yaml` 用于说明数据格式。
完整的来源与处理说明见 [docs/DATASET_LICENSE.md](docs/DATASET_LICENSE.md)。

> 训练所得的模型权重（`best.pt`）属于本项目产出，按 GPL-3.0 发布；
> 使用者在将此模型用于商业场景前，建议自行评估训练数据的权利风险。
