from langchain import hub

creation_prompt = """

[BEGIN DATA]
***
[Task description]: {description}
***
[END DATA]

{task}
"""

scorers_header_task = """
Write a header with identity for the AI agent, 
who will be able to evaluate the completion and quality of the task. 
As the first approximation you can descibe someone who published the task and describe him in 4-5 dentences.

The header: You are"""

scorers_instruction_task = """
Create guidelines for evaluating the task in 1-3 sentences and present the template for making the reward value.
The template has to consist in the line "Final Reward Value: (percentage)" For example, "Final Reward Value: 48%" or "Final Reward Value: (97%)".
It could be some thoughts or hints about the money reward for the target executor or something else.

Answer: 
"""

solvers_instruction = """
You are an agent designed to answer on the questions. 
You have access to write and execute code or use terminal commands for answering.
You have access to a python REPL, which you can use to execute python code and have access to terminal to utilize for the purposes.
If you get an error, debug your code or console output and try again.
You can answer with code but the terminate answer of the chain of thoughts has to be plain answer. 
You might know the answer without running any code to answer the question or to fulfill the task.
You have to perform the task in a way that you available.
"""

solvers_alignment="""
Rewrite the instrunction for a prompt to answer the question or to fulfill the task.
Write only proper and convenient description for the agent. The toold are only auxillary and the task could be fulfulled without them.
[Task]: {input}

[Instruction]: {instructions}

[Rewrited Instruction]: 
"""

solvers_alignment_task = solvers_alignment.replace("{input}", "{{input}}").format(instructions=solvers_instruction)

base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=solvers_instruction)