import uuid
import xlwt
import time
from app.models import db, Order, Store
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
    order_data_head = ['序号', '零件ID', '零件名称', '采购数量', '供应商编号(主)',
                       '名称', '联系人名称', '联系方式', '地址', '供应商编号(次)',
                       '名称', '联系人名称', '联系方式', '地址']

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
        orders = db.session.query(Order).order_by('order_id').all()
        for order_idx, i in enumerate(orders):
            if i.o_part != None and i.o_part.p_supplier != None:
                worksheet.write(6 + order_idx, 0, order_idx + 1, data_style)
                part_id_ = str(i.part_id)
                part_id = part_id_.zfill(8)
                worksheet.write(6 + order_idx, 1, part_id, data_style)
                worksheet.write(6 + order_idx, 2, i.o_part.part_name, data_style)
                worksheet.write(6 + order_idx, 3, i.order_num, data_style)
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

    # 写入采购人签名

    # 保存表格
    xls_dir = 'static/order_folder/' + strtime_ + '.xls'
    workbook.save(xls_dir)
    # print('订货报表已经生成')


def update_store():
    # 每一个小时更新一次库存清单，暂定从早上7点到晚上7点
    # 如果库存小于库存临界值，则更新订货报表
    with scheduler.app.app_context():
        stores_list = db.session.query(Store).order_by('store_id').all()
        for i in stores_list:
            # 如果库存清单的值小于临界值
            if i.store_num < i.store_cv:
                # 产生订货信息
                # 如果订货信息已经存在，则更新订货数量
                order = db.session.query(Order).filter_by(part_id=i.part_id).first()
                if order != None:
                    order.order_num = i.store_max - i.store_num
                    db.session.commit()
                else:
                    order = Order(order_num=i.store_max - i.store_num, part_id=i.part_id)
                    order.save()
            else:
                # 如果数量没有少于库存临界值，则查看订单中有无，若有则删除订单
                order = db.session.query(Order).filter_by(part_id=i.part_id).first()
                if order != None:
                    db.session.delete(order)
                    db.session.commit()
    # print('库存清单已经更新,已经生成对应的订货信息')
