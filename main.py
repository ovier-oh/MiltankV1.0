import pandas as pd 

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def show_columns(df: pd.DataFrame) -> None: 
    print("\nColumn availables:")
    for i, col in enumerate(df.columns):
        print(f"[{i}] {col}")

def describe_column(df: pd.DataFrame, column: int) -> None: 
    series = pd.to_numeric(df[column], errors = "coerce").dropna() 

    print("\nSummary Stadistics")
    print("--------------------")
    print(f"Column: {column}")
    print(f"Quantity: {series.count():.4f}")
    print(f"Mean: {series.mean():.4f}")
    print(f"Standard deviation: {series.std():.4f}")
    print(f"Minimum: {series.min():.4f}")
    print(f"Maximum: {series.max():.4f}")
    print(f"P25: {series.quantile(0.25):.4f}")
    print(f"Median: {series.median():.4f}")
    print(f"P75: {series.quantile(0.75):.4f}")


def main():
    path = input("Path of CSV: ").strip() 

    df = load_csv(path)
    show_columns(df) 

    index = int(input("\nChoose numer of column: "))
    column = df.columns[index]

    describe_column(df, column)

if __name__ == "__main__":
    main() 
