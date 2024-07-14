import glob
import os.path
import shutil
import traceback
from typing import List

import gradio as gr
from omegaconf import OmegaConf

import app
from src.containers import LLMContainer
from src.controller import pipe
from src.core.errors import NotFoundInSource
from src.ui.Models import ResultTab

SRC_PATH = '/app/data/document_store'
CONFIGS_PATH = '/app/data/strategies'

ResultTabs: List[ResultTab] = []


def get_result_tab_items():
    items = []
    for tab in ResultTabs:
        items.extend(tab.items())
    return items


def get_src_files():
    files = glob.glob(pathname=f'{SRC_PATH}/*.*')
    files = [x for x in files if os.path.isfile(x)]
    return files


def get_configs():
    files = glob.glob(pathname=f'*.yml', root_dir=CONFIGS_PATH)
    files = [x[:-4] for x in files]
    return files


def update_config_choises():
    choices = get_configs()
    return gr.update(choices=choices)


def config_select(config):
    with open(CONFIGS_PATH + f'/{config}.yml', 'r') as f:
        return f.read()


def get_src_names():
    return [x.split('/')[-1] for x in get_src_files()]


def update_src_choices():
    choices = get_src_names()
    return gr.update(choices=choices)


def upload_src(path):
    print(path)
    file_name = path.split('/')[-1]
    dst = SRC_PATH + '/' + file_name
    shutil.copy(path, dst)
    return get_src_files(), update_src_choices()


def render_result_tabs(n: int = 10):
    ResultTabs.clear()
    for i in range(n):
        with gr.Tab(f"Слайд {i}", visible=False) as tab:
            with gr.Tab('Текст') as text_tab:
                text = gr.Markdown('')
            with gr.Tab('vim') as vim_tab:
                vim = gr.Code(language='html', interactive=True)
        ResultTabs.append(
            ResultTab(tab=tab,
                      text_tab=text_tab,
                      vim_tab=vim_tab,
                      text_md=text,
                      vim_code=vim)
        )


async def generate_lesson(title: str, sources: List[str], config: str):
    config_path = f"{CONFIGS_PATH}/{config}.yml"
    returned = {}
    lesson = None
    try:
        lesson = await app.generate_lesson(title, sources, config_path)
        returned[generate_error] = gr.update(value='')
    except NotFoundInSource as e:
        returned[generate_error] = gr.update(value=e.info)
    except:
        error = traceback.format_exc()
        error = error.replace("\n", "<br/>")
        returned[generate_error] = gr.update(value=error)

    for i, tab in enumerate(ResultTabs):
        if i == 0:
            if lesson and lesson.plan:
                returned[tab.tab] = gr.update(visible=True, label='План')
                returned[tab.text_tab] = gr.update(visible=True)
                returned[tab.vim_tab] = gr.update(visible=False)
                returned[tab.text_md] = gr.update(value=lesson.plan)
            else:
                returned[tab.tab] = gr.update(visible=False, label='')
        else:
            if lesson and len(lesson.problems) >= i:
                problem = lesson.problems[i - 1]
                returned[tab.tab] = gr.update(visible=True)
                returned[tab.text_tab] = gr.update(visible=bool(problem.lines))
                returned[tab.vim_tab] = gr.update(visible=bool(problem.vim_lines))
                returned[tab.text_md] = gr.update(value=problem.lines)
                returned[tab.vim_code] = gr.update(value=problem.vim_lines)
            else:
                returned[tab.tab] = gr.update(visible=False, label='')
    return returned


with gr.Blocks() as demo:
    gr.Markdown('# Генерация уроков')
    with gr.Tab('Генерация'):
        with gr.Row():
            source = gr.Checkboxgroup(choices=get_src_names(), label='Источники', interactive=True)
            config = gr.Dropdown(label='Конфигурация', choices=get_configs())
            title = gr.Textbox(label='Тема')

            demo.load(update_src_choices, outputs=source)
            demo.load(update_config_choises, outputs=config)
        with gr.Row():
            generate_btn = gr.Button('Генерировать')
        with gr.Row():
            result_title = gr.Markdown('# Результат')
        with gr.Row():
            generate_error = gr.Markdown('', line_breaks=True)
        with gr.Row():
            render_result_tabs(10)
            generate_btn.click(generate_lesson, inputs=[title, source, config],
                               outputs=[*get_result_tab_items(), result_title, generate_error])
            title.submit(generate_lesson, inputs=[title, source, config],
                         outputs=[*get_result_tab_items(), result_title, generate_error])
    with gr.Tab('Источники'):
        with gr.Row():
            with gr.Column():
                src_files = gr.File(value=get_src_files, interactive=False)
                delete_src_btn = gr.Button(value='Удалить', visible=False)
                delete_src_btn.click(lambda x: print(x), inputs=[src_files])
            with gr.Column():
                src_upload_file = gr.File(label='Загрузить новый', file_count='single')
                src_upload_btn = gr.Button(value='Загрузить')
                src_upload_btn.click(upload_src, inputs=[src_upload_file], outputs=[src_files, source])
    with gr.Tab('Конфигурации'):
        def config_copy(config: str):
            new_name = f"{config}-копия"
            src = f"{CONFIGS_PATH}/{config}.yml"
            dst = f"{CONFIGS_PATH}/{new_name}.yml"
            shutil.copy(src, dst)
            return gr.update(value=new_name, choices=get_configs())


        def config_save(config: str, new_name: str, code: str):
            src = f"{CONFIGS_PATH}/{config}.yml"
            dst = f"{CONFIGS_PATH}/{new_name}.yml"
            if (src != dst) and os.path.exists(dst):
                raise gr.Error(f'Конфигурация {new_name} уже существует')
            os.remove(src)
            with open(dst, 'w') as f:
                f.write(code)
            return gr.update(value=new_name, choices=get_configs())


        with gr.Row():
            config_dd = gr.Dropdown(label='Конфигурация', choices=get_configs())
            config_update_btn = gr.Button('Обновить')
            config_copy_btn = gr.Button('Дублировать')

        with gr.Row():
            config_code = gr.Code(language='yaml', interactive=True)
        with gr.Row():
            with gr.Column():
                ...
            with gr.Column():
                with gr.Row():
                    new_config_name = gr.Textbox(label='Сохранить как', interactive=True)
                    config_save_btn = gr.Button('Сохранить')

        config_dd.change(config_select, inputs=config_dd, outputs=config_code)
        config_dd.change(lambda x: x, inputs=config_dd, outputs=new_config_name)
        demo.load(update_config_choises, outputs=config_dd)
        config_update_btn.click(update_config_choises, outputs=config_dd)
        config_copy_btn.click(config_copy, inputs=config_dd, outputs=config_dd)
        config_save_btn.click(config_save, inputs=[config_dd, new_config_name, config_code], outputs=config_dd)

if __name__ == '__main__':
    cfg = OmegaConf.load('config/config.yml')
    container = LLMContainer()
    container.config.from_dict(cfg)
    container.wire([app, pipe])

    demo.launch(debug=True,
                server_port=80,
                server_name='0.0.0.0'
                )
