import pandas as pd

from utils.paths import BETS_PATH


# Compute additional required columns
def compute_profit(row):
    """Compute the profit for each bet."""
    if row["Result"] == "W":
        return row["Wager"] * (row["Odds"] - 1)
    elif row["Result"] == "L":
        return -row["Wager"]
    else:  # Draw
        return 0


def load_bets():
    """Load the bets ledger CSV file and compute additional columns."""
    # Load the CSV file
    data = pd.read_csv(BETS_PATH)

    # Select only the required columns
    data = data[
        [
            "Date",
            "Team",
            "League",
            "Game",
            "Type",
            "Sportbook",
            "Bet",
            "Result",
            "Odds",
            "Wager",
        ]
    ]

    # Convert 'Date' to datetime
    data["Date"] = pd.to_datetime(data["Date"])

    # Compute the 'To_Win' column
    data["To_Win"] = data["Wager"] * (data["Odds"] - 1)

    # Compute the 'Profit' column
    data["Profit"] = data.apply(compute_profit, axis=1)

    # Compute the ROI column
    data["ROI"] = (data["Profit"] / data["Wager"] * 100).apply(
        lambda x: f"{str(round(x, 2))}%"
    )

    return data
