# typing、dataclass、异常处理的小练习

# typing
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


def build_greeting(name: str) -> str:
    return f"hello {name}"


print(build_greeting("ellis"))

# 故意演示，Python在运行时不会自动检查输入类型
print(build_greeting(123))


# 异常处理
def str_to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"输入必须是整数，收到：{value!r}") from exc


print(str_to_int("45"))
try:
    print(str_to_int("test"))
except ValueError as exc:
    print(f"转换失败：{exc}")


# dataclass
"""
- 什么时候使用
当创建对象时，对象属性的初始值是固定的，那么就可以使用 dataclass 来创建对象。

- 背后做了什么事情？
1. 自动生成很多东西，比如 __init__ 、 __repr__ 、 __eq__ 方法。

"""


@dataclass
class LLMEngineeringLab:
    name: str
    description: str
    url: str
    start_time: str | None = None
    age: int | None = None
    tags: list[str] = field(default_factory=list)
    tags2: list[str] = field(default_factory=lambda: ["tag1", "tag2"])


lab = LLMEngineeringLab(
    name="LLM-Engineering-Lab",
    description="LLM-Engineering-Lab",
    url="https://github.com/LLM-Engineering-Lab/LLM-Engineering-Lab",
)
lab1 = LLMEngineeringLab(
    name="LLM-Engineering-Lab",
    description="LLM-Engineering-Lab",
    url="https://github.com/LLM-Engineering-Lab/LLM-Engineering-Lab",
)
print(f"lab = {lab}")
print(lab == lab1)


@dataclass
class Student:
    name: str
    target_role: str


student = Student("Ellis", "LLM 应用开发工程师")
print(student)


# pydantic
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    temperature: float = Field(ge=0, le=2)


question = ChatMessage.model_validate(
    {"role": "user", "content": "hello world", "temperature": 0.8}
)
print(question)

try:
    question2 = ChatMessage.model_validate(
        {"role": "ai", "content": "hello world", "temperature": 1}
    )
    print(question2)
except ValidationError as e:
    print(e)
