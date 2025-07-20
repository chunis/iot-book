#!/bin/bash
# 脚本的第一行叫 shebang，用来告知系统如何执行该脚本:
# 参见： http://en.wikipedia.org/wiki/Shebang_(Unix)
# 如你所见，注释以 # 开头，shebang 也是注释。

# 简单的hello world示例
echo "Hello world!" # 输出：Hello world!

# 每一句指令以换行或分号隔开
echo "This is the first command"; echo "This is the second command"
# 输出：This is the first command
# 输出：This is the second command

# 声明一个变量：
variable="Some string"

# 下面是错误的做法：
variable = "Some string" # 输出：返回错误："variable: command not found"
# Bash 会把 Variable 当做一个指令，由于找不到该指令，因此这里会报错。

# 也不可以这样：
variable= "Some string" # 输出：返回错误："Some string: command not found"
# Bash 会认为 'Some string' 是一条指令，由于找不到该指令，这里再次报错。
# （这个例子中 'Variable=' 这部分会被当作仅对 'Some string' 起作用的赋值。）

# 使用变量：
echo "$Variable"
echo '$Variable'
# 当你赋值 (assign) 、导出 (export)，或者以其他方式使用变量时，变量名前不加 $。
# 如果要使用变量的值， 则要加 $。
# 注意： ' (单引号) 不会展开变量（即会屏蔽掉变量）。

# 在变量内部进行字符串代换
echo "${variable/Some/A}" # 输出：A string
# 会把 Variable 中首次出现的some替换成 A。

# 字符串长度:
echo "${#variable}" # 输出：11

# 变量的默认值
echo ${Foo:-"DefaultValueIfFooIsMissingOrEmpty"}
# 对 null (Foo=) 和空串 (Foo="") 起作用； 零（Foo=0）时返回0
# 注意这仅返回默认值而不是改变变量的值

# 内置变量
echo "Last program's return value: $?"
echo "Script's PID: $$"
echo "Number of arguments passed to script: $#"
echo "All arguments passed to script: $@"
echo "Script's arguments separated into different variables: $1 $2..."

# 大括号扩展 {...}
echo {1..10} # 输出：1 2 3 4 5 6 7 8 9 10
echo {a..z} # 输出：a b c d e f g h i j k l m n o p q r s t u v w x y z

# 命令`clear`用于清理屏幕，同样适用于Windows的CMD清屏:
clear  # 快捷键Ctrl-L提供了同样的功能.

# 读取输入：
echo "What's your name?"
read Name # 这里不需要声明新变量
echo "Hello, $Name!"

# 通常的 if 结构看起来像这样：
if [ $Name -ne $USER ]; then
    echo "Your name isn't your username"
else
    echo "Your name is your username"
fi

# 在 if 语句中使用 && 和 || 需要多对方括号
if [ $Name == "Steve" ] && [ $Age -eq 15 ]; then
    echo "This will run if $Name is Steve AND $Age is 15."
fi

if [ $Name == "Daniya" ] || [ $Name == "Zach" ]; then
    echo "This will run if $Name is Daniya OR Zach."
fi

# 针对数字进行比较还有如下操作符：
# -ne（不等于）； -lt (小于）； -gt（大于）
# -le （小于或等于）；-ge（大于或等于）

# 根据上一个指令执行结果决定是否执行下一个指令
echo "Always run" || echo "Only run if first command fails"
# 输出：Always run
echo "Always run" && echo "Only run if first command does NOT fail"
# 输出：Always run
# 输出：Only run if first command does NOT fail

# 在命令后添加 & 会将命令放到后台运行，此时命令的输出仍然显示到终端，但是无法从终端进行输入。
sleep 30 &
jobs  # 列出后台任务
# 输出：[1]+  Running          sleep 30 &
# Ctrl-C 用于杀死进程, Ctrl-Z 用于挂起进程使其暂停执行
fg  # 将后台任务转为前台任务
bg  # 将通过 Ctrl-Z 挂起的当前进程放入后台运行
kill %2  # 杀死后台任务号为2的进程

# 表达式的格式如下:
echo $(( 10 + 5 )) # 输出：15

# 通过子shell进行跨目录操作
(echo "First, I'm here: $PWD") && (cd someDir; echo "Then, I'm here: $PWD")
pwd # 当前shell仍然在初始目录下

# 创建新的目录
mkdir myNewDir
# 用`-p` 标志可以创建不存在的中间层目录
mkdir -p myNewDir/with/intermediate/directories

# 重定向输入和输出（标准输入，标准输出，标准错误）。
# 以 ^EOF$ 作为结束标记从标准输入读取数据并覆盖hello.py。
cat > hello.py << EOF
#!/usr/bin/env python
from __future__ import print_function
import sys
print("#stdout", file=sys.stdout)
print("#stderr", file=sys.stderr)
for line in sys.stdin:
    print(line, file=sys.stdout)
EOF

# 重定向可以到输出，输入和错误输出。
python hello.py < hello.py # 将文件hello.py自身作为脚本的输入
python hello.py > output.out # 重定向脚本输出到文件output.out
python hello.py 2> error.err # 重定向错误输出到文件error.err
python hello.py > output-error.log 2>&1  # 同时重定向输出和错误
python hello.py > /dev/null 2>&1 # 重定向输出和错误到/dev/null（即丢弃所有输出和错误）
python hello.py >> output.out 2>> error.err # 以添加而非覆盖的方式进行重定向

# 一个指令可用 $( ) 嵌套在另一个指令内部：
# 以下的指令会打印当前目录下的目录和文件总数
echo "There are $(ls | wc -l) items here."

# 反引号 `` 起相同作用，但不允许嵌套，因此建议优先使用 $(  ).
echo "There are `ls | wc -l` items here."

# Bash 的 case 语句与 Java 和 C++ 中的 switch 语句类似:
case "$Variable" in
    # 列出需要匹配的模式
    0) echo "There is a zero.";;
    1) echo "There is a one.";;
    *) echo "It is not null.";;  # 匹配所有情况
esac

# 循环遍历给定的参数序列:
# 变量 a 的值会被打印 3 次。
for a in {1..3}
do
    echo "$a"
done

# 传统的 for循环 格式，和上面的代码等价
for ((a=1; a <= 3; a++))
do
    echo $a
done

# 也可以用于遍历文件或者命令的输出，并且支持模式匹配
for Variable in file1 file2; do cat "$Variable"; done
for Output in $(ls); do cat "$Output"; done
for Output in ./*.markdown; do cat "$Output"; done

# while 循环
while [ true ]
do
    echo "loop body here..."
    break
done

# 函数定义
foo ()
{
    echo "Arguments work just like script arguments: $@"
    echo "And: $1 $2..."
    returnValue=0
    return $returnValue
}

# 调用函数 `foo` 并提供arg1和arg2作为参数:
foo arg1 arg2
# 输出：Arguments work just like script arguments: arg1 arg2
# 输出：And: arg1 arg2...

foo # 不提供参数调用函数 `foo`:
# 输出：Arguments work just like script arguments:
# 输出：And:  ...

# 可通过$?获得函数的返回值
resultValue=$?

# `trap`命令可以用于当脚本接收到某些信号时执行指定的命令
# 如下述语句使得当脚本接收到列出的三种信号中的任意一种时，运行rm来删除文件并退出。
trap "rm $TEMP_FILE; exit" SIGHUP SIGINT SIGTERM
