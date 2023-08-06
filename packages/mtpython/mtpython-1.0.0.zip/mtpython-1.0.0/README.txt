发布自定module
---------------------------------
环境变量中配置好python的路径
在module目录下打开cmd
写入命令

python setup.py sdist
python setup.py install
---------------------------------

demo文件信息

setup.py
---------------------------------
from distutils.core import setup
setup(
        name = 'mtpython',
        version = '1.0.0',
        py_modules = ['nester'],
        author = 'mcgradytien',
        author_email = '106559363@qq.com',
        url = '',
        description = 'A simple printer of nested lists'
    )
---------------------------------

上传代码到pypi
---------------------------------
http://pypi.python.org/

