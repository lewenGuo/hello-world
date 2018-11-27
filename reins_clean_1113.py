#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import time


class Reins:

    def __init__(self, file, browser='ie'):
        """

        :param file: original reins text file                                                  // written by Lewen, Guo
        :param browser: browser used to extract original reins text file                       // written by Lewen, Guo
        """
        self.browser = browser
        self.file = file

    def read_file(self):
        """

        :return: file with '\t' and '\n' replaced with blank                                   // written by Lewen, Guo
        """
        if self.browser == 'ie':
            with open(self.file, 'r') as f:
                file_text = f.read()

            return file_text.replace('\n', '').split(' ')

        elif self.browser == 'chrome':
            with open(self.file, 'r') as f:
                file_text = f.read()
            return file_text.replace('\n', ' ').replace('\t', ' ').split(' ')



    def get_col_name(self):
        """

        :return: column names of reins data                                                    // written by Lewen, Guo
        """
        split_file = self.read_file()
        # obtain the starting index by getting the index of "物件番号"                          // written by Lewen, Guo
        index = [i for i in range(len(split_file)) if split_file[i] == '物件番号']
        if len(index) > 1:
            raise ValueError("二つの物件番号項目があるので、ファイルの形をチェックしてください。")
        else:
            index = index[0]
        col_names = ['id']
        # deal with abnormal columns 異常処理                                                   // written by Lewen, Guo
        for k in range(index, index + 27):
            if '/' in split_file[k]:
                for j in range(len(split_file[k].split('/'))):
                    col0 = split_file[k].split('/')[j]
                    col_names.append(col0)
            else:
                col = split_file[k]
                col_names.append(col)
        # raise ValueError if the number of columns is not correct(33/31 for kodate/mansion)    // written by Lewen, Guo
        if len(col_names) != 33 and len(col_names) != 31:
            raise ValueError("項目の数は誤っています、ファイルの形をチェックしてください")
        return col_names

    def get_col_data(self, object_num=1):
        """

        :param object_num: the object number in reins data                                     // written by Lewen, Guo
        :return: dict of data for the object {'col_names1': 'data1', 'col_names2': 'data2'...} // written by Lewen, Guo
        """
        col_names = self.get_col_name()
        split_file = self.read_file()
        # index is the starting index of recording the starting of the content

        if self.browser == 'ie':
            for index in range(len(split_file)):
                if split_file[index] == '問合せ電話番号':
                    break
            # new_index adds the index of first appearance of object number(1,2..) to index     // written by Lewen, Guo
            new_index = split_file[index:].index(str(object_num)) + index
            # type_index is the index where indicates the type of all the objects in text file  // wriiten by Lewen, Guo
            type_index = split_file.index('ＮＯ') - 1
            if split_file[type_index] == '売り・戸建て' or split_file[type_index] == '売り・土地':
                iterators = [new_index, new_index + 2, new_index + 3, new_index + 4, new_index + 5, new_index + 7,
                            new_index + 7, new_index + 8, new_index + 9, new_index + 10, new_index + 11, new_index + 12,
                            new_index + 12, new_index + 13, new_index + 15, new_index + 16, new_index + 17,
                            new_index + 18, new_index + 19, new_index + 21, new_index + 22, new_index + 23,
                            new_index + 24, new_index + 25, new_index + 26, new_index + 28, new_index + 29,
                            new_index + 30, new_index + 31, new_index + 32, new_index + 33, new_index + 33,
                            new_index + 34]
            elif split_file[type_index] == '売り・マンション':
                iterators = [new_index, new_index + 2, new_index + 3, new_index + 4, new_index + 5, new_index + 7,
                             new_index + 8, new_index + 9, new_index + 10, new_index + 11,
                             new_index + 12, new_index + 13, new_index + 15, new_index + 16, new_index + 17,
                             new_index + 18, new_index + 19, new_index + 21, new_index + 22, new_index + 23,
                             new_index + 24, new_index + 25, new_index + 26, new_index + 28, new_index + 29,
                             new_index + 30, new_index + 31, new_index + 32, new_index + 33, new_index + 33,
                             new_index + 34]
            list_row = []
            # lag is used to record the number of lag that should be added to original iterator // written by Lewen, Guo
            lag = 0
            for i, j in zip(col_names, iterators):

                if i == '築年月':

                    if split_file[j] == '':
                        col_name_data = [i, split_file[j]]
                        lag += 0
                    # deal with (平成12年12月)                                                  // written by Lewen, Guo
                    elif '年' in split_file[j] and '月' in split_file[j]:
                        col_name_data = [i, split_file[j]]
                        lag += 0
                    # deal with (平成11年　2月)                                                 // written by Lewen, Guo
                    elif '年' in split_file[j] and '月' not in split_file[j]:
                        add_month = split_file[j] + split_file[j + 1]
                        col_name_data = [i, add_month]
                        lag += 1

                    elif '年' not in split_file[j] and '月' not in split_file[j]:
                        # deal with (平成 1年12月)                                              // written by Lewen, Guo
                        if '年' in split_file[j + 1] and '月' in split_file[j + 1]:
                            add_yearmonth = split_file[j] + split_file[j + 1]
                            col_name_data = [i, add_yearmonth]
                            lag += 1
                        # deal with (平成 1年 1月)                                              // written by Lewen, Guo
                        if '年' in split_file[j + 1] and '月' not in split_file[j + 1]:
                            add_year_and_month = split_file[j] + split_file[j + 1] + split_file[j + 2]
                            col_name_data = [i, add_year_and_month]
                            lag += 2

                    list_row.append(col_name_data)
                elif i == '接道状況' or i == '幅員' or i == '取引態様':
                    col_name_data = [i, split_file[j + lag].split('/')[0]]
                    list_row.append(col_name_data)

                elif i == '方向' or i == '接面' or i == '報酬形態':
                    try:
                        col_name_data = [i, split_file[j + lag].split('/')[1]]
                    except IndexError:
                        col_name_data = [i, '']

                    list_row.append(col_name_data)
                elif i == '徒歩' or i == 'バス' or i == '停歩':
                    col_name_data = [i, split_file[j + lag].replace('/', '')]

                    list_row.append(col_name_data)

                else:
                    list_row.append([i, split_file[j + lag]])

            return dict(list_row)

        elif self.browser == 'chrome':
            for index in range(len(split_file)):
                if split_file[index] == '問合せ電話番号':
                    break

            new_index = split_file[index:].index(str(object_num)) + index
            type_index = split_file.index('ＮＯ') - 1

            if split_file[type_index] == '売り・戸建て' or split_file[type_index] == '売り・土地':
                iterators = [new_index, new_index + 5, new_index + 7, new_index + 8, new_index + 10,
                         new_index + 11, new_index + 11, new_index + 13, new_index + 14,
                         new_index + 16, new_index + 17, new_index + 18, new_index + 18,
                         new_index + 20, new_index + 22, new_index + 24, new_index + 25,
                         new_index + 26, new_index + 28, new_index + 30, new_index + 32,
                         new_index + 33, new_index + 34, new_index + 35, new_index + 36,
                         new_index + 38, new_index + 40, new_index + 41, new_index + 42,
                         new_index + 43, new_index + 44, new_index + 44, new_index + 45]

            elif split_file[type_index] == '売り・マンション':
                iterators = [new_index, new_index + 5, new_index + 7, new_index + 8, new_index + 10,
                             new_index + 11, new_index + 13, new_index + 14,
                             new_index + 16, new_index + 17, new_index + 18, new_index + 19,
                            new_index + 22, new_index + 24, new_index + 25,
                             new_index + 26, new_index + 27, new_index + 29, new_index + 30,
                             new_index + 31, new_index + 33, new_index + 34, new_index + 35,
                             new_index + 37, new_index + 39, new_index + 40, new_index + 41,
                             new_index + 42, new_index + 43, new_index + 43, new_index + 44]

            list_row = []
            lag = 0
            for i, j in zip(col_names, iterators):

                if i == '築年月':

                    if split_file[j] == '':
                        col_name_data = [i, split_file[j]]
                        lag += 0
                    # deal with (平成12年12月)                                                  // written by Lewen, Guo
                    elif '年' in split_file[j] and '月' in split_file[j]:
                        col_name_data = [i, split_file[j]]
                        lag += 0
                    # deal with (平成11年　2月)                                                 // written by Lewen, Guo
                    elif '年' in split_file[j] and '月' not in split_file[j]:
                        add_month = split_file[j] + split_file[j + 1]
                        col_name_data = [i, add_month]
                        lag += 1

                    elif '年' not in split_file[j] and '月' not in split_file[j]:
                        # deal with (平成 1年12月)                                              // written by Lewen, Guo
                        if '年' in split_file[j + 1] and '月' in split_file[j + 1]:
                            add_yearmonth = split_file[j] + split_file[j + 1]
                            col_name_data = [i, add_yearmonth]
                            lag += 1
                        # deal with (平成 1年 1月)                                              // written by Lewen, Guo
                        if '年' in split_file[j + 1] and '月' not in split_file[j + 1]:
                            add_year_and_month = split_file[j] + split_file[j + 1] + split_file[j + 2]
                            col_name_data = [i, add_year_and_month]
                            lag += 2

                    list_row.append(col_name_data)
                elif i == '接道状況' or i == '幅員' or i == '取引態様':
                    col_name_data = [i, split_file[j + lag].split('/')[0]]
                    list_row.append(col_name_data)

                elif i == '方向' or i == '接面' or i == '報酬形態':
                    try:
                        col_name_data = [i, split_file[j + lag].split('/')[1]]
                    except IndexError:
                        col_name_data = [i, '']
                    list_row.append(col_name_data)
                elif i == '徒歩' or i == 'バス' or i == '停歩':
                    col_name_data = [i, split_file[j + lag].replace('/', '')]
                    list_row.append(col_name_data)
                else:
                    list_row.append([i, split_file[j + lag]])

            return dict(list_row)


    def clean_data(self):
        """

        :return: list of dicts, where each dict represents a single object                      //written by Lewen, Guo
        """
        if self.browser == 'ie':
            split_file = self.read_file()
            # counter the number of total objects in the text file                               //written by Lewen, Guo

            obj_number_indicator = split_file.index('件目') - 1
            if int(split_file[obj_number_indicator]) % 100 == 0:
                object_number = 100 + 1
            elif int(split_file[obj_number_indicator]) % 100 != 0:
                object_number = int(split_file[obj_number_indicator][1:]) + 1
            # store the dicts in final_lists                                                     //written by Lewen, Guo
            final_lists = [self.get_col_data(i) for i in range(1, object_number)]

        elif self.browser == 'chrome':
            split_file = self.read_file()
            obj_number_indicator = split_file.index('件目') - 1
            if int(split_file[obj_number_indicator]) % 100 == 0:
                object_number = 100 + 1
            elif int(split_file[obj_number_indicator]) % 100 != 0:
                object_number = int(split_file[obj_number_indicator][1:]) + 1
            final_lists = [self.get_col_data(i) for i in range(1, object_number)]
        print(final_lists)
        return  final_lists


