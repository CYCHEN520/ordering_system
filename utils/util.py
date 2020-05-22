import uuid
import xlwt
import time, datetime
from app.models import db, Order, Store, Affair
from utils.comment import scheduler


def Create_id():
    u_id = str(uuid.uuid1())
    id = u_id.replace('-', '')
    return id


def get_page(request, database, id):
    # 查询第几页的数据
    page = int(request.args.get('page', 1))
    # 谷歌每页的条数是多少,默认为9条
    # page_num = int(request.args.get('page_num', 9))
    # IE每页的条数是多少,默认为7条
    page_num = int(request.args.get('page_num', 7))
    # 查询当前第几个的多少条数据
    paginate = database.query.order_by(id).paginate(page, page_num)
    # 获取某也的具体数据
    database = paginate.items

    return database, paginate


# 定时生成订货报表
def generate_order():
    # 生成workbook
    workbook = xlwt.Workbook(encoding='utf-8')
    # 生成worksheet
    worksheet = workbook.add_sheet('订货报表')

    # 添加数据的列说明
    # 写入数据序号、零件ID、零件名称、主要供应商信息、次要供应商信息、采购数量
    order_data_head = ['序号', '订货编号', '零件编号', '零件名称', '供应商编号(主)',
                       '名称', '联系人名称', '联系方式', '地址', '供应商编号(次)',
                       '名称', '联系人名称', '联系方式', '地址', '零件单价(元)',
                       '采购数量(件)', '采购总金额(元)']

    # 写入标题'零件订货报表'
    # 设置样式
    head_style = xlwt.XFStyle()
    # 添加字体
    head_font = xlwt.Font()
    head_font.name = '宋体'
    # 20为衡量单位，16位字号
    head_font.height = 20 * 18
    head_style.font = head_font
    # 设置对齐方式
    head_alignment = xlwt.Alignment()
    head_alignment.horz = xlwt.Alignment.HORZ_CENTER
    head_alignment.vert = xlwt.Alignment.VERT_CENTER
    head_style.alignment = head_alignment
    # 设置边框
    head_borders = xlwt.Borders()
    head_borders.left, head_borders.right, head_borders.top, head_borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
    head_style.borders = head_borders
    # 写入'零件订货报表'
    worksheet.write_merge(0, 3, 0, len(order_data_head) - 1, '零件订货报表', head_style)

    # 写入生成时间
    # 设置样式
    time_style = xlwt.XFStyle()
    # 添加字体
    time_font = xlwt.Font()
    time_font.name = '宋体'
    # 20为衡量单位，16位字号
    time_font.height = 20 * 12
    time_style.font = time_font
    # 设置对齐方式
    time_alignment = xlwt.Alignment()
    time_alignment.horz = xlwt.Alignment.HORZ_LEFT
    time_alignment.vert = xlwt.Alignment.VERT_CENTER
    time_style.alignment = time_alignment
    # 设置边框
    time_borders = xlwt.Borders()
    time_borders.left, time_borders.right, time_borders.top, time_borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
    time_style.borders = time_borders
    # 写入时间
    strtime_ = time.strftime("%Y-%m-%d")
    time_ = '报表生成时间：' + strtime_
    worksheet.write_merge(4, 4, 0, len(order_data_head) - 1, time_, time_style)

    # 初始化数据的样式
    data_head_style = xlwt.XFStyle()
    # 添加字体
    data_head_font = xlwt.Font()
    data_head_font.name = '宋体'
    # 20为衡量单位，12位字号
    data_head_font.height = 20 * 10
    data_head_style.font = data_head_font
    # 设置对齐方式
    data_head_alignment = xlwt.Alignment()
    data_head_alignment.horz = xlwt.Alignment.HORZ_CENTER
    data_head_alignment.vert = xlwt.Alignment.VERT_CENTER
    data_head_style.alignment = data_head_alignment
    # 设置边框
    data_head_borders = xlwt.Borders()
    data_head_borders.left, data_head_borders.right, data_head_borders.top, data_head_borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
    data_head_style.borders = data_head_borders
    # 循环写入
    for idx, i in enumerate(order_data_head):
        # 设置单元格宽度
        worksheet.col(idx).width = 3333
        worksheet.write(5, idx, i, data_head_style)

    worksheet.col(0).width = 1111

    # 写入数据
    # 设置字体
    data_style = xlwt.XFStyle()
    data_font = xlwt.Font()
    data_font.name = '宋体'
    # 20为衡量单位，12位字号
    data_font.height = 20 * 10
    data_style.font = data_font
    # 设置对齐方式
    data_alignment = xlwt.Alignment()
    data_alignment.horz = xlwt.Alignment.HORZ_LEFT
    data_alignment.vert = xlwt.Alignment.VERT_CENTER
    data_style.alignment = data_alignment
    # 设置边框
    data_borders = xlwt.Borders()
    data_borders.left, data_borders.right, data_borders.top, data_borders.bottom = xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN, xlwt.Borders.THIN
    data_style.borders = data_borders
    # 循环写入数据
    with scheduler.app.app_context():
        orders = db.session.query(Order).filter_by(order_status=0).order_by('order_id').all()
        for order_idx, i in enumerate(orders):
            if i.o_part != None and i.o_part.p_supplier != None:
                worksheet.write(6 + order_idx, 0, order_idx + 1, data_style)
                order_id_ = str(i.order_id)
                order_id = order_id_.zfill(8)
                worksheet.write(6 + order_idx, 1, order_id, data_style)
                part_id_ = str(i.part_id)
                part_id = part_id_.zfill(8)
                worksheet.write(6 + order_idx, 2, part_id, data_style)
                worksheet.write(6 + order_idx, 3, i.o_part.part_name, data_style)
                p_supper_id_ = str(i.o_part.p_supplier_id)
                p_supper_id = p_supper_id_.zfill(8)
                worksheet.write(6 + order_idx, 4, p_supper_id, data_style)
                worksheet.write(6 + order_idx, 5, i.o_part.p_supplier.supplier_contact_name, data_style)
                worksheet.write(6 + order_idx, 6, i.o_part.p_supplier.supplier_name, data_style)
                worksheet.write(6 + order_idx, 7, i.o_part.p_supplier.supplier_contact, data_style)
                worksheet.write(6 + order_idx, 8, i.o_part.p_supplier.supplier_address, data_style)
                if i.o_part.s_supplier != None:
                    s_supper_id_ = str(i.o_part.s_supplier_id)
                    s_supper_id = s_supper_id_.zfill(8)
                    worksheet.write(6 + order_idx, 9, s_supper_id, data_style)
                    worksheet.write(6 + order_idx, 10, i.o_part.s_supplier.supplier_contact_name, data_style)
                    worksheet.write(6 + order_idx, 11, i.o_part.s_supplier.supplier_name, data_style)
                    worksheet.write(6 + order_idx, 12, i.o_part.s_supplier.supplier_contact, data_style)
                    worksheet.write(6 + order_idx, 13, i.o_part.s_supplier.supplier_address, data_style)
                else:
                    worksheet.write(6 + order_idx, 9, '/', data_style)
                    worksheet.write(6 + order_idx, 10, '/', data_style)
                    worksheet.write(6 + order_idx, 11, '/', data_style)
                    worksheet.write(6 + order_idx, 12, '/', data_style)
                    worksheet.write(6 + order_idx, 13, '/', data_style)
                worksheet.write(6 + order_idx, 14, i.o_part.part_price, data_style)
                worksheet.write(6 + order_idx, 15, i.order_num, data_style)
                worksheet.write(6 + order_idx, 16, (i.order_num * i.o_part.part_price), data_style)
                # 修改订货信息状态
                i.order_status = 1
        db.session.commit()

    # 写入采购人签名

    # 保存表格
    xls_dir = 'static/order_folder/订货报表' + strtime_ + '.xls'
    workbook.save(xls_dir)
    print('订货报表已经生成')


