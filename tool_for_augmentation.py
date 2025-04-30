import cv2,os
import numpy as np
from PIL import Image
from os.path import join as osj

from tool_for_augmentation_affine import affine_transform_with_yolo
from tool_for_augmentation_hsv import adjust_by_plan,hsv_transform_with_yolo

from tool_for_file import get_files,update_info
'''
0
1 2 3 4
5 6 7 8
9 10 11
'''
gr_augmentation_choices = ['None',
                           'PlanA','PlanB','PlanC','PlanD',
                            '高饱和','低饱和','高亮度','低亮度',
                            'rotate +90°','rotate -90°','rotate 180°',]
plans = {
    'PlanA': (90,255,10,'A'),
    'PlanB': (118,255,10,'B'),
    'PlanC': (28,255,10,'C'),
    'PlanD': (45,255,14,'D'),
    
    '高饱和': (0,255,0,'E'),
    '低饱和': (0,-255,0,'F'),
    '高亮度': (0,0,10,'G'),
    '低亮度': (0,0,-5,'H'),
}


def get_affine_agle(augm_radiolist):
    aug_id = gr_augmentation_choices.index(augm_radiolist)
    if aug_id == 9:
        return 90
    if aug_id == 10:
        return -90
    if aug_id == 11:
        return 180
    return None
    
def get_hsv_plan(augm_radiolist):
    aug_id = gr_augmentation_choices.index(augm_radiolist)
    if aug_id not in [1,2,3,4,5,6,7,8]:
        return None
    plan = plans[augm_radiolist]
    return plan

def handle_augmentation(augm_radiolist,
                        folder_path, subfolder_name, image_name,
                        is_final_save=False):
    # print(image_name)
    n,ext = image_name.split('.')
    label_name = n+'.txt'
    image_path = osj(folder_path,subfolder_name,image_name)
    label_path = osj(folder_path,subfolder_name,label_name)
     
    if augm_radiolist == 'None':
        return Image.open(image_path)
    angle = get_affine_agle(augm_radiolist)
    plan = get_hsv_plan(augm_radiolist)
    print(plan)
    
    if angle is not None:
        save_name = f'{n}-affine{angle}'
        save_img_name = f'{save_name}.{ext}'
        save_label_name = f'{save_name}.txt'
        save_image_path = osj(folder_path,subfolder_name,save_img_name)
        save_label_path = osj(folder_path,subfolder_name,save_label_name)
        return affine_transform_with_yolo(
            image_path=image_path,label_path=label_path,
            angle=angle,
            save_image_path=save_image_path,
            save_label_path=save_label_path,
            is_final_save=is_final_save
        )

    if plan is not None:
        save_name = f'{n}-hsv{plan[-1]}'
        save_img_name = f'{save_name}.{ext}'
        save_label_name = f'{save_name}.txt'
        save_image_path = osj(folder_path,subfolder_name,save_img_name)
        save_label_path = osj(folder_path,subfolder_name,save_label_name)
        return hsv_transform_with_yolo(
            image_path=image_path,label_path=label_path,
            save_image_path=save_image_path,save_label_path=save_label_path,
            plan=plan,
            is_final_save=is_final_save
        )
# affine


# 预览选择的图片 with augmentation
'''
1 aug获取下标
2 根据下标，发动增强函数
3 预览时is_save为false，反之为true
'''
def preview_image(folder_path, subfolder_name, selected_files,augm_radiolist):
    print(f'augm_radiolist {augm_radiolist}')
    # 把 radiolist 内容传给其他函数，由其他函数自行判断是否参与增强
    
    if not selected_files:
        return None, "未选择任何文件！"
    first_file = selected_files[0]
    file_path = os.path.join(folder_path, subfolder_name, first_file)
    if not os.path.isfile(file_path):
        return None, "选择的文件无效或不存在！"
    
    show_img = handle_augmentation(augm_radiolist,
                                   folder_path, subfolder_name, first_file,
                                   is_final_save=False)
    return show_img, f"预览文件：{first_file}"


def save_augm_image(folder_path, subfolder_name, selected_files,augm_radiolist):
    print(f'augm_radiolist {augm_radiolist}')
    # 把 radiolist 内容传给其他函数，由其他函数自行判断是否参与增强
    
    if not selected_files:
        return None, "未选择任何文件！"
    for select_file in selected_files:
        if select_file.endswith('.txt'):
            continue
        file_path = os.path.join(folder_path, subfolder_name, select_file)
        if not os.path.isfile(file_path):
            return None, "选择的文件无效或不存在！"
        
        handle_augmentation(augm_radiolist,
                            folder_path, subfolder_name, select_file,
                            is_final_save=True)
    # return show_img, f"预览文件：{first_file}"
    files_checklist, preview_status = get_files(folder_path,subfolder_name)
    output = update_info(folder_path)
    return files_checklist, preview_status,output
