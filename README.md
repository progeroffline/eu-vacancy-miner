# EU Vacancy Miner

[![Build Status](https://img.shields.io/github/actions/workflow/status/progeroffline/eu-vacancy-miner/ci.yml?branch=dev&style=for-the-badge)](https https://github.com/progeroffline/eu-vacancy-miner/actions)
[![License](https://img.shields.io/github/license/progeroffline/eu-vacancy-miner?style=for-the-badge)](https://github.com/progeroffline/eu- vacancy-miner/blob/dev/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/progeroffline/eu-vacancy-miner?style=for-the-badge)](https://github.com/progeroffline/eu-vacancy-miner /issues)

## Description

**EU Vacancy Miner** is a tool for parsing vacancies from various European sites. The current version supports parsing of the following resources:

- [European Union Public Employment Services (EURES)](https://ec.europa.eu/eures/public/en/homepage)
- [Bundesagentur für Employment (Arbeitsagentur)](https: //www.arbeitsagentur.de/)

## Contents

- [Description](#description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project structure](#project-structure)
- [Contribution](#contribution)
- [License](#license)

## Features

- **Scalability**: Easily add support for new sites for parsing.
- **Flexibility**: All settings are located in in the `settings.ini` file. - **Efficiency**: Optimized for fast data collection and processing.
- **CAPTCHA Recognition**: Support for [2captcha](https://2captcha.com/) service for automatic CAPTCHA solving.

## Installation

1. Clone the repository :

```bash
git clone -b dev https://github.com/progeroffline/eu-vacancy-miner.git
```

2. Go to the project directory:

````bash
cd eu-vacancy-miner
``` 3. Install the required dependencies:

```bash
pip install -r requirements.txt
````

4. Register on the [2captcha](https://2captcha.com/) platform and top up your balance with the minimum amount.

5. Get the API key on the 2captcha platform and add it to the `settings.ini` file in the `[2captcha]` section:

```ini
[TwoCaptcha]
api_key = YOUR_API_KEY
```

## Usage

1. Configure parsing parameters in the file `settings.ini`.

2. Run the parser:

```bash
python src/app.py
```

3. The collected data will be saved to the `vacancies.csv` table.

## Project structure

```plaintext
eu-vacancy-miner/
├── vacancies.csv # File with parsing results
├── src/ # Project source code
│ ├── app.py # Main application file
│ ├── settings.py # Logic for working with settings.ini
│ ├── arbeitsagentur/ # Module for parsing the Arbeitsagentur website
│ │ ├── __init__.py
│ │ ├── api.py
│ │ ├── captcha.py
│ │ ├── dtypes.py
│ │ └── endpoints.py
│ └── europa_eu/ # Module for parsing the EURES website
│ ├── __init__.py
│ ├── api.py
│ ├── endpoints.py
│ └ ── formatter.py
├── requirements.txt # List of project dependencies
├── settings.ini # Project configuration file
└── README.md # Current file
```

## Contributions

We welcome community contributions! If you would like to add support for a new site or improve existing functionality, please create an [issue](https://github.com/progeroffline/eu-vacancy-miner/issues) or submit a [pull request](https://github. com/progeroffline/eu-vacancy-miner/pulls).

## License

This project is licensed under the MIT license. For details, see the [LICENSE](https://github.com/progeroffline/eu-vacancy-miner/blob /dev/LICENSE).
