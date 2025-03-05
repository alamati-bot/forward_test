import datetime

the_date = datetime.date.today()         #2024-09-06
year = datetime.date.today().year        #2024
month = datetime.date.today().month      #9
day =datetime. date.today().day          #6


# current_time = datetime.datetime.now().time()
# add_hours = datetime.timedelta(hours=3)
# new_time = (datetime.datetime.combine(datetime.date.today(), current_time) + add_hours).time()

# current_time = datetime.datetime.now().time()
# future_time = datetime.time(16, 40, 0)  # الساعة 6 مساءً

# if future_time > current_time:
#     print("الوقت في المستقبل.")
# else:
#     print("الوقت في الماضي أو الحال.")

def add_mounth():
    mounth_later = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    return mounth_later


def info_date(year,month,day):
    spe_date = datetime.datetime(year, month, day)
    current_date = datetime.datetime.now()

    if spe_date.date() > current_date.date():
        remaining_days = (spe_date.date() - current_date.date()).days
        return("future",remaining_days)
    elif spe_date.date() < current_date.date():
        return(["past"])
    else:
        return(["today"])
    
print(info_date(2024,10,29)[0])
if info_date(2024,10,29)[0] == "future":
    pass