"""
Inital project Setup
"""


from distutils.core import setup, find_packages

setup(
    name='BittrexCliTrader',
    version='1.0',
    author='Andre V. Banks',
    author_email='andrebanks.ab@gmail.com',
    description=("A command line application that allows for trading of coins\
                 found on Bittrex.com using the Bittrex.com API"),
    license='MIT',
    keywords="bittrex cryptocurrency coinmarketcap cryptotrading",
    url="https://github.com/avbanks/Bittrex-CommandLine-Trader",
    packages=find_packages(),
    long_description=read('README'),
)


