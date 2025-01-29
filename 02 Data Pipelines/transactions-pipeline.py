import pandas as pd
import os
import glob
import numpy as np


def main():
    """
    Data pipeline for financial transactions across multiple institutions. \n
    Iterates through folders of .csv files and applies per folder data cleanup. \n
    Outputs single .csv file of all cleaned transactions.
    """

    # Map of functions to process each folder
    folder_processing_map = {
        "american_express": process_american_express,
        "capital_one": process_capital_one,
        "chase": process_chase,
        "fidelity_business": process_fidelity,
        "fidelity_personal": process_fidelity,
        "wells_fargo": process_wells_fargo,
    }

    # Intial dictionary of raw .csv files
    csv_directory_dict = directory_to_dict("transactions_raw")

    # Make dictionary and list to hold processed dataframes
    processed_dfs_dict = {}
    processed_dfs_list = []

    # Apply processing to each dataframe according to folder_processing_map
    for key, value in csv_directory_dict.items():
        if key in folder_processing_map:
            processed_dfs_dict[key] = folder_processing_map[key](value)
            processed_dfs_list.append(folder_processing_map[key](value))

    # Create transactions_df
    columns = ["date", "account", "amount", "category", "description", "notes"]
    transactions = pd.DataFrame(columns=columns)

    # Concatenate list of dataframes
    transactions = pd.concat(processed_dfs_list, ignore_index=True)

    # convert date column to datetime
    transactions["date"] = pd.to_datetime(transactions["date"])

    # export csv
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(parent_dir, "transactions-all-current-accounts.csv")
    transactions.to_csv(output_path, index=False)

    return transactions


def directory_to_dict(subfolder):
    # Current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    transactions_dir = os.path.join(current_dir, subfolder)

    # Empty dictionary of all .csv files. Keys will be parent folder
    csv_directory_dict = {}

    # Set parent folders to keys
    for parent_folder in os.listdir(transactions_dir):
        if parent_folder != ".DS_Store":
            csv_directory_dict[parent_folder] = []

        parent_folder_path = os.path.join(transactions_dir, parent_folder)

        if os.path.isdir(parent_folder_path):
            # List to hold all datarames in current parent_folder
            parent_folder_dfs = []

            # Pattern to find all .csv files in parent_folder
            pattern = os.path.join(parent_folder_path, "*.csv")

            # Traverse and read each .csv file
            for file_path in glob.glob(pattern):
                # Load .csv into dataframe and append to list
                # Handle wells_fargo not having headers
                if parent_folder == "wells_fargo":
                    df = pd.read_csv(file_path, header=None)
                else:
                    df = pd.read_csv(file_path)
                parent_folder_dfs.append(df)

            combined_df = pd.concat(parent_folder_dfs, ignore_index=True)
            csv_directory_dict[parent_folder] = combined_df

    return csv_directory_dict


def process_american_express(df):

    df = df[["Date", "Description", "Amount", "Category"]].copy()

    # Lowercase the column names
    df.columns = df.columns.str.lower()

    # Convert dates
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y", errors="coerce")

    # Add account and notes features
    df["account"] = "american_express"
    df["notes"] = ""

    return df


def process_chase(df):

    df = df[["Transaction Date", "Description", "Category", "Amount", "Memo"]].copy()
    df["Transaction Date"] = df["Transaction Date"].str.strip()
    df.rename(columns={"Transaction Date": "date", "Memo": "notes"}, inplace=True)

    # Lowercase the column names
    df.columns = df.columns.str.lower()
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y", errors="coerce")

    # Add account feature
    df["account"] = "chase"

    return df


def process_fidelity(df):
    # Select desired columns
    df = df[["Run Date", "Account", "Amount ($)", "Description"]].copy()

    # Strip whitespace on date column for processing in is_valid_date
    df["Run Date"] = df["Run Date"].str.strip()

    # Rename columns
    df.rename(columns={"Run Date": "date", "Amount ($)": "amount"}, inplace=True)

    # Lowercase the column names
    df.columns = df.columns.str.lower()

    # Remove rows that don't contain dates in 'date' column
    def is_valid_date(date):
        # Check if the date is in the format 'mm/dd/yyyy'
        try:
            parsed_date = pd.to_datetime(date, format="%m/%d/%Y", errors="raise")
            return True
        except ValueError:
            return False

    filtered_df = df[df["date"].apply(is_valid_date)].copy()

    # Convert column to datetime
    filtered_df["date"] = pd.to_datetime(
        filtered_df["date"], format="%m/%d/%Y", errors="coerce"
    )

    # Add empty notes and category features
    filtered_df["notes"] = ""
    filtered_df["category"] = ""

    # Replace "No Description" with NaN
    filtered_df["description"] = filtered_df["description"].replace(
        "No Description", np.nan
    )  # , inplace=True)

    return filtered_df


def process_capital_one(df):

    # Make subselection of dataframe
    df = df[["Transaction Date", "Description", "Category", "Debit", "Credit"]].copy()

    # Rename columns
    df.rename(columns={"Transaction Date": "date"}, inplace=True)

    # Lowercase the column names
    df.columns = df.columns.str.lower()

    # create 'amount' column based on credit or debit

    # Fill NaN calues with 0
    df["credit"] = df["credit"].fillna(0)
    df["debit"] = df["debit"].fillna(0)

    # Calculate amount
    df["amount"] = df["credit"] - df["debit"]

    # Add account and notes fields
    df["account"] = "american_express"
    df["notes"] = ""

    df = df.drop(["debit", "credit"], axis=1)

    return df


def process_wells_fargo(df):
    df.columns = ["date", "amount", "blank", "checkno", "description"]

    # Convert dates
    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y", errors="coerce")

    # Drop extra columns
    df = df.drop(["blank", "checkno"], axis=1)

    # add account, notes, and category fields
    df["notes"] = ""
    df["account"] = "wells_fargo"
    df["category"] = ""

    return df


if __name__ == "__main__":
    main()
