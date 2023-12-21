import csv
import time


def read_csv_file(file_path):
    """
    Imports shares data from a CSV file.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: Shares data as a list of tuples (action, cost, profit).
    """
    shares_list = []

    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row

        for row in reader:
            action = row[0].strip()
            cost = float(row[1])
            profit = float(row[2])

            # Exclude shares with negative costs
            if cost >= 0:
                shares_list.append((action, cost, profit))
    return shares_list


def maximize_profit(shares_list, max_budget):
    """
    Maximizes the profit for a given list of shares and maximum budget using dynamic programming.

    Args:
        shares_list (list): List of shares as tuples (action, cost, profit).
        max_budget (float): Maximum budget for the investment.

    Returns:
        tuple: the Best investment options as a tuple (combination, profit).8
    """

    # Get the length of the share list
    n = len(shares_list)

    # Create a dynamic programming table with (n+1) rows and (max_budget+1) columns
    dp = [[0] * (int(max_budget) + 1) for _ in range(n + 1)]

    # Iterate over the share list and maximum budget
    for i in range(1, n + 1):
        for j in range(1, int(max_budget) + 1):
            # Extract action, cost, and profit from the current share
            action, cost, profit = shares_list[i - 1]
            # Check if the current share cost is less than or equal to the current budget
            if cost <= j:
                # Retrieve the previous profit from the valid index
                prev_profit = dp[i - 1][int(j - cost)]
                # Calculate the new profit by adding the current share's profit
                # with the profit obtained from the remaining budget after buying the current share
                new_profit = prev_profit + (cost * profit) / 100

                # Update the dynamic programming table if the new profit is greater
                if new_profit > dp[i - 1][j]:
                    dp[i][j] = new_profit
                else:
                    dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]

    # Retrieve the best combination of shares based on the dynamic programming table
    combination = []
    i, j = n, int(max_budget)
    while i > 0 and j > 0:
        if dp[int(i)][int(j)] != dp[int(i - 1)][int(j)]:
            combination.append(shares_list[i - 1])
            j -= shares_list[i - 1][1]
        i -= 1

    # Return the best combination of shares and the maximum profit
    return tuple(combination), dp[n][int(max_budget)]


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
        print("\033[1;35m{: ^75}\033[0m".format("Best investment options:"))
        total_cost = sum(stock[1] for stock in investment)
        for stock in investment:
            print(f"- \033[1;34mAction: {stock[0]}\033[0m || "
                  f"\033[1;32mCost per share: {stock[1]} euros\033[0m || "
                  f"\033[1;33mProfit after 2 years: {stock[2]}%\033[0m")
        print("\033[1;31m{: ^75}\033[0m".format(f"Total cost: {total_cost}"))
        print("\033[1;31m{: ^75}\033[0m".format(f"Total profit after 2 years: {profit: .2f}"))


def main():
    file_path = '../data/dataset2_Python+P7.csv'
    max_budget = 500

    start_time = time.time()

    shares_list = read_csv_file(file_path)

    best_investment, max_profit = maximize_profit(shares_list, max_budget)

    display_investment(best_investment, max_profit)

    elapsed_time = time.time() - start_time
    print("\033[1;35m{: ^75}\033[0m".format(f"Elapsed time: {elapsed_time:.2f} seconds"))


if __name__ == '__main__':
    main()
