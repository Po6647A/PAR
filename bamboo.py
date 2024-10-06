from typing import NamedTuple, TypeVar, Generic, Protocol, runtime_checkable, Callable
from abc import ABCMeta, abstractmethod
import bisect
import math

from easing import EasingFunction, LVALUE

S = TypeVar('S', bound='_Interpable')


@runtime_checkable
class _Interpable(Protocol):
    @abstractmethod
    def __add__(self: S, other: S, /) -> S:
        ...

    @abstractmethod
    def __sub__(self: S, other: S, /) -> S:
        ...

    @abstractmethod
    def __mul__(self: S, other: float | int, /) -> S:
        ...


T = TypeVar('T', bound=_Interpable)


class Bamboo(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def __matmul__(self, time: float) -> T:
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...


def equal(a: float, b: float) -> float:
    return math.isclose(a, b)


class Segment(NamedTuple, Generic[T]):
    start: float
    end: float
    start_value: T
    end_value: T


class BrokenBamboo(Bamboo[T]):
    segments: list[Segment[T]]

    def __init__(self) -> None:
        super().__init__()
        self.segments = []

    def cut(self, start: float, end: float, start_value: T, end_value: T) -> None:
        bisect.insort_left(self.segments, Segment(start, end, start_value, end_value), key=lambda s: s.start)

    def __matmul__(self, time: float) -> T:
        right = bisect.bisect_left(self.segments, time, key=lambda s: s.start)
        if right < len(self.segments) and equal(self.segments[right].start, time):
            return self.segments[right].start_value
        seg = self.segments[right - 1]
        t = (time - seg.start) / (seg.end - seg.start)
        return seg.start_value + (seg.end_value - seg.start_value) * t

    def __repr__(self) -> str:
        if self.segments:
            return f'''BrokenBamboo(segments={len(self.segments)})'''
        return 'BrokenBamboo(empty)'

