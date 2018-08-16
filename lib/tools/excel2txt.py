# -*- coding: utf-8 -*-
import xlrd


def excel_to_list(input_file_list, sheet_name, indexes=None, ignore_header=True):
    for input_file in input_file_list:
        workbook = xlrd.open_workbook(input_file)
        sh = workbook.sheet_by_name(sheet_name)
        for n in range(sh.nrows):
            result = []
            if ignore_header and n == 0:
                continue
            for i in range(sh.ncols):
                if indexes is not None and i not in indexes:
                    continue
                data = sh.cell_value(n, i)
                if type(data) is unicode:
                    result.append(data.encode('utf-8'))
                else:
                    result.append(str(data))
            yield result


def excel_to_txt(input_file_list, output_file, sheet_name, indexes=None, ignore_header=True):
    with open(output_file, 'w') as outf:
        for line in excel_to_list(input_file_list, sheet_name, indexes, ignore_header):
            outf.write('\t'.join(line))
            outf.write('\n')


if __name__ == '__main__':
    # arg parser
    # parser = argparse.ArgParser(description='convert an excel file to txt file')
    # parser.add_argument('input', help='the excel file(*.xlsx) what to convert', metavar='<input file>')
    # parser.add_argument('sheet', help='sheet in excel workbook you want to output', metavar='<sheet name>')
    # parser.add_argument('output', help='txt file you want to output', metavar='<output file>')
    # args = parser.parse_args()

    excel_to_txt(['/Users/xiaotz/work/舆情/舆情平台数据导出/第一次/蚂蚁舆情平台数据导出17-08-02 18-32-08.xls'],
                 '/Users/xiaotz/work/舆情/舆情平台数据导出/第一次/3.txt',
                 'Sheet0',
                 [2, 3],
                 True)
