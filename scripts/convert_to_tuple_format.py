import pandas as pd

def convert_to_tuple_format(df: pd.DataFrame) -> list[tuple]:
    """
    Converts a DataFrame to a list of tuples, dynamically using all columns.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        list of tuples: Each tuple corresponds to a row in the DataFrame.
    
    Raises:
        ValueError: If the input is not a pandas DataFrame.
    """
    # Validate input
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    # Convert the DataFrame to a list of tuples, including all columns
    data = [tuple(row) for row in df.itertuples(index=False, name=None)]
    return data
