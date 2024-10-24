def convert_to_tuple_format(df):
    """
    Converts a DataFrame to a list of tuples, dynamically using all columns.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        list of tuples: Each tuple corresponds to a row in the DataFrame.
    """
    # Convert the DataFrame to a list of tuples, including all columns
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]
    return data