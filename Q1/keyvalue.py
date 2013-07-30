#some key value
j = [74,106] #key j J
q = [81,113] #key q Q
k = [75,107] #key k K
number0to9 = [i for i in range(48,58)] #key 0 to 9
spade = [85,115] #key s S
heart = [72,104] #key h H
diamond = [68,100] #key d D
club = [67,99] #key c C
keysOfPokerNumber = number0to9 + j + q + k
keysOfPokerSymbol = spade + heart + diamond + club
keys = keysOfPokerNumber + keysOfPokerSymbol