from obspy import UTCDateTime
import os
input_filename = r'1.dat'
output_pha_filename = r'2.pha'
output_ctlg_filename = r'3.ctlg'

#从一行里读时间字符串返回，例如00:47:19.75
def get_time(line_str):
    for v in line_str.split():
        if v.count(':') == 2:
            return v

def main():
    input_file = open(input_filename, 'r', encoding = 'utf8')
    output_pha = open(output_pha_filename, 'w')
    output_ctlg = open(output_ctlg_filename, 'w')
    seq_no = 0
    lines = input_file.readlines()
    i = 0
    while i < len(lines):
        if ':' in lines[i] and '/' in lines[i]: #数据单元的标题
            values = lines[i].split()
            date = values[1]
            is_ignore = False
            #如果缺少数据,舍弃这个数据单元
            if len(values) < 9:
                is_ignore = True
            else:
                #得到标题写到文件
                date_time = UTCDateTime(values[1] + ' ' + values[2]).strftime('%Y%m%d%H%M%S.%f')[:-4]
                title = '{},{},{},{},{},{}'.format(date_time,values[3],values[4],values[5],values[6],seq_no)
                seq_no += 1
                output_pha.write(title + '\n')
                output_ctlg.write(title + '\n')
                print(title)
            #跳过标题继续读数据
            i += 1
            while i < len(lines) and not (':' in lines[i] and '/' in lines[i]):
                #读前两行的数据
                if not is_ignore and lines[i][0].isalpha():
                    time1 = get_time(lines[i]) 
                    time2 = get_time(lines[i+1])
                    date_time1 = UTCDateTime('{} {}'.format(date, time1))
                    date_time2 = UTCDateTime('{} {}'.format(date, time2))
                    v1, v2 = lines[i].split()[0:2]
                    output_pha.write('{}.{},{},{},1,1\n'.format(v1, v2, date_time1, date_time2))
                    #跳过其他行数据
                    i += 1
                    while i < len(lines) and not lines[i][0].isalpha():
                        i += 1
                else:
                    i += 1
        else:
            i += 1
    input_file.close()
    output_pha.close()
    output_ctlg.close()
    print('saved:')
    print(os.path.abspath(output_pha_filename))
    print(os.path.abspath(output_ctlg_filename))
main()    
