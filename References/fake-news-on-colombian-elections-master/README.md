# Fake news on the 2018 presidental elections in Colombia

## Objective

The purpose of this project is to identify fake news that were shared during the presidential campaign of 2018 in Colombia, and to see if a change in the perception or intention of voting for the different candidates were influenced by this factor.

## A little context

Some news have mentioned that one of the candidates might have used the services of Cambridge Analytica, the same company that triggered a scandal after the US presidential elections of 2016. You can check those out [here](https://colombiareports.com/cambridge-analytica-in-colombia-uribe-fuels-speculation-of-election-fraud/) and [here](https://www.pulzo.com/nacion/yohir-akerman-denuncia-asesoria-cambridge-analytica-centro-democratico-PP460015) and [here](https://www.elespectador.com/opinion/asesoria-secreta-columna-746323). If you look further, you'll surely find more sources suggesting that.

This wouldn't come as a surprise, since the Plebiscito por la paz, a referendum to vote on a deal between the Colombian government and the oldest guerrilla from the Americas, was known to be tainted by fake news and misinformation that finally led to the result being negative.

Other electoral processes in different countries, have been known or speculated to be influenced by these tactics, which is an awful hit on democracy.

## Structure of the project

This project will be mostly analytical. Data from different social networks will be gathered, to analyze the sentiment among users toward the different candidates, and if it changed after fake news were divulged.

The first step of this project is, of course, to gather the data.

**Update** On [this notebook](./retrieving_the_data.ipynb) about retrieving the data, you'll find steps to generate a dataset with data scraped from Twitter. For that purpose, a script `./twitter_data_extractor.py` was created, which will use Selenium to search for different queries on Twitter, and parse the results with BeautifulSoup. On the notebook, you'll also find steps to download data using the Twitter API, however, you'll need to sign up for those in case you want to run it by yourself, and the free version won't allow to retrieve too many tweets. I strongly recommend using the extractor. I'm not uploading the data extracted by myself, but you can personally request the data from me in order to recreate the steps that will come next.
