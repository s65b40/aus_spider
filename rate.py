# -*- coding: utf-8 -*-
#author:Haochun Wang
import xlrd, xlwt, os, time

font0 = xlwt.Font()
font0.colour_index = 2
font1 = xlwt.Font()
font1.colour_index = 3
style0 = xlwt.XFStyle()
style1 = xlwt.XFStyle()
style0.font = font0
style1.font = font1
with open('res_tmp.txt') as d:
    p = d.readlines()
    products = sorted(p)

    path_exist = 'price.xls'
    save_path = 'price.xls'
    if os.path.exists(path_exist):
        color = ['black', 'red']
        oldsheet = xlrd.open_workbook(path_exist).sheet_by_index(0)
        numrow = oldsheet.nrows
        olddic = {}
        for i in range(1, numrow):
            olddic[oldsheet.row_values(i)[0].replace(' ', '-').replace('\'', '39')] = oldsheet.row_values(i)[1]

        newbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
        newsheet = newbook.add_sheet('sheet1', cell_overwrite_ok=True)

        currentrow = 1
        newsheet.write(0, 0, 'product_name_en')
        newsheet.write(0, 1, 'price_aud')
        newsheet.write(0, 2, 'price_yuan')
        for i in xrange(len(products) - 1):
            rowsplits = products[i].split(', ')
            #print rowsplits[1][1:]
            #print type(rowsplits[1][1:])
            #print len(rowsplits[1][1:])
            newsheet.write(currentrow, 0, rowsplits[0].replace('-', ' ').replace('39', '\''))
            if olddic.has_key(rowsplits[0]) and float(olddic[rowsplits[0]]) > float(rowsplits[1][1:]):
                newsheet.write(currentrow, 1, float(rowsplits[1][1:]), style0)
                newsheet.write(currentrow, 2, float(rowsplits[2]), style0)
            elif olddic.has_key(rowsplits[0]) and float(olddic[rowsplits[0]]) < float(rowsplits[1][1:]):
                newsheet.write(currentrow, 1, float(rowsplits[1][1:]), style1)
                newsheet.write(currentrow, 2, float(rowsplits[2]), style1)
            else:
                newsheet.write(currentrow, 1, float(rowsplits[1][1:]))
                newsheet.write(currentrow, 2, float(rowsplits[2]))
            currentrow += 1
        newbook.save(save_path)
    else:
        newbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
        newsheet = newbook.add_sheet('sheet1', cell_overwrite_ok=True)

        currentrow = 1
        newsheet.write(0, 0, 'product_name_en')
        newsheet.write(0, 1, 'price_aud')
        newsheet.write(0, 2, 'price_yuan')
        for i in xrange(len(products)-1):
            rowsplits = products[i].split(', ')
            newsheet.write(currentrow, 0, rowsplits[0].replace('-', ' ').replace('39', '\''))
            newsheet.write(currentrow, 1, float(rowsplits[1][1:]))
            newsheet.write(currentrow, 2, float(rowsplits[2]))
            currentrow += 1
        newbook.save(save_path)
