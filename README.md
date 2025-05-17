# Helldivers 2 Web Scraper

This project is a web scraping tool designed to extract information about stratagems from the Helldivers 2 wiki. The scraper collects data such as the resized PNG image, stratagem name, stratagem code (ULRD), and the filename for the PNG, and saves this information in both CSV and JSON formats.

## Project Structure

```
helldivers2-web-scraper
├── src
│   ├── scraper.py        # Main logic for web scraping
│   ├── utils
│   │   └── __init__.py   # Utility functions for data processing
├── data
│   ├── output.csv        # Scraped data in CSV format
│   └── output.json       # Scraped data in JSON format
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Installation

To set up the project, you need to install the required dependencies. You can do this by running:

```
pip install -r requirements.txt
```

## Usage

To run the scraper, execute the following command:

```
python src/scraper.py
```

This will start the scraping process, and the data will be saved in both `data/output.csv` and `data/output.json`.

## Dependencies

The project requires the following Python libraries:

- requests
- beautifulsoup4
- pandas

Make sure these are included in your `requirements.txt` file.

## Contributing

If you would like to contribute to this project, feel free to submit a pull request or open an issue for discussion.

## License

This project is open-source and available under the MIT License.#
