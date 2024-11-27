import random

class Stock_Exchange:
    #bid list and offer list for 10 stocks for which each trade is sorted in ascending order
    bid_list = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[] ,'G':[] , 'H':[] ,'I':[] ,'J':[]} # stored in ascending order, price , time ,number of shares, trader is the order
    offer_list = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[] ,'G':[] , 'H':[] ,'I':[] ,'J':[]} # stored in ascending order, price , time ,number of shares, trader is the order

    def get_last_traded_price(self, stock): #returns last traded stock
        return self.last_traded[stock]

    def get_best_bid(self, stock): # returns best bid
        return self.bid_list[stock][-1][0]

    def get_best_offer(self, stock): #returns best offer
        return self.offer_list[stock][0][0]

    def get_top_five_bids(self, stock): #we have only top 5 bids for each stock thus it returns the top 5 bids
        return self.bid_list[stock]

    def get_top_five_offers(self,stock): #we have only top 5 offers for each stock thus it returns the top 5 offers
        return self.offer_list[stock]

    def add_bid(self, stock, price, time, shares, trader): # adds a bid to bid_list and maintains the bid_list as having only top 5 bids

        self.bid_list[stock].append([price, time, shares, trader])

        self.bid_list[stock].sort()

        if(len(self.bid_list[stock]) > 5):

            self.bid_list[stock] = self.bid_list[stock][:-5]


    def add_offer(self, stock, price, time, shares, trader): # adds an offer to offer_list and maintains the offer_list as having only top 5 offers

        self.offer_list[stock].append([price, time, shares, trader])

        self.offer_list[stock].sort()

        if(len(self.offer_list[stock]) > 5):

            self.offer_list[stock] = self.offer_list[stock][:5]


    def order_matching_engine(self,stock):
        n = len(self.bid_list[stock])
        m = len(self.offer_list[stock])


        bids_to_be_deleted = [] # keeps track of bid orders that have been matched
        offers_to_be_deleted = [] # keeps track of offer orders that have been matched


        for k in range(n):
            i = n-1-k
            for j in range(m):
                if i in bids_to_be_deleted or j in offers_to_be_deleted: # if order has already been executed, do nothing
                    continue


                buy_price, tm, num_of_shares_buyer, buyer_name = self.bid_list[stock][i]
                offer_price, tm, num_of_shares_seller, seller_name = self.offer_list[stock][j]

                #give sthe trader class for particular trader which includes portfolio_stocks, cash, initial_cash, name
                buyer = traders[buyer_name]

                seller = traders[seller_name]

                #if buyer doesn't have the cash to buy the bid that he made then delete the bid
                if buyer.cash < buy_price * num_of_shares_buyer: #check if the order is eligible at the time of matching
                    bids_to_be_deleted.append(i)
                    continue

                #if seller doesn't have the number of stocks that he offered to sell then delete that offer
                if seller.portfolio_stocks[stock] < num_of_shares_seller: #check if the order is eligible at the time of matching
                    offers_to_be_deleted.append(j)
                    continue

                #if buy_price matches the offer_price then perform the stock exchange
                if(buy_price==offer_price): # if price of a bid order and an ask order matches


                    num_of_shares=min(num_of_shares_buyer,num_of_shares_seller)
                    # updating cash of the traders who's orders were executed


                    buyer.cash -= buy_price * num_of_shares
                    seller.cash += offer_price * num_of_shares


                    # updating portfolio stocks of each trader
                    buyer.portfolio_stocks[stock] += num_of_shares
                    seller.portfolio_stocks[stock] -= num_of_shares

                    # updating last traded price of the stock traded
                    last_traded[stock] = buy_price

                    # adding the executed orders from bid_list and offer_list to their respective lists
                    if (num_of_shares_buyer<num_of_shares_seller):
                        self.offer_list[stock][j][2] -= num_of_shares_buyer
                        bids_to_be_deleted.append(i)

                    elif (num_of_shares_buyer>num_of_shares_seller):
                        self.bid_list[stock][i][2] -= num_of_shares_seller
                        offers_to_be_deleted.append(j)

                    else:
                        bids_to_be_deleted.append(i)
                        offers_to_be_deleted.append(j)

                buyer.cash = round(buyer.cash, 2)
                seller.cash = round(seller.cash, 2)

        bids_to_be_deleted.sort()
        bids_to_be_deleted.reverse()
        offers_to_be_deleted.sort()
        offers_to_be_deleted.reverse()

        # deleting the executed orders from offer_list
        for pos in offers_to_be_deleted:
            self.offer_list[stock].pop(pos)


        # deleting the executed orders from bid_list
        for pos in bids_to_be_deleted:
            self.bid_list[stock].pop(pos)


