from distutils.core import setup

setup(
    name='doge',
    version='0.5.0',
    url='https://github.com/thiderman/doge',
    author='Lowe Thiderman',
    author_email='lowe.thiderman@gmail.com',
    description=('wow very terminal doge'),
    license='MIT',
    packages=['doge'],
    package_data={'doge': ['static/*.txt']},
    scripts=[
        'bin/doge'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
)
