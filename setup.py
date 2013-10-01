from setuptools import setup

setup(
    name='doge',
    version='0.3',
    url='https://github.com/thiderman/doge',
    author='Lowe Thiderman',
    author_email='lowe.thiderman@gmail.com',
    description=('wow very doge'),
    license='MIT',
    packages=['doge'],
    package_dir={'doge': '.'},  # wow python why
    package_data={'doge': ['static/*.txt']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'doge = doge.doge:main'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta'
        'Environment :: Console'
        'Operating System :: Unix'
    ],
)
