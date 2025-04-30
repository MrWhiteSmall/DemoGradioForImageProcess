import os
import gradio as gr

import sys
sys.path.insert(0,os.path.dirname( os.path.abspath(__file__) ))

from tool_for_split_to_subdir import move_files_by_class
from tool_for_file import get_files,get_subfolders
from tool_for_augmentation import gr_augmentation_choices,preview_image,save_augm_image
from tool_for_merge import ratio_by_dataset_type,init_dataset_type,change_dataset_type,merge_and_split

from gr_slice import gr_slice
from gr_extract import gr_extract
from gr_show_defect import gr_show_defect
'''
1 分组
2 增强
3 合并

4 slice
5 extract

2024-11-28
6 show全局/局部 缺陷
'''
# 1 分组
def gr_split():
    gr.Markdown("## 图片分类与标注文件分组工具")
    
    with gr.Row():
        source_folder = gr.Textbox(label="原文件夹路径", placeholder="请选择包含图片的文件夹路径")
        source_label_folder = gr.Textbox(label="原文件label路径", placeholder="请选择包含标注文件的文件夹路径")
    with gr.Row():
        target_folder = gr.Textbox(label="目标文件夹路径", placeholder="请选择分类结果存放的文件夹路径")
        organize_btn = gr.Button("开始分类")
    output = gr.Textbox(label="分类结果统计", lines=10, interactive=False)
    


    organize_btn.click(
        move_files_by_class,
        inputs=[source_folder,source_label_folder, target_folder],
        outputs=output
    )
# 2 增强
def gr_augmentation():
    gr.Markdown("## 图片增强与预览工具")

    # 根据
    # 2.0 目标文件夹
    # 2.1 子文件夹 select
    # 2.2 子文件 checkbox (随机选择n个；手动选择n个；全选)
    # 2.3 预览
    # 2.4 新的更新box
    # 2.5 开始增强button
        # 左侧：输入目标文件夹
    with gr.Row():
        with gr.Column():
            folder_path_input = gr.Textbox(label="目标文件夹路径", placeholder="输入目标文件夹路径")
            output = gr.Textbox(label="分类结果统计", lines=10, interactive=False)
            folder_confirm_btn = gr.Button("加载子文件夹")

        # 中间：选择子文件夹
        with gr.Column():
            subfolder_dropdown = gr.Dropdown(
                label="子文件夹", choices=[], interactive=True
            )
            subfolder_confirm_btn = gr.Button("加载文件")
    with gr.Row():
        # 左侧：显示增强选项
        # 左侧：
        with gr.Column():
            # 显示增强选项
            augm_radiolist = gr.Radio(label="增强方法",choices=gr_augmentation_choices,
                                      value=gr_augmentation_choices[0])
            start_augm_btn = gr.Button("开始增强")
            # 选择文件
            files_checklist = gr.CheckboxGroup(label="文件列表", choices=[], interactive=True)
            preview_btn = gr.Button("预览文件")

        '''
        当 interactive=False 时，组件会被禁用，用户无法修改其内容或选择值
        '''
        # 最右侧：显示图片预览
        with gr.Column():
            
            # 显示图片预览
            preview_image_output = gr.Image(label="图片预览", type="pil", interactive=False)
            preview_status = gr.Textbox(label="状态", interactive=False)

    # 逻辑绑定
    folder_confirm_btn.click(
        fn=get_subfolders,
        inputs=[folder_path_input],
        outputs=[subfolder_dropdown, preview_status,output],
    )

    subfolder_confirm_btn.click(
        fn=get_files,
        inputs=[folder_path_input, subfolder_dropdown],
        outputs=[files_checklist, preview_status],
    )

    start_augm_btn.click(
        fn=save_augm_image,
        inputs=[folder_path_input, subfolder_dropdown, files_checklist,augm_radiolist],
        outputs=[files_checklist, preview_status,output],
    )
    preview_btn.click(
        fn=preview_image,
        inputs=[folder_path_input, subfolder_dropdown, files_checklist,augm_radiolist],
        outputs=[preview_image_output, preview_status],
    )

    pass
# 3 合并
def gr_merge():
    gr.Markdown("## 图片按比例合并数据集")

    # 3.0 源文件夹（2.0中的文件夹一致）【内部包含class的分类】
    # 3.1 输出文件夹
    # 3.2 选择det文件夹还是cls文件夹
    # 3.3 根据选择，det:train[images,labels] & val[images,labels]
    #               cls:train[class1,class2...] & test[class1,class2...] & val[...]
    # 3.4 输入比例 det:(2:1) | (3:1) | (3:2) | (4:1) | (4:3) | (5:1) | (5:2) | (5:3) | (5:4)
    #             cls:(2:1:1) | (3:1:1) | (3:2:1) | (4:1:1) | (4:3:2) | (5:1:1) | (5:2:2) | (5:3:2) | (5:4:3)
    # 3.5 开始merge 
    with gr.Row():
        with gr.Column():
            folder_path_input = gr.Textbox(label="目标文件夹路径", placeholder="输入目标文件夹路径")
            folder_path_output = gr.Textbox(label="merge文件夹路径", placeholder="输入merge文件夹路径")
        with gr.Column():
            merge_types = list(ratio_by_dataset_type.keys())
            radio_folder_type = gr.Radio(
                label='merge的文件夹类型(det检测文件夹,cls分类文件夹)',
                choices=merge_types,
                value=merge_types[0],
                interactive=True)
            # radio_ratio = gr.Radio(
            #     label='文件夹train_test比例',
            #     choices=[])
            radio_ratio = init_dataset_type()
            
        radio_folder_type.change(
            fn=change_dataset_type,
            inputs=radio_folder_type,
            outputs=radio_ratio
        )
    with gr.Row():
        preview_status = gr.Textbox(label="合并后的文件结构",lines=10, interactive=False)
    with gr.Row():
        start_merge_btn = gr.Button(value='开始合并数据集')
    
    start_merge_btn.click(
        fn=merge_and_split,
        inputs=[folder_path_input,folder_path_output,
                radio_folder_type,radio_ratio],
        outputs=preview_status,
    )
# 4 slice
# 5 extract
# 6 show全局/局部 缺陷

# 创建Gradio界面
with gr.Blocks() as demo:
    '''
    1 分组
    2 增强
    3 合并

    4 slice
    5 extract
    '''
    # 1 分组
    gr_split()
    # 2 增强
    gr_augmentation()
    # 3 合并
    gr_merge()
    # 4 slice
    gr_slice()
    # 5 extract
    gr_extract()
    # 6 show全局/局部 缺陷
    gr_show_defect()
    demo.launch(share=True)
