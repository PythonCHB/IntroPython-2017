def print_grid(n):
    halfsize = int(n/2)
    print(halfsize)
    print('+', '- ' * halfsize, end = '')
    print('+', '- ' * halfsize, end = '',)
    print('+')
    for i in range(halfsize):
        print('|', '  ' * halfsize, end = '')
        print('|', '  ' * halfsize, end = '')
        print('|')
    print('+', '- ' * halfsize, end = '')
    print('+', '- ' * halfsize, end = '',)
    print('+')
    for i in range(halfsize):
        print('|', '  ' * halfsize, end = '')
        print('|', '  ' * halfsize, end = '')
        print('|')
    print('+', '- ' * halfsize, end = '')
    print('+', '- ' * halfsize, end = '',)
    print('+')

print_grid(6)
print_grid(0)
print_grid(1)
print_grid(15)
