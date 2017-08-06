# Bittrex Command-Line Trader
## Andre V. Banks

!!!Project Not Complete!!!  
A command-line application for Mac OS that enables coin tradring through Bittrex on the CLI. 

## Why?
Bittrex is one of the best exchanges for trading crypto coins however they face the same problems as other exchanges.  The user-interface isn't that great, login process isn't convinent for quick trading, the website is sometimes down for maintainance, and trading amount and price is specified in Bitcoin instead of fiat currency. This application is intended to allow users to complete trades in under 5 seconds a feat which is nearly impossible in Bittrex due to the login process and UI. This is necessary when trading crypto coins due to their volatile trading nature. 

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
* For the documentation I've named the command cli_trade however this can changed to your liking, if speed is a concern changing it to a single letter could be ideal.  

## Default Functionality
### cli_trade (no arguments)
The default functionality will cause all purchased coins to be displayed with each positions total value and the total value of the portfolio displayed.
The the coins rank, ticker, 1hr, 24hr, and 7day change will be displayed.

]==========================================  
Bitcoin $1050.0000  
Rank 1 | 1 HR %10 | 24HR %20 | 7D %50  
]==========================================  
Balance $90000

![Cli Defualt Functionality](https://media.giphy.com/media/26n6EtVM4DQyQvoti/giphy.gif)

## Buy Order @ ASK Price 
### cli_trade -b ticker lots
#### UUID of trade will display if successful if not a trade not filled message will appear 

## Buy Order @ BID Price  
### cli_trade -bbid ticker lots  
#### UUID of trade will display if successful if not a trade not filled message will appear 

## Sell order @ BID Price
### cli_trade -s ticker lots  
#### UUID of trade will display if successful if not a trade not filled message will appear 


## Sell order @ ASK Price
### cli_trade -s ticker lots  
#### UUID of trade will display if successful if not a trade not filled message will appear 

## Sell All Quantity of A Coin In The Portfolio 
### cli_trade -sa ticker  
#### Will sell the coin into Bitcoin, This command will not work on Bitcoin

## Get All Open Orders
### cli_trade -oo 
#### Displays the UUID of all open orders





