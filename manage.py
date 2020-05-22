from utils.comment import scheduler
from utils.config import APSchedulerJobConfig
from flask_script import Manager

from utils.functions import create_app

app = create_app()
app.config.update({"SCHEDULER_API_ENABLED": True})
app.config.from_object(APSchedulerJobConfig)  # 导入配置
scheduler.init_app(app)
scheduler.start()

# manage = Manager(app=app)

if __name__ == '__main__':
    # 解决FLASK DEBUG模式定时任务执行两次
    # if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    # scheduler.init_app(app)
    # scheduler.start()
    # manage.run()
    app.run(host='0.0.0.0',port=8090)