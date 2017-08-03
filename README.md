# Bittrex Command-Line Trader
## Andre V. Banks

!!!Project Not Complete!!!
A command-line application for Mac OS that enables coin tradring through Bittrex on the CLI. 

## Installation
Make sure you have an API key and secret generated from Bittrex with “Read Info” and “Trade Limit” properties activated.  A ```secrets.py``` file will need to be created in the projects ```bin/cli_trade/``` directory to read the API key and secret into into the application.  The file should contain the following contents:  
```python
#!/usr/bin/env python

BKEY = 'YOUR_BITTREX_KEY_HERE'
BSECRET = 'YOUR_BITTREX_SECRET_HERE'  
```  
In order for the application to run the application the ```cli_trader.py``` file located in the ```bin/cli_trade/``` directory needs to be granted execution permission. This can be done by running the following command in the projects ```bin/cli_trade/``` directory ```
chmod u+x cli_trader.py ```    
The application can now be run by running the cli_trader.py file  
```./cli_trader.py```    
  

I would recommend creating a symlink of the ```cli_trader.py``` file to ```/usr/local/bin/COMMAND_NAME``` so the application can be ran by calling a designated command. This can be done by running the following command:  
  

 ```ln -s FULL_PATH/cli_trader.py /user/local/bin/COMMAND_NAME```  
  

 Replacing 'FULL_PATH' with the full path of the file and 'COMMAND_NAME' with the desired command name. The cli_trader.py file contains a global variable 'LOT' this determines what dollar lots the coins should be traded.  The default value is 5 which means coins will be traded in $5 USD lots.  This functionality makes trading between coins a lot easier to deal with.  Due to the extremely volatile nature of Bitcoin I find pricing purchase size in USD a lot easier.    

### Adjusting Trade Size	
The default trade quantity is a lot size of $5 USD. When commands to buy or sell are used a quantity of lots has to be specified so if you wanted to by 2 lots of Ethereum you would be buying $10 USD worth of Ethereum.  It's my personal preference to trade in $5 USD lots however this can be changed to meet your needs. Default lot size can be changed by altering the LOT constant in the ```cli_trader.py``` file.  

## Commands

## Default Functionality
### ./cli_trader.py (no arguments)
The default functionality will cause all purchased coins to be displayed with each positions total value and the total value of the portfolio displayed.
The the coins rank, ticker, 1hr, 24hr, and 7day change will be displayed.

]==========================================  
Bitcoin $1050.0000  
Rank 1 | 1 HR %10 | 24HR %20 | 7D %50  
]==========================================  
Balance $90000

![Cli Defualt Functionality](https://media.giphy.com/media/l0EoBilWm7mOSksta/giphy.gif)

## Buy Order @ ASK Price
### ./cli_trader.py --b <ticker> <lots>




