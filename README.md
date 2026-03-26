# Amazon Hashing Project

## Overview
This project is for a data structures / algorithms assignment.  
I will build a hash-based indexing and frequency analysis application for noisy real-world Amazon product review data.

## Main Algorithm
- Hashing

## Project Goal
The goal of this project is to move beyond clean classroom datasets and apply hashing to real-world data with:
- 568,454 items
- multiple metadata fields
- missing values
- inconsistent formatting
- varied data types

## Planned Application
I plan to use hashing for:
- indexing review records by product-related keys
- indexing records by user / author-related keys
- frequency counting for ratings, brands, or other metadata
- testing insertion and lookup efficiency when the key count exceeds 10,000

## Dataset
I plan to use the following public dataset:
- Amazon Product Reviews Dataset (Kaggle) 
- link: https://www.kaggle.com/code/saurav9786/recommendation-based-on-amazon-food-review/input
- Source: PromptCloud

## Project Structure
```text
amazon-hashing-project/
│
├── data/
│   └── .gitkeep
│
├── src/
│   ├── inspect_data.py
│   ├── preprocess.py
│   ├── hashtable.py
│   ├── indexer.py
│   ├── benchmark.py
│   └── main.py
│
├── README.md
├── requirements.txt
├── .gitignore
└── proposal.md
```

## AI statement
AI was used to search for solutions to github version conflicts on March 23, 25 commits.

## How to run
python src/main.py
python src/benchmark.py