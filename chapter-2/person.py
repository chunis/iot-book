class Person:
    def __init__(self, age = 0, addr = ''):  # 初始化属性；可以提供默认值
        self.__age = age
        self.addr = addr

    def change_age(self, new_age):
        self.__age = new_age

    def print_age(self):
        print('age:', self.__age)

tom = Person(15, 'Shanghai')
tom.print_age()
tom.change_age(24)
tom.print_age()
print(tom.addr)
print(tom.__age)  # 以两个下划线开头的属性无法从外直接访问
