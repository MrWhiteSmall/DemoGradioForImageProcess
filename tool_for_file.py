import os,pickle
from glob import glob
from os.path import join as osj
import gradio as gr
from PIL import Image
import numpy as np



def update_info(folder_path):
    _,_,info = get_subfolders(folder_path)
    return info
# 获取目标文件夹的子文件夹列表
def get_subfolders(folder_path):
    sep = os.sep
    if not os.path.isdir(folder_path):
        return [], "目标文件夹无效或不存在！"
    subfolders = [
        f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))
    ]
    # 获得每个子文件夹下的图片数量
    info = []
    for parent_dir,sub_dirs,files in os.walk(folder_path):
        for sub_dir in sub_dirs:
            cur_dir = osj(parent_dir,sub_dir)
            num = len(glob(f'{cur_dir}{sep}*.bmp'))
            info.append(f'{sub_dir}\t:\t{num}')
    info = '\n'.join(info)
    return gr.Dropdown(choices=subfolders,value=None), f"找到 {len(subfolders)} 个子文件夹。",info

# 获取选定子文件夹下的文件列表
def get_files_ori(folder_path):
    if not os.path.isdir(folder_path):
        return [], "未找到子文件夹！"
    files = [
        f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))
    ]
    return files, f"找到 {len(files)} 个文件。"

def get_files_for_gr_show_defect(folder_path):
    files,info = get_files_ori(folder_path)
    return gr.Radio(choices=files,value=None),info
def get_files_for_gr_extract(folder_path):
    files,info = get_files_ori(folder_path)
    return gr.Radio(choices=files,value=None),info
# 获取选定子文件夹下的文件列表 checkbox
def get_files(folder_path, subfolder_name):
    subfolder_path = os.path.join(folder_path, subfolder_name)
    files,info = get_files_ori(subfolder_path)
    return gr.CheckboxGroup(choices=files,value=None),info


# merge之后文件夹的树状信息
def get_tree_structure(root_folder):
    show_info = []
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Calculate the level of indentation based on the depth
        depth = dirpath[len(root_folder):].count(os.sep)
        # Indentation for this level
        current_indent = ' ' * 4 * depth

        # Only print folder names, not the full path
        if dirnames:  # Folder contains subdirectories
            show_info.append(f"{current_indent}{os.path.basename(dirpath)}")
        elif filenames:  # Folder contains files
            show_info.append(f"{current_indent}{os.path.basename(dirpath)} (files: {len(filenames)})")

        # Optionally, print files inside folders (can be removed if not needed)
        # for filename in filenames:
        #     show_info.append(f"{current_indent}    {filename}")
    print(show_info)
    return '\n'.join(show_info) if len(show_info) else '数据集最终结构显示区'


## tool for show local defect
# 将图片转换为 numpy 数组并保存为 pickle 文件
def save_images_to_pickle(images):
    image_arrays = []
    for img in images:
        img_array = np.array(img)  # 将PIL图像转换为numpy数组
        image_arrays.append(img_array)
    
    # 保存为 pickle 文件
    with open("tmp_show_defect.pickle", "wb") as f:
        pickle.dump(image_arrays, f)

# 从 pickle 文件中加载图片并返回
def load_images_from_pickle(index=None):
    with open("tmp_show_defect.pickle", "rb") as f:
        image_arrays = pickle.load(f)  # 从pickle文件加载数组
    
    # 将 numpy 数组转换回 PIL 图片
    images = [Image.fromarray(arr) for arr in image_arrays]
    return images if index is None else images[index]