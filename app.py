from os import error
from flask import Flask, jsonify, request
import db_controller as dbc
import data_controller as dc

app = Flask(__name__)
payorcancle = True #결제 및 취소 여부 판단 bool

#get 결제 정보 조회
##결제만 : payment , 취소 : cancle, 관리번호 존재 X : nothing
@app.route('/payinfo', methods=["GET"])
def paymentinfoGet():
    uniqueId = request.args.get('id')
    print(uniqueId)
    paygubun = dbc.select_payorcancle(uniqueId)
    if paygubun == "payment" or paygubun == "cancle":
        paymentData = dc.paymentInfoSelect(uniqueId,paygubun)
        print(paymentData)
        return paymentData
    else:
        return "관리번호가 존재하지 않습니다."

#post 결제 내용 insert
@app.route('/pay', methods=["POST"])
def paymentPost():
    payInfo = request.get_json()
    cardnum = payInfo["cardnum"] #카드정보
    installment = payInfo["installment"] #할부개월수
    effectiveterm = payInfo["effectiveterm"] #유효기간
    cvcnum = payInfo["cvcnum"] #cvc번호
    bill = payInfo["bill"] #결제금액
    optionalbill = payInfo["optionalbill"] #부가가치세 있을수도 있고 없을수도 있음
    # print ("cardnum : ",cardnum," effectiveterm : ",effectiveterm," cvcnum : ",cvcnum," bill : ",bill)
    #데이터 유효성 검사 진행
    validation,error_message = dc.data_validation(cardnum,installment,effectiveterm,cvcnum,bill,optionalbill)
    print("validation",validation)
    if validation:
        result,uniqueId = dc.make_encryption(cardnum,effectiveterm,cvcnum,bill,payorcancle)
        dc.insertpaymentinfo(result,uniqueId)
        return result,uniqueId
    else:
        return error_message


#post 결제 취소
@app.route('/cancle', methods=["POST"])
def paymentcanclePost():
    payInfo = request.get_json()
    uniqueId = payInfo["uniqueId"] #관리번호
    canclebill = payInfo["canclebill"] #취소금액
    cancleoptionalbill = payInfo["cancleoptionalbill"] #부가가치세
    print ("uniqeId : ",uniqueId," canclebill : ",canclebill, "optionalbill : ",cancleoptionalbill)
    #데이터 유효성 검사 진행
    payorcancle = False
    validation_cancle,error_message = dc.data_validation_cancle(uniqueId,canclebill,cancleoptionalbill)
    print("validation_cancle",validation_cancle,"에러 = ",error_message)
    if validation_cancle:
        result,cancleuniqueId = dc.make_cancle_paymentinfo(uniqueId,canclebill,payorcancle)
        dc.insertcanclepaymentinfo(result,cancleuniqueId,uniqueId)
        return result,cancleuniqueId
    else:
        return error_message


if __name__ == "__main__":
    """
    Here you can change debug and port
    Remember that, in order to make this API functional, you must set debug in False
    """
    app.run(host='0.0.0.0', port=8080, debug=True)    