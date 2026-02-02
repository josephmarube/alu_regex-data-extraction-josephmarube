# Regex Data Extraction & Secure Validation

## Project Overview

This project demonstrates the use of **regular expressions (regex)** to extract structured data from large volumes of **untrusted raw text**, similar to data returned from external APIs in real-world systems.

The program is designed with:
- Accuracy in data extraction
- Support for realistic input variations
- Basic security awareness when handling hostile or malformed input
- Protection of sensitive information

The solution is implemented in **Python** and focuses entirely on regex extraction and validation logic.

## Technologies Used

- Python 3
- `re` (Regular Expressions)
- `json`
- Standard file I/O

## Input Design

The input is a plain text file (`sample_input.txt`) that simulates real-world API responses.  
It intentionally includes:

- Valid structured data
- Inconsistent spacing and formatting
- Mixed data types
- Noise and irrelevant text
- Malicious or malformed input attempts (e.g. script tags, SQL keywords)

This ensures the program operates under realistic conditions.

## Extracted Data Types

The program extracts the following data types using regex patterns:

1. **Email Addresses**
   - Example input: `user@example.com`, `firstname.lastname@company.co.uk`
   - Masked in output to protect user identity
      - Keeps the first and last character of the username.
      - Example output : j********e@gmail.com

2. **URLs**
   - Example: `https://www.example.com`, `http://blog.example.org/page?id=12`

3. **Phone Numbers**
   - Formats supported:
     - `(123) 456-7890`
     - `123-456-7890`
     - `123.456.7890`

4. **Credit Card Numbers**
   - Formats supported:
     - `1234 5678 9012 3456`
     - `1234-5678-9012-3456`
   - **Masked in output for security**

5. **Time Values**
   - 24-hour and 12-hour formats
   - Example: `09:00`, `5:30 PM`

6. **Hashtags**
   - Example: `#FrontendDev`, `#Web_Development`

## Security Considerations

This program treats all input as **untrusted**.

Security measures include:

- Strict regex patterns to prevent malformed matches
- Filtering of common hostile input patterns such as:
  - `<script>` tags
  - SQL injection-like keywords (`DROP TABLE`, `SELECT FROM`)
- Sensitive data handling:
  - Maked email addresses exposing only minimal identifying information
  - Credit card numbers are **masked**, exposing only the last four digits
- Invalid or suspicious matches are ignored rather than processed

These measures demonstrate defensive programming practices without implementing a full backend security system.

## How to Run the Program

1. Ensure Python 3 is installed
2. Navigate to the project directory
3. Run the script:

```bash
python extractor.py
````

The program will:

* Read data from `sample_input.txt`
* Extract valid structured data
* Mask sensitive fields
* Save results to `sample_output.json`

## Output Format

The output is written in **JSON format** for clarity and ease of downstream processing.

Example:

```json
{
    "emails": ["support@example.com"],
    "urls": ["https://www.example.com"],
    "phones": ["123-456-7890"],
    "credit_cards": ["**** **** **** 1111"],
    "times": ["09:00"],
    "hashtags": ["#FrontendDev"]
}
```


