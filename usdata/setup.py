from setuptools import setup

setup(
    name='usdata',
    version='0.0.1',
    description='Tools to get information about US states and counties.',
    long_description='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points={
        "console_scripts": [
        ]
    },
    keywords='',
    url='https://github.com/bayeshack2016/sysj',
    author='Yang Hong, Sasha Targ, Steven Troxler, Jeff Wu',
    author_email='yanghong.ee@gmail.com, sasha.targ@gmail.com, steven.troxler@gmail.com, wuthefwasthat@gmail.com',
    license='MIT',
    packages=['usdata'],
    install_requires=[
        'pandas'
    ],
    include_package_data=True,
    zip_safe=False
)

