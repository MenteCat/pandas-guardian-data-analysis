The aim of this challenge is to pull data from the [Guardian Public API](https://open-platform.theguardian.com) to return all articles related to both "AI" and "analytics" .

The data are saved to a csv "gardian_original.csv".

The results are sorted in descending order based on the `webPublicationDate` column.
   
The challenge consists in making the following changes to the CSV then to save the Pandas dataframe to the `guardian_final.csv` file. 

1. Format the dates into day/month/year format and add the results as a new column named `formatted_date`
2. Extract the year from `webPublicationDate` into a new column named `year`
3. Format the column headers to snake_case

This repository doesn't come with a `requirements.txt`; the only two packages required to run the script are `requests`, `pandas` and `numpy`.
