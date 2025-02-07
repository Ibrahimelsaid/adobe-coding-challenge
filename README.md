# Adobe Programming Challenge

## Overview
Take a variable number of identically structured JSON records and de-duplicate the set.

An example file of records is given in the accompanying 'leads.json'. The output should be in the same format, with duplicates reconciled according to the following rules:

1. The data from the newest date should be preferred.
2. Duplicate `_id`s count as duplicates. Duplicate `email`s count as duplicates. Both must be unique in our dataset. Duplicate values elsewhere do not count as duplicates.
3. If the dates are identical, the data from the record provided **last in the list** should be preferred.

**Simplifying assumption:** The program can do everything in memory (don't worry about large files).

The application should also provide a **log of changes**, including:
- Some representation of the **source record**
- The **output record**
- The **individual field changes** (previous value → new value)

This program is implemented as a **command-line tool**.

## 🚀 Steps to Run the Program

1. **Clone the repository:**
   git clone https://github.com/yourusername/adobe-coding-challenge.git

2. **Make the script executable:**
    chmod +x src/json_deduplicator.py

3. **Run the script with your input file:**
    ./src/json_deduplicator.py data/leads.json (input file)

4. **Check the output files:**
    cat data/deduplicated_leads.json
    cat data/change_log.json

5. **Run tests:**
    pytest tests/

