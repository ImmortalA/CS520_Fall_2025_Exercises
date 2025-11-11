from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


def load_module_from_path(module_name: str, file_path: Path) -> ModuleType:
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create spec for module {module_name} from {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def load_solution_function(file_path: Path, function_name: str) -> Callable[..., Any]:
    """Load a function named `function_name` from the Python file at `file_path`."""
    module_name = f"candidate_{file_path.stem}"
    module = load_module_from_path(module_name, file_path)
    if not hasattr(module, function_name):
        raise AttributeError(
            f"Function {function_name!r} not found in {file_path}. Available: {dir(module)}"
        )
    func = getattr(module, function_name)
    if not callable(func):
        raise TypeError(f"{function_name!r} in {file_path} is not callable")
    return func



