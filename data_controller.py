from hashlib import new
from os import error
from sqlite3.dbapi2 import InternalError
import app as app
import string
import random
from datetime import datetime
import time
import db_controller as dbc
import json


payOptionalbill = "" ##부가가치세 global 변수
installmentnum = "" ##할부 개월 수 global 변수
gcOptionalbill = "" ##취소시 부가가치세 global 변수

#String 데이터 조합 - 결제
def make_encryption (cardnum,effectiveterm,cvcnum,bill,payorcancle):
    global payOptionalbill
    global installmentnum
    cardnum = cardnum #카드번호
    installment = installmentnum #할부개월수
    effectiveterm = effectiveterm #유효기간
    cvcnum = cvcnum #cvc번호
    bill = bill #결제금액
    optionalbill = payOptionalbill #부가가치세
    payorcancle = payorcancle ##결제 및 취소 여부 판단 bool = True

    encryption_cardInfo = make_encryption_cardInfo(cardnum,effectiveterm,cvcnum)

    newcardnum = cardnum.ljust(20,' ')
    newbill = bill.rjust(10,' ')
    newoptionalbill = optionalbill.rjust(10,'0')
    newencryption_cardInfo = encryption_cardInfo.ljust(300,' ')
    datalength = 0 #데이터 길이
    datalengthStr = ""
    datagubun = ""
    if payorcancle:
        datagubun = "PAYMENT"
    else:
        datagubun = "CANCEL"
    datagubun = datagubun.ljust(10,' ')

    uniquecode = random_string() #관리번호    
    paymnet_string_data = make_payStrData(datagubun,uniquecode,installment,newencryption_cardInfo,newcardnum,effectiveterm,cvcnum,newbill,newoptionalbill,payorcancle,uniquecode)
    datalength = len(paymnet_string_data)
    datalengthStr = str(str(datalength).rjust(4,' '))
    paymnet_string_data = datalengthStr + paymnet_string_data
    # print("Final_data = ", paymnet_string_data)
    return paymnet_string_data,uniquecode


#관리번호 랜덤생성
def random_string():
    #make_random_length : 20 #20자리
    string_random = string.ascii_uppercase
    result = ""
    for i in range(20):
        result +=random.choice(string_random)
    return result

#데이터 유효성검사-결제
def data_validation(cardnum,installment,effectiveterm,cvcnum,bill,optionalbill):
    cardnum = cardnum #카드번호
    error_message = ""
    global installmentnum
    global payOptionalbill
    if cardnum.isdigit():
        if len(cardnum) >=10 and len(cardnum) <=16:
            cardnum = cardnum
        else:
            error_message = "카드번호를 다시 입력해 주세요"
            return False,error_message
    else:
        error_message = "카드번호를 다시 입력해 주세요"
        return False,error_message
    # print ("cardnum : ", cardnum)

    installment = installment #할부개월수
    
    if installment.isdigit():
        installmentint = int(installment)
        if installmentint == 1 or 0:
            installment = "00"
            installmentnum = installment
        elif installmentint>=2 and installmentint<=12:
            installment = installment.rjust(2,'0')
            installmentnum = installment
        else:
            error_message = "다시 입력해 주세요"
            return False,error_message
    else:
        if installment == "":
            installment = "00"
            installmentnum = installment
        else:
            error_message = "다시 입력해 주세요"
            return False,error_message
    print ("installment : ", installment)  

    effectiveterm = effectiveterm #유효기간
    if effectiveterm.isdigit():
        effectiveterm_month = effectiveterm[0:2]
        effectiveterm_year = effectiveterm[2:4]
        today = datetime.today().strftime("%Y%m")
        effectiveterm_new_year = "20" + effectiveterm_year
        effectiveterm_yyyymm = effectiveterm_new_year + effectiveterm_month
        date_compare = effectiveterm_yyyymm > today
        if date_compare:
            if int(effectiveterm_month) <1 or int(effectiveterm_month) >13:
                error_message = "유효기간을 다시 입력해 주세요"
                return False,error_message
            else:
                effectiveterm = effectiveterm
        else:
            error_message = "유효기간을 다시 입력해 주세요"
            return False,error_message
    else:
        error_message = "유효기간을 다시 입력해 주세요"
        return False,error_message
    # print ("effectiveterm : ", effectiveterm) 

    cvcnum = cvcnum #cvc번호
    if cvcnum.isdigit():
        if len(cvcnum)>3:
            error_message = "cvc번호가 3자리가 넘어갑니다. 다시 입력해 주세요"
            return False,error_message
        else:
            cvcnum = cvcnum
    else:
        error_message = "cvc번호를 다시 입력해 주세요"
        return False,error_message
    # print ("cvcnum : ", cvcnum)

    if bill.isdigit() and int(bill) >= 100 and int(bill) <= 1000000000 :
        bill = bill#결제금액
    else:
        error_message = "결제금액을 다시 입력해 주세요"
        return False,error_message
    # print ("bill : ", bill)

    if optionalbill == "":
        optionalbillint = round(int(bill) * (1/11))#부가가치세
        optionalbill = str(optionalbillint)
        payOptionalbill = optionalbill
    elif optionalbill.isdigit() and int(optionalbill) < int(bill):
        payOptionalbill = optionalbill #부가가치세
    else:
        error_message = "부가가치세를 다시 입력해 주세요"
        return False,error_message
    # print ("optionalbill : ", payOptionalbill)

    return True,error_message

