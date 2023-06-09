limit = 7
ml = []


def rec_fibo(limit):
    a, b = 0, 1

    for _ in range(limit - 1):
        a, b = b, a + b
        limit -= 1
    print(b)


rec_fibo(limit)


# fibo(7) => [0,1,1,2,3,5,8] => produces the total of the list
def myrecfibo(n):
    if n == 1 or n == 2:
        return 1
    else:
        return myrecfibo(n - 1) + myrecfibo(n - 2)


print(myrecfibo(7))


def sumdigit(digit):
    if digit // 10 == 0:
        return digit
    else:
        return digit % 10 + sumdigit(digit // 10)


print(sumdigit(6589714785))


def rec_natural(digit):
    if digit < 1:
        return 0
    else:
        return digit + rec_natural(digit - 2)


print(rec_natural(6))


def reciprocal_rec(num):
    if num < 2:
        return 1
    else:
        return 1 / (num) + reciprocal_rec(num - 1)


print(reciprocal_rec(7))


def rec_power(num, power):
    if power == 0:
        return 1
    else:
        return num * rec_power(num, power - 1)


print(rec_power(3, 2))


# Write a Python program to check if a given positive integer is a power of two.
# def check_power(num):
#     if num ==0 :
#         return 1
#     else:
#         return 2*check_power(num-1)



def check_power(num, checking_num):

    tmp = num


    while(tmp>=0):
        if tmp == 0 or tmp == 1:
            return (num,True)

        quo = tmp //checking_num
        rem = tmp % checking_num
        if rem == 1:
            return (tmp,False)
        tmp = quo
    # check_power(quo)

# print([check_power(i) for i in range(1,10)])
print(check_power(65,2))
print(check_power(81,3))
print(check_power(27,3))
print(check_power(9,3))
print(check_power(16,4))
print(check_power(20,4))

# # ip = [1,2,3,4,6,7,10]
# max = max(ip)
# min = min(ip)
# missing = []
# for i in range(min, max):
#     if i not in ip:
#         missing.append(i)
# print(missing)

def num_list(list_to_check):
    ma = max(list_to_check)
    mi = min(list_to_check)
    missing = []
    for i in range(mi, ma):
        if i not in list_to_check:
            missing.append(i)
    return  missing

print(num_list([5,6,8,10,11,14,17]))















