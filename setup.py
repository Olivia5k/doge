from setuptools import setup

setup(
    name='doge',
    version='0.1-dev',
    url='https://github.com/thiderman/doge',
    author='Lowe Thiderman',
    author_email='lowe.thiderman@gmail.com',
    description=('wow very doge'),
    license='MIT',
    entry_points={
        'console_scripts': [
            'doge = doge.doge:main'
        ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
    ],
)
