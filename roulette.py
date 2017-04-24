import random
from tools import clear
money = 500

class group:
    def __init__(self, names, nums = [], mult = 1):
        self.names = names
        self.mult = mult
        self.nums = nums
        self.bet = 0

    def result(self,num):
        if self.bet > 0:
            if num in self.nums:
                return self.bet * (self.mult + 1)
        return 0

    def __str__(self):
        s = "{names: " + str(self.names) + "\n"
        s += "nums: " + str(self.nums) + "}"
        return s

    @property
    def name(self):
        if len(names) > 0:
            return names[0]
        else:
            return ''

def roll():
    result = random.randint(0,36)
    return result

def make_bet(value, name):
    global money
    if value < 0:
        raise ValueError("You cannot bet negative amount!")
    if money >= value:
        global groups
        for i in range(len(groups)):
            if name in groups[i].names:
                groups[i].bet += value
                money -= value
                break
    else:
        raise ValueError("You don't have enough money!")

def status():
    table()
    print("="*20)
    print("money: " + str(money))
    print("bets: ")
    for i in range(len(groups)):
        if groups[i].bet > 0:
            print(str(groups[i].bet) + " for " + groups[i].names[0])

def table():
    print("""
|3 |6 |9 |12|15|18|21|24|27|30|33|36|column 3
|2 |5 |8 |11|14|17|20|23|26|29|32|35|column 2
|1 |4 |7 |10|13|16|19|22|25|28|31|34|column 1
|  dozen 1  |  dozen 2  |  dozen 3  |
| low | even| red|black |odd | high |
""")
    
def init():
    groups = []
    groups.append(group(['red'], [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]))
    groups.append(group(['black'], [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]))
    groups.append(group(['even'], [i for i in range(1,37) if i%2 == 0]))
    groups.append(group(['odd'], [i for i in range(1,37) if i%2 == 1]))
    groups.append(group(['1-18', 'low'], list(range(1,19))))
    groups.append(group(['19-36', 'high'], list(range(19,37))))
    groups.append(group(['column 1'], [i for i in range(1,37) if i%3 == 1], 2))
    groups.append(group(['column 2'], [i for i in range(1,37) if i%3 == 2], 2))
    groups.append(group(['column 3'], [i for i in range(1,37) if i%3 == 0], 2))
    groups.append(group(['dozen 1'], list(range(1,13)), 2))
    groups.append(group(['dozen 2'], list(range(13,25)), 2))
    groups.append(group(['dozen 3'], list(range(25,37)), 2))
    for i in range(11):
        l = list(range(i*3+1, (i+2)*3+1))
        groups.append(group(['{0}-{1}'.format(l[0], l[5]), 'six ' + str(i*3+1)], l, 5))
    for i in [j for j in range(1, 33) if j %3 != 0]:
        groups.append(group(['corner '+str(i)], [i, i+1, i+3, i+4], 8))
    for i in range(1, 37, 3):
        groups.append(group(['street '+str(i)], [i,i+1,i+2], 11))
    for i in [j for j in range(1, 33) if j %3 != 0]:
        groups.append(group(['{0}-{1}'.format(i, i+1)], [i,i+1], 17))
    for i in range(1,34):
        groups.append(group(['{0}-{1}'.format(i, i+3)], [i,i+3], 17))
    groups.append(group(['zero','0'], [0], 35))
    for i in range(1, 37):
        groups.append(group([str(i)], [i], 35))
    return groups

clear()
groups = init()
#for i in groups:
 #   print(i)
while True:
    status()
    s = ""
    while True:
        s = input("Your bet: ")
        if s == "vars":
            for i in groups:
                print("{0}:1 {1}".format(str(i.mult), i.names))
            continue
        if s == "table":
            table()
            continue
        if s == "all":
            break
        bets = s.split(', ')
        for i in bets:
            b,n = i.split(': ')
            try:
                make_bet(int(b),n)
            except ValueError as err:
                print(err.args[0])
        clear()
        status()
    r = roll()
    clear()
    print("result: " + str(r))
    sum = 0
    for i in range(len(groups)):
        res = groups[i].result(r)
        if res > 0:
            sum += res
            print(groups[i].names[0])
        groups[i].bet = 0
    money += sum
    if money == 0:
        table()
        print("You LOST")
        break
