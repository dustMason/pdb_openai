import inspect
import pdb
import sys

import openai


def get_default_debugger_config():
    return {
        'model_name': "gpt-4-turbo-preview",
        'api_key': None,
        'debug_prompts': False
    }


def set_trace(**kwargs):
    config = get_default_debugger_config()
    config.update(kwargs)
    debugger = Debug(**config)
    debugger.set_trace(sys._getframe().f_back)


def post_mortem(t=None, wtf=False, **kwargs):
    t = t or sys.exc_info()[2]
    if not t:
        raise ValueError("A valid traceback must be passed if no exception is being handled")
    config = get_default_debugger_config()
    config.update(kwargs)
    debugger = Debug(**config)
    debugger.reset()
    if wtf:
        def preloop():
            debugger.do_wtf("??")

        debugger.preloop = preloop
    debugger.interaction(None, t)


def pm():
    post_mortem(sys.last_traceback)


class Debug(pdb.Pdb):
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs.pop("model_name")
        self.api_key = kwargs.pop("api_key")
        self.debug_prompts = kwargs.pop("debug_prompts")
        super(Debug, self).__init__(*args, **kwargs)
        self.prompt = "(Pdb OpenAI) "
        self._history: list[str] = []

    def message(self, msg: str) -> None:
        self._history.append(str(msg))
        super(Debug, self).message(msg)

    def default(self, line: str) -> None:
        self._history.append(f"(Pdb) {line}")
        super(Debug, self).default(line)

    def error(self, msg: str) -> None:
        self._history.append(f"*** {msg}")
        super(Debug, self).error(msg)

    def _sample(self, line: str, system_message: dict[str, str]):
        client = openai.OpenAI(api_key=self.api_key)
        messages = [
            system_message,
            {"role": "user", "content": '\n'.join(self._history[:-1])},
            {"role": "user", "content": line},
        ]
        if self.debug_prompts:
            for m in messages:
                print(f"----- {m['role']} message -----")
                print(m['content'], "\n")
        response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=2000,
            stream=True,
        )
        full_output = ""
        for chunk in response:
            if chunk.choices:
                c = chunk.choices[0].delta.content
                if c:
                    yield c
                    full_output += c
        self._history.append(f"[{self.model_name} output] {full_output}")

    def do_ask(self, line: str) -> None:
        self._history.append(f"(Pdb) [{self.model_name} prompt] {line}")
        sys_message = {
            "role": "system",
            "content": """
            You are a python debugging assistant, running in a pdb session.
            Be concise and tailor your answers for a staff level engineer.
            You may use markdown.
            """
        }
        for sample in self._sample(line, sys_message):
            print(sample, end="")
        print()

    def do_wtf(self, line: str) -> None:
        prompt = "Explain how the program arrived at this state, including the cause of any errors. Be concise."
        wtfs = line.count("?")
        if wtfs > 0:
            prompt += "\nExtra debug info:\n\n"
            prompt += "\n\n".join([
                f"{self.curframe_locals=}",
                f"{self.curframe.f_globals=}",
                f"call stack:\n{format_call_stack(self.stack, 2 + wtfs)}",
            ])
        self.do_ask(prompt)

    def do_gen(self, line: str) -> None:
        self._history.append(f"(Pdb) [{self.model_name} prompt] {line}")
        sys_message = {
            "role": "system",
            "content": """
            You are a python debugging assistant, running in a pdb session.
            Respond ONLY in python source code. Do not use markdown.
            """
        }
        full_response = ""
        for sample in self._sample(line, sys_message):
            full_response += sample
            print(sample, end="")
        print()
        print("\nRun it? y/n")
        if input().strip() == "y":
            code = trim_markdown(full_response)
            locals = self.curframe_locals
            ns = self.curframe.f_globals.copy()
            ns.update(locals)
            try:
                exec(code, ns, locals)
            except BaseException:
                self._error_exc()


def trim_markdown(inp: str) -> str:
    return inp.strip().rstrip().removeprefix("```python").removeprefix("```").removesuffix("```")


def format_call_stack(stack, context=3):
    formatted_stack = []
    for frame, _ in stack:
        frame_info = inspect.getframeinfo(frame, context=context)
        filename = frame_info.filename
        lineno = frame_info.lineno
        function = frame_info.function
        lines = frame_info.code_context
        ind = frame_info.index
        formatted_stack.append(f"File \"{filename}\", line {lineno}, in {function}\n")
        for i, line in enumerate(lines):
            m = "=>" if ind == i else "  "
            formatted_stack.append(f"{m} {lineno - ind + i} {line}")
    return "".join(formatted_stack)


if __name__ == "__main__":
    set_trace(debug_prompts=True)
