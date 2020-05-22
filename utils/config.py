from utils.util import generate_order, update_store


class APSchedulerJobConfig(object):
    JOBS = [
        {
            "id": "update_store",  # 任务ID
            "func": update_store,  # 任务位置
            # "trigger": "cron",  # 触发器
            # "day_of_week": '0-6',
            # "hour": '7-16'
            "trigger": "interval",  # 触发器
            "seconds": 600
        }, {
            "id": "generate_order",  # 任务ID
            "func": generate_order,  # 任务位置
            # "trigger": "cron",  # 触发器
            # "day_of_week":'0-6',
            # "hour":16,
            # "minute":30
            "trigger": "interval",  # 触发器
            "seconds": 1200
        }
    ]
