from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Kevin Stevens',
    author_email='kevin@kstev.com',
    description='Webtron is a tool to deploy static websites',
    license='GPLv3+',
    packages=['webotron'],
    url='https://github.com/kstev/awspython',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)