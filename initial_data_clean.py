# Import libraries
import pandas as pd
from datetime import datetime

# Welcome message
def welcome():
    print("Greetings! Welcome to my project that is designed to simplify the initial steps of data cleaning both for beginners and experienced data scientists.\n")
    print("This simple script should help to make the first overview of the .csv file we are working with: understand its contents, data types, work with possible date column, drop unnecessary columns and empty strings, etc.\n")
    print("I also hope that this script will help the beginners to understand the basic steps of initial data cleaning\n")
    print("Please note that this script is in its initial stage. Although it should not make any changes neither to your original files or system, I have no resposibility for any of them, so please be careful :)\n")
    print("Please also note that any changes to this script made by yourself are made at your own risk!\n")
    init_answer = input("Do you want to continue? [y/n]")
    return init_answer

# Function to take the path from the input
def read_input_path():
    path = input("\nPlease enter the full path to the csv file: ")
    print("Loading... It might take some time depending on your computer and the file size.\n")
    df = pd.read_csv(path)
    return df

# Function that analyses the columns for data types and their features
def describe_dtypes(df):
    dates = list(df.select_dtypes(include = 'datetime').columns)
    strings = list(df.select_dtypes(include = 'O').columns)
    numbers = list(df.select_dtypes(include = 'number').columns)
    booleans = list(df.select_dtypes(include = 'bool').columns)
    print('\nOverall amount of strings in this dataset: ', len(df))
    print('\nHere is the List of all columns in the dataset: ', list(df.columns), '\n')
    print('List of date columns: ', dates, '\n')
    if len(dates) != 0:
        print('The dates column(s) was found!\n')
        print('Here is their format:\n')
        print(df[dates].head(), '\n')
    else:
        print('Warning: No datetime columns: either dataset does not contain them or their dtype is "object"!\n')
    print('-----------------------------------------')

    print('\nList of object columns: ', strings, '\n')
    for string in strings:
        if any(df[string].str.contains('1|2|3|4|5|6|7|8|9|0')):
            print('Warning: the "' + string + '" column contains numbers! It might be datetime, ID, coordinate or other valuable info!\n')
            print('Here is the head of it:\n')
            print(df[string].head(), '\n')
        else:
            print('Looks like the "' + string + '" column contains no numbers and it is a categorical column!')
            print('It has ' + str(len(df[string].unique())) + ' unique values. Here are the most common of them and their counts:\n')
            print(df[string].value_counts().head(), '\n')
    print('-----------------------------------------')


    print('\nList of num columns: ', numbers, '\n')
    print('Here are some basic stats for num columns:\n')
    for number in numbers:
        print(df[number].describe(), '\n')
    print('-----------------------------------------')

    print('\nList of boolean columns: ', booleans, '\n')
    if len(booleans) == 0:
        print('Looks like there are no booleans in this dataset!\n')

# Function to drop the chosen columns from the dataset
def drop_columns(df):
    cols_to_drop = input("Please state the columns to drop one by one using ';' as a separator: column1;column2...columnN\n").split(';')
    print("Here are the list of columns you chose: ", cols_to_drop)
    try:
        df = df.drop(columns = cols_to_drop, axis = 1)
        return df
    except:
        print("Oops, looks like one or more chosen columns are either missing or was already dropped. Returning the original dataset...")
        return df
        
# Function that ask if there are columns to be dropped:
def ask_to_drop_cols(df):
    answer = input("Do you want to drop any columns from the dataset? Don't worry, they will be dropped only from the variable, not the original file :).\nTake your time and study the column stats, I am not going anywhere :)\n Choose [y/n] as an option.")
    if (answer != 'y')&(answer != 'n'):
        print("Oops, looks like you didn't choose between [y/n] choises. Please try again.")
        return df
    elif answer == 'n':
        print('Ok, all the columns are kept in the new dataset.')
        return df
    else:
        df = drop_columns(df)
        print('Here is the result of dropping:\n\n', df.head())
        answer2 = input("\nDo you want to save these results (in case you don't, please be careful, if something goes wrong you will have to start all over again)? [y/n]")
        if answer2 == 'n':
            return df
        else:
            path2 = input("Please choose the folder to save beginning and ending with '/'. Example: /home/user/Desktop/\n")
            dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M")
            df.to_csv(path2 + 'dropped_columns_' + dt_string + '.csv', index = False)
            print('The result was saved successfully! The full path to it: ' + path2 + 'dropped_columns_' + dt_string + '.csv')
            return df
            
