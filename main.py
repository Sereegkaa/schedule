import json, sqlite3, datetime
from time import sleep

from flask import Flask, request

app = Flask(__name__)
days_f = {1: "Понедельник", 2: "Вторник", 3: "Среда", 4: "Четверг", 5: "Пятница", 6: "Суббота"}


@app.route('/schedule', methods=['get'])
def schedule():
    con = sqlite3.connect("schedule.db")
    cur = con.cursor()

    group = request.args.get('group')
    ch = request.args.get('ch')
    a = cur.execute(f"""SELECT * FROM schedule WHERE `group`='{group}' and `chetn`='{ch}'""").fetchall()
    sch = {"group": group, "week": ch, "schedule": []}
    day = 1
    y = {"dayOfWeek": "", "lessons": []}
    for i in range(len(a)):
        x = a[i]
        print(x)
        if x[0] == day:
            if x[-2] == '-':
                y["lessons"].append({})
                continue
            y["dayOfWeek"] = days_f[day]
            y["lessons"].append({"name": x[-2], "time": x[2], "type": x[4], "classroom": x[3], "teacher": x[5]})
            if i == len(a) - 1:
                day = x[0]
                print(y)
                sch["schedule"].append(y)
                y = {"dayOfWeek": "", "lessons": []}
        else:
            day = x[0]
            print(y)
            sch["schedule"].append(y)
            y = {"dayOfWeek": "", "lessons": []}
            y["lessons"].append({"name": x[-2], "time": x[2], "type": x[4], "classroom": x[3], "teacher": x[5]})

    return json.dumps(sch, ensure_ascii=False)


if __name__ == "__main__":
    app.run(debug=True)
