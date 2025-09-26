# Week 2 - Python Intro Exercises
TODO:write requrements.txt and explain more about each excerise.
## Dependencies
All requirements are listed in requirements.txt
You can install them using pip:
```pip install -r requirements.txt```


**Intro to Pandas is run in Jupyter Notebook, which needs to be installed.**

## Running the scripts

The scripts **except Intro to Pandas** should be run from the root folder, (In this case "Python Intro")
All data for exercises is in the data folder, scripts are in individual folders.
The scripts folders also contain an output folder if needed.

## Exercises
### Python Intro Exercise
The intro exercise was quite simple, the biggest challenge was plotting the data 
and figuring out how to count the number of occurrences. I decided to use Counter from the collections module,
which also nicely integrates with matplotlib/seaborn for plotting.
I've never really gotten a hang of the plot building, so I used an LLM to help me with the data visualization.

### Logfile Analysis
The logfile analysis was also quite simple and straightforward. 
You simply need to split the lines and access the correct index andd make a data structure that handles the 4 categories.

### Error Handling and Data Migration
This exercise was a bit more challenging, as I am not very familiar with error handling.
I used try/except blocks to handle potential errors when reading the CSV file and converting data types.
I implemented a buffer to handle missing values and a check for each field to ensure data integrity.
This could be improved by imputing ID from row index. I also added user input for the input and output file names.

### Intro to Pandas
This exercise was done in a Jupyter Notebook, which is included in the folder. They can also be found in this gist: https://gist.github.com/whelixw/4afe0d51fbadbd14ecbc9c9e489eb306

The exercise was very open-ended, so I just cleaned up the data and explored it with some basic plots.