class OrderManagementSystem():

    def show_cash(self):
        print(self.cash)

    def show_portfolio(self):
        current_value = 0    # value->curr value
        for i in 'ABCDEFGHIJ':
            current_value += self.portfolio_stocks[i]*last_traded[i]
        print(current_value)

    def initiate_buy(self, stock, shares, price): # function to place buy orders
        global clock
        global file_writer
        current_time = show_time(clock)
        file_writer.write(self.name + " placed bids for " + str(shares) + " number of shares of the stock " + str(stock) + " at the price of - " + str(price) + " Rs per share.\n")
        S.add_bid(stock, price, current_time, shares, self.name)

    def initiate_offer(self, stock, shares, price): # function to place ask orders   #placeoffer-initiateoffer
        global clock
        global file_writer
        current_time = show_time(clock)
        file_writer.write(self.name + " placed offers for " + str(shares) + " number of shares of the stock " + str(stock) + " at the price of - " + str(price) + " Rs per share.\n")
        S.add_offer(stock, price, current_time, shares, self.name)


class Trader(OrderManagementSystem):

    def __init__(self, portfolio_stocks, cash, initial_cash, name):
        self.portfolio_stocks = portfolio_stocks # portfolio_stocks is a dictionary, with key as the Stock and value as the number of shares of that stock
        self.cash = cash
        self.initial_cash = initial_cash
        self.name = name

    def action(self, stock):
        placing_orders = {0: self.initiate_buy, 1: self.initiate_offer}
        can_act = 1 # if the trader cannot do the action , this variable takes the value of 0
        orders_for_bid = S.bid_list[stock]
        orders_for_offer = S.offer_list[stock]
        own_shares = self.portfolio_stocks[stock]
        own_cash = self.cash

        if(len(orders_for_bid)==0 and len(orders_for_offer)==0): # no offers and no bids case
            #0 for buy, 1 for offer
            if(own_cash == 0):
                price = 0.95 * last_traded[stock]
                buy_offer = 1
            elif (own_shares==0):
                price = 1.05 * last_traded[stock]
                buy_offer = 0

            else:
                i = random.randint(0,1)
                price = (i==0) * 1.05 * last_traded[stock] + (i==1) * 0.95 * last_traded[stock]
                buy_offer=i

        elif (len(orders_for_offer)==0): # no offers case

            if(own_shares==0):
                can_act = 0
            else:
                i = random.randint(0,1)
                price = orders_for_bid[-1][0]+0.05*i*orders_for_bid[-1][0]
                buy_offer = 1

        elif (len( orders_for_bid)==0): # no bids case

            if(own_cash <= 0 ):
                can_act = 0
            else:
                i = random.randint(0,1)
                price = orders_for_offer[-1][0]-0.05*i*orders_for_offer[-1][0]
                buy_offer = 0

        else:
            i = random.randint(0,2)
            buy_offer = random.randint(0,1)

            if(own_cash <= 0 and own_shares>0):
                buy_offer = 1
            elif(own_shares <= 0 and own_cash>0):
                buy_offer = 0
            elif(own_shares<=0 and own_cash<=0):
                can_act = 0

            if(i==0):
                price = orders_for_offer[0][0]
            elif(i==1):
                price =  orders_for_bid[-1][0]
            else:
                price = (orders_for_bid[-1][0]+orders_for_offer[0][0])/2


        if(can_act!=0):
            my_shares = own_shares//1000
            affordable_shares = own_cash//(1000*last_traded[stock])
            if(buy_offer==1 and my_shares > 0):
                # a trader cannot place a sell order of shares which exceed his current number of shares for that particular stock
                shares = 1000 * random.randint(1, my_shares)
            # if no shares, the trader cannot do the action of selling
            elif (buy_offer==1 and my_shares == 0):
                # since selling isn't possible, the trader does a buy action
                buy_offer = 0
                if(affordable_shares <= 0):
                     # if a buy action isn't possible because the trader doesn't have sufficient amount to buy 1000 units of that stock, the trader can neither buy nor sell, thus can_do_action is set to 0
                    can_act = 0
                else:
                    shares = 1000 * random.randint(1, affordable_shares)
            else:
                # trader cannot place a buy order, so he places a sell order
                if(affordable_shares <= 0):
                    buy_offer = 1
                    # if the trader doesn't have shares to sell , he can do nothing
                    if(my_shares <= 0):
                        can_act = 0
                    else:
                        shares = 1000 * random.randint(1, my_shares)
                else:
                    shares = 1000 * random.randint(1, affordable_shares)
            # if the trader can do some action , he/she places an order
            if(can_act!=0):
                placing_orders[buy_offer](stock, shares, round(price,2))
        if can_act==0:
            file_writer.write(self.name + " cannot buy or sell any shares.\n")