def ask_to_dropna(df):
    answer = input("\nDo you want to drop strings with NaN values from the dataset? Don't worry, they will be dropped only from the variable, not the original file :).\n Choose [y/n] as an option.")
    if (answer != 'y')&(answer != 'n'):
        print("Oops, looks like you didn't choose between [y/n] choises. Please try again.")
        return df
    elif answer == 'n':
        print('Ok, all the NaNs are kept in the new dataset.')
        return df
    else:
        answer2 = input("Choose the subset of columns to drop NaNs one by one using ';' as a separator: column1;column2...columnN\n").split(';')
        print("Here are the list of columns you chose: ", answer2)
        answer3 = input("Choose the type of dropping: 'all' - drop only strings where all chosen columns are NaNs / 'any' - drop strings containing NaN in any of the chosen columns: ")
        print("Your chosen columns ", answer2, " will drop strings containing " + answer3 + " of NaNs")
        df.dropna(axis =0, how = answer3, subset = answer2, inplace= True)
        print('Here is the result of dropping:\n\n', df.head())
        answer4 = input("\nDo you want to save these results (in case you don't, please be careful, if something goes wrong you will have to start all over again)? [y/n]")
        if answer4 == 'n':
            return df
        else:
            path2 = input("Please choose the folder to save beginning and ending with '/'. Example: /home/user/Desktop/\n")
            dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M")
            df.to_csv(path2 + 'dropped_nans_' + dt_string + '.csv', index = False)
            print('The result was saved successfully! The full path to it: ' + path2 + 'dropped_nans_' + dt_string + '.csv')
            return df
        
def ask_to_convert_datetime(df):
    answer = input("\nIf your dataset contains datetime columns, but they have 'object' dtype, it is recommended to parse them as datetime dtype. Do you want to try it? Don't worry, they will be changed only inside the variable, not the original file :).\n Choose [y/n] as an option.")
    if (answer != 'y')&(answer != 'n'):
        print("Oops, looks like you didn't choose between [y/n] choises. Please try again.")
        return df
    elif answer == 'n':
        print('Ok, all the columns are kept in the new dataset as they are.')
        return df
    else:
        answer2 = input("Type the column name to parse as a datetime (you can scroll up to see the description of your dataset): ")
        answer3 = input("Now please carefully type the format that is used there using percent signs and correct separators (for example, %d/%m/%Y, where d is day, m is month and Y is year with four digits, please see the reference for available formats: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior):\n")
        print("Ok, fingers crossed! :)")
        df[answer2] = pd.to_datetime(df[answer2],format = answer3)
        print('Here is the result of parsing:\n\n', df.head())
        answer4 = input("\nDo you want to save these results (in case you don't, please be careful, if something goes wrong you will have to start all over again)? [y/n]")
        if answer4 == 'n':
            return df
        else:
            path2 = input("Please choose the folder to save beginning and ending with '/'. Example: /home/user/Desktop/\n")
            dt_string = datetime.now().strftime("%Y-%m-%d-%H-%M")
            df.to_csv(path2 + 'date_parsing_results_' + dt_string + '.csv', index = False)
            print('The result was saved successfully! The full path to it: ' + path2 + 'date_parsing_results_' + dt_string + '.csv')
            return df



init_answer = welcome()
if init_answer == 'n':
    print("Ok, nothing happened, don't worry! :)")
    
else:
    df = read_input_path()
    describe_dtypes(df)
    df = ask_to_drop_cols(df)
    df = ask_to_dropna(df)
    df = ask_to_convert_datetime(df)
    print("If you ran this script inside any python environment (not just used command 'python3 [this script]' from your shell), the results of your previous interactions with the dataset are contained in 'df' variable. You can use it for further edits! :)")

