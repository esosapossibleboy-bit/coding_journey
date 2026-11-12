def count_money(coins):
    # 'coins' is a list of numbers, like [5, 10, 25]
    total = 0
    for coin in coins:
        total += coin
    return total

def count_big_coins(coins):
    # Count how many coins in the list are 10 or bigger (coin >= 10)
    big_count = 0
    for coin in coins:
        if coin >= 10:
            big_count += 1
    return big_count
