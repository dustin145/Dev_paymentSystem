# 프로젝트명
> Python을 이용하여 결제정보, 결제취소, 결제 및 취소 정보를 조회하는 API를 개발한 프로젝트입니다. 


## 개발 프레임워크
> Flask Framework


## 테이블 설계
* DB : SQLite3
* 결제 테이블
    * id : TEXT 형식, 관리번호, PK, 결제정보의 관리번호
    * string : TEXT 형식, 결제정보의 데이터를 String으로 변환
* 결제 취소 테이블
    * cancle_id : TEXT 형식, 결제취소 관리번호 PK, 결제취소정보의 관리번호
    * string : TEXT 형식, 결제취소정보의 데이터를 String으로 변환
    * id : TEXT 형식, 결제정보의 관리번호


## 문제해결 전략
1. 간단한 API 개발이므로 Python 그 중 Flask 프레임워크를 이용하여 API를 개발한다.
2. 결제시 필요한 정보는 모두 유효성 검사를 진행한다 (ex : 카드번호 자리수, 결제금액 범위, 유효기간 범위, 부가 가치세는 결제금액보다 작아야 한다 등등)
3. MVC패턴을 사용, Post로 결제요청 Data를 받고 해당 Data는 Data_controller로 전송, 유효성 검사를 통과하면, String데이터로 만들어 DB에 전송 결제 정보 Insert 진행  
4. 결제 취소는 부분취소 기능을 구현하지 않았기 때문에 현재는 전체 취소만 가능하도록 설계. 결제 취소시 결제금액이 해당 결제 정보의 금액과 일치하지 않으면 진행 되지 않게 개발
5. 결제 취소시 결제기능과 같이 MVC패턴을 사용, Post로 결제취소 요청을 받고, Data 유효성 검사 진행 후 String 데이터 만들고 결제 취소 정보 Insert
6. 결제 정보 조회는 Get방식을 이용, 현재는 결제정보 관리번호로 조회 중, 결제 취소 관리번호로는 현재 조회 불가능, 결제 취소가 존재 할 경우 결제 취소정보로 조회 진행


## 빌드 및 실행방법

* 빌드 환경
    * python 3.9.5 [다운로드 링크](https://www.python.org/downloads/)
    * flask 1.1.4 : 파이썬 설치 후 (`pip install flask`)
    * SQLite3 : SQLite3 파이썬 설치 시 자동 설치
* DB Setting
    * 'paymentinfo.db'파일 경로를 'db_connect.py'의 'DATABASE_NAME'로 설정한다. 
    * 현재 해당 'paymentinfo.db'에는 'paymentinfo'와 'cancle_paymentinfo'테이블이 생성되어 있다.
    * 해당 DB 말고 새로 DB를 생성할 경우 DB 생성 후 해당 DB 경로를 'db_connect.py'의 'DATABASE_NAME'로 설정한다. 
* 실행방법
    * 현재 View에 해당하는 Html이 존재하지 않기 때문에 Postman[다운로드 링크](https://www.postman.com/downloads/)으로 API 테스트 진행
    * 결제 API는 http://localhost:8080/pay로 Post방식으로 실행, body는 Json형식으로 ex(
        ~~~json
        {
            "cardnum" : "123456789123456",
            "effectiveterm" : "1125",
            "cvcnum" : "777",
            "installment" : "0",
            "bill" : "110000",
            "optionalbill" : "10000"
        }
        ~~~
        )로 보낸다. 정상적으로 작동 시 결제정보 관리번호와, String데이터가 return된다.

    * 결제 취소 API는 http://localhost:8080/cancle로 Post방식으로 실행, body는 Json형식으로 ex(
        ~~~json
        {
            "uniqueId" : "VOLSVBDSCHNNIGNWLIFE",
            "canclebill" : "110000",
            "cancleoptionalbill" : ""
        }
        ~~~
    )로 보낸다. 정상적으로 작동 시 결제취소정보와 결제취소관리번호가 return된다.

    * 결제 및 결제취소 정보 조회 API는 http://localhost:8080/payinfo?id={결제정보 관리번호}로 Get방식으로 실행한다.
    ex(http://localhost:8080/payinfo?id=VOLSVBDSCHNNIGNWLIFE)

    



