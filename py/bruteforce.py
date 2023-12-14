import csv
import time
from itertools import combinations


def read_csv_file(file_path):
    shares_list = []
    # Open the CSV file with explicit encoding
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            share = row[0].strip()
            cost = float(row[1])
            profit = float(row[2])
            shares_list.append((share, cost, profit))

    return shares_list


def calculate_total_cost(combination):
    total_cost = sum(share[1] for share in combination)
    return total_cost


def calculate_total_profit(combination):
    total_profit = sum(share[1] * share[2] / 100 for share in combination)
    return total_profit


def maximize_profit(shares_list, max_budget):
    """
    Maximizes the profit for a given list of shares and maximum budget.

    Args:
        shares_list (list): List of shares as tuples (action, cost, profit).
        max_budget (float): Maximum budget for the investment.

    Returns:
        tuple: the Best investment options as a tuple (combination, profit).
    """
    max_profit = 0
    best_investment = ()

    # Generate combinations of shares
    for i in range(len(shares_list)):
        for combination in combinations(shares_list, i):
            total_cost = calculate_total_cost(combination)
            if total_cost <= max_budget:
                total_profit = calculate_total_profit(combination)
                if total_profit > max_profit:
                    max_profit = total_profit
                    best_investment = combination
    return best_investment, max_profit


def display_investment(investment, profit):
    """
    Displays the best investment options and total profit.

    Args:
        investment (tuple): Best investment options as a tuple (combination, profit).
        profit (float): Total profit.
    """
    if not investment:
        print("\033[1;31mNo feasible investment options within the given constraints.\033[0m")
    else:
        print("\033[1;35m{: ^75}\033[0m".format("Best investment option:"))
        total_cost = sum(stock[1] for stock in investment)
        for stock in investment:
            print(f"- \033[1;34mAction: {stock[0]}\033[0m || "
                  f"\033[1;32mCost per share: {stock[1]} euros\033[0m || "
                  f"\033[1;33mProfit after 2 years: {stock[2]}%\033[0m")
        print("\033[1;31m{: ^75}\033[0m".format(f"Total cost: {total_cost}"))
        print("\033[1;31m{: ^75}\033[0m".format(f"Total profit after 2 years: {profit: .2f}"))


def main():
    file_path = 'data/test_shares.csv'
    max_budget = 500

    # Start timing
    start_time = time.time()

    # Read shares data from the CSV file
    shares_list = read_csv_file(file_path)

    # Find the best investment options
    best_investment, max_profit = maximize_profit(shares_list, max_budget)

    # Display the investment options and profit
    display_investment(best_investment, max_profit)

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print("\033[1;35m{: ^75}\033[0m".format(f"Elapsed time: {elapsed_time:.2f} seconds"))


if __name__ == '__main__':
    main()
