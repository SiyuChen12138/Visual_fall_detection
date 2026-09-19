"""
行人跌倒检测系统 —— PyQt5 图形界面主程序

Copyright (C) 2026 SiyuChen12138

本文件是「行人跌倒检测系统」的一部分，以 GNU General Public License v3.0 发布，
完整许可文本见仓库根目录的 LICENSE 文件。

上游依赖：Ultralytics YOLOv5 v6.0 (GPL-3.0) — https://github.com/ultralytics/yolov5
"""

import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QMetaObject, Q_ARG
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from untitled import Ui_MainWindow
from detect import detect_image, detect_video, preprocess_image, detect_single_frame


class VideoThread(QThread):
    frame_signal = pyqtSignal(np.ndarray, list)

    def __init__(self, source):
        super().__init__()
        self.source = source  # 输入源可以是摄像头ID（如0）或文件路径
        self._is_running = True

    def run(self):
        try:
            # 判断输入源类型（摄像头或文件）
            if isinstance(self.source, int) or str(self.source).isdigit():
                cap = cv2.VideoCapture(int(self.source))  # 摄像头模式
            else:
                cap = cv2.VideoCapture(self.source)  # 文件模式

            if not cap.isOpened():
                print("无法打开视频源！")
                return

            while self._is_running:
                ret, frame = cap.read()
                if not ret:
                    break
                # 预处理和检测
                img = preprocess_image(frame)
                result, labels = detect_single_frame(img, frame.copy())
                if result is not None:
                    self.frame_signal.emit(result.copy(), labels.copy())
            cap.release()
        except Exception as e:
            print(f"视频线程错误：{e}")
        finally:
            self.stop()

    def stop(self):
        self._is_running = False


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 初始化变量
        self.video_thread = None
        self.is_camera_running = False  # 摄像头状态标志

        # 连接按钮事件
        self.OpenVideoBtn.clicked.connect(self.load_media)
        self.CameraBtn.clicked.connect(self.toggle_camera)

    def toggle_camera(self):
        """切换摄像头开关状态"""
        if not self.is_camera_running:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        """启动摄像头检测"""
        if self.video_thread:
            self.video_thread.stop()

        self.is_camera_running = True
        self.CameraBtn.setText("停止摄像头")
        self.video_thread = VideoThread(source=0)  # 摄像头设备号0
        self.video_thread.frame_signal.connect(self.update_video_frame)
        self.video_thread.start()

    def stop_camera(self):
        """停止摄像头检测"""
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.quit()
        self.is_camera_running = False
        self.CameraBtn.setText("启动摄像头")
        self.Imglabel.clear()

    def cvimg_to_qtimg(self, cvimg):
        """将OpenCV图像转换为QPixmap"""
        if cvimg is None or cvimg.size == 0:
            return QPixmap()
        h, w, ch = cvimg.shape
        bytes_per_line = ch * w
        q_img = QImage(cvimg.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap.fromImage(q_img)

    @pyqtSlot()
    def load_media(self):
        """加载图片或视频文件"""
        filepath, _ = QFileDialog.getOpenFileName(
            self, "选择媒体文件", "", "媒体文件 (*.jpg *.jpeg *.png *.mp4 *.avi)"
        )
        if not filepath:
            return

        # 如果摄像头正在运行，先停止
        if self.is_camera_running:
            self.stop_camera()

        # 停止之前的线程
        if self.video_thread:
            self.video_thread.stop()

        # 启动新线程
        if filepath.lower().endswith(('.mp4', '.avi')):
            self.video_thread = VideoThread(source=filepath)
            self.video_thread.frame_signal.connect(self.update_video_frame)
            self.video_thread.start()
        else:
            result, labels = detect_image(filepath)
            self.display_result(result, labels)

    @pyqtSlot(np.ndarray, list)
    def update_video_frame(self, frame, labels):
        """更新视频帧到UI（线程安全）"""
        QMetaObject.invokeMethod(self, "_update_frame",
                               Qt.QueuedConnection,
                               Q_ARG(np.ndarray, frame),
                               Q_ARG(list, labels))

    @pyqtSlot(np.ndarray, list)
    def _update_frame(self, frame, labels):
        """实际更新UI的槽函数"""
        try:
            pixmap = self.cvimg_to_qtimg(frame)
            self.Imglabel.setPixmap(pixmap.scaled(
                self.Imglabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            self.Infolabel.setText("\n".join(labels))
        except Exception as e:
            print(f"更新帧失败：{e}")

    def display_result(self, image, labels):
        """显示图片检测结果"""
        if image is not None:
            pixmap = self.cvimg_to_qtimg(image)
            self.Imglabel.setPixmap(pixmap.scaled(
                self.Imglabel.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
            self.Infolabel.setText("\n".join(labels))

    def closeEvent(self, event):
        """窗口关闭时释放资源"""
        if self.video_thread:
            self.video_thread.stop()
            self.video_thread.quit()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())