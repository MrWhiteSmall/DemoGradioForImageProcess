import os
import shutil
import gradio as gr

from tool_for_extract import extract_types
from tool_for_extract import preview_image_by_extract,extract_image_truly

from tool_for_file import get_files_for_gr_extract

types = list(extract_types.keys())

# 回调函数：根据选择的提取方式动态更新组件的可见性
def update_visibility(selected_type):
    if selected_type == types[1]:
        init_h,init_s,init_v = extract_types[selected_type]
        h_min,h_max = init_h
        s_min,s_max = init_s
        v_min,v_max = init_v
        return gr.update(visible=True,value=h_min), gr.update(visible=True,value=h_max), \
                gr.update(visible=True,value=s_min), gr.update(visible=True,value=s_max), \
                gr.update(visible=True,value=v_min), gr.update(visible=True,value=v_max), \
                gr.update(visible=False),gr.update(visible=False),
    elif selected_type == types[2]:
        init_gray = extract_types[selected_type][0]
        gray_min,gray_max = init_gray
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
                gr.update(visible=True,value=gray_min),gr.update(visible=True,value=gray_max)
    else:
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
                gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), \
                gr.update(visible=False), gr.update(visible=False)


def gr_extract():
    gr.Markdown("## 图片提取工具")
    
    with gr.Row():
        with gr.Column():
            source_folder = gr.Textbox(label="原文件夹路径", placeholder="请选择包含图片的文件夹路径")
            source_label_folder = gr.Textbox(label="原文件label路径", placeholder="请选择包含标注文件的文件夹路径")
            dst_save_folder = gr.Textbox(label="extract后的保存路径", placeholder="extract后的保存路径")
        
            btn_load_files = gr.Button('加载图片文件夹')
            radio_file_list = gr.Radio(label='图片文件夹',choices=[],interactive=True)
            
            btn_preview_img = gr.Button('预览图片')
            
            process_info = gr.Textbox('处理结果信息展示',lines=10)
            
            btn_start_extract = gr.Button('开始提取')
            
        with gr.Column():
            radio_extract_type = gr.Radio(label='提取方式',
                                          choices=types,value=types[0])
            with gr.Row():
                # hsv_show = radio_extract_type.value == types[1]
                # gray_show = radio_extract_type.value == types[2]
                with gr.Column():
                    with gr.Row():
                        h_threshold_min = gr.Number(label='H 最小阈值',minimum=0,maximum=255,
                                                    interactive=True,
                                                    visible=False)
                        h_threshold_max = gr.Number(label='H 最大阈值',minimum=0,maximum=255,
                                                    interactive=True,
                                                    visible=False)
                with gr.Column():
                    with gr.Row():
                        s_threshold_min = gr.Number(label='S 最小阈值',minimum=0,maximum=255,
                                                    interactive=True,
                                                    visible=False)
                        s_threshold_max = gr.Number(label='S 最大阈值',minimum=0,maximum=255,
                                                    interactive=True,
                                                    visible=False)
                with gr.Row():
                    v_threshold_min = gr.Number(label='V 最小阈值',minimum=0,maximum=255,
                                                interactive=True,
                                                visible=False)
                    v_threshold_max = gr.Number(label='V 最大阈值',minimum=0,maximum=255,
                                                interactive=True,
                                                visible=False)
            with gr.Row():
                gray_threshold_min = gr.Number(label='Gray 最小阈值',minimum=0,maximum=255,
                                                interactive=True,
                                            visible=False)
                gray_threshold_max = gr.Number(label='Gray 最大阈值',minimum=0,maximum=255,
                                                interactive=True,
                                            visible=False)
            preview_img = gr.Image(label='图片预览',type='pil',interactive=False)
                
        
        radio_extract_type.change(
            fn=update_visibility,
            inputs=radio_extract_type,
            outputs=[h_threshold_min,h_threshold_max, 
                     s_threshold_min, s_threshold_max,
                     v_threshold_min, v_threshold_max,
                     gray_threshold_min,gray_threshold_max]
        )
        
        btn_load_files.click(
            fn=get_files_for_gr_extract,
            inputs=[source_folder],
            outputs=[radio_file_list,process_info],
        )
        btn_preview_img.click(
            fn=preview_image_by_extract,
            inputs=[source_folder,source_label_folder,
                    dst_save_folder,
                    radio_file_list,
                    radio_extract_type,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,
                    gray_threshold_min,gray_threshold_max],
            outputs=[preview_img,process_info],
        )
        btn_start_extract.click(
            fn=extract_image_truly,
            inputs=[source_folder,source_label_folder,
                    dst_save_folder,
                    radio_extract_type,
                    h_threshold_min,h_threshold_max,
                    s_threshold_min,s_threshold_max,
                    v_threshold_min,v_threshold_max,
                    gray_threshold_min,gray_threshold_max],
            outputs=process_info,
        )