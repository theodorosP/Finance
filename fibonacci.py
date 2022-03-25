import pandas as pd
while True:
	try:
		x = input("Please choose: upward/downward: ")
		if x != "upward" and x !="downward" :
			raise NameError
	except(NameError):
		print("Please give a value upward or downward to continue...")
		
	else:
		break


if x == "upward":
	while True:
		try:
			up = float(input("Please give the upper limit: "))
			down = float(input("Please give the lower limit: "))
		except(ValueError, NameError):
			print("Please give a float number: ")
		else:
			break
	
	while down > up:	
		print("Please be careful. You chose upper trend. \n Upper limit must be greater than lower limit \n and/or numbers must be floats")
		try:	
			up = float(input("Please give the upper limit: "))
			down = float(input("Please give the lower limit: "))    	
		except(ValueError, NameError):
				print("Please give a float number")
	while True:
		try:
			custom = float(input("Please give the custom point: "))
		except:
			print("Please give a float number")
		else:
			break
	dif = up - down
	extension = [2.618, 2, 1.618, 1.382, 1, 0.618, 0.5, 0.382, 0.236]
	ext = {}
	l = [0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.272, 1.1618]
	total = {}
	for i in range(0,len(l)):
		total["Level %s" %( str(round(l[i]*100, 2)))+"%"] = round(up - (dif*l[i]), 3)
	
	for i in range(0, len(extension)):
		ext["extension %s" %( str(round(extension[i]*100, 2)))+"%"] = round(custom + (dif*extension[i]), 3)
	print("="*80)
	df1 = pd.DataFrame(list(total.items()),columns = ['Fibonacci retracement','possible support']) 
	df2 = pd.DataFrame(list(ext.items()),columns = ['Fibonacci extension','posible value']) 
	print(df1)
	print("="*80)
	print(df2)
	print("="*80)
	print("Please be careful if the price moves bellow: ", total["Level 61.8%"] )
	print("="*80)
	print("BE CAREFUL if you se the price in: [", round(total["Level 61.8%"]-0.05*total["Level 61.8%"], 3) ,", ", round(total["Level 61.8%"]+0.05*total["Level 61.8%"],3), "]" )
	print("="*80)
	print("Possible support between: [", round(total["Level 61.8%"], 3), ", ", round(total["Level 38.2%"],3), "]")
	print("="*80)

if x == "downward":
	while True:
		try:
			up = float(input("Please give the upper limit: "))
			down = float(input("Please give the lower limit: "))
		except(ValueError, NameError):
			print("Please give a float number: ")
		else:
			break
	
	while down > up:	
		print("Please be careful. You chose upper trend. \n Upper limit must be greater than lower limit \n and/or numbers must be floats")
		try:	
			up = float(input("Please give the upper limit: "))
			down = float(input("Please give the lower limit: "))    	
		except(ValueError, NameError):
				print("Please give a float number")
	while True:
		try:
			custom = float(input("Please give the custom point: "))
		except:
			print("Please try again")
		else:
			break
	dif = up - down
	l = [1.382, 1 , 0.764, 0.618, 0.5, 0.382, 0.236]
	extension = [0.236, 0.382, 0.5, 0.618, 1, 1.382, 1.618, 2, 2.618]
	total = {}
	ext = {}
	for i in range(0,len(l)):
		total["Level %s" %( str(round(l[i]*100, 2)))+"%"] = round(down + (dif*l[i]), 3)
	print("="*80)
	print("Possible trend change if the value moves up: ", total["Level 61.8%"] )
	print("="*80)
	print("Possible resitance between: [", round(total["Level 23.6%"], 3), ", ", round(total["Level 61.8%"],3), "]")
	print("="*80)
	for i in range(0, len(extension)):
		ext["extension %s" %( str(round(extension[i]*100, 2)))+"%"] = round(custom - (dif*extension[i]), 3)
	df1 = pd.DataFrame(list(total.items()),columns = ['Fibonacci retracement','possible resistance']) 
	df2 = pd.DataFrame(list(ext.items()),columns = ['Fibonacci extension','posible value']) 
	print(df1)
	print("="*80)
	print(df2)
	print("="*80)
