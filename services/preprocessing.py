import pandas as pd
def clean_dataset(path: str) -> pd.DataFrame:
    """
    Loads and cleans a CSV dataset.
    Steps:
    - Normalize column names
    - Removes string whitespace
    - Convert numeric columns safely
    - Handle missing values
    - Remove completely empty rows
    - Reset index
    """
    #loading csv dataset
    df = pd.read_csv(
        path,
        encoding="latin-1",
        engine="python",
        on_bad_lines="skip"
    )

    # normalize column names-
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # no whitespace in string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # convert numeric columns need to Use actual column names from the dataset after normalization
    
    possible_numeric_cols = ["average_rating", "num_pages", "ratings_count", "published_year"]
    for col in possible_numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # drop fullly empty rows
    df.dropna(how="all", inplace=True)

    #Reset index
    df.reset_index(drop=True, inplace=True)

    return df