##String 데이터 만들기
def make_payStrData(datagubun,uniquecode,installment,newencryption_cardInfo,newcardnum,effectiveterm,cvcnum,bill,optionalbill,payorcancle,payuniqueId):
    Strdata = ""
    paygubun = ""
    spare = ""
    spare = spare.rjust(47," ")
    # print ("payorcancle1",payorcancle)
    if payorcancle == True:
        #paygubun = "                    "
        paygubun = paygubun.rjust(20," ")
    else:
        paygubun = payuniqueId
        paygubun = paygubun.rjust(20," ")
    Strdata = datagubun + uniquecode + newcardnum + installment + effectiveterm + cvcnum + bill + optionalbill + paygubun + newencryption_cardInfo + spare
    # print("Strdata = ", Strdata)
    return Strdata


##카드 데이터 암호화
def make_encryption_cardInfo(cardnum,effectiveterm,cvcnum):
    encard = ""
    eneffec = ""
    encvc = ""
    x = ''
    y = ''
    z = ''
    ac0 = 0
    ac1 = 0
    ac2 = 0
    for i in range(len(cardnum)) :
        x = cardnum[i]
        ac0 = ord(x)
        ac0 += 2
        x = chr(ac0)
        encard += x
    
    for i in range(len(effectiveterm)) :
        y = effectiveterm[i]
        ac1 = ord(y)
        ac1 += 2
        y = chr(ac1)
        eneffec += y

    for i in range(len(cvcnum)) :
        z = cvcnum[i]
        ac2 = ord(z)
        ac2 += 2
        z = chr(ac2)
        encvc += z

    enc_cardInfo = encard + "|" + eneffec+ "|" + encvc
    enc_cardInfo.ljust(300," ")
    return enc_cardInfo

##카드 데이터 복호화
def make_decryption_cardInfo(newencryption_cardInfo):
    encryption_cardInfo = newencryption_cardInfo.strip()
    encardnum = encryption_cardInfo.split('|')[0]
    eneffectiveterm = encryption_cardInfo.split('|')[1]
    encvcnum = encryption_cardInfo.split('|')[2]
    decardnum = ""
    deeffectiveterm = ""
    decvcnum = ""
    x = ''
    y = ''
    z = ''
    ac0 = 0
    ac1 = 0
    ac2 = 0
    for i in range(len(encardnum)) :
        x = encardnum[i]
        ac0 = ord(x)
        ac0 -= 2
        x = chr(ac0)
        decardnum += x
    
    for i in range(len(eneffectiveterm)) :
        y = eneffectiveterm[i]
        ac1 = ord(y)
        ac1 -= 2
        y = chr(ac1)
        deeffectiveterm += y

    for i in range(len(encvcnum)) :
        z = encvcnum[i]
        ac2 = ord(z)
        ac2 -= 2
        z = chr(ac2)
        decvcnum += z
    

    return decardnum, deeffectiveterm, decvcnum

