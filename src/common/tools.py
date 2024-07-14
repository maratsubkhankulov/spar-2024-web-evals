import re

from langchain_community.tools import ShellTool
from langchain_experimental.tools import PythonREPLTool

from inspect_ai.scorer import Score


async def ask(model, template, kwargs):
    return await model.generate(template.format(**kwargs))

shell_tool = ShellTool()
shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")

tools = [PythonREPLTool(), shell_tool]


def extract_grade(result, metadata):
    # extract the grade
    match = re.search(r'Final Reward Value:\s*\(?(\d+)\)?', result.completion)
    if match:
        return Score(
            value=int(match.group(1)),
            answer=match.group(0),
            explanation=result.completion,
            metadata=metadata,
        )
    else:
        return Score(
            value=0,
            explanation="Grade not found in model output: "
                        + f"{result.completion}",
        )