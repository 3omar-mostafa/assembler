def findTwoscomplement(str):
    i = len(str) - 1
    while(i >= 0):
        if (str[i] == '1'):
            break
        i -= 1

    if (i == -1):
        return '1' + str

    k = i - 1
    str = list(str)

    while(k >= 0):
        str[k] = '1' if str[k] == '0' else '0'
        k -= 1

    return ''.join(str)
