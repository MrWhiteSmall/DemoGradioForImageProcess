import cv2
import numpy as np
from PIL import Image
from os.path import join as osj

def affine_transform_with_yolo(image_path, label_path, angle, 
                               save_image_path, save_label_path,
                               is_final_save=False):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像，请检查路径是否正确。")
        return

    # 获取图像中心和尺寸
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    # 生成旋转矩阵
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    # 执行仿射变换
    rotated_image = cv2.warpAffine(image, M, (w, h))
    if is_final_save:
        cv2.imwrite(save_image_path, rotated_image)

        # 读取YOLO标注文件
        with open(label_path, 'r') as f:
            lines = f.readlines()

        new_lines = []

        for line in lines:
            # YOLO标注格式: class_id x_center y_center width height
            parts = line.strip().split()
            class_id = parts[0]
            x_center = float(parts[1]) * w
            y_center = float(parts[2]) * h
            bbox_width = float(parts[3]) * w
            bbox_height = float(parts[4]) * h

            # 计算边界框四个顶点的坐标
            corners = np.array([
                [x_center - bbox_width / 2, y_center - bbox_height / 2],
                [x_center + bbox_width / 2, y_center - bbox_height / 2],
                [x_center + bbox_width / 2, y_center + bbox_height / 2],
                [x_center - bbox_width / 2, y_center + bbox_height / 2]
            ])

            # 应用仿射变换到每个顶点
            transformed_corners = cv2.transform(np.array([corners]), M)[0]

            # 获取新的边界框
            x_min, y_min = transformed_corners.min(axis=0)
            x_max, y_max = transformed_corners.max(axis=0)

            # 计算新的中心点和宽高（归一化到0-1范围）
            new_x_center = ((x_min + x_max) / 2) / w
            new_y_center = ((y_min + y_max) / 2) / h
            new_width = (x_max - x_min) / w
            new_height = (y_max - y_min) / h

            # 添加新的标注行
            new_line = f"{class_id} {new_x_center:.6f} {new_y_center:.6f} {new_width:.6f} {new_height:.6f}"
            new_lines.append(new_line)

        # 保存新的标注文件
        with open(save_label_path, 'w') as f:
            f.write("\n".join(new_lines))
    # print(f"仿射变换后的标注已保存到: {save_label_path}")
    if not is_final_save:
        show_img = cv2.cvtColor(rotated_image,cv2.COLOR_BGR2RGB)
        return Image.fromarray(show_img)
