import os
import shutil
from collections import defaultdict
import argparse
from tqdm import tqdm


def get_label_path(label_dirs,labelname):
    for dir in label_dirs:
        path = os.path.join(dir,labelname)
        if os.path.exists(
            path
        ):
            return path
    return None
def move_files_by_class(target_folder, label_folder, output_folder:str):
    sep = os.sep
    # 创建一个字典来保存每个类别的图片数量和框数量
    class_stats = defaultdict(lambda: {'image_count': 0, 'box_count': 0})
    
    # 确保目标输出文件夹存在
    if output_folder!='' and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    '''
    1 获取所有图片file
    2 获取所有label dir
    3 遍历图片file，根据图片name，找label path是否存在
    4 不存在则跳过，存在则继续
    '''
    image_files = []
    # 获取所有图片和标签文件的列表
    # 遍历 root_folder 文件夹中的所有子文件夹及文件
    for dirpath, _, files in os.walk(target_folder):
        for image_file in tqdm(files):
            if image_file.endswith(('.jpg', '.jpeg', '.png','.bmp')):  # 假设图像文件是这几种格式
                image_files.append(
                    os.path.join(dirpath,image_file)
                )
    label_dirs = [label_folder]
    # 遍历 root_folder 文件夹中的所有子文件夹及文件
    for dirpath, subdirs, files in os.walk(label_folder):
        subdirs = [ os.path.join(dirpath,subdir) for subdir in subdirs]
        label_dirs.extend(subdirs)
    print(label_dirs)
        
    for image_path in tqdm(image_files):
        imgname = image_path.split(sep)[-1]
        n = image_path.split(sep)[-1].split('.')[0]
        labelname=f'{n}.txt'
        label_path = get_label_path(label_dirs,labelname)
        if label_path is None:
            print(image_path)
            print(label_path)
            print(f'{imgname}不存在对应的label')
            continue
        
        # 读取标签文件
        with open(label_path, 'r') as f:
            labels = f.readlines()
        
        # 获取每个类别的标签
        categories_in_image = set()  # 用set确保每个类别只计一次
        for label in labels:
            try:
                class_id, _, _, _, _ = label.split()  # 我们只需要类别id
                categories_in_image.add(class_id)
                class_stats[class_id]['box_count'] += 1  # 统计每个类别的框数量
            except Exception as e:
                print(e)
                print(label_path,' 出现错误')
                print('label ',label)
        
        # 根据类别创建子目录并移动文件
        for class_id in categories_in_image:
            if output_folder != '':
                class_folder = os.path.join(output_folder, f'class_{class_id}')
                
                if not os.path.exists(class_folder):
                    os.makedirs(class_folder)
                
                # 移动图像文件
                shutil.copy(image_path, os.path.join(class_folder, imgname))
                # 移动标签文件
                shutil.copy(label_path, os.path.join(class_folder, labelname))
                
            # 更新图像数量
            class_stats[class_id]['image_count'] += 1
    
    sorted_class_stats = sorted(class_stats.items(), key=lambda x: int(x[0]))
    if output_folder != '':
        # 按照 class_id 排序并写入 class_info.txt
        class_info_file = os.path.join(output_folder, 'class_info.txt')
        with open(class_info_file, 'w') as f:
            # 排序 class_id
            
            for class_id, stats in sorted_class_stats:
                f.write(f"Class {class_id}: {stats['image_count']} images, {stats['box_count']} boxes\n")
    
    results = []
    # 输出每个类别的统计信息
    for class_id, stats in sorted_class_stats:
        info = f"Class {class_id}: {stats['image_count']} images, {stats['box_count']} boxes"
        print(info)
        results.append(info)
    
    print("Files moved and statistics computed successfully!")
    return '\n'.join(results) if len(results)!=0 else "未找到符合条件的标注和图片文件！"

