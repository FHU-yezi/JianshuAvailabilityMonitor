from db_config import init_db, RunLog, MonitorLog
from datetime import datetime

"""
日志等级定义：
0：CRITICAL
1：ERROR
2：WARNING
3：INFO
4：DEBUG
"""

try:
    init_db()
except Exception as e:
    print(f"初始化日志数据库失败：{e}")


def AddRunLog(level: int = 3, message: str = "") -> None:
    if not message:  # 不允许创建 message 为空的日志
        raise ValueError("message 不能为空")
    RunLog.create(time=datetime.now(), level=level, message=message)


def AddMonitorLog(monitor_name: str, successed: bool = True,
                  status_code: int = 0, message: str = "") -> None:
    if not message:  # 不允许创建 message 为空的日志
        raise ValueError("message 不能为空")
    try:
        MonitorLog.create(time=datetime.now(), monitor_name=monitor_name, successed=successed, status_code=status_code, message=message)
    except:
        AddRunLog(level=1, message=f"添加监控日志失败：{message}")
