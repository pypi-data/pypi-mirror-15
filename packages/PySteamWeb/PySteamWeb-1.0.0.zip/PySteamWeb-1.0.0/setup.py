try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PySteamWeb',
    version='1.0.0',
    packages=['pysteamweb'],
    url='https://github.com/patryk4815/PySteamWeb',
    license='MIT',
    author='Patryk Sondej',
    author_email='patryk.sondej@gmail.com',
    description='python3 steam web login async',
    keywords=['python3', 'steam', 'login', 'api', 'async', 'aiohttp', 'asyncio', 'asynchronous'],
    platforms='Posix; MacOS X; Windows',
    install_requires=[
        'pycrypto>=2.6',
        'aiohttp>=0.21',
    ]
)
