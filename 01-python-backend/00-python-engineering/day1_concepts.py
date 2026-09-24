# typing、dataclass、异常处理的小练习

# typing
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel


def build_greeting(name: str) -> str:
    return f"hello {name}"


print(build_greeting("world"))

print(build_greeting(123))


# 异常处理
def str_to_int(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        print(f"输入错误{value}")
        return 0


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
print(f"lab = {lab}")

# class 私有属性
"""
在 python 的类中，只有公共属性和方法、私有属性和方法。 没有 protected 属性。 
私有属性：使用  _变量名 形式。 仅在类内部和子类内部访问。

继承：
私有属性和私有方法无法被继承

"""


class Girl:
    def __init__(self, name) -> None:

        self.__name__ = name
        # 私有属性：使用  __变量名 形式。 只能在类内部访问，实例对象无法访问。
        self.__age = 18

    def get_age(self):
        # 通过函数获取私有属性的好处是，可以在函数中做权限控制
        return self.__age


girl = Girl("小花")
print(girl.__name__)

try:
    print(girl.__age)  # 会报错
except AttributeError as e:
    # raise AttributeError("无法在类外部获取私有属性") from e
    print(e)

print(girl.get_age())


# 父类
class Animal:
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def get_age(self):
        return self.age


# 子类
class Dog(Animal):
    def __init__(self, name, age) -> None:
        super().__init__(name, age)


print(Dog.__mro__)
dog = Dog("小花狗", 2)
print(dog.name)
print(dog.get_age())


## 多继承
"""
1. 就近原则


class A:
    def __init__(self) -> None:
        pass


class B:
    def __init__(self) -> None:
        pass


class C(A, B):
    def __init__(self) -> None:
        super().__init__()
        pass
"""


# pydantic
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    temperature: float


question = ChatMessage.model_validate(
    {"role": "user", "content": "hello world", "temperature": 0.8}
)
print(question)
