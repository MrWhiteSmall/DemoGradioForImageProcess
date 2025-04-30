import os
import shutil
import gradio as gr

from tool_for_slice import area_needs,direction_needs
from tool_for_slice import slice_by_area_direct_need

def gr_slice():
    gr.Markdown("## 图片切片工具")
    
    with gr.Row():
        with gr.Column():
            source_folder = gr.Textbox(label="原文件夹路径", placeholder="请选择包含图片的文件夹路径")
            source_label_folder = gr.Textbox(label="原文件label路径", placeholder="请选择包含标注文件的文件夹路径")
        
            # 保存 image + label
            dst_labeled_folder = gr.Textbox(label="有label的slice+标注路径", placeholder="请选择待保存的文件夹路径")
            # only保存 image
            dst_unlabel_folder = gr.Textbox(label="无label的slice图片路径(可选)", placeholder="请选择待保存的文件夹路径")
        with gr.Column():
            with gr.Row():
                crop_x = gr.Number(label='切片宽度',minimum=32,maximum=4096)
                crop_y = gr.Number(label='切片高度',minimum=32,maximum=4096)
            radio_area_need = gr.Radio(label='slice分割的区域',
                                       choices=area_needs,value=area_needs[0])
            ckbox_direction_need = gr.CheckboxGroup(label='slice切片方向选择',
                                                    choices=direction_needs,value=direction_needs)
            gr.Textbox('==slice切片方向越多，限制越多==',label='注')
    with gr.Row():
        btn_start_slice = gr.Button(value='开始切片')
    
    with gr.Row():
        preview_slice_res = gr.Textbox(label='slice结果展示(文件结构)',lines=10)
        
    btn_start_slice.click(
        fn=slice_by_area_direct_need,
        inputs=[source_folder,source_label_folder,
                dst_labeled_folder,dst_unlabel_folder,
                crop_x,crop_y,
                radio_area_need,
                ckbox_direction_need],
        outputs=preview_slice_res,
    )
        