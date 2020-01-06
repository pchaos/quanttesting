import pandas as pd
import numpy as np


# Returns x*y
def multiplyData(x, y):
    return x * y


# Multiply given value by 2 and returns
def doubleData(x):
    return x * 2


def main():
    # List of Tuples
    matrix = [(222, 34, 23),
              (333, 31, 11),
              (444, 16, 21),
              (555, 32, 22),
              (666, 33, 27),
              (777, 35, 11)
              ]

    # Create a DataFrame object
    dfObj = pd.DataFrame(matrix, columns=list('abc'))

    print("Original Dataframe", dfObj, sep='\n')

    print('************* Apply a lambda function to each row or each column in Dataframe *************')

    print('*** Apply a lambda function to each column in Dataframe ***')

    # Apply a lambda function to each column by adding 10 to each value in each column
    modDfObj = dfObj.apply(lambda x: x + 10)

    print("Modified Dataframe by applying lambda function on each column:")
    print(modDfObj)

    print('*** Apply a lambda function to each row in Dataframe ***')

    # Apply a lambda function to each row by adding 5 to each value in each column
    modDfObj = dfObj.apply(lambda x: x + 5, axis=1)

    print("Modified Dataframe by applying lambda function on each row:")
    print(modDfObj)

    print('************* Apply a User Defined function to each row or each column in Dataframe *************')

    print('*** Apply a user defined function to each column in Dataframe ***')

    # Apply a user defined function to each column by doubling each value in each column
    modDfObj = dfObj.apply(doubleData)

    print("Modified Dataframe by applying a user defined function to each column in Dataframe :")
    print(modDfObj)

    print('*** Apply a user defined function to each row in Dataframe ***')

    # Apply a user defined function to each row by doubling each value in each column
    modDfObj = dfObj.apply(doubleData, axis=1)

    print("Modified Dataframe by applying a user defined function to each row in Dataframe :")
    print(modDfObj)

    print(
        '************* Apply a User Defined function (with Arguments) to each row or each column in Dataframe *************')

    print('*** Apply a user defined function ( with arguments ) to each column in Dataframe ***')

    # Apply a user defined function to each column that will multiply each value in each column by given number
    modDfObj = dfObj.apply(multiplyData, args=[4])

    print("Modified Dataframe by applying a user defined function (with arguments) to each column in Dataframe :")
    print(modDfObj)

    print('*** Apply a user defined function ( with arguments ) to each row in Dataframe ***')

    # Apply a user defined function to each row by doubling each value in each column
    modDfObj = dfObj.apply(multiplyData, axis=1, args=[3])

    print("Modified Dataframe by applying a user defined function (with arguments) to each row in Dataframe :")
    print(modDfObj)

    print('************* Apply a numpy function to each row or each column in Dataframe *************')

    # Apply a numpy function to each column by doubling each value in each column
    modDfObj = dfObj.apply(np.square)

    print("Modified Dataframe by applying a numpy function to each column in Dataframe :")
    print(modDfObj)

    # Apply a numpy function to each row by square root each value in each column
    modDfObj = dfObj.apply(np.sqrt, axis=1)

    print("Modified Dataframe by applying a numpy function to each row in Dataframe :")
    print(modDfObj)

    print('************* Apply a reducing function to each column or row in DataFrame *************')

    # Apply a numpy function to get the sum of values in each column
    modDfObj = dfObj.apply(np.sum)

    print("Modified Dataframe by applying a numpy function to get sum of values in each column :")
    print(modDfObj)

    # Apply a numpy function to get the sum of values in each row
    modDfObj = dfObj.apply(np.sum, axis=1)

    print("Modified Dataframe by applying a numpy function to get sum of values in each row :")
    print(modDfObj)


if __name__ == '__main__':
    main()