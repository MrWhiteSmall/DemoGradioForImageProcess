import os
import shutil
import random
import gradio as gr
from tqdm import tqdm

from tool_for_file import get_tree_structure

ratio_by_dataset_type={
    'det': [
        (2, 1), 
        (3, 1), (3, 2), 
        (4, 1), (4, 3),
        (5, 1), (5, 2), (5, 3), (5, 4)
    ],
    'cls': [
        (2, 1, 1), 
        (3, 1, 1), (3, 2, 1), 
        (4, 1, 1), (4, 3, 2),
        (5, 1, 1), (5, 2, 2), (5, 3, 2), (5, 4, 3)
    ]
}

def init_dataset_type():
    return change_dataset_type(radio_folder_type='det')
# 触发dataset type改变的ratio
def change_dataset_type(radio_folder_type):
    show_ratios = ratio_by_dataset_type[radio_folder_type]
    show_ratios = [f'{s[0]}:{s[1]}:{s[2]}' if len(s)==3 else f'{s[0]}:{s[1]}' for s in show_ratios]
    return gr.Radio(
                    label='文件夹train_test比例',
                    choices=show_ratios,
                    value=show_ratios[0],
                    interactive=True)
    


def create_directories(merge_type, target_folder, classes=None):
    if merge_type == 'det':
        # Create directories for 'det' merge type
        os.makedirs(os.path.join(target_folder, 'train', 'images'), exist_ok=True)
        os.makedirs(os.path.join(target_folder, 'train', 'labels'), exist_ok=True)
        os.makedirs(os.path.join(target_folder, 'val', 'images'), exist_ok=True)
        os.makedirs(os.path.join(target_folder, 'val', 'labels'), exist_ok=True)
    elif merge_type == 'cls':
        # Create directories for 'cls' merge type
        os.makedirs(os.path.join(target_folder, 'train'), exist_ok=True)
        os.makedirs(os.path.join(target_folder, 'test'), exist_ok=True)
        os.makedirs(os.path.join(target_folder, 'val'), exist_ok=True)
        for cls in classes:
            os.makedirs(os.path.join(target_folder, 'train', str(cls)), exist_ok=True)
            os.makedirs(os.path.join(target_folder, 'test', str(cls)), exist_ok=True)
            os.makedirs(os.path.join(target_folder, 'val', str(cls)), exist_ok=True)

def split_and_copy_files(merge_type, source_folder, target_folder, merge_ratio):
    # Get class directories
    class_dirs = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]
    # classes = [ class_dir.split('_')[-1] for class_dir in class_dirs]
    
    for class_dir in class_dirs:
        class_path = os.path.join(source_folder, class_dir)
        image_files = [f for f in os.listdir(class_path) if f.endswith('.bmp')]  # Assuming images are .jpg
        label_files = [f.replace('.bmp', '.txt') for f in image_files]  # Assuming labels are .txt
        
        # Shuffle files
        combined = list(zip(image_files, label_files))
        random.shuffle(combined)
        image_files, label_files = zip(*combined)
        
        # Split according to the given ratio
        if merge_type == 'det':
            split_train = int(len(image_files) * (int(merge_ratio.split(':')[0]) / sum(map(int, merge_ratio.split(':')))))
            split_val = len(image_files) - split_train
            train_images = image_files[:split_train]
            train_labels = label_files[:split_train]
            val_images = image_files[split_train:]
            val_labels = label_files[split_train:]
            
            # Copy images and labels to train and val directories
            for img, lbl in tqdm(zip(train_images, train_labels)):
                shutil.copy(os.path.join(class_path, img), os.path.join(target_folder, 'train', 'images', img))
                shutil.copy(os.path.join(class_path, lbl), os.path.join(target_folder, 'train', 'labels', lbl))
            for img, lbl in tqdm(zip(val_images, val_labels)):
                shutil.copy(os.path.join(class_path, img), os.path.join(target_folder, 'val', 'images', img))
                shutil.copy(os.path.join(class_path, lbl), os.path.join(target_folder, 'val', 'labels', lbl))
        
        elif merge_type == 'cls':
            # Split according to cls merge ratio
            ratio = list(map(int, merge_ratio.split(':')))
            split_train = int(len(image_files) * (ratio[0] / sum(ratio)))
            split_val = int(len(image_files) * (ratio[1] / sum(ratio)))
            split_test = len(image_files) - split_train - split_val
            train_images = image_files[:split_train]
            val_images = image_files[split_train:split_train + split_val]
            test_images = image_files[split_train + split_val:]
            
            # Copy images to corresponding directories
            for img in tqdm(train_images):
                shutil.copy(os.path.join(class_path, img), os.path.join(target_folder, 'train', class_dir, img))
            for img in tqdm(val_images):
                shutil.copy(os.path.join(class_path, img), os.path.join(target_folder, 'val', class_dir, img))
            for img in tqdm(test_images):
                shutil.copy(os.path.join(class_path, img), os.path.join(target_folder, 'test', class_dir, img))

def merge_and_split(source_folder, target_folder, merge_type, merge_ratio):
    # Create target directory structure
    class_dirs = [d for d in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, d))]
    # num_classes = len(class_dirs)
    
    create_directories(merge_type, target_folder, class_dirs)
    split_and_copy_files(merge_type, source_folder, target_folder, merge_ratio)

    return get_tree_structure(target_folder)