from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# 初始化db
db = SQLAlchemy()


class Users(db.Model):
    # 用户表
    # 定义表名
    __tablename__ = 'cyc_users'
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(6))
    password = db.Column(db.String(16))

    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()


class Store(db.Model):
    # 库存清单
    # 定义表名
    __tablename__ = 'cyc_store_list'
    store_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    store_num = db.Column(db.Integer)
    store_cv = db.Column(db.Integer)
    store_max = db.Column(db.Integer)

    # 定义外键
    part_id = db.Column(db.Integer, db.ForeignKey('cyc_part.part_id'))
    part = db.relationship('Part', backref='part')

    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()


class Part(db.Model):
    # 零件信息
    # 定义表名
    __tablename__ = 'cyc_part'
    part_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    part_name = db.Column(db.String(16), unique=True)
    part_price = db.Column(db.Float)
    # 设置与供应商一对二的关系
    # 主要供应商
    p_supplier_id = db.Column(db.Integer, db.ForeignKey('cyc_supplier.supplier_id'))
    p_supplier = db.relationship('Supplier', backref='p_supplier', foreign_keys=p_supplier_id)
    # 次要供应商
    s_supplier_id = db.Column(db.Integer, db.ForeignKey('cyc_supplier.supplier_id'))
    s_supplier = db.relationship('Supplier', backref='s_supplier', foreign_keys=s_supplier_id)

    # 定义与库存清单的relationship
    store = db.relationship(Store, backref='store')

    order = db.relationship('Order', backref='order')

    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()


class Supplier(db.Model):
    # 供应商信息
    # 定义表名
    __tablename__ = 'cyc_supplier'
    supplier_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    supplier_name = db.Column(db.String(16))
    supplier_contact_name = db.Column(db.String(20))
    supplier_contact = db.Column(db.String(11))
    supplier_address = db.Column(db.String(50))

    # 建立零件与供应商的关系
    P_part = db.relationship(Part, backref='p_part', foreign_keys=Part.p_supplier_id)
    S_part = db.relationship(Part, backref='s_part', foreign_keys=Part.s_supplier_id)

    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()


class Affair(db.Model):
    # 事务信息
    # 定义表名
    __tablename__ = 'cyc_affair'
    affair_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    affair_type = db.Column(db.Integer)
    affair_time = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'),
                            server_onupdate=text('CURRENT_TIMESTAMP'))

    affair_num = db.Column(db.Integer)
    part_id = db.Column(db.Integer)
    part_name = db.Column(db.String(16))


    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()


class Order(db.Model):
    # 订货信息
    # 定义表名
    __tablename__ = 'cyc_order'
    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    order_num = db.Column(db.Integer)
    order_time = db.Column(db.TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'),
                            server_onupdate=text('CURRENT_TIMESTAMP'))

    part_id = db.Column(db.Integer, db.ForeignKey('cyc_part.part_id'))
    o_part = db.relationship(Part, backref='o_part')

    # 定义保存数据的方法，方便后面使用
    def save(self):
        db.session.add(self)
        db.session.commit()