def update_store():
    # 每一个小时根据事务更新一次库存清单，暂定从早上7点到下午4点
    # 如果库存小于库存临界值，则更新订货报表
    with scheduler.app.app_context():
        # 处理事务
        # 获取按照时间排序未处理的事务
        affairs = db.session.query(Affair).filter_by(affair_status=0).order_by('affair_commit_time').all()
        for affair in affairs:
            store = db.session.query(Store).filter_by(part_id=affair.part_id).first()
            if store != None:
                # 如果是出库，且可以出库
                if affair.affair_type == 0 and affair.affair_num <= store.store_num:
                    store.store_num = store.store_num - affair.affair_num
                    # 修改事务信息
                    affair.affair_status = 1
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    curr_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    affair.affair_finish_time = curr_time
                    db.session.commit()
                # 如果是入库，且可以入库
                elif affair.affair_type == 1 and affair.affair_num + store.store_num <= store.store_max:
                    # 修改事务信息
                    store.store_num = store.store_num + affair.affair_num
                    affair.affair_status = 1
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    curr_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                    affair.affair_finish_time = curr_time
                    if affair.order_id != None:
                        # 如果有订单信息，则同时更新订单信息
                        order = Order.query.filter_by(order_id=affair.order_id).first()
                        order.purchased_num = min((order.purchased_num + affair.affair_num), order.order_num)
                        # o_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        # o_curr_time = datetime.datetime.strptime(o_time_str, '%Y-%m-%d %H:%M:%S')
                        order.order_time = curr_time
                    db.session.commit()
                # 其他情况
                else:
                    pass
            else:
                pass

        stores_list = db.session.query(Store).order_by('store_id').all()
        for i in stores_list:
            # 如果库存清单的值小于临界值
            if i.store_num < i.store_cv:
                # 产生订货信息，如果订货信息已经存在，则更新订货数量
                # 已经产生了订货报表的，且已经购买的数量小于订货数量的
                order_writed = db.session.query(Order).filter(Order.part_id == i.part_id, Order.order_status == 1,
                                                              Order.purchased_num < Order.order_num).all()
                # 计算新的订单需要购买的数量
                pre_order_num = 0
                pre_purchased_num = 0
                # need_order_num = 0
                for j in order_writed:
                    pre_order_num = pre_order_num + j.order_num
                    pre_purchased_num = pre_purchased_num + j.purchased_num

                need_order_num = i.store_max - i.store_num - (pre_order_num - pre_purchased_num)
                if need_order_num > 0:
                    order = db.session.query(Order).filter_by(part_id=i.part_id, order_status=0).first()
                    if order != None:
                        # 如果已经产生未写入的订货报表，则更新订货数量
                        order.order_num = need_order_num
                        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        curr_time = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                        order.order_time = curr_time
                        db.session.commit()
                    else:
                        # 否则，就创建新的订货信息
                        order_new = Order(order_num=need_order_num, purchased_num=0, part_id=i.part_id,
                                          order_status=0)
                        order_new.save()
            else:
                # 如果数量没有少于库存临界值，则查看订单中有无未写入订货报表的订货信息，若有则删除订单
                ordering = db.session.query(Order).filter_by(part_id=i.part_id, order_status=0).first()
                if ordering != None:
                    db.session.delete(ordering)
                    db.session.commit()
    print('库存清单已经更新,已经生成对应的订货信息')