#데이터 유효성검사-취소
def data_validation_cancle(uniqueId,canclebill,cancleoptionalbill):
    uniqueId = uniqueId
    canclebill = canclebill
    cancleoptionalbill = cancleoptionalbill
    uniqueIdIsTrue = True
    error_message = ""
    global gcOptionalbill
    ##paymentInfo = String 데이터
    uniqueId_gubun, paymentInfo = dbc.select_paymentInfo(uniqueId)
    cancleuniqueId_gubun, canclepaymentInfo = dbc.select_paymentcancleInfo(uniqueId)
    ##결제취소 정보가 있는경우 결제 취소를 더 진행하지 못함 => 추후 부분취소기능 구현시 수정
    if cancleuniqueId_gubun == True:
        error_message = "이미 취소한 결제입니다."
        return False,error_message

    ##결제정보가 존재하는지 파악
    if uniqueId_gubun == True:
        uniqueIdIsTrue = True
    else:
        uniqueIdIsTrue = False
        error_message = "취소가 가능한 결제정보가 존재하지 않습니다."
        return False,error_message
    
    datalength,datagubun,uniquecode,cardnum,installment,effectiveterm,cvcnum,bill,optionalbill,paygubun,spare = unwind_paymentInfo(paymentInfo)
    
    ##취소금액 유효성 판단, 현재는 전체취소 기능 조건으로 결제 금액이랑 취소금액이랑 같지 않으면 진행 X, 추후 부분취소 기능 구현시 수정
    if canclebill.isdigit() and int(canclebill) == int(bill):
        canclebill = canclebill#결제금액
    else:
        error_message = "현재는 전체금액에 대한 취소만 가능합니다. 취소금액을 결제 금액과 같게 입력해 주세요"
        return False,error_message
    # print ("canclebill : ", canclebill)


    if cancleoptionalbill == "":
        cancleoptionalbill = optionalbill
        gcOptionalbill = cancleoptionalbill
    elif cancleoptionalbill.isdigit() and int(cancleoptionalbill) < int(canclebill):
        #cancleoptionalbill = cancleoptionalbill #부가가치세
        ##현재 전체취소 기능만 구현하였으므로 부가가치세는 현재 결제정보금액의 부가가치세와 일치시킨다.
        gcOptionalbill = optionalbill
    else:
        error_message = "부가가치세 금액이 올바르지 않습니다. 다시 입력 혹은 입력하지 마세요"
        return False,error_message
    # print ("cancleoptionalbill : ", cancleoptionalbill)
    
    return True,error_message

#String 데이터 조합 - 취소
def make_cancle_paymentinfo(uniqueId,canclebill,payorcancle):
    uniqueId = uniqueId
    canclebill = canclebill
    ##paymentInfo = String 데이터
    uniqueId_gubun, paymentInfo = dbc.select_paymentInfo(uniqueId)
    payorcancle = payorcancle

    datalength,datagubun,uniquecode,cardnum,installment,effectiveterm,cvcnum,bill,optionalbill,paygubun,spare = unwind_paymentInfo(paymentInfo)
    datagubun = "CANCLE"
    installment = "00"
    cardnum = cardnum.strip()
    effectiveterm = effectiveterm.strip()
    cvcnum = cvcnum.strip()

    encryption_cardInfo = make_encryption_cardInfo(cardnum,effectiveterm,cvcnum)

    newcardnum = cardnum.ljust(20,' ')
    newbill = canclebill.rjust(10,' ')
    newoptionalbill = optionalbill.rjust(10,'0')
    newencryption_cardInfo = encryption_cardInfo.ljust(300,' ')
    datagubun = datagubun.ljust(10,' ')
    cancle_uniqueId = random_string()
    payuniqueId = uniquecode
    # print("payorcancle",payorcancle)
    cancle_string_data = make_payStrData(datagubun,cancle_uniqueId,installment,newencryption_cardInfo,newcardnum,effectiveterm,cvcnum,newbill,newoptionalbill,payorcancle,payuniqueId)
    datalength = len(cancle_string_data)
    datalengthStr = str(str(datalength).rjust(4,' '))
    cancle_string_data = datalengthStr + cancle_string_data
    # print("Final_data = ", cancle_string_data)
    return cancle_string_data,cancle_uniqueId    



