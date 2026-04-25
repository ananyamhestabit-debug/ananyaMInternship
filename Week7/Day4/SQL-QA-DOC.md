# SQL QUESTION ANSWERING SYSTEM

## Overview

Converts natural language queries into SQL queries and executes them.

## Flow

1. User enters question
2. Schema is loaded
3. LLM generates SQL query
4. Query is validated
5. Query is executed
6. Results are summarized

## Components

### SQL Generator

* Uses LLM
* Schema-aware prompting

### Validator

* Only SELECT allowed
* Blocks unsafe queries

### Executor

* Runs SQL on SQLite
* Returns rows + columns

### Schema Loader

* Extracts table and column info

## Example

User: "Top artists in India"

Generated SQL:

```sql
SELECT artist FROM sales WHERE country='India'
```

## Commands

```bash
python database/sample_db.py
streamlit run app.py
```
