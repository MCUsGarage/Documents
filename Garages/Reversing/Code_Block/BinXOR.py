def xor_binary_strings(bin_str1, bin_str2):
    # 입력된 이진 문자열을 2진수 정수로 변환합니다.
    int1 = int(bin_str1, 2)
    int2 = int(bin_str2, 2)
    
    # 두 정수를 XOR 연산합니다.
    result_int = int1 ^ int2
    
    # 결과를 이진 문자열로 변환합니다.
    result_bin = bin(result_int)[2:]
    
    # 결과 문자열의 길이가 짧은 쪽에 맞춰서 앞에 '0'을 채웁니다.
    max_length = max(len(bin_str1), len(bin_str2))
    result_bin = result_bin.zfill(max_length)
    
    return result_bin

# 두 개의 이진 문자열 입력
bin_str1 = "110101"
bin_str2 = "101011"

xor_result = xor_binary_strings(bin_str1, bin_str2)

print(f"{bin_str1} XOR {bin_str2} = {xor_result}")
