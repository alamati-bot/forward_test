from bs4 import BeautifulSoup
import pandas as pd

def get_xlsx(filename):
        with open(filename, 'r') as file:
                html_content = file.read()

        # قم بتحليل الملف باستخدام BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        pd.set_option('display.max_colwidth', 500)

        # استخراج جميع الجداول في الملف
        db = soup.get_text()[120:290]
        tables = soup.find_all('table')
        df = pd.read_html(str(tables))[0]  # تحويل الجدول إلى DataFrame
        sub = db.split(" مقرر ")[1].split("لطلاب ")[0][:-5]
        year = db.split("قسم ")[0].split("الصف ")[1]
        dep = db.split(" قسم ")[1].split("\n")[0]
        print(f"{sub}  :  {dep}  :  {year}" )
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
        name = f"س{year_num} ـ {sub} ـ {dep}"
        print(name)
        # تصدير البيانات إلى ملف Excel
        df.to_excel(filename[:-5] + ".xlsx", index=False)  # تحويل البيانات إلى ملف Excel