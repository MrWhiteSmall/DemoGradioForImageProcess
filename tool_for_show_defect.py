import os,cv2,math,random
from os.path import join as osj
import matplotlib.pyplot as plt
from PIL import Image
import gradio as gr

from tool_for_file import save_images_to_pickle,load_images_from_pickle

def get_n_ext(name):
    name_split = name.split('.')
    ext = name_split[-1]
    n = '.'.join(name_split[:-1])
    return n,ext
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
# 返回rgb numpy格式的list
'''
img_ori 不改动
img_copy 添加label框
'''
def get_zoomed_areas(img_ori,img_copy,boxes):
    zoomed_areas = []
    for cls, abs_x_center, abs_y_center, abs_width, abs_height in boxes:
        # 计算边界框坐标
        x1 = int(abs_x_center - abs_width / 2)
        y1 = int(abs_y_center - abs_height / 2)
        x2 = int(abs_x_center + abs_width / 2)
        y2 = int(abs_y_center + abs_height / 2)

        # 绘制边界框
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 添加类别标签
        label_text = f"Class {int(cls)}"
        cv2.putText(img_copy, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
            
        cropped_area = img_ori[y1:y2, x1:x2].copy()
        # 放大裁剪区域
        zoomed_area = cv2.resize(cropped_area
                                ,(cropped_area.shape[1] * 4, cropped_area.shape[0] * 4)
                                ,interpolation=cv2.INTER_NEAREST)
        rgb = cv2.cvtColor(zoomed_area,cv2.COLOR_BGR2RGB)
        zoomed_areas.append(rgb)
    return zoomed_areas

def get_imgpath_labelpath(name,img_dir,label_dir):
    n,ext = get_n_ext(name=name)
    img_name = name
    label_name = n+'.txt'
    img_path = osj(img_dir,img_name)
    label_path = osj(label_dir,label_name)
    return img_path,label_path

def get_labeled_img_pil(img_path,label_path):
    img_ori = cv2.imread(img_path)
    h,w,_ = img_ori.shape
    boxes = convert_yolo_to_absolute(label_path,w,h)
    
    img_copy = img_ori.copy()
    # 保存下来 后续根据radio_defect_type选择其中的进行显示
    # image_copy已经保存label的框信息
    zoomed_areas = get_zoomed_areas(img_ori,img_copy,boxes)
    
    labeled_rgb = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)
    labeled_pil = Image.fromarray(labeled_rgb)

    return labeled_pil,boxes,zoomed_areas
    
# save zoomed areas


'''
boxes.append([cls, abs_x_center, abs_y_center, abs_width, abs_height])
'''
def show_defect_global(source_folder,source_label_folder,radio_file_list):
    # 图
    img_path,label_path = \
        get_imgpath_labelpath(radio_file_list,source_folder,source_label_folder)
    labeled_pil,boxes,zoomed_areas = get_labeled_img_pil(img_path,label_path)
    # defect choice
    print('zoom areas',len(zoomed_areas))
    if len(zoomed_areas)==0:
        defect_types = []
    else:
        # save zoomed areas(numpy rgb 格式)
        save_images_to_pickle(zoomed_areas)
        
        defect_types = list(range(len(zoomed_areas)))
        defect_types = [f'Defect {d+1}' for d in defect_types]
    defect_types = gr.Radio(choices=defect_types)
    # info  
    show_info = []
    for id,box in enumerate(boxes):
        show_info.append(
            f'Defect {id+1}: cls_{box[0]},x_center {box[1]},y_center {box[2]},width {box[3]},height {box[4]}')
    show_info = '\n'.join(show_info)
    return labeled_pil,defect_types,show_info
    pass

def show_defect_local(radio_defect_types):
    if radio_defect_types is None:
        return None
    radio_defect_types = radio_defect_types.split(' ')[-1]
    print('radio_defect_types',radio_defect_types)
    radio_defect_types = int(radio_defect_types)-1
    return load_images_from_pickle(radio_defect_types)
    pass