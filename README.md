# 订货系统Flask实现
## 基本功能

* 登录功能，暂时没有实现注册功能
* 零件信息的查询、添加、删除、修改
* 供应商信息的查询、添加、删除
* 零件的出入库的事务信息的查询
* 零件库存清单的查询、添加、修改、删除
* 订货信息的定时更新和订货报表的定时打印

## 代码实现
前后端是在Leezhonglin大神的flask项目的基础上修改的
[https://github.com/Leezhonglin/learingnote](https://github.com/Leezhonglin/learingnote)

* 前端使用bootstrap美化
* 后端使用Flask框架
* 定时功能使用Flask-APScheduler，详细的可以查看csdn上arnolan博主的博客[https://blog.csdn.net/arnolan/article/details/84936075](https://blog.csdn.net/arnolan/article/details/84936075)
* 数据库使用mysql
* 最后可以简单地使用uwsgi部署到服务器上，详细的可以查看csdn上开心果汁博主的博客[https://blog.csdn.net/u013421629/article/details/84103873](https://blog.csdn.net/u013421629/article/details/84103873)

## 运行代码
1. 导入sql文件，创建**order_sys**数据库
2. 将数据库的信息/utils/functions.py中的app.config['SQLALCHEMY_DATABASE_URI']修改为自己的数据库信息
3. 启动manage.py，访问127.0.0.1:5000/login/index或者127.0.0.1:8090/login/index，初始用户名为admin、密码为admin