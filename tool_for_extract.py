import cv2,os
from PIL import Image
import numpy  as np
from os.path import join as osj
from glob import glob
from tqdm import tqdm

from tool_for_file import get_tree_structure

extract_types = {
    'No Extract':[],
    'HSV Extract':[(35,77),(143,255),(23,43)],
    'Gray Extract':[(80, 255)]
}

def get_croped_xywh_hsv(img_path,
                        h_threshold_min,h_threshold_max,
                        s_threshold_min,s_threshold_max,
                        v_threshold_min,v_threshold_max):
    # 读取图像
    image_rgb_ori = cv2.imread(img_path)
    ori_h,ori_w,_ = image_rgb_ori.shape
    # 转换为 HSV 色彩空间
    image_hsv = cv2.cvtColor(image_rgb_ori, cv2.COLOR_BGR2HSV)

    lower = np.array([h_threshold_min,s_threshold_min,v_threshold_min])
    upper = np.array([h_threshold_max,s_threshold_max,v_threshold_max])

    # 创建掩码
    mask = cv2.inRange(image_hsv, lower, upper)

    image_rgb_ori[mask==0]=[0,0,0]

    img = image_rgb_ori.copy()
    # 将图像转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 应用二值化
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    # 找到轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        # Step 6: 使用minAreaRect找到最小外接矩形
        rect = cv2.minAreaRect(largest_contour)  # 返回中心点、宽高和旋转角度
        box = cv2.boxPoints(rect)  # 获取矩形的四个顶点坐标
        box = np.intp(box)  # 将坐标转为整数
        # print('box',box)
        
        # Step 7: 绘制外接矩形
        xmin = min(box[:,0])
        xmax = max(box[:,0])
        ymin = min(box[:,1])
        ymax = max(box[:,1])
        # print(xmin,xmax,ymin,ymax)
        w=xmax-xmin
        h=ymax-ymin
        
        # Step 7: 绘制外接矩形
        image_rgb = image_rgb_ori.copy() # h w c
        image_rgb = image_rgb[ymin:ymax,xmin:xmax,:]

    return image_rgb_ori,image_rgb,ori_h,ori_w,xmin,ymin,w,h

def get_croped_xywh_gray(img_path,gray_threshold_min,gray_threshold_max):
        
        # Step 1: 读取图像
        image_rgb_ori = cv2.imread(img_path)
        ori_h,ori_w,_ = image_rgb_ori.shape
        gray = cv2.cvtColor(image_rgb_ori, cv2.COLOR_BGR2GRAY)
        # 将图像二值化
        _, gray = cv2.threshold(gray, 
                                gray_threshold_min, gray_threshold_max, 
                                cv2.THRESH_BINARY)

        # Step 4: 轮廓检测
        contours, _ = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Step 6: 选择最大轮廓（假设玻璃是最大或一个相对大的轮廓）
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            # Step 6: 使用minAreaRect找到最小外接矩形
            rect = cv2.minAreaRect(largest_contour)  # 返回中心点、宽高和旋转角度
            box = cv2.boxPoints(rect)  # 获取矩形的四个顶点坐标
            box = np.intp(box)  # 将坐标转为整数
            # print('box',box)
            
            # Step 7: 绘制外接矩形
            xmin = min(box[:,0])
            xmax = max(box[:,0])
            ymin = min(box[:,1])
            ymax = max(box[:,1])
            # print(xmin,xmax,ymin,ymax)
            w=xmax-xmin
            h=ymax-ymin
            
            # Step 7: 绘制外接矩形
            image_rgb = image_rgb_ori.copy() # h w c
            image_rgb = image_rgb[ymin:ymax,xmin:xmax,:]
                
        return image_rgb_ori,image_rgb,ori_h,ori_w,xmin,ymin,w,h

def get_croped_xywh(radio_extract_type,
                    origin_path_img,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,
                    gray_threshold_min,gray_threshold_max):
    types = list(extract_types.keys())
    index = types.index(radio_extract_type)
    if index == 1:
        return get_croped_xywh_hsv(origin_path_img,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,)
    if index == 2:
        return get_croped_xywh_gray(origin_path_img,
                    gray_threshold_min,gray_threshold_max)
    # 读取图像
    image_rgb_ori = cv2.imread(origin_path_img)
    image_rgb = image_rgb_ori.copy()
    ori_h,ori_w,_ = image_rgb.shape
    return image_rgb_ori,image_rgb,ori_h,ori_w,0,0,ori_w,ori_h

def convert_yolo_to_absolute(label_file, ori_w, ori_h):
    boxes = []
    with open(label_file, 'r') as f:
        for line in f:
            cls, x_center, y_center, width, height = map(float, line.strip().split())
            abs_x_center = x_center * ori_w
            abs_y_center = y_center * ori_h
            abs_width = width * ori_w
            abs_height = height * ori_h
            boxes.append([cls, abs_x_center, abs_y_center, abs_width, abs_height])
    return boxes
