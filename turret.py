import Settings, traceback
from api import *
from coincheck import order,market

order_api = order.Order(access_key=Settings.access_token, secret_key=Settings.access_key)
#order_api.create(rate=1, amount=0.01, order_type='buy', pair='btc_jpy')

clear = time.time() + 5
def clear_your_mind_buddy_everything_is_going_to_be_okay():
  orders = order_api.list()
  for order in orders['orders']:
    order_api.cancel(str(order['id']))

bid_id = ''
ask_id = ''
last_bid_price = 0
last_ask_price = 0
def loop():
  global bid_id, ask_id, clear, last_bid_price, last_ask_price
  start_time = time.time()
  
  if time.time() > clear:
    clear_your_mind_buddy_everything_is_going_to_be_okay()
    clear = time.time() + 5
  else:
    if bid_id != '':
      order_api.cancel(bid_id)
    if ask_id != '':
      order_api.cancel(ask_id)
  
  position_data = coincheckapi.accounts_balance()
  net_holdings = float(position_data['btc']) + float(position_data['btc_reserved'])
  position = net_holdings - Settings.bitcoin

  order_book = coincheckapi.get_orderbook(count=10)
  bid_depth, ask_depth, best_bid, best_ask = 0,0,0,0
  for bid in order_book['bids']:
    if int(float(bid[0])) == last_bid_price:
      #print('Same bid ignore')
      pass
    else:
      bid_depth += float(bid[1])
    if bid_depth > Settings.filter:
      best_bid = int(float(bid[0]))
      print(best_bid, last_bid_price)
      break
  for ask in order_book['asks']:
    if int(float(ask[0])) == last_ask_price:
      #print('Same ask ignore')
      pass
    else:
      ask_depth += float(ask[1])
    if ask_depth > Settings.filter:
      best_ask = int(float(ask[0]))
      print(best_ask, last_ask_price)
      break
  #print(order_book['bids'][0:3], best_bid, order_book['asks'][0:3], best_ask)
  
  algorithim_best_bid = best_bid + Settings.increment
  algorithim_best_ask = best_ask - Settings.increment
  while algorithim_best_ask - algorithim_best_bid < Settings.minimum_yen_spread:
    algorithim_best_bid -= Settings.increment
    algorithim_best_ask += Settings.increment

  non_bitcoin_balance = float(position_data['jpy']) + float(position_data['jpy_reserved']) + (position * best_bid)
  if position > 0:
    buy_amount = Settings.order_size
    sell_amount = round(Settings.order_size + abs(position) - 0.002, 3)
  elif position < 0:
    buy_amount = round(Settings.order_size + abs(position) - 0.002, 3)
    sell_amount = Settings.order_size
  else:
    buy_amount = Settings.order_size
    sell_amount = Settings.order_size
  if position >= Settings.max_position:
    buy_amount = 0
  if position <= -Settings.max_position:
    sell_amount = 0
  
  if buy_amount > 0:
    buy_order = order_api.create(rate=algorithim_best_bid, amount=abs(buy_amount), order_type='buy', pair='btc_jpy')
  
  if sell_amount > 0:
    sell_order = order_api.create(rate=algorithim_best_ask, amount=abs(sell_amount), order_type='sell', pair='btc_jpy')
  
  if buy_amount > 0:
    try:
      bid_id = str(buy_order['id'])
    except:
      print('error', buy_order)
      bid_id = ''
  
  if sell_amount > 0:
    try:
      ask_id = str(sell_order['id'])
    except:
      print('error', sell_order)
      ask_id = ''

  print("{} \t \t \t {} \t \t \t {} \t \t \t {}".format(algorithim_best_bid, algorithim_best_ask, position, non_bitcoin_balance))
  
  last_bid_price = algorithim_best_bid
  last_ask_price = algorithim_best_ask

while True:
  try:
    loop()
  except:
    print(traceback.format_exc())
  time.sleep(0.5)
