from max_profit import calculate_max_profit

def test_stock_max_profit():
    # Buy on Day 2 at $1, sell on Day 5 at $6 -> Profit = $5
    assert calculate_max_profit([7, 1, 5, 3, 6, 4]) == 5

    # Prices only go down every day -> Never buy, profit = 0
    assert calculate_max_profit([7, 6, 4, 3, 1]) == 0

    # Empty list or single day -> Profit = 0
    assert calculate_max_profit([]) == 0
    assert calculate_max_profit([5]) == 0
