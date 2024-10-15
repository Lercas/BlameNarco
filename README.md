# BlameNarco

This Python script is designed to parse websites, either individually or from a list, and detect prohibited words (such as drug-related terminology) using a dynamically generated list of word mutations. It can also handle redirects and generates a detailed report in JSON format.

## Features
- **Prohibited Words Detection**: Detects prohibited words, including various mutations and combinations of those words.
- **Word Mutation Generation**: Generates thousands of mutations of the base prohibited words to ensure a wide coverage.
- **Handles Redirects**: Identifies and warns about any redirects encountered during parsing.
- **JSON Report Generation**: Creates a detailed report of all checks, including found words and whether redirects occurred.
- **Progress Bar**: When parsing multiple sites from a file, a progress bar displays the status of the parsing process.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `beautifulsoup4`
  - `tqdm`

Install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

Usage

The script provides several options for generating word lists, checking individual sites, or checking multiple sites from a file.
1. Generate the Prohibited Words List

Before you can scan any websites, you need to generate the list of prohibited word mutations. Run the following command to generate the list:

```bash
python3 blmn.py --generate
```
This command will generate a file named keywords.txt containing all the word mutations that the script will use to detect prohibited words.
2. Check a Single Website

You can check a specific website for prohibited words using the --site option:

```bash
python3 blmn.py --site "https://example.com"
```

This command will parse the provided website and search for any occurrences of prohibited words. The results, including any redirects and found words, will be saved in results.json.
3. Check Multiple Websites from a File

To check multiple websites at once, create a text file (e.g., sites.txt) with each URL on a new line. Then run the following command:

```bash
python3 blmn.py --file "sites.txt"
```

This will parse each website in the file and search for prohibited words. A progress bar will display the status of the parsing process, and the results will be saved in results.json.

Error Handling
- Redirects: The script detects and warns about any redirects by printing a warning to the console and marking the site as redirected in the JSON report.
- Request Failures: If a site cannot be accessed or parsed, the script marks the status as Error in the report and prints an error message to the console.
