from setuptools import setup

setup(
    name='yolog',
    version='0.1.3',
    description='Beautify your git logs!',
    url='http://github.com/karandesai-96/yolog',
    author='Karan Desai',
    author_email='karandesai281196@gmail.com',
    license='MIT',
    packages=['yolog'],
    entry_points={
        'console_scripts': ['yolog = yolog.main:main']
    },
    zip_safe=True
)
