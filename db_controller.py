import db_connect as db_con

#결제 정보 insert 쿼리
def insert_paymentInfo(result,uniqueId):
    db = db_con.get_db()
    cursor = db.cursor()
    statement = "INSERT INTO paymentInfo(id,string) VALUES (?, ?)"
    cursor.execute(statement, [(uniqueId),(result)])
    db.commit()
    db.close()
    return True

#결제 취소정보 insert 쿼리
def insert_canclepaymentInfo(result,cancleuniqueId,uniqueId):
    db = db_con.get_db()
    cursor = db.cursor()
    statement = "INSERT INTO cancle_paymentInfo(cancle_id,string,id) VALUES (?, ?,?)"
    cursor.execute(statement, [(cancleuniqueId),(result),(uniqueId)])
    db.commit()
    db.close()
    return True

##결제 정보 조회 쿼리
def select_paymentInfo(uniqueId):
    db = db_con.get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM paymentInfo WHERE id = ?"
    cursor.execute(statement, (uniqueId,))
    rows = cursor.fetchall()
    uniqueCode = ""
    paymentInfo = ""
    uniqueCodeIsTrue = True
    for row in rows:
        uniqueCode = row[0]
        paymentInfo = row[1]
        print("uniqueCode = ",uniqueCode)
        print("paymentInfo",paymentInfo)
    db.close()
    if uniqueCode == "":
        uniqueCodeIsTrue = False
        return uniqueCodeIsTrue, paymentInfo
    else:
        return uniqueCodeIsTrue, paymentInfo

##결제취소 정보 조회 쿼리
def select_paymentcancleInfo(uniqueId):
    db = db_con.get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM cancle_paymentInfo WHERE id = ?"
    cursor.execute(statement, (uniqueId,))
    rows = cursor.fetchall()
    cancleuniqueCode = ""
    uniqueCode = ""
    paymentInfo = ""
    cancleuniqueCodeIsTrue = True
    for row in rows:
        cancleuniqueCode = row[0]
        paymentInfo = row[1]
        uniqueCode = row[2]
        print("cancleuniqueCode = ",cancleuniqueCode)
        print("paymentInfo",paymentInfo)
        print("uniqueCode = ",uniqueCode)
    db.close()
    if cancleuniqueCode == "":
        cancleuniqueCodeIsTrue = False
        return cancleuniqueCodeIsTrue, paymentInfo
    else:
        return cancleuniqueCodeIsTrue, paymentInfo

##결제조회시 취소된 내역이 있는지 파악
##결제 및 취소 내역이 없는경우 해당 결제 관리번호 존재하지 않는다고 표시
def select_payorcancle(uniqueId):
    pay_gubun = "cancle"
    Id = ""
    db = db_con.get_db()
    cursor = db.cursor()
    statement = "SELECT * FROM cancle_paymentInfo WHERE id = ?"
    cursor.execute(statement, (uniqueId,))
    rows = cursor.fetchall()
    for row in rows:
        Id = row[0]
    db.close()
    if Id != "":
        return pay_gubun
    else:
        db = db_con.get_db()
        cursor = db.cursor()
        statement = "SELECT * FROM paymentInfo WHERE id = ?"
        cursor.execute(statement, (uniqueId,))
        rows = cursor.fetchall()
        for row in rows:
            Id = row[0]
        db.close()
        if Id != "":
            pay_gubun = "payment"
            return pay_gubun
        else:
            pay_gubun = "nothing"
            return ""
        


