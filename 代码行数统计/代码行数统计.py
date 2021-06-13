import os
extract = ['.java','.py','.cpp','.c','.h','.cs']
# 两年课程代码
# paths = [r"./", 'D:/MyFiles/数据库课设', 'D:/D_backup']
# paths += ['D:/Junior Spring/Artificial Intelligence Ⅱ', 'D:/Junior Spring/autoClock', 'D:/Junior Spring/Computer Networks', 'D:/Junior Spring/Computer System Engineering Training/Task 3', 'D:/Junior Spring/Data Mining', 'D:/Junior Spring/Digital Image Processing and Experiment/数字实验备份/结课实验/上传GitHub', 'D:/Junior Spring/Discrete Mathematics Ⅲ']
# paths += ['D:/Junior Spring/Compiling Principle/大实验/综合实验提交_钟路迦_2017309040213/源程序及测试文件']
# # 安卓不算 'D:/Junior Spring/Development Technology of Mobile Software/submit'
# paths += ['D:/Junior Spring/Software Engineering/Project/LaboratoryAnimalHousing']

paths = ['YOLOv3源码学习']

value_n = [0, 0, 0, 0, 0, 0] #java, py, cpp, c, h, cs
values = [0, 0, 0, 0, 0, 0] #java, py, cpp, c, h, cs
for path in paths:
	for root, dirs, files in os.walk(path, topdown=False):
	    for name in files:
	        last = os.path.splitext(name)[1]
	        if last in extract:
	            if last == ".cs":
	                if "Program" in name or "Designer" in name or "AssemblyInfo" in name:
	                    continue
	            temp_num = 0
	            try:
	                with open(os.path.join(root,name),"r",encoding="UTF-8") as file:
	                    temp_num = len(file.readlines())
	            except:
	                try:
	                    with open(os.path.join(root,name)) as file:
	                        temp_num = len(file.readlines())
	                except:
	                    continue      
	            values[extract.index(last)] += temp_num
	            value_n[extract.index(last)] += 1
            

print("java    nums: {:<4} lines: {:<6}".format(value_n[0],values[0]))
print("python  nums: {:<4} lines: {:<6}".format(value_n[1],values[1]))
print("c & c++ nums: {:<4} lines: {:<6}".format(sum(value_n[2:5]),sum(values[2:5])))
print("c#      nums: {:<4} lines: {:<6}".format(value_n[5],values[5]))
print("sum     nums: {:<4} lines: {:<6}".format(sum(value_n),sum(values)))