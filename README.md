# Crummy Proxy Checker ⛓️

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/pentestfunctions/crummy-proxy-checker)
![Issues](https://img.shields.io/github/issues/pentestfunctions/crummy-proxy-checker)
![Pull Requests](https://img.shields.io/github/issues-pr/pentestfunctions/crummy-proxy-checker)
![Forks](https://img.shields.io/github/forks/pentestfunctions/crummy-proxy-checker)
![Stars](https://img.shields.io/github/stars/pentestfunctions/crummy-proxy-checker)
![License](https://img.shields.io/github/license/pentestfunctions/crummy-proxy-checker)

Crummy Proxy Checker is an asynchronous proxy checker tool that helps you filter out bad proxies and identify the working ones. It's built using Python and leverages aiohttp for asynchronous HTTP requests.

## Features

- Supports SOCKS4, SOCKS5, and HTTP proxies.
- Asynchronous checking of proxies for higher efficiency.
- Rich console interface for easy viewing of live and dead proxies.

## Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/pentestfunctions/crummy-proxy-checker.git
cd crummy-proxy-checker
pip install -r requirements.txt
```

## Usage

Run the script using Python:

```bash
python proxychecker.py
```

The script will automatically fetch proxy lists from predefined URLs and check their status by attempting to make HTTP requests through them.

## Dependencies

- Python 3.7+
- aiohttp
- aiohttp_socks
- rich

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
