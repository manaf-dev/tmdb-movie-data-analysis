from src.config import get_logger

logger = get_logger(__name__)


def check_duplicates(df):
    if not df["id"].is_unique:
        duplicates = df[df["id"].duplicated()]["id"]
        logger.warning(f"Duplicate movie IDs found: {duplicates.tolist()}")

        return duplicates
    logger.info("No duplicate movie IDs found")
    return []


def check_outliers(df, column, factor=1.5):
    """Detect outliers using IQR method."""
    if column not in df.columns:
        logger.warning(f"Column '{column}' not found.")
        return None

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - factor * IQR
    upper = Q3 + factor * IQR

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    logger.info(f"Outliers detected in {column}: {len(outliers)} rows")

    return outliers
