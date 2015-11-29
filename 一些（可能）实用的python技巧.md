#一些（可能）实用的Python技巧
##List Comprehending
##列表理解
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
	lambda x:x+1