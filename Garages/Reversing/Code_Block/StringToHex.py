def string_to_hex(input_string):
    # 문자열을 바이트로 인코딩합니다. 여기서는 UTF-8을 사용합니다.
    encoded_bytes = input_string.encode('utf-8')
    
    # 바이트를 16진수 문자열로 변환합니다.
    hex_string = encoded_bytes.hex()
    
    return hex_string

# 변환할 문자열 입력
input_string = "Hello, World!"
hex_result = string_to_hex(input_string)

print("원본 문자열:", input_string)
print("16진수로 변환된 문자열:", hex_result)
