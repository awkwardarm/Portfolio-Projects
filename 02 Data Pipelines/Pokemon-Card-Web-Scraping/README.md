# Goal
Practice data ETL by scraping Pokèmon card data from the website https://ptcgpocket.gg/ using Python and BeautifulSoup. This proved an interesting excercise in handling a diverse set of data with complicated scraping and cleaning. 

# Key Lessons

- Utilized PlayWright and time delays when scraping via BeautifulSoup on webpages with JavaScript-rendered content. 
- Split the pipeline into multiple steps as scraping a single Pokèmon card could take up to 180 seconds. I saved `.html` files for each card for later parsing. 
- Created a custom `PokemonCard` class in `pokemon_utilities.py` for extracting data and handling the various types of processing of the relevant data in the `.html` files.

# Steps

1. `01-html-extraction.py` iterates through all Pokèmon cards in `collection.csv` and saves all `.html` files to `card-html-files` folder.
2. `02-ETL-pokemon.ipynb` iterates through all `.html` files using the `PokemonCard` class to extract, clean, and add new data to a dataframe. The dataframe is then exported to `pokemon-cards.csv` for later exploratory data analysis.