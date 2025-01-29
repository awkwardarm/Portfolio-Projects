# Goal
Practice data ETL by scraping Pokèmon card data from the website https://ptcgpocket.gg/ using Python and BeautifulSoup. This proved an interesting excercise in handling a diverse set of data with complicated scraping and cleaning. 

# Key Lessons

- Utilize PlayWright and time delays when scraping via BeautifulSoup on webpages with JavaScript-rendered content. 
- Break the pipeline into multiple steps as scraping a single Pokèmon card could take up to 180 seconds. I saved `.html` files for each card for later parsing. 
- Create a custom `PokemonCard` class for extracting data and handling the various types of cards processing the relevant data in the scraped HTML.

# Steps

1. Iterate through all Pokèmon cards in `collection.csv` and save all `.html` files to `card-html-files` folder.
2. Create class `PokemonCard` in `pokemon_utilites.py` for processing data.
3. Use Jupyter Notebook `02-ETL-pokemon.ipynb` to iterate through all `.html` files, extract data, clean, add new row to a dataframe, and save the dataframe to `pokemon-cards.csv`.


