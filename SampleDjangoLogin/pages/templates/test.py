

def copy(s, n):
    if n <= 0:
        return ''
    return s + copy(s, n - 1)

def recursion(word, n):
    return copy(word, n)

new_word = recursion('hello', 5)
print(new_word)

#Question 2

def recursion2(l1, l2, new_count):
    if not l1 or not l2:
        return new_count

    if l1[0] < l2[0]:
        new_count += 1

    return recursion2(l1[1:], l2[1:], new_count)

def compare(l1, l2):
    return recursion2(l1, l2, 0)

l1 = [3, 1, 4, 1, 5]
l2 = [5, 1, 3, 4, 2]
result = compare(l1, l2)
print(result)

#Question 3

def double(s):
    if s == '':
        return ''
    return s[0] * 2 + double(s[1:])



print(copy("hello", 3))
print(compare([5, 3, 7, 9, 1, 3], [2, 4, 7, 8, 3]))
print(double('a'))