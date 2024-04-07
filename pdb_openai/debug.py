import inspect
import pdb
import sys

import openai


def stop(model_name="gpt-4-turbo-preview", api_key=None):
    debugger = Debug(model_name=model_name, api_key=api_key)
    debugger.set_trace(sys._getframe().f_back)


class Debug(pdb.Pdb):
    def __init__(self, *args, **kwargs):
        self.model_name = kwargs.pop("model_name")
        self.api_key = kwargs.pop("api_key")
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
        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                system_message,
                {"role": "user", "content": '\n'.join(self._history)},
                {"role": "user", "content": line},
            ],
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
        self._history.append(f"[openai] {full_output}")

    def do_ask(self, line: str) -> None:
        self._history.append(f"[ask] {line}")
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
        if line.count("?") > 0:
            prompt += "\nExtra debug info:\n\n"
            prompt += "\n\n".join([
                f"{self.curframe_locals=}",
                f"{self.curframe.f_globals=}",
                f"inspect.stack()={format_call_stack(self.stack)}",
            ])
        self.do_ask(prompt)

    def do_gen(self, line: str) -> None:
        self._history.append(f"[gen] {line}")
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


def format_call_stack(stack):
    formatted_stack = []
    for frame, _ in stack:
        frame_info = inspect.getframeinfo(frame, context=3)
        filename = frame_info.filename
        lineno = frame_info.lineno
        function = frame_info.function
        lines = frame_info.code_context
        formatted_stack.append(f"{filename}:{lineno} - {function}")
        for line in lines:
            formatted_stack.append(line)
    return "".join(formatted_stack)


if __name__ == "__main__":
    stop()
