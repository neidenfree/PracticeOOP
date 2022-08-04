from stack import Stack, StackElement

s = Stack()
s.push((1, 2))
s.push([2, 3])
s.push({"some": [2, 3, 4]})
s2 = Stack()
s2.push(s)
s2.push([22])
print(s)

print(s2)
