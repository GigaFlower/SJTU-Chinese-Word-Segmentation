#一些（可能）实用的Python技巧
##List Comprehending
##列表解析
####一种生成列表的简单方法
	常规方法：
	l = [ ]
	for i in range(10):
		l.append(i)
		
	使用列表理解：
	l = [i for i in range(10)]
	
	多个变量也是可以的
	从（0，0）到（9，9）的所有坐标点：
	l = [(x,y) for x in range(10) for y in range(10)]
	
	加上if条件限制也是可以的
	l = [x for x in range(10) if x%2 == 0]
	
	更复杂的例子：
	输出小于100的素数表：
	l = [x for x in range(2,100) if 0 not in [x%p for p in range(2,int(x**0.5)+1)]]

##lambda函数
##匿名函数
####一种生成函数的简单方法
	常规函数：
	def f(x):
		return x+1
	
	匿名函数：
	f = lambda x:x+1
	
	注：def是语句而lambda是表达式
	可以将lambda赋给变量而不能把def赋给变量
	
	没有返回值也可以
	f = lambda x:print(x)
	
	多个参数也可以
	f = lambda x,y,z:x+y+z
	
	没有参数也可以
	f = lambda: print("I'm called!")

	稍微复杂一点的例子：
	f = lambda seq:[i**2 for i in seq]
	f([1,2,3]) returns [1,4,9]
	
	
##zip函数
####zip函数是一个内置函数，意思是‘拉链’
	e.g.
	zip([1,2,3,4],[5,6,7,8]) -> [(1,5),(2,6),(3,7),(4,8)]