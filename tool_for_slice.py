from tqdm import tqdm
from glob import glob
import cv2,os,math,shutil
from os.path import join as osj

from tool_for_file import get_tree_structure

# area need
# slice所需区域
area_needs = ['全部区域','主体区域','周边区域']
direction_needs = ['上方区域','下方区域','左边区域','右边区域']

get_n = lambda length,slice_width:math.ceil(length/slice_width)
get_overlap = lambda slice_width,origin_size,n:int((slice_width*n-origin_size)/(n-1)) if n>1 else 0

def update_direction_need(ckbox_direction_need):
    need_top=False
    need_bottom=False
    need_left=False
    need_right=False
    for need in ckbox_direction_need:
        index = direction_needs.index(need)
        if index == 0:
            need_top=True
        elif index==1:
            need_bottom=True
        elif index==2:
            need_left=True
        elif index==3:
            need_right=True
    return need_top,need_bottom,need_left,need_right
def update_area_need(radio_area_need):
    index = area_needs.index(radio_area_need)
    need_all = True if index ==0 else False
    need_content = True if index==1 else False 
    need_surround = True if index==2 else False
    return need_all,need_content,need_surround

def is_final_need(block_id,rows,cols,
                  need_top,need_bottom,need_left,need_right,
                  need_all,need_content,need_surround):
    if need_all:
        return True
    idx = block_id - 1
    # 周边区域 and 全部区域 ：存储边
    # 主体区域             ：不存储边
    if (need_top and idx // cols==0) or (need_bottom and idx // cols == rows-1) \
        or (need_left and idx % cols ==0) or (need_right and idx % cols == cols-1):
            if need_surround:
                return True
            else:
                return False
    else:
        if need_content:
            return True
        else:
            return False

def get_new_labels(labels,w,h,crop_xmax,crop_xmin,crop_ymax,crop_ymin):
    new_labels = []
    for label in labels:
        # YOLO标签文件格式: class_id x_center y_center width height
        label_info = label.strip().split()
        # print(label_info)
        class_id = int(label_info[0])
        x_center, y_center, box_width, box_height = map(float, label_info[1:])
        
        x_center *= w
        y_center *= h
        box_width *= w
        box_height *= h
        
        # 计算标注框的边界坐标
        x_min = x_center - box_width / 2
        y_min = y_center - box_height / 2
        x_max = x_center + box_width / 2
        y_max = y_center + box_height / 2
        
        # 检查该标注框是否与当前分块有交集
        if x_max < crop_xmax and x_min > crop_xmin and y_max < crop_ymax and y_min > crop_ymin:
            # 计算该标注框在当前分块中的相对坐标
            new_x_center = (x_center - crop_xmin) / (crop_xmax - crop_xmin)
            new_y_center = (y_center - crop_ymin) / (crop_ymax - crop_ymin)
            new_box_width = box_width / (crop_xmax - crop_xmin)
            new_box_height = box_height / (crop_ymax - crop_ymin)
            
            # 只保存有效的标注框
            bbox = [class_id, new_x_center, new_y_center, new_box_width, new_box_height]
            new_labels.append(" ".join(map(str, bbox))+'\n')
    return new_labels


'''
输入：图片文件夹，label文件夹，slice+label保存文件夹，unlabel的图片保存文件夹
输出：分割结果+文件结构树
'''
def slice_by_area_direct_need(source_folder,source_label_folder,
                              dst_labeled_folder,dst_unlabel_folder,
                              crop_x,crop_y,
                              radio_area_need,
                              ckbox_direction_need):
    # sep = os.sep
    
    # path_images = osj(source_folder,'*.jpg')
    # path_labels = osj(source_label_folder,'*.txt')
    
    if os.path.exists(dst_labeled_folder):
        shutil.rmtree(dst_labeled_folder)
    os.makedirs(dst_labeled_folder,exist_ok=True)
    print('dst_unlabel_folder',dst_unlabel_folder)
    if dst_unlabel_folder!='':
        if os.path.exists(dst_unlabel_folder):
            shutil.rmtree(dst_unlabel_folder)
        os.makedirs(dst_unlabel_folder,exist_ok=True)
    
    # glob(path_images)
    # glob(path_labels)
    names = []
    for n in os.listdir(source_folder):
        n_split = n.split('.')
        if len(n_split)>1:
            if n_split[-1] in ['jpg','jpeg','png','bmp']:
                names.append(n)

    need_top,need_bottom,need_left,need_right = update_direction_need(ckbox_direction_need)
    need_all,need_content,need_surround = update_area_need(radio_area_need)
    
    save_count_labeled,save_count_unlabeled = 0,0
    count = 0
    for name in tqdm(names):
        n,ext = name.split('.')
        base_name = n
        name_label = n+'.txt'
        name_img = f'{n}.{ext}'
        path_label  = os.path.join(source_label_folder,name_label)
        path_img    = os.path.join(source_folder,name_img)

        # 读取图片
        try:
            image = cv2.imread(path_img)
            h, w, _ = image.shape  # 获取图片的高度和宽度
        except Exception as e:
            # cv2 路径不可以有中文
            print(path_img,'  出现错误，检查一下（cv2 路径不可以有中文）')
            print(e)
            return path_img+'  出现错误，检查一下（cv2 路径不可以有中文）'
        
        # 打开label文件读取每一行的标注信息
        with open(path_label, "r") as f:
            labels = f.readlines()
        
        cols = get_n(w,crop_x)
        rows = get_n(h,crop_y)
        overlap_x = get_overlap(crop_x,w,get_n(w,crop_x))
        overlap_y = get_overlap(crop_y,h,get_n(h,crop_y))
        offset_x = (cols-1)*(crop_x - overlap_x)-(w-crop_x) + 1
        offset_y = (rows-1)*(crop_y - overlap_y)-(h-crop_y) + 1
        print(overlap_x,overlap_y,offset_x,offset_y)
        block_id = 1
        for y in range(0, h-crop_y+offset_y, crop_y - overlap_y):
            for x in range(0, w-crop_x+offset_x, crop_x - overlap_x):
                crop_xmin = x
                crop_ymin = y
                crop_xmax = min(x + crop_x, w)
                crop_ymax = min(y + crop_y, h)
                # crop_box = (crop_xmin, crop_ymin, crop_xmax, crop_ymax)
                
                sub_img = image[crop_ymin:crop_ymax, crop_xmin:crop_xmax].copy()
                
                if is_final_need(block_id,rows,cols,
                                 need_top,need_bottom,need_left,need_right,
                                 need_all,need_content,need_surround): # 根据 区域的选择 判断 最终是否需要 ? 
                    new_labels = get_new_labels(labels,w,h,crop_xmax,crop_xmin,crop_ymax,crop_ymin)
                    if len(new_labels)!=0:
                            
                        output_images_dir = dst_labeled_folder
                        output_labels_dir = dst_labeled_folder
                        
                        sub_img_name = f"{base_name}-sub{block_id}.{ext}"
                        sub_img_path = os.path.join(output_images_dir, sub_img_name)
                        cv2.imwrite(sub_img_path, sub_img)
                        
                        # start label
                        sub_label_name = f"{base_name}-sub{block_id}.txt"
                        sub_label_path = os.path.join(output_labels_dir, sub_label_name)
                        # 保存到目标文件 img + label
                        with open(sub_label_path, 'w') as f:
                            f.writelines(new_labels)
                        # end label

                        
                        save_count_labeled += 1
                    else:
                        # unlabel可选，如果路径不存在，就不保存
                        if dst_unlabel_folder!='':
                            output_unlabeled_images_dir = dst_unlabel_folder
                            
                            sub_img_name = f"{base_name}-sub{block_id}.{ext}"
                            sub_img_path = os.path.join(output_unlabeled_images_dir, sub_img_name)
                            cv2.imwrite(sub_img_path, sub_img)
                            
                            save_count_unlabeled += 1
                        # continue
                count += 1
                    
                block_id += 1
    # print('save labeled num',save_count_labeled,'save unlabeled num',save_count_unlabeled,
    #     'total num',count)
    show_info = [f'save labeled num:{save_count_labeled} \n save unlabeled num:{save_count_unlabeled} \n total num {count}']
    show_info.append(get_tree_structure(dst_labeled_folder))
    return '\n'.join(show_info)