class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")


'''
用例设计原则

文件名以test_*.py文件和*_test.py
以test_开头的函数
以Test开头的类
以test_开头的方法
所有的包pakege必须要有__init__.py文件
 

执行用例#
1.执行某个目录下所有的用例

pytest 文件名/
2.执行某一个py文件下用例

pytest 脚本名称.py
3.-k 按关键字匹配

pytest -k "MyClass and not method"

'''