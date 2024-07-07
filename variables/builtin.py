import datetime
import os


class BuiltinTemgenVersion:
    def __init__(self, is_eval_context: bool):
        self.__is_eval_context = is_eval_context

    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        from temgen import Temgen
        match format_spec:
            case "":
                return f"Version.parse('{Temgen.VERSION}')" if self.__is_eval_context else str(Temgen.VERSION)
            case "major":
                return str(Temgen.VERSION.major)
            case "minor":
                return str(Temgen.VERSION.minor)
            case "patch":
                return str(Temgen.VERSION.patch)
            case _:
                raise RuntimeError(f"Format spec not handled for $TEMGEN_VERSION: '{format_spec}'.")


class BuiltinDate:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        today = datetime.date.today()
        return f"{today.year}{format_spec}{today.month:02}{format_spec}{today.day:02}"


class BuiltinTime:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        now = datetime.datetime.now()
        return f"{now.hour:02}{format_spec}{now.minute:02}{format_spec}{now.second:02}"


class BuiltinStrftime:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        return datetime.datetime.now().strftime(format_spec)


class BuiltinEnv:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        return os.environ[format_spec]


class BuiltinEval:
    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        res = eval(format_spec)
        return str(res)


class BuiltinJoin:
    def __init__(self, skip_empty: bool = True):
        self.__skip_empty = skip_empty

    def __format__(self, format_spec):
        assert isinstance(format_spec, str)
        args = eval(format_spec)
        binder = args[0]
        if self.__skip_empty:
            res = binder.join(filter(None, args[1:]))
        else:
            res = binder.join(args[1:])
        return res