#a function to print the contents of a dictionary
def output_dict(dict):
    global file_writer
    for key, value in dict.items():
        file_writer.write(key + ": " + str(value))
        file_writer.write('\t')


# function for displaying time from 9:00 to 15:30
def show_time(time_secs):
    hours = str(9+time_secs//3600)
    mins = str((time_secs//60)%60)
    if len(mins)==1:
        mins = '0' + mins
    secs = str(time_secs%60)
    if len(secs)==1:
        secs = '0' + secs
    return hours + ":" + mins + ":" + secs


# this function makes the Trader 't' do an action and executes the order matching engine for that stock which the trader t took action on
def act_and_match(t):
    this_stock = random_stocks[random.randint(1,10)]
    t.action(this_stock)
    S.order_matching_engine(this_stock)


#this functions simulates the stock exchange
def simulate():
    global clock
    global traders
    global file_writer
    file_writer = open("log.txt", "w")

    # Create empty dictionaries to store stock holdings over time for each trader
    trader_stock_holdings = {name: {stock: [] for stock in "ABCDEFGHIJ"} for name in traders}

    # 23400 is the number of seconds in 6.5 hrs
    while clock < 23400:
        file_writer.write("At time " + show_time(clock) + ":\n\n")
        file_writer.write("Last Traded Price of Stocks:\n")
        output_dict(last_traded)
        file_writer.write('\n\n')

        # Update trader stock holdings and write to log file
        for name, t in traders.items():
            file_writer.write(name + " Cash = \t \t \t" + str(t.cash) + " Rs. \n")
            file_writer.write(name + " Portfolio = \t \t")
            output_dict(t.portfolio_stocks)
            file_writer.write('\n')

            # Append current stock holdings to the dictionary
            for stock, holding in t.portfolio_stocks.items():
                trader_stock_holdings[name][stock].append(holding)

        file_writer.write('\n')

        # Perform actions and matching for each trader
        for t in traders.values():
            act_and_match(t)

        clock += 1
        file_writer.write('\n\n\n')

    file_writer.close()  # Close the log file

    # Plot stock holdings variation for each trader
    for trader, stock_holdings in trader_stock_holdings.items():
        plt.figure(figsize=(12, 6))
        for stock, holdings in stock_holdings.items():
            plt.plot(range(23400), holdings, label=stock)
        plt.title(f"Stock Holdings Variation for {trader}")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Number of Shares")
        plt.legend()
        plt.grid(True)
        plt.show()

def initialise_entities():
    global S
    global last_traded
    global traders
    global clock
    global random_stocks


    # creating 5 trader instances and one stock exchange S.
    S = Stock_Exchange()
    trader_obj = []
    trader_obj.append(Trader({'A':21000, 'B':8000, 'C':4000, 'D':12000, 'E':12000, 'F':10000 ,'G':15000 , 'H':8000 ,'I':3000 ,'J':13000}, 40100, 40100, 'Trader 1'))
    trader_obj.append(Trader({'A':12000, 'B':5000, 'C':4000, 'D':18000, 'E':0, 'F':9000 ,'G':25000 , 'H':18000 ,'I':13000 ,'J':6000}, 10000, 10000, 'Trader 2'))
    trader_obj.append(Trader({'A':12000, 'B':13000, 'C':3000, 'D':19000, 'E':5000, 'F':8000 ,'G':10000 , 'H':6000 ,'I':5000 ,'J':9000}, 5230, 5230, 'Trader 3'))
    trader_obj.append(Trader({'A':15000, 'B':10000, 'C':14000, 'D':7000, 'E':1000, 'F':1000 ,'G':17000 , 'H':10000 ,'I':7000 ,'J':10000}, 20000, 20000, 'Trader 4'))
    trader_obj.append(Trader({'A':14000, 'B':7000, 'C':4000, 'D':15000, 'E':11000, 'F':9000 ,'G':19000 , 'H':12000 ,'I':9000 ,'J':11000}, 100, 100,'Trader 5'))


    last_traded = {'A':51, 'B':15, 'C':14, 'D':32, 'E':48, 'F':22 ,'G':64 , 'H':58 ,'I':18 ,'J':27}
    traders = {'Trader ' + str(i+1):trader_obj[i] for i in range(len(trader_obj))}
    clock = 0
    random_stocks = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J'}


import matplotlib.pyplot as plt

def show_profit():
    profits = {}  # Dictionary to store profits of traders
    for t in traders.values():
        profit = round((t.cash - t.initial_cash), 2)
        profits[t.name] = profit

    # Writing profits to a file
    with open("profits.txt", "w") as f:
        f.write("Profit of each trader at the end of the day is : \n \n")
        for trader, profit in profits.items():
            f.write(f"Profit of {trader} is {profit} Rs.\n")

    # Plotting bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(profits.keys(), profits.values())
    plt.xlabel('Traders')
    plt.ylabel('Profit (Rs)')
    plt.title('Profit of each trader')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()



def print_list_of_bids():
    f = open("bid_list.txt", "w")
    f.write('price, time, num_shares, trader name\n')


    for this_stock in "ABCDEFGHIJ":
        f.write('Stock ' + this_stock + ':\n')
        st = ""
        for l in S.bid_list[this_stock]:
            for x in l:
                st+=str(x) + ', '
            st+='\n'
        f.write(st+'\n')
    f.close()


def print_list_of_offers():
    f = open("offer_list.txt", "w")
    f.write('price, time, num_shares, trader name\n')


    for this_stock in "ABCDEFGHIJ":
        f.write('Stock ' + this_stock + ':\n')
        st = ""
        for l in S.offer_list[this_stock]:
            for x in l:
                st+=str(x) + ', '
            st+='\n'
        f.write(st+'\n')
    f.close()


def close():
    show_profit()
    print_list_of_bids()
    print_list_of_offers()


    # cancelling all pending orders in the bid_list and offer_list
    for i in 'ABCDEFGHIJ':
        S.bid_list[i] = []
        S.offer_list[i] =[]




#main program
initialise_entities()
simulate()
close()