if __name__ == '__main__':

    # Test IE Tochi

    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(京都市北区~東区　土地　期間指定なし　1ページ目）.txt").\
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(京都市北区~東区　土地　期間指定なし　3ページ目）.txt").\
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(京都市北区~東区　土地　期間指定なし　5ページ目）.txt").\
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(京都府亀岡市~長岡京市土地　期間指定なし　1ページ目）.txt").\
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(京都府亀岡市~長岡京市土地　期間指定なし　4ページ目）.txt"). \
        clean_data()

    # Test IE Kodate
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(奈良県奈良市戸建　期間指定なし　1ページ目）.txt"). \
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(奈良県奈良市戸建　期間指定なし　5ページ目）.txt"). \
        clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(和歌山県有田市～岩出市戸建　期間指定なし　1ページ目）.txt"). \
        clean_data()

    # Test IE mansion
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(奈良県奈良市マンション　期間指定なし　1ページ目）.txt"). clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(奈良県奈良市マンション　期間指定なし　3ページ目）.txt"). clean_data()
    Reins(r"C:\AMSdata\近畿レインズ（IE）\180928近畿レインズIE(大阪市浪速区・西淀川区マンション　期間指定なし　1ページ目）.txt").clean_data()

    # Test Chrome Tochi
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(京都府京都市全域土地　期間指定なし　2500万以下　1ページ目）.txt",
          browser='chrome').clean_data()
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(京都府京都市全域土地　期間指定なし　2500万以下　4ページ目）.txt",
          browser='chrome').clean_data()
    # Test Chrome Kodate
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(滋賀県大津市戸建　期間指定なし　2500万以下　1ページ目）.txt",
          browser='chrome').clean_data()
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(滋賀県大津市戸建　期間指定なし　2500万以下　5ページ目）.txt",
          browser='chrome').clean_data()
    # Test Chrome mansion
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(滋賀県大津市～野州市マンション　期間指定なし　1ページ目）.txt",
          browser='chrome').clean_data()
    Reins(r"C:\AMSdata\近畿レインズ10月（chrome）\181024近畿レインズChrome(滋賀県大津市～野州市マンション　期間指定なし　4ページ目）.txt",
          browser='chrome').clean_data()