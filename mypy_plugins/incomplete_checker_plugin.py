from typing import Callable, Type

from mypy.plugin import AnalyzeTypeContext, Plugin
from mypy.types import AnyType, TypeOfAny


def plugin(version: str) -> type[Plugin]:
    return IncompleteCheckerPlugin


class IncompleteCheckerPlugin(Plugin):
    def get_type_analyze_hook(self, fullname: str) -> Callable[[AnalyzeTypeContext], Type] | None:
        if fullname == "_typeshed.Incomplete":
            return self._analyze_incomplete
        return None

    def _analyze_incomplete(self, ctx: AnalyzeTypeContext) -> Type:
        ctx.api.fail("Found Incomplete type - specify concrete type instead", ctx.context)
        return AnyType(TypeOfAny.special_form)
