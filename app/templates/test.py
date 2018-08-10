itt = 2
itt2 = 0
base = 1.0
while True:
    base += 1 / itt
    itt2 += 1
    if itt2 == 1000000:
        print("itt: %s, value: %s" % (itt, base))
        itt2 = 0
    itt += 1