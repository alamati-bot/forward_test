from bs4 import BeautifulSoup
import pandas as pd
import csv
import glob
import numpy as np
from io import StringIO



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
        print(element)
        print(type(element))
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
        if name != 0 :
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
        if name != 0 :
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
        if name != 0 :
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
        if name != 0 :
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
        if name != 0 :
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


def get_xlsx(filename):
        with open(filename, 'r') as file:
                html_content = file.read()

        # قم بتحليل الملف باستخدام BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        pd.set_option('display.max_colwidth', 500)

        # استخراج جميع الجداول في الملف
        tables = soup.find_all('table')
        table_html = tables[1].prettify() 
        dh = pd.read_html(StringIO(table_html))[0]    # تحويل الجدول إلى DataFrame
        # dh = pd.read_html(str(tables))[1] 
        dh = dh.fillna(0)
        table_html = tables[0].prettify() 
        nas = pd.read_html(StringIO(table_html))[0]    # تحويل الجدول إلى DataFrame
        # nas = pd.read_html(str(tables))[0] 
        db = nas.to_string(index=False)
        sub = db.split(" مقرر ")[1].split("  لطلاب ")[0]
        year = db.split(" مقرر ")[1].split("  لطلاب ")[1].split("قسم ")[0].split("الصف ")[1]
        department = db.split(" مقرر ")[1].split("  لطلاب ")[1].split("قسم ")[1].split(" Character")[0]
        print(f"{sub}  :  {department}  :  {year}" )
        year_num = 0
        if year == "الاول ":
                year_num = 1
        elif year == "الثاني ":
                year_num = 2
        elif year == "الثالث ":
                year_num = 3
        elif year == "الرابع ":
                year_num = 4
        else:
                print(f"::{year}::")
        name = f"س{year_num} ـ {sub} ـ {department}"
         # تصدير البيانات إلى ملف Excel
        dh.to_excel(filename[:-5] + ".xlsx", index=False)  # تحويل البيانات إلى ملف Excel
        df = pd.read_excel(filename[:-5] + ".xlsx", header=1, engine='openpyxl')
        try:
               department = department.split(" شعبة")[0]
        except:
               pass
        if department:
                department = department.strip()
                if department == 'اللغة العربية':
                        dep = "arabic.csv"
                elif department == 'اللغة الانكليزية':
                        dep = "english.csv"
                elif department == 'اللغة الفرنسية':
                        dep = "french.csv"
                elif department == 'اللغة الفارسية':
                        dep = "parisan.csv"
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
                                mark = f"علامة : {marks[ii]} في {sub} من السنةس{year_num}"
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
                                mark = f"علامة : {marks[ii]} في {sub} من السنةس{year_num}"
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

       

# get_xlsx(r"C:\Users\DELL\Desktop\Alamati\forward\adab\كلية الآداب والعلوم الانسانية ـ اللغة الانكليزية بتاريخ 2024 ـ 07 ـ 25\س1\س1 ـ الترجمه 1 ـ اللغة الانكليزية.html")