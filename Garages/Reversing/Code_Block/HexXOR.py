def xor_hex_strings(hex_str1, hex_str2):
    # 입력된 16진수 문자열을 16진수 정수로 변환합니다.
    int1 = int(hex_str1, 16)
    int2 = int(hex_str2, 16)
    
    # 두 정수를 XOR 연산합니다.
    result_int = int1 ^ int2
    
    # 결과를 16진수 문자열로 변환합니다.
    result_hex = hex(result_int)[2:]  # [2:]는 '0x'를 제거하기 위해 사용됩니다.
    
    # 결과 문자열의 길이가 홀수인 경우 앞에 '0'을 추가합니다.
    if len(result_hex) % 2 != 0:
        result_hex = '0' + result_hex
    
    return result_hex

# 두 개의 16진수 문자열 입력
hex_str1 = "1a3f"
hex_str2 = "259b"

xor_result = xor_hex_strings(hex_str1, hex_str2)

print(f"{hex_str1} XOR {hex_str2} = {xor_result}")
