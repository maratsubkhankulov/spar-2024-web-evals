from dataclasses import dataclass

import gradio


@dataclass
class ResultTab:
    tab: gradio.Tab
    text_tab: gradio.Tab
    text_md: gradio.Markdown
    vim_tab: gradio.Tab
    vim_code: gradio.Code

    def items(self):
        return [self.tab, self.text_tab, self.text_md, self.vim_tab, self.vim_code]
