
# Betting-Dashboard

## Overview

**Betting-Dashboard** is a Streamlit application designed to visualize and manage a public ledger of bets. The dashboard offers insights into your betting history, helping you analyze performance and trends. This project is maintained by **Yureeh**.

## Features

- **Public Ledger:** The dashboard serves as a transparent ledger for all bets, enhancing accountability and transparency.
- **Daily Updates:** The CSV file with all bets is updated daily to ensure the dashboard reflects the most recent data.
- **Interactive Visualizations:** Gain insights into your betting history with interactive charts and tables.
- **Data Filtering:** Easily filter and search through your bet history.
- **Performance Analysis:** View summaries and statistics of your betting performance.

## Prerequisites

To run this project locally, you will need the following installed:

- Python 3.9 or higher
- Poetry (Python dependency management tool)


## Installation

Follow these steps to set up the Betting-Dashboard on your local machine:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Yureehh/Betting-Dashboard.git
   cd Betting-Dashboard
   ```

2. **Install Poetry:**

   ```bash
   pip install poetry
   ```

3. **Install dependencies:**

   ```bash
   poetry install
   ```

4. **Activate the virtual environment:**

   ```bash
   poetry shell
   ```

## Usage

Once the installation is complete, you can run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser, allowing you to interact with the dashboard.

## Testing

To run the tests for the Betting-Dashboard, use the following command:

```bash
poetry run pytest
```

## Data Source

The Betting-Dashboard uses a public ledger of bets to generate visualizations and insights. You can check the required format for the data by examining the `bets_ledger.csv` file in the data folder.

## Versioning

This project uses [Commitizen](https://commitizen.github.io/cz-cli/) for versioning. To create a new version, run the following command:

```bash
poetry run cz bump --check --tag
```

## Contributing

Contributions are welcome! To contribute to the Betting-Dashboard, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Run the tests.
5. Commit your changes using Commitizen.
6. Push your branch to your fork.
7. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to me on X [@Yureehh](https://twitter.com/Yureehh).
