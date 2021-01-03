Copyright Ronen Singer, All Rights Reserved

# CoinCheck Sniper

This repository contains the two algorithms I used to make-markets on a Japanese Bitcoin Exchange called CoinCheck.
Before I get into the specifics of the algorithms and how to set them up, I've included a brief explanation on what market-making is.

# What's Market-Making
**Market-making** is the process of adding **liquidity** to any type of exchange (stocks, futures, or in this case, a bitcoin exchange) to make a profit.

## What's Liquidity
**Liquidity** is the ease to which you can buy or sell an asset.

For example, in the stock market, Apple is the stock with the most liquidity. You can buy great amounts of it with ease, and you don't move the price much.
For example, the best bid (buy price) for Apple could be $160, and the best ask (sell price) for Apple could be $160.01. 

Since the **spread** (the difference), between the best buy and best sell prices is so low, the stock is liquid.  

For some assets, especially Bitcoin, the spread can be quite high. For example, on CoinCheck, before I began market-making, the spread was quite high (100 yen which is about $1) per bitcoin.

To illustrate this principle, I've made a table of the best buy and best sell prices on CoinCheck: (this table is commonly referred to as **market depth**)


Price per Bitcoin:

Buy | Sell 
--- | ---
500000 Yen | 500100 Yen
Spread: | 100 Yen

This market for Bitcoin has a spread of **100 yen per coin**. This is a large amount, so at this point, the market is **not liquid**.

# So What Does a Market-Making Bot Do?
A market-making algorithm will step in to offer better buy and better sell prices. This makes the market more efficient, and also allows you to capture a small, but steady profit.

So in this case, my computer would outbid the best bid by 10 yen, and undercut the best ask by 10 yen.

The market for the price of Bitcoin now looks like this: the bolded prices are my bids and asks

Buy | Sell
--- | ---
**500010** Yen | **500090** Yen
500000 Yen | 500100 Yen
Spread: | **80** Yen

The spread has dropped from 100 yen to 80 yen, so the market is becoming more **liquid** because it is now less costly for a customer to buy or sell, since they receieve a much better price.

# And This Makes Me Money
Now that my computer is offering the best bid, 500010 yen, and the best ask, 500090, let's say someone comes along and places an order to sell.
I'll buy their coins at 500010 yen, and wait until someone eventually comes along to buy (the coins I just bought) from me at 500090 yen. 
I then sell the coins I just bought for an **80 yen profit for me**.

Although this is a simplified version of how my algorithms trade, they give you an idea of basic market-making.

Below is a photo of what the actual market for Bitcoin on CoinCheck looks like, the green prices are bids, and the red prices are asks.

![](http://ronen.io/orderbook.PNG)

# Getting Started  With the Bots
Enclosed in this repository are two bots: **market_maker** and it's smarter cousin (which I affectionately call): **the turret**.
The Settings.Py file contains the advanced Settings for these bots. Below is an explanation of each setting:
```
minimum_yen_spread = 1 //This is the minimum **spread** the bot is willing to make. Any spread less than 1 yen would lose the bot money, thus the minimum spread must be at least one for the bot to be profitable.

increment = 5 //This is the amount by which the bot beats the existing bid and ask. For example, in this case, if the best bid is 1000 yen, the bot will bid 1000 + 5 = 1005 yen

bitcoin = 0.1 //The amount of bitcoin you actually start with, so the bot can keep track of gains and losses

max_position = 0.02 //The maximum deviation from the bitcoin you start with. So in this case, the bot would be willing to own a minimum of 0.08 bitcoin, and a maximum of 0.12 bitcoin.

order_size = 0.01 //The order amount for the bots bids and asks

filter = 0.05 //An advanced Setting for turret.py Simply put, this setting filters out other smaller bots that trade less than 0.05 bitcoin, in order to prevent them from confusing my bot.
```

## Running a Bot
First, make sure you have the python2 coincheck package installed. To install it, just run:

```
pip install coincheck
```

If you want to run a bot, say, for example, turret.py, just enter the directory and enter:

```
python turret.py
```

# Go and Make Some Money!
After raking in some pretty good profits, I was kicked of the CoinCheck exchange for failing identity verification (US Citizens are not allowed to trade).
However, **if you have citizenship in any other country**, I encourage you to open an account, and test out my bot. Just remember to change the API key in the Settings.py file to your own.

P.S. Since Japan is a long ways from the United States, I recommend you rent a **VPS** (Virtual Private Sever) in Japan, to run these bots.
It's pretty cheap, an **Amazon one costs just $10 per month**, and is actually inside the same datacenter as CoinCheck's servers, so your bots can be blazingly fast, almost like a **high frequency trading algorithm**.

If you have any questions about the algorithms, feel free to email me! I hope you've enjoyed my brief lesson on market-making and liquidity!

Lastly, for this repository, I've actually included past versions, so you can see the progression of the market-maker and turret bots.
If you do use these bots to trade, I strongly recommend turrent.py, it's a **beast**.
