import pandas as pd
from bps.attendance_bp.dao.attendance_dao import get_all_records, insert_one, by_date, by_student
from bps.attendance_bp.dao.students_dao import get_all_students

def process_index_data():
    records = get_all_records()
    n = l = t = a = 0
    for r in records:
        s = r['status']
        if s == '正常': n += 1
        elif s == '迟到': l += 1
        elif s == '请假': t += 1
        elif s == '未到': a += 1
    return {"records": records, "normal": n, "late": l, "leave": t, "absent": a}

def do_import(request, username):
    f = request.files['file']
    df = pd.read_excel(f)
    cnt = 0
    for _, r in df.iterrows():
        try:
            sid = str(r['student_id']).strip()
            dt = str(r['attend_date']).split()[0]
            tp = r['attend_type']
            ct = r['check_time'] if pd.notna(r['check_time']) else None
            st = str(r['status']).replace('缺勤', '未到')
            insert_one((sid, dt, tp, ct, st, username))
            cnt += 1
        except:
            continue
    return f"导入成功 {cnt} 条"

def query_data(request):
    students = get_all_students()
    records = []
    n = l = t = a = 0
    qtype = ""
    if request.method == 'POST':
        qtype = request.form['query_type']
        if qtype == 'date':
            records = by_date(
                request.form.get('start_date'),
                request.form.get('end_date'),
                request.form.get('status_type')
            )
        elif qtype == 'name':
            records = by_student(
                request.form.get('student_id'),
                request.form.get('status_type')
            )
        for r in records:
            print(r)
            s = r['status']
            if s == '正常': n +=1
            elif s == '迟到': l +=1
            elif s == '请假': t +=1
            elif s == '未到': a +=1
    return {
        "students": students,
        "records": records,
        "normal": n, "late": l, "leave": t, "absent": a,
        "query_type": qtype
    }