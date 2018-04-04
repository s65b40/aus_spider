# -*- coding: utf-8 -*-
#author:Haochun Wang
import xlrd, xlwt, os, time
class Tablemaker:
    def __init__(self):
        self.font0 = xlwt.Font()
        self.font0.colour_index = 2  # red
        self.font1 = xlwt.Font()
        self.font1.colour_index = 3  # green
        self.style0 = xlwt.XFStyle()
        self.style1 = xlwt.XFStyle()
        self.style0.font = self.font0
        self.style1.font = self.font1
        self.write_table()

    def write_table(self):
        with open('res_tmp.txt') as d:   # open the temporary text file
            p = d.readlines()
            products = sorted(p)   # sort the lines by the alphabet order of product names
            timestamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            path_exist = 'price_folder/price.xls'
            save_path = 'price_folder/price' + timestamp + '.xls'
            path_folder = '/Users/hcwang/Desktop/spider-py/aus_spider/price_folder/'

            try:
                lists = os.listdir(path_folder)  # 列出目录的下所有文件和文件夹保存到lists
                lists.sort(key=lambda fn: os.path.getmtime(path_folder + "/" + fn))  # 按时间排序
                path_exist = os.path.join(path_folder, lists[-1])  # 获取最新的文件保存到file_new

                oldsheet = xlrd.open_workbook(path_exist).sheet_by_index(0)
                numrow = oldsheet.nrows
                olddic = {}
                for i in range(1, numrow):
                    olddic[oldsheet.row_values(i)[0].replace(' ', '-').replace('\'', '39')] = oldsheet.row_values(i)[1]

                newbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
                newsheet = newbook.add_sheet('sheet1', cell_overwrite_ok=True)
                new_sheet_sorted = newbook.add_sheet('sheet2', cell_overwrite_ok=True)

                currentrow = 1
                newsheet.write(0, 0, 'product_name_en')
                newsheet.write(0, 1, 'price_aud')
                newsheet.write(0, 2, 'price_yuan')
                newsheet.write(0, 3, 'discount')      

                for i in xrange(len(products) - 1):
                    rowsplits = products[i].split(', ')
                    #print rowsplits[1][1:]
                    #print type(rowsplits[1][1:])
                    #print len(rowsplits[1][1:])
                    newsheet.write(currentrow, 0, rowsplits[0].replace('-', ' ').replace('39', '\''))
                    if olddic.has_key(rowsplits[0]) and float(olddic[rowsplits[0]]) > float(rowsplits[1][1:]):
                        newsheet.write(currentrow, 1, float(rowsplits[1][1:]), self.style0)
                        newsheet.write(currentrow, 2, float(rowsplits[2]), self.style0)
                        newsheet.write(currentrow, 3, float(rowsplits[3]), self.style0)
                    elif olddic.has_key(rowsplits[0]) and float(olddic[rowsplits[0]]) < float(rowsplits[1][1:]):
                        newsheet.write(currentrow, 1, float(rowsplits[1][1:]), self.style1)
                        newsheet.write(currentrow, 2, float(rowsplits[2]), self.style1)
                        newsheet.write(currentrow, 3, float(rowsplits[3]), self.style1)
                    else:
                        newsheet.write(currentrow, 1, float(rowsplits[1][1:]))
                        newsheet.write(currentrow, 2, float(rowsplits[2]))
                        newsheet.write(currentrow, 3, float(rowsplits[3]))
                    currentrow += 1
                newbook.save(save_path)
            except:
                newbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
                newsheet = newbook.add_sheet('sheet1', cell_overwrite_ok=True)

                currentrow = 1
                newsheet.write(0, 0, 'product_name_en')
                newsheet.write(0, 1, 'price_aud')
                newsheet.write(0, 2, 'price_yuan')
                newsheet.write(0, 3, 'discount')
                for i in xrange(len(products)-1):
                    rowsplits = products[i].split(', ')
                    newsheet.write(currentrow, 0, rowsplits[0].replace('-', ' ').replace('39', '\''))
                    newsheet.write(currentrow, 1, float(rowsplits[1][1:]))
                    newsheet.write(currentrow, 2, float(rowsplits[2]))
                    newsheet.write(currentrow, 3, float(rowsplits[3]))
                    currentrow += 1
                newbook.save(save_path)


        return
Tablemaker()