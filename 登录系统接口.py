import os,json,random

def main_show():
	'''进入主页展示'''
	login_message = '''
-------------------------------------------------------------
					您好，欢迎来到京东二货市场
-------------------------------------------------------------
		【1】 登录		【2】 注册		【3】	解锁		【q】 退出
-------------------------------------------------------------
'''
	print(login_message)

def test_file(file):
	'''
	验证存储用户的文件是否存在，不存在就生成
	：parma file：文件名
	：return：无返回值
	'''
	if os.path.exists(file):
		pass
	else:
		with open(file,'w+') as f:
			users = {}
			json.dump(users,f)

def read_file(file):
	'''
	从用户文件中读取用户列表，以方便进行验证
	：param file: 文件名
	：return: 返回读取的用户列表
	'''
	with open(file,'r+') as fr:
		users = json.load(fr)
	return users

def write_file(users,file):
	'''
	把修改后的用户列表重新写入进去
	：param users：用户名列表
	：param file： 文件名
	'''
	with open(file,'w+') as fw:
		json.dump(users,fw)

def random_code(length):
	'''
	随机验证码生成模块
	：param length： 验证码的长度，自己定义多长的验证码，开发人员自己制定
	：return：返回生成的随机验证码
	'''
	codes = []
	for i in range(length):
		num = random.randrange(length)
		if i == num:
			code = random.randint(0,9)
			codes.append(str(code))
		else:
			#小写字母随机验证符
			capital_codes = list(range(65,91))
			#大写字母随机验证符
			capital_codes.append(list(range(97,123)))
			#随机挑选出一个元素
			tem_code = random.choice(capital_codes)
			codes.append(chr(tem_code))
	rand_code = ''.join(codes)
	return rand_code

def log_in(users):
	'''
	登录模块
	：param user: 用户名
	：param pwd: 密码
	：param users: 用户列表
	:return: 无返回值
	'''
	flag = True
	while flag:
		user = input('请输入您的名字：')
		if user in users.key():
			'''判断用户名是否存在，存在之后验证是否锁定，
			如果锁定，告诉联系员解锁
			'''
			if user[user][1] == 'locked':
				print('对不起，您输入的密码已经锁定，请辽西管理员解锁！！！')
				break
			'''
			我们知道，我们登录网站都是先验证用户名存不存在，如果存在了，就输入密码，
			但是不会先验证密码，而是验证码输入之后，验证码验证是否正确，如果正确才会验证密码
			'''
			pwd = input('请输入您的密码')
			'''
			输入验证码，并且先验证验证码是否正确，验证码输入是没有限制的，一直到你输入对为止
			'''
			while True:
				#调用随机验证码函数，生成一个6位数的随机验证码
				random_num = rand_code(6)
				print('验证码：'，random_num)
				verification_code = input('请输入验证码：').lower()
				if verification_code == random_num.lower():
					break
				else:
					print('验证码输入有误，请重新输入：')
					continue
			'''
			验证码验证完毕之后，去验证密码，密码和验证码不一样，密码是有输入次数限制的，密码只能输入三次
			'''
			try_num = 0
			while try_num < 3:
				if pwd == users[user][0]:
					print('登录成功，欢迎来到京东二手市场！')
					flag = False
					break
				elif try_num !=2:
					print('您输入的密码有误，你还有%s次锁定用户！' %(2-try_num))
					pwd = input('请输入您的密码：')
				else:
					print('您输入的密码次数过多，账户已经锁定，请联系管理员解锁！')
					users[user][1] = 'locked'
					flag = False
					break
				try_num += 1
		else:
			print('对不起，您输入的用户名没有注册！！！')
			break
	return users

def register(status = 'unlocked'):
	'''
	进行注册，注册之后写入文件内部，默认都是内有锁定的
	：return: 无返回值，只是注册时候重新写入文件库
	'''
	message = '''
	--------------------------------------------------------------
		\033[34;1m 欢迎来到注册平台，请按照下面提示进行注册\033[0m
	--------------------------------------------------------------
	'''
	flag = True
	while flag:
		username = input('请出入你的用户名：')
		flag = uniqueness_verification(username)
	'''我们知道，密码一般是要输入两次的，两次一致才算成功'''
	while True:
		pwd1 = input('请输入您的密码：')
		pwd2 = input('请再次输入密码：')
		if pwd1 == pwd2:
			break
		else:
			print('两次输入的密码不一致，请重新输入：')
	while True:
		telephone_num = input('请输入你的手机号：')
		if len(telephone_num) == 11:
			break
		else:
			print('对不起，您输入的手机号码有误，请重新输入！！')
	'''都输入完成之后，要存入到文件中
	注册验证码都是最后输入的，输入只需要正确就可以，没说验证码要在密码验证前面
	'''
	while True:
		random_num = random_code(4)
		print('\033[31m验证码：%\033[0m' % random_num)
		input_num = input('请输入验证码：')
		#统一转化为小写，这样就不用在意用户输入什么
		if random_num.lower() == input_num.lower():
			break
		else:
			print('您输入的验证码有误，请重新输入！')
		filename = 'users_file'
		users = read_file(filename)
		users[username] = [pwd1,status,telephone_num]#新增注册
		print('恭喜你，注册成功！')
		'''注册成功之后，写入文件'''
		write_file(users,filename)

def uniqueness_verification(username):
	'''
	用户名唯一性验证，我们知道，用户名是不允许重复的，其实手机号也有唯一约束，
	但是我们知道，手机号总是经常改变，
	：param username: 用户名
	：return: 无返回值
	'''
	flag = False
	filename = 'users_file'
	users = read_file(filename)
	if username in users.key():
		print('对不起，您输入的用户名已经注册，请重新输入！')
		return True
	else:
		return flag

def unlocked(filename):
	'''
	管理员进行解锁，正常来说只有管理员才能够解锁，这样就只能载添加控制条件了，不过也没有关系，就当练习尝试了
	不过超级管理员都是在一个文件单独存放的，只有练习超级管理员才能够解锁，需要一些验证，才能够登超级管理员
	这里因为没有太好的办法来交互了，就用户自己解锁，通过手机号，这个还是很多网站常用的找回密码的方法，只要修改了密码
	就当重新解锁了，支付宝也是这样操作的
	：param filename：文件名
	：return:
	'''
	'''打开文件，读取用户信息'''
	users = read_file(filename)
	message = '''\033[36;1m
	---------------------------------------------------------------
			【1】修改密码						【2】找回密码
	---------------------------------------------------------------
	\033[0m'''
	print(message)
	flag = True #循环开启和关闭的标志
	while flag:
		function_num = input('请选择您要操作的功能：')
		if not function_num in ['1','2']:
			print('您输入的功能有误，请重新输入！')
			continue
		username = input('请输入用户名：') #判断用户名是否存在
		if username in users.key():
			#通过手机号进修改密码
			while True:
				telephone_num = input('请输入您的手机号：')
				if telephone_num == users[username][2]:
					'''验证码验证'''
					while True:
						rand_num = random_code(4)
						print('验证码：'，rand_num)
						tem_random_code = input('请输入验证码：')
						if rand_num.lower() == tem_random_code.lower():
							break
						else:
							print('您输入的验证码有误，请重新输入！')
					break
				else:
					print('您输入的手机号有误，请重新输入！')
			while True:
				if function_num == '1':
					pwd1 = input('请输入你要修改的密码：')
					pwd2 = input('请再次输入您要修改的密码：')
					if pwd1 == pwd2:
						print('密码修改成功！')
						users[username][0] = pwd1
						users[username][1] = 'unlocked'
						flag = False
						break
					else:
						print('对不起，您两次输入的密码不一致，请重新输入！')
						continue
					elif function_num == '2':
						print('\033[30m您的账户密码是：\033[0m',users[username][0])
						users[username][1] = 'unlocked'
						flag = False
						break
		else:
			print('对不起，您输入的用户没有注册！！！')
			break
	return users #解锁成功之后，返回新的用户民表，并重写写入到文件中

def login_show():
	#登录展示提醒
	show_message = '''
	------------------------------------------------------------------------------------------
							\033[34m 欢迎来到登录界面，请按一下提示完成登录
							如果发现账号锁定，请进行验证解锁，祝你冲浪愉快[0m
	------------------------------------------------------------------------------------------
	'''
	print(show_message)

def register_show():
	'''
	注册展示页面，进行提醒
	：return:
	'''
	show_message = '''
	------------------------------------------------------------------------------------------
						\033[32;1m 欢迎来到注册界面，请按照以下提示完成注册 \033[0m
	------------------------------------------------------------------------------------------
	'''
	print(show_message)

def unlock_show():
	#解锁页面展示
	show_message = '''\033[33;1m
	------------------------------------------------------------------------------------------
						欢迎来到解锁页面，请按照下面的提示进行解锁
						您可以选择找回密码，或者修改密码
	------------------------------------------------------------------------------------------
	\033[0m'''
	print(show_message)

if __name__ == '__main__':
	main_show()
	flag =	True
	while flag:
		choice_num = input('请选择要选择的操作：')
		if choice_num == '1':
			login_show()
			'''判断用户文件是否存在'''
			filename = 'users_file'
			test_file(filename)
			users = read_file(filename)
			users_message = log_in(users)
			write_file(users_message,filename)
		elif choice_num =='2':
			register_show()
			register()
		elif choice_num == '3':
			unlock_show()
			'''修改密码，解除锁定，我们知道，现在网络平台都是通过手机号解锁的，不过要通过验证充当密码'''
			filename = 'users_file'
			users = unlock(filename)
			write_file(users, filename)
		elif choice_num == 'q':
			break
		else:
			print('对不起，找不到您输入编号的功能，请重新输入')
			continue
