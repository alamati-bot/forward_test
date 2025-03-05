import os
import pandas as pd
import glob
import numpy as np
import csv

directory = r"C:\Users\DELL\Desktop\Alamati\New folder\علامات كلية العلوم ـ ف2 ـ 2023-2024"

files = []
for dirpath, dirnames, filenames in os.walk(directory):
    files += glob.glob(os.path.join(dirpath, "*.xlsx"))

dfs = [pd.read_excel(file, header=1, engine='openpyxl') for file in files]
file_names = [os.path.basename(file) for file in files]

def convert_to_int(element):
    if isinstance(element, np.int64):
        return element.item()
    elif isinstance(element, np.float64):
        return int(element.item())
    elif element == "صفر":
        return 0
    elif element == "حجب":
        return element
    elif isinstance(element, float):
        return int(element)
    elif isinstance(element, str):
        try:
            return int(element)
        except:
            return element
    else:
        return element

def get_info_2(df):
    nums = []
    names = []
    marks = []
    data = df['الرقم الجامعي'].values
    for i, num in enumerate(data) :
        name = df['اسم الطالب'].values[i]
        names.append(name)
        mark = df['مجموع'].values[i]
        mark = convert_to_int(mark)
        marks.append(mark)
        num = convert_to_int(num)
        nums.append(num)

    nums1 = []
    names1 = []
    marks1 = []
    data1 = df['الرقم الجامعي.1'].values
    for i, num in enumerate(data1) :
        name = df['اسم الطالب.1'].values[i]
        names1.append(name)
        mark = df['مجموع.1'].values[i]
        mark = convert_to_int(mark)
        marks1.append(mark)
        num = convert_to_int(num)
        nums1.append(num)

    names.extend(names1)
    marks.extend(marks1)
    nums.extend(nums1)
    return nums, names, marks

def get_info_3(df):
    nums = []
    names = []
    marks = []
    data = df['الرقم الجامعي'].values
    for i, num in enumerate(data) :
        name = df['اسم الطالب'].values[i]
        names.append(name)
        mark = df['العلامة'].values[i]
        mark = convert_to_int(mark)
        marks.append(mark)
        num = convert_to_int(num)
        nums.append(num)

    nums1 = []
    names1 = []
    marks1 = []
    data1 = df['الرقم الجامعي.1'].values
    for i, num in enumerate(data1) :
        name = df['اسم الطالب.1'].values[i]
        names1.append(name)
        mark = df['العلامة.1'].values[i]
        mark = convert_to_int(mark)
        marks1.append(mark)
        num = convert_to_int(num)
        nums1.append(num)

    names.extend(names1)
    marks.extend(marks1)
    nums.extend(nums1)
    
    nums2 = []
    names2 = []
    marks2 = []
    data2 = df['الرقم الجامعي.2'].values
    for i, num in enumerate(data2) :
        name = df['اسم الطالب.2'].values[i]
        names2.append(name)
        mark = df['العلامة.2'].values[i]
        mark = convert_to_int(mark)
        marks2.append(mark)
        num = convert_to_int(num)
        nums2.append(num)

    names.extend(names2)
    marks.extend(marks2)
    nums.extend(nums2)
    return nums, names, marks

for i, df in enumerate(dfs):
    df = df.fillna(0)
    filename = file_names[i]
    print(filename)
    filename_without_extension = os.path.splitext(filename)[0]
    listv = filename_without_extension.split("ـ")
    sentence_list_without_spaces = [sentence.strip() for sentence in listv]
    year = sentence_list_without_spaces[0]
    sub = sentence_list_without_spaces[1]
    department = sentence_list_without_spaces[2]
    if department:
        if department == 'اللغة العربية':
            dep = "arabic.csv"
        elif department == 'اللغة الانكليزية':
            dep = "english.csv"
        elif department == 'اللغة الفرنسية':
            dep = "french.csv"
        elif department == 'الجغرافية':
            dep = "geography.csv"
        elif department == 'التاريخ':
            dep = "history.csv"
        elif department == 'الفلسفة':
            dep = "philosophy.csv"
        elif department == 'الآثار':
            dep = "archeology.csv"
        elif department == 'علم الاجتماع':
            dep = "sociology.csv"
        elif department == 'علم الحياة':
            dep = "biology.csv"
        elif department == 'الرياضيات':
            dep = "math.csv"
        elif department == 'الكيمياء':
            dep = "chemistry.csv"
        elif department == 'الفيزياء':
            dep = "physics.csv"
        elif department == 'الجيلوجيا':
            dep = "geology.csv"
        elif department == 'الاحصاء الرياضي':
            dep = "statics.csv"
    header = df.columns.tolist()
    header_str = ' '.join(header)
    if header_str == "الرقم الجامعي اسم الطالب العلامة الرقم الجامعي.1 اسم الطالب.1 العلامة.1 الرقم الجامعي.2 اسم الطالب.2 العلامة.2":
        if get_info_3(df) != None:
            nums, names, marks = get_info_3(df)
            with open('marks.csv', 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)
            f.close()
            for ii, num in enumerate(nums):
                mark = f"علامة : {marks[ii]} في {sub} من السنة{year}"
                for row in data:
                    if len(row) != 0:
                        if int(row[0]) == num and row[3] == dep:
                            row[2] += f"\n{mark}"
                            break
                else:
                    if num != 0 :
                        data.append([num,names[ii],mark,dep])
            with open('marks.csv', 'w', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            f.close()
    else:
        if get_info_2(df) != None:
            nums, names, marks = get_info_2(df)
            with open('marks.csv', 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                data = list(reader)
            f.close()
            for ii, num in enumerate(nums):
                mark = f"علامة : {marks[ii]} في {sub} من السنة{year}"
                for row in data:
                    if len(row) != 0:
                        if int(row[0]) == num and row[3] == dep:
                            row[2] += f"\n{mark}"
                            break
                else:
                    if num != 0 :
                        data.append([num,names[ii],mark, dep])
            with open('marks.csv', 'w', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            f.close()

print("Done")
