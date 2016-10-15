a = int(input())
b = int(input())
c = int(input())

if a * b == c:
    print("YES")
else:
    print("NO")
    
if a != 0:
    if c == -b / a:
        print("YES")
    else:
        print("NO")
else:
    if b == 0:
        print("YES")
    else:
        print("NO")
