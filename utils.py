from typing import Dict


def CronToKwargs(cron: str) -> Dict[str, str]:
    second, minute, hour, day, month, day_of_week = cron.split()
    result = {"second": second, "minute": minute, "hour": hour, "day": day, "month": month, "day_of_week": day_of_week}
    return result