##결제정보 복호화 함수
def unwind_paymentInfo(paymentInfo):
    datalength = paymentInfo[0:4]
    datagubun = paymentInfo[4:14]
    uniquecode = paymentInfo[14:34]
    newcardnum = paymentInfo[34:54]
    installment = paymentInfo[54:56]
    effectiveterm = paymentInfo[56:60]
    cvcnum = paymentInfo[60:63]
    bill = paymentInfo[63:73]
    optionalbill = paymentInfo[73:83]
    paygubun = paymentInfo[83:103]
    newencryption_cardInfo = paymentInfo[103:403]
    spare = paymentInfo[403:450]

    cardnum,effectiveterm,cvcnum = make_decryption_cardInfo(newencryption_cardInfo)
    op_bill = list(optionalbill)
    countopbill = 0
    newoptionalbill = ""
    for i in range(len(op_bill)):
        if op_bill[i] != "0":
            countopbill = i
            break
    newoptionalbill = optionalbill[countopbill:10]
    return datalength,datagubun,uniquecode,cardnum,installment,effectiveterm,cvcnum,bill,newoptionalbill,paygubun,spare



##결제정보 조회 함수 return json
def paymentInfoSelect(uniqueId,paygubun):
    isTrue = True
    paymentInfo = ""
    if paygubun == "payment":
        isTrue,paymentInfo = dbc.select_paymentInfo(uniqueId)
    else:
        isTrue,paymentInfo = dbc.select_paymentcancleInfo(uniqueId)

    datalength,datagubun,uniquecode,cardnum,installment,effectiveterm,cvcnum,bill,optionalbill,originalId,spare = unwind_paymentInfo(paymentInfo)

    paymentInfo_json = {}
    paymentInfo_json['data'] = []
    if paygubun == "payment":
        paymentInfo_json['data'].append({"관리번호 ": uniquecode, "카드번호 ": cardnum, "유효기간 ": effectiveterm,"cvc번호" : cvcnum,"결제구분 ": paygubun,"결제금액 ": bill,"부가가치세 ": optionalbill}) 
    else:
        paymentInfo_json['data'].append({"관리번호 ": uniquecode, "카드번호 ": cardnum, "유효기간 ": effectiveterm,"cvc번호 ": cvcnum,"결제구분 ": paygubun,"결제금액 ": bill,"부가가치세 ": optionalbill,"결제관리번호 ": originalId}) 
    
    
    paymentInfo_jsondata = json.dumps(paymentInfo_json, sort_keys=True, indent=4, ensure_ascii = False)
    # print(paymentInfo_jsondata)
    return paymentInfo_jsondata

##결제정보 조회 함수 return json
def insertpaymentinfo(result,uniqueId):
    payOk = dbc.insert_paymentInfo(result,uniqueId)
    if payOk == True:
        return True 
    
##결제정보 조회 함수 return json
def insertcanclepaymentinfo(result,cancleuniqueId,uniqueId):
    cancleOk = dbc.insert_canclepaymentInfo(result,cancleuniqueId,uniqueId)
    if cancleOk == True:
        return True




