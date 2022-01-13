from functools import wraps
from typing import Callable, Dict, List

registered_funcs = {}


def register_task(task_name: str = None, run_cron: str = None) -> Callable:
    """将一个函数注册为监控任务

    Args:
        func (Callable): 监控任务函数
        task_name (str): 监控任务名称, Defaults to None.
        run_cron (str): 监控任务运行的 cron 表达式, Defaults to None.
    """
    if not run_cron:
        raise ValueError("run_cron 不能为空")

    def outer(func: Callable):
        @wraps(func)
        def inner(task_name: str = None, run_cron: str = None):
            if task_name:
                registered_funcs[task_name] = [func, run_cron]
            else:
                registered_funcs[func.__name__] = [func, run_cron]
            return func
        return inner(task_name)
    return outer


def get_registered_funcs_info() -> Dict[str, List]:
    """获取所有注册的监控任务

    Returns:
        Dict[str, Callable]: 所有注册的监控任务
    """
    return registered_funcs
