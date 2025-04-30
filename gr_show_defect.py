import os
import shutil
import gradio as gr

from tool_for_file import get_files_for_gr_show_defect
from tool_for_show_defect import show_defect_global,show_defect_local

def gr_show_defect():
    gr.Markdown("## 图片缺陷展示工具")
    
    with gr.Row():
        with gr.Column(scale=2):
            source_folder = gr.Textbox(label="原文件夹路径", placeholder="请选择包含图片的文件夹路径")
            source_label_folder = gr.Textbox(label="原文件label路径", placeholder="请选择包含标注文件的文件夹路径")
            
            btn_load_files = gr.Button('加载图片文件')
            radio_file_list = gr.Radio(label='图片列表',choices=[],interactive=True)
            btn_show_global = gr.Button('Try Show [整体]')
            
            preview_info = gr.Textbox(label='处理信息展示',lines=10,interactive=False)
        with gr.Column(scale=3):
            image_defect_global = gr.Image(label='缺陷[整体]图片显示(附带label)', type="pil", interactive=False)
            radio_defect_types = gr.Radio(label='局部缺陷列表',choices=[],interactive=True)
            btn_show_local = gr.Button('Try Show [局部]')
            image_defect_local = gr.Image(label='缺陷[局部]图片显示(附带label)', type="pil", interactive=False)
            
    btn_load_files.click(
        fn=get_files_for_gr_show_defect,
        inputs=source_folder,
        outputs=[radio_file_list,preview_info],
    )
    
    btn_show_global.click(
        fn=show_defect_global,
        inputs=[source_folder,source_label_folder,radio_file_list],
        outputs=[image_defect_global,radio_defect_types,preview_info],
    )
    
    btn_show_local.click(
        fn=show_defect_local,
        inputs=radio_defect_types,
        outputs=image_defect_local,
    )