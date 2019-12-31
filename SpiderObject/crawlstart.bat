::请提前安装python3.7，并将其添加到环境变量
::进入requirement.txt所在的目录
@set /p reqPwd=请输入requirement.txt文件所在的路径: 
@echo 您输入的路径为：
@echo %reqPwd%
@cd /d %reqPwd%
@echo 安装python依赖开始
@pip install --no-index --find-links=.\packages\ -r requirements.txt
@echo 安装python依赖完毕
::加入程序工作目录，并执行python程序启动脚本
@set /p projPwd=请输入程序工作目录（如项目含requirements.txt文件，则为该文件所在路径）：
@echo 进入项目路径
@echo %projPwd%
@cd /d %projPwd%
@echo 程序运行开始
@python .\SpiderObject\startAllSpiders.py
@echo 程序运行结束
pause
