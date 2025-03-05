import zipfile
import os
import get_adab
import get_elom
import glob
import shutil
from io import StringIO

def save_message(message, filename='messages.txt'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(message + '\n')

def extractor(filename, collage):
    new_folder_name = f"{collage}old"
    done = True
    try:
        try:
            shutil.rmtree(new_folder_name)
        except Exception as e:
            save_message(str(e))
        try:
            os.rename(collage, new_folder_name)
            save_message(f"تم تغيير اسم المجلد من '{collage}' إلى '{new_folder_name}'")
        except Exception as e:
            save_message(str(e))
            try:
                os.mkdir(collage)
                save_message(f"تم انشاء مجلد جديد باسم {collage}")
            except Exception as e:
                save_message(str(e))
        
        zip_file = zipfile.ZipFile(filename, 'r')
        zip_file.extractall(collage)
        zip_file.close()

    except FileNotFoundError as ff:
        save_message(f"لم يتم العثور على المجلد '{collage}'")
        save_message(str(ff))
    except OSError as e:
        save_message(f"حدث خطأ os أثناء تغيير اسم المجلد: {e}")
    except Exception as e:
        save_message(f"حدث خطأ أثناء تغيير اسم المجلد: {e}")

    directory = collage
    files = []
    for dirpath, dirnames, filenames in os.walk(directory):
        files += glob.glob(os.path.join(dirpath, "*.html"))
    file_names = [os.path.basename(file) for file in files]

    directory1 = new_folder_name
    files1 = []
    for dirpath1, dirnames1, filenames1 in os.walk(directory1):
        files1 += glob.glob(os.path.join(dirpath1, "*.html"))
    file_names1 = [os.path.basename(file1) for file1 in files1]

    total_files = len(files)
    save_message(f"تتم معالجة {total_files} من الملفات")
    
    for num, file in enumerate(files):
        file_name = os.path.basename(file)
        if file_name not in file_names1:
            if collage == "adab":
                get_adab.get_xlsx(file)
            elif collage == "elom":
                get_elom.get_xlsx(file)

            print(f"{num} file have converted successfully")
            
            percentage = (num + 1) / total_files * 100
            
            if int(percentage) % 10 == 0:
                try:
                    save_message(f"تم معالجة {percentage:.2f}% من الملفات")
                except Exception as e:
                    save_message(str(e))

# extractor("كلية_الآداب_والعلوم_الانسانية_ـ_التاريخ_بتاريخ_2024_ـ_07_ـ_25.zip", "adab")
