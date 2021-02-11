stars = ''

def star(n):
    global stars
    stars += '**'
    if n == 0:
        return
    for i in range(n):
        star(i)

print('Testing 0:')
stars = ''
star(0)
print(len(stars))

print('Testing 1:')
stars = ''
star(1)
print(len(stars))

print('Testing 2:')
stars = ''
star(2)
print(len(stars))

print('Testing 3:')
stars = ''
star(3)
print(len(stars))

print('Testing 4:')
stars = ''
star(4)
print(len(stars))

print('Testing 5:')
stars = ''
star(5)
print(len(stars))

print('Testing 6:')
stars = ''
star(6)
print(len(stars))

