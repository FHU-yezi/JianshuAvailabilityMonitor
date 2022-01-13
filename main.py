from ast import Add
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler

import monitors  # 不加这行会导致任务列表为空
from event_handlers import JobExecutedSuccessfully, JobExecutedFailure
from config_service import CreateDefaultConfig, GetConfig
from log_service import AddRunLog
from message_service import SendFeishuMessage
from register import get_registered_funcs_info
from utils import CronToKwargs

AddRunLog(4, "导入模块成功")

scheduler = BackgroundScheduler()

AddRunLog(4, "初始化调度器成功")

funcs_to_schedule = get_registered_funcs_info()

AddRunLog(3, f"已注册的监控任务数量：{len(funcs_to_schedule)}")

AddRunLog(4, "开始添加监控任务")
for task_name, (func, run_cron) in funcs_to_schedule.items():
    scheduler.add_job(func, "cron", **CronToKwargs(run_cron), id=task_name)
    AddRunLog(4, f"添加监控任务：{task_name} 成功，运行 cron 表达式：{run_cron}")

AddRunLog(4, "监控任务添加完成")

AddRunLog(4, "开始注册事件回调")
scheduler.add_listener(JobExecutedSuccessfully, EVENT_JOB_EXECUTED)
scheduler.add_listener(JobExecutedFailure, EVENT_JOB_ERROR)
AddRunLog(4, "事件回调注册完成")

scheduler.start()
AddRunLog(3, "调度器启动成功")
SendFeishuMessage(GetConfig()["message_service"]["app_id"],
                  GetConfig()["message_service"]["app_secret"],
                  GetConfig()["message_service"]["email"],
                  "调度器启动成功")

input()
