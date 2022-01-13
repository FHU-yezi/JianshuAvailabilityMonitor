from peewee import (BooleanField, CharField, DateTimeField, IntegerField,
                    Model, SqliteDatabase)


class RunLog(Model):
    id = IntegerField(primary_key=True)
    time = DateTimeField()
    level = IntegerField()
    message = CharField()

    class Meta:
        database = SqliteDatabase('run_log.db')


class MonitorLog(Model):
    id = IntegerField(primary_key=True)
    time = DateTimeField()
    monitor_name = CharField()
    successed = BooleanField()
    status_code = IntegerField()
    message = CharField()

    class Meta:
        database = SqliteDatabase('monitor_log.db')


def init_db() -> None:
    """初始化数据库"""
    RunLog.create_table()
    MonitorLog.create_table()
