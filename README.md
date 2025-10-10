# IP Info Collector

This project collects IP information and uploads it to Cloudflare KV storage.

## Features

- Collects IP information from text files
- Queries IP geolocation data using ip-api.com
- Filters and processes IP data
- Uploads processed data to Cloudflare KV storage
- Runs automatically every 2 hours via GitHub Actions

## Setup

1. Clone this repository
2. Set up GitHub Secrets:
   - `CF_DOMAIN`: Your Cloudflare Workers domain
   - `CF_TOKEN`: Your API token for Cloudflare KV
3. Place your IP files in the `ips/443/` directory

## Workflow

The workflow runs every 2 hours and performs the following steps:

1. Collects IP addresses from files in `ips/443/`
2. Queries geolocation information for each IP
3. Processes and filters the data
4. Saves results to `ip-info/443/`
5. Uploads processed files to Cloudflare KV storage
6. Commits and pushes updated files to the repository

## File Structure

- `ip_info_collector.py`: Main Python script for collecting and processing IP data
- `ips_to_cfkv.sh`: Shell script for uploading data to Cloudflare
- `config.ini`: Configuration file
- `.github/workflows/run_every_2hours.yml`: GitHub Actions workflow
