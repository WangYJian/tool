from math import sqrt


class numberTheory:
    # 判断一个数是否为素数
    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True

    # 判断一个数由哪几个素数组成
    def prime_factorization(self, n):
        result = []
        while n % 2 == 0:
            result.append(2)
            n = n // 2
        for i in range(3, int(sqrt(n)) + 1, 2):
            while n % i == 0:
                result.append(i)
                n = n // i
        if n > 2:
            result.append(n)
        return result

    # 计算在一个数范围内的互质数
    def coprime(self, n):
        result = []
        for i in range(1, n):
            if self.gcd(i, n) == 1:
                result.append(i)
        return result

    # 计算原根
    def primitive_root(self, n):
        result = []
        coprime = self.coprime(n)
        for i in coprime:
            if set([self.big_mod(i, j, n) for j in coprime]) == set(coprime):
                result.append(i)
        return result

    # 计算欧拉函数
    def euler(self, n):
        result = 1
        f = self.prime_factorization(n)

        for i in set(f):
            result = result * (i - 1) * (i ** (f.count(i) - 1))

        return int(result)

    # 计算大指数模
    def big_mod(self, n, exp, mod):
        # 计算指数的二进制表示
        b = self.decimal_to_binary(exp)
        # 翻转二进制表示
        b = b[::-1]
        # 算每一位的结果
        result = []
        for i in range(0, len(b)):
            if i == 0:
                result.append(n % mod)
            else:
                result.append(result[i - 1] ** 2 % mod)
        # 计算最终结果
        final_result = 1
        for i in range(0, len(b)):
            if b[i] == 1:
                final_result = (final_result * result[i]) % mod
        return final_result

    # 计算两个数的线性组合等于它们的最大公约数的解
    def linear_combination(self, a, b):
        # 计算辗转相除法的系数
        coefficient = []
        b1 = b
        a1 = a
        while b1 != 1:
            coefficient.append(a1 // b1)
            a1, b1 = b1, a1 % b1
        # 翻转系数
        coefficient = coefficient[::-1]
        S = [0, 1]
        for i in range(0, len(coefficient)):
            S.append(S[i] - (coefficient[i] * S[i + 1]))
        return S[-1], S[-2], b * S[-1] + a * S[-2]

    # 计算原根
    def primitive_root(self, n):
        result = []
        coprime = self.coprime(n - 1)
        # 获取n - 1的质因数
        prime_factor = set(self.prime_factorization(n - 1))

        for i in range(1, n):
            flag = True
            for j in prime_factor:
                if self.big_mod(i, (n - 1) // j, n) == 1:
                    flag = False
                    break
            if flag:
                result.append(i)
                break

        # 根据第一个原根计算其他原根
        for i in coprime:
            if i != 1:
                result.append(self.big_mod(result[0], i, n))

        return result

    # 计算指标表
    def index_table(self, n):
        # 获取原根
        primitive_root = self.primitive_root(n)[0]
        result = [None] * n
        for i in range(1, n):
            result[self.big_mod(primitive_root, i, n)] = i
        return result

    # 计算逆元
    def inverse_element(self, a, n):
        x, y, gcd = self.linear_combination(a, n)
        if gcd == 1:
            return y % n
        else:
            return None

    # 计算多个数的最大公约数
    def gcd(self, *args):
        result = args[0]
        for i in args[1:]:
            result = self.gcd_two(result, i)
        return result

    # 计算两个数的最大公约数
    def gcd_two(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    # 转换十进制数为二进制数
    def decimal_to_binary(self, n):
        result = []
        while n > 0:
            result.append(n % 2)
            n = n // 2
        return result[::-1]

    # 转换二进制数为十进制数
    def binary_to_decimal(self, num):
        result = 0
        n = num.split('')
        for i in range(0, len(n)):
            result += n[i] * (2 ** i)
        return result
    # 计算余数方程
    def remainder_equation(self, a, b, n):
        # 计算a的逆元
        a_inverse = self.inverse_element(a, n)
        if a_inverse:
            return (a_inverse * b) % n
        else:
            return None




# 计算机网络类
class computerNetwork:
    # 将IP地址转换为二进制数，并给出子网掩码
    def ip_to_binary(self, ip):
        # 单独取出末尾的子网掩码位数
        if '/' in ip:
            ip, mask = ip.split('/')
            mask = int(mask)
        # 将
        # 将前面n位转换为1，后面32 - n位转换为0
        mask = [1] * mask + [0] * (32 - mask)
        # 将子网掩码分为4组
        mask = ["".join([str(i) for i in mask[0:8]]), "".join([str(i) for i in mask[8:16]]),
                "".join([str(i) for i in mask[16:24]]), "".join([str(i) for i in mask[24:32]])]
        ip = ip.split('.')
        result = []
        for i in ip:
            now = "".join([str(i) for i in numberTheory().decimal_to_binary(int(i))])
            # 将每一组ip地址补齐为8位
            now = now + '0' * (8 - len(now))
            result.append(now)

        # 补充ip地址为32位
        result.append('0' * (32 - len("".join(result))))
        return '.'.join(result), '.'.join(mask)

    # 将二进制数转换为IP地址
    def ip_mask_to_decimal(self, ip_bin, mask_bin):
        ip_parts = ip_bin.split('.')
        mask_parts = mask_bin.split('.')

        ip_decimal = [int(part, 2) for part in ip_parts]
        mask_decimal = [int(part, 2) for part in mask_parts]

        ip_address = '.'.join(str(part) for part in ip_decimal)
        mask_cidr = sum(bin(part).count('1') for part in mask_decimal)

        return f'{ip_address}/{mask_cidr}'

# 密码类
class cryptography:
    # 移位密码
    def shift_cipher(self, text, key):
        result = ''
        for i in text:
            if i.isalpha():
                if i.isupper():
                    result += chr((ord(i) + key - 65) % 26 + 65)
                else:
                    result += chr((ord(i) + key - 97) % 26 + 97)
            else:
                result += i
        return result

    # 置换密码
    def substitution_cipher(self, text, key):
        # 将明文分为多个组，每个组的长度为密钥长度
        text = [text[i:i + len(key)] for i in range(0, len(text), len(key))]
        result = ''
        for i in text:
            for j in key:
                result += i[j - 1]
        return result

    # 解置换密码逆置换
    def substitution_cipher_inverse(self, key):
        result = []
        for i in range(0, len(key)):
            result.append(key.index(i + 1) + 1)
        return result

    # 频率分析
    def frequency_analysis(self, text):
        # 先列出英语字母使用频率排序
        frequency = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c',
                     'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x',
                     'q', 'z']
        # 将text转换为小写
        text = text.lower()
        # 分析密文中每个字母出现的频率，存入字典中
        text_frequency = {}
        for i in text:
            if i.isalpha():
                if i in text_frequency:
                    text_frequency[i] += 1
                else:
                    text_frequency[i] = 1
        # 将字母按照出现频率排序
        text_frequency = sorted(text_frequency.items(), key=lambda x: x[1], reverse=True)
        return text_frequency






print(cryptography().frequency_analysis('EMGLOSUDCGDNCUSWYSFHNSFCYKDPUMLWGYICOXYSIPJCKOPKUGKMGOLICGINCGACKSNISACYKZSCKXECJCKSHYSXCGOIDPKZCNKSHICGIWYGKKGKGOLDSILKGGOIUSIGLEDSPWZUGFZCCNDGYYSFUSZCNXEOJNCGYEOWEUPXEZGACGNFGLKNSACIGOIYCKXCJUCIUZCFZCCNDGYYSFEUEKUZCSOCFZCCNCIACZEJNCSHFZEJZEGMXCYHCJUMGKUCY'))