# 更新标签坐标，并删除不在裁剪区域内的标签
def update_labels_after_crop(boxes, x_crop, y_crop, w_new, h_new):
    updated_boxes = []
    for box in boxes:
        cls, abs_x_center, abs_y_center, abs_width, abs_height = box
        # 更新中心点坐标
        new_x_center = abs_x_center - x_crop
        new_y_center = abs_y_center - y_crop

        # 计算框的半宽和半高
        half_width = abs_width / 2
        half_height = abs_height / 2

        # 判断是否完全在裁剪区域内
        if (new_x_center - half_width >= 0 and new_x_center + half_width <= w_new and 
            new_y_center - half_height >= 0 and new_y_center + half_height <= h_new):
            # 如果框在裁剪区域内，保留这个框
            updated_boxes.append([cls, new_x_center, new_y_center, abs_width, abs_height])
    
    return updated_boxes

# 转换为归一化坐标并保存
def save_new_labels(updated_boxes, label_file, w_new, h_new):
    with open(label_file, 'w') as f:
        for box in updated_boxes:
            cls, new_x_center, new_y_center, abs_width, abs_height = box
            norm_x_center = new_x_center / w_new
            norm_y_center = new_y_center / h_new
            norm_width = abs_width / w_new
            norm_height = abs_height / h_new
            f.write(f"{int(cls)} {norm_x_center} {norm_y_center} {norm_width} {norm_height}\n")

def extract_by_type(source_folder,source_label_folder,
                    dst_save_folder,
                    radio_file_list,
                    radio_extract_type,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,
                    gray_threshold_min,gray_threshold_max,
                    is_save=False):
    sep = os.sep
    n,ext = radio_file_list.split('.')
    label_name = f'{n}.txt'
    origin_path_img = osj(source_folder,radio_file_list)
    dst_path_img = osj(dst_save_folder,radio_file_list)
    origin_path_label = osj(source_label_folder,label_name)
    dst_path_label = osj(dst_save_folder,label_name)
    
    image_rgb_ori,image_rgb,ori_h,ori_w,xmin,ymin,w,h = \
        get_croped_xywh(radio_extract_type,origin_path_img,
                        h_threshold_min,h_threshold_max,
                        s_threshold_min,s_threshold_max,
                        v_threshold_min,v_threshold_max,
                        gray_threshold_min,gray_threshold_max)
    
    boxes = convert_yolo_to_absolute(origin_path_label,ori_w,ori_h)
    updated_boxes = update_labels_after_crop(boxes, xmin, ymin, w, h)
    # print(boxes)
    # print(updated_boxes)
    
    # if len(updated_boxes)==0:
        # 全被筛选掉了，这张图就不要
        # print('剪裁后，剪裁区域没有label',name)
        # pass
    # 要先把原图中缺陷部分复制到现在的对应区域，因为绿色被筛选出来以后，原来的缺陷部分都被筛选掉了
    img = image_rgb_ori[ymin:ymin+h,xmin:xmin+w].copy()
    
    
    '''
    next：
        show defect
        选择性保存/only show
    '''
    if is_save:
        try:
            cv2.imwrite(dst_path_img,img) # 保存时自动成为RGB
            # 重新归一化并保存
            save_new_labels(updated_boxes, dst_path_label, w, h)
            return 1
        except Exception as e:
            return 0
    else:
        return img,updated_boxes
        
    
def preview_image_by_extract(source_folder,source_label_folder,
                            dst_save_folder,
                            radio_file_list,
                            radio_extract_type,
                            h_threshold_min,h_threshold_max,
                            s_threshold_min,s_threshold_max,
                            v_threshold_min,v_threshold_max,
                            gray_threshold_min,gray_threshold_max):
    is_save = False
    img,updated_boxes = extract_by_type(source_folder,source_label_folder,
                    dst_save_folder,
                    radio_file_list,
                    radio_extract_type,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,
                    gray_threshold_min,gray_threshold_max,
                    is_save)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)
    return img_pil,f'预览文件:{radio_file_list}'

def extract_image_truly(source_folder,source_label_folder,
                        dst_save_folder,
                        radio_extract_type,
                        h_threshold_min,h_threshold_max,
                        s_threshold_min,s_threshold_max,
                        v_threshold_min,v_threshold_max,
                        gray_threshold_min,gray_threshold_max):
    sep = os.sep
    is_save=True
    path_images = osj(f'{source_folder}','*.bmp')
    names = [p.split(sep)[-1] for p in glob(path_images)]
    os.makedirs(dst_save_folder,exist_ok=True)
    
    success_num = 0
    fail_num = 0
    for name in tqdm(names):
        res = extract_by_type(source_folder,source_label_folder,
                        dst_save_folder,
                        name,
                        radio_extract_type,
                        h_threshold_min,h_threshold_max,
                        s_threshold_min,s_threshold_max,
                        v_threshold_min,v_threshold_max,
                        gray_threshold_min,gray_threshold_max,
                        is_save)
        success_num += 1 if res == 1 else 0
        fail_num += 1 if res ==0 else 0

    show_info = [f'提取成功:{success_num}\n 提取失败:{fail_num}']
    show_info.append(get_tree_structure(dst_save_folder))
    return '\n'.join(show_info)
    