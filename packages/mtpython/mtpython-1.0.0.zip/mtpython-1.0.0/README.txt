�����Զ�module
---------------------------------
�������������ú�python��·��
��moduleĿ¼�´�cmd
д������

python setup.py sdist
python setup.py install
---------------------------------

demo�ļ���Ϣ

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

�ϴ����뵽pypi
---------------------------------
http://pypi.python.org/

