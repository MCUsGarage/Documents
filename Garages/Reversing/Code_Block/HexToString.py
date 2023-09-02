def hex_to_string(hex_string):
    try:
        # 16진수 문자열을 바이트로 디코딩합니다.
        decoded_bytes = bytes.fromhex(hex_string)
        
        # 바이트를 문자열로 디코딩합니다. 여기서는 UTF-8을 사용합니다.
        decoded_string = decoded_bytes.decode('utf-8')
        
        return decoded_string
    except ValueError:
        # 유효하지 않은 16진수 문자열인 경우 예외 처리합니다.
        return "유효하지 않은 16진수 문자열입니다."

# 변환할 16진수 문자열 입력
hex_string = "48656c6c6f2c20576f726c6421"  # 예시 16진수 문자열

string_result = hex_to_string(hex_string)

print("원본 16진수 문자열:", hex_string)
print("문자열로 변환된 문자열:", string_result)
