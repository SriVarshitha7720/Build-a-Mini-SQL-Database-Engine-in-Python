# In-Memory SQL Engine 
This project implements a simplified in-memory SQL query engine in Python.
It allows you to load a CSV file and execute basic SQL queries interactively through a command-line interface (CLI).


<img width="620" height="371" alt="image" src="https://github.com/user-attachments/assets/34b8d0c2-b5da-463f-944c-b105982026c3" />


The engine demonstrates the core principles of a database:

>> Parsing SQL queries

>> Filtering rows with WHERE

>> Selecting specific columns

>> Aggregating data with COUNT


# Setup & Run 

**1.Clone the repository** 

**Bash**:-

>> git clone <your-repo-url>


>> cd in_memory_sql_engine

**2.Prepare CSV files**


Place your CSV files in the data/ folder (e.g., people.csv)

**Example people.csv:**

id,name,age,country

1,Alice,34,USA

2,Bob,28,Canada

3,Charlie,45,USA

4,Diana,40,UK

**3.Run the CLI**

**Bash**

>>python engine.py


**4.Enter the CSV file path when prompted**

Enter CSV file path: data/people.csv


**5.Type SQL queries in the REPL**


sql> SELECT * FROM people;
sql> SELECT name, age FROM people WHERE age > 30;
sql> SELECT COUNT(*) FROM people WHERE country = 'USA';
sql> exit


**Files**


> parser.py → SQL parser

> engine.py → query execution engine + CLI

> data/ → sample CSV files (people.csv, etc.)
