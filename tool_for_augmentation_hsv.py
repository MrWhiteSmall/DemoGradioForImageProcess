import cv2,shutil
import numpy as np
from PIL import Image
from os.path import join as osj


def adjust_hue_saturation(img, hue_shift, saturation_shift, lightness_shift):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
 
    h, s, v = cv2.split(hsv_img)

    hue_shift = hue_shift//2
    add1 = (h < 100)*(hue_shift)
    add2 = (h > 100)*(180-hue_shift)
    h = h + add1
    h = h - add2
    h = np.clip(h, 0, 180).astype(np.uint8)
 
    # 这里我直接加了奥
    s = cv2.add(s, saturation_shift)
    s = np.clip(s, 0, 255).astype(np.uint8)
 
    v = cv2.add(v, lightness_shift * 5)
    v = np.clip(v, 0, 255).astype(np.uint8)

    adjusted_hsv = cv2.merge([h, s, v])
 
    adjusted_img = cv2.cvtColor(adjusted_hsv, cv2.COLOR_HSV2BGR)
 
    return adjusted_img
def adjust_by_plan(img,plan):
    return adjust_hue_saturation(img,plan[0],plan[1],plan[2])


def hsv_transform_with_yolo(image_path, label_path, 
                            save_image_path, save_label_path,
                            plan,
                            is_final_save=False):
    
    # save_name = f'{n}-plan{plan_name}.{ext}'
    # img_path = osj(origin_dir,img_name)
    # save_img_path = osj(save_path,save_name)
    # label_path = osj(origin_dir,label_name)

    # 读取图片
    image = cv2.imread(image_path)
    adjust_img = adjust_by_plan(image,plan)
    # print(adjust_img[1000:1003,1000:1003,:])
    if is_final_save:
        cv2.imwrite(save_image_path,adjust_img)
        shutil.copy2(label_path,save_label_path)
    else:
        show_img = cv2.cvtColor(adjust_img,cv2.COLOR_BGR2RGB)
        return Image.fromarray(show_img)
