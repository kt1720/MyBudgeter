def get_input(option_list):
    """Returns user input in the form of an int based on the number of options given in the option_list."""
    n = len(option_list)
    options = [f'{i} - {option_list[i]}\n' for i in range(n)]
    
    while True:
        print('Please select one of the following options by typing the corresponding digit into your console:')
        try:
            selection = input("".join(options))
            if int(selection) in range(n):
                return int(selection)
            else:
                print("The input you supplied was not a valid option.")
        except:
            print('The input you supplied was not a valid option.')


if __name__ == '__main__':
    print('Welcome to the budgeting app.\nAre you a new user or would you like to load your transactions and budget information?')
    new = get_input(['New User', 'Load Transactions/Budget'])
    if new == 0:
        # create new user
        pass
    else:
        # load in csvs
        pass

    