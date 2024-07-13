import re
from abc import ABC, abstractmethod


class AbstractStringCheck(ABC):
    def __init__(self, **kargs):
        self.__next = kargs.get("next")
        assert self.__next is None or isinstance(self.__next, AbstractStringCheck)
        self._type = kargs.get("type")
        regex_arg = kargs.get("regex")
        if isinstance(regex_arg, re.Pattern):
            self._regex_str = str(regex_arg.pattern)
            self._regex = regex_arg
        else:
            self._regex_str = regex_arg
            self._regex = re.compile(self._regex_str) if self._regex_str is not None else None

    def check(self, value: str) -> (bool, str):
        res = self._check(value)
        if res:
            if self.__next:
                return self.__next.check(value)
            return True, ""
        error_msg = f"INVALID ENTRY: '{value}'\n"
        if self._type:
            error_msg += f"Expecting a value of type {self._type}"
            error_msg += f", regex: {self._regex_str}" if self._regex_str else "."
        else:
            assert self._regex_str
            error_msg += f"Expecting a value satisfying the regex: {self._regex_str}"
        return False, error_msg

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next_check):
        self.__next = next_check

    @abstractmethod
    def _check(self, value: str) -> bool:
        pass


class StringCheck(AbstractStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="str", **kargs)

    def _check(self, value: str) -> bool:
        return True


class AbstractGraphicStringCheck(AbstractStringCheck):
    def __init__(self, **kargs):
        super().__init__(**kargs)

    def _check(self, value: str) -> bool:
        value = value.strip()
        return len(value) > 0 and (not self._regex or bool(re.fullmatch(self._regex, value)))


class GraphicStringCheck(AbstractGraphicStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="gstr", **kargs)


class BoolStringCheck(AbstractGraphicStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="bool", regex=r"[tT]rue|[fF]alse", **kargs)


class IntStringCheck(AbstractGraphicStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="int", regex=r"-?\d+", **kargs)

    def _check(self, value: str) -> bool:
        value = value.strip()
        return bool(re.fullmatch(self._regex, value))


class UintStringCheck(AbstractGraphicStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="uint", regex=r"\d+", **kargs)

    def _check(self, value: str) -> bool:
        value = value.strip()
        return bool(re.fullmatch(self._regex, value))


class FloatStringCheck(AbstractGraphicStringCheck):
    def __init__(self, **kargs):
        super().__init__(type="float", regex=r"-?\d+(\.\d+)?", **kargs)

    def _check(self, value: str) -> bool:
        value = value.strip()
        return bool(re.fullmatch(self._regex, value))


class MatchStringCheck(AbstractStringCheck):
    def __init__(self, strip=True, **kargs):
        if "regex" not in kargs:
            raise RuntimeError(f"Named argument 'regex' is expected to init a RegexStringstr_check.")
        super().__init__(**kargs)
        self.__strip = strip

    def _check(self, value: str) -> bool:
        if self.__strip:
            value = value.strip()
        return bool(re.match(self._regex, value))


class FullmatchStringCheck(AbstractStringCheck):
    def __init__(self, strip=True, **kargs):
        if "regex" not in kargs:
            raise RuntimeError(f"Named argument 'regex' is expected to init a RegexStringstr_check.")
        super().__init__(**kargs)
        self.__strip = strip

    def _check(self, value: str) -> bool:
        if self.__strip:
            value = value.strip()
        return bool(re.fullmatch(self._regex, value))
