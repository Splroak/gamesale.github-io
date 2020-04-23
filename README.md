This is a simple API to retrieve data from an existing game sale database. It is made with Flask and flask-restful extension.

[Website](http://flask-env.eba-rppbmmfr.eu-north-1.elasticbeanstalk.com/)
## FILES:

1. game_data.csv:
  - Free database from [Kaggle](https://www.kaggle.com/rush4ratio/video-game-sales-with-ratings). The database consists mainly of sales data of different games.
2. csv-to-json-converter.py:
  - This file is used to convert the downloaded csv file to JSON.
  - execute this file will simply undo all the POST, PUT or DELETE methods.
3. main.py:
  - Main file that builds the API.
  - execute this file to set up the API on local environment.
  
## API Docs:
#### GET api/v1/games/
  Return a list of games. Each call is limit to 20 results unless specified otherwise.
  |Parameter|Description|
  |-----------|-----------|
  |*limit*|the number of results you want to call|
  
#### GET api/v1/games/[game-id]/
  Search games by IDs.

#### GET api/v1/sales/
  Return a list of game organized by their sales accross different platforms.
  |Parameter|Description|
  |-----------|-----------|
  |*limit*|the number of results you want to call|
  
#### GET api/v1/sales/search
  Search games by their names.
  |Parameter|Description|
  |-----------|-----------|
  |*name*|Name of the game you want to return|
#### POST api/v1/games/
  Post a new game to the game endpoint.
  |Parameter|Description|
  |-----------|-----------|
  |*name*|Name of the game you want to return|
  |*platform*| Platform on which the game was piblished on|
  |*year*| The game's release year|
  |*genre*| The game's genre|
  |*publisher*| The game's publisher|
  |*eu_sales*| The game's sales in EU region|
  |*na_sales*| The game's sales in NA region|
  |*JP_sales*| The game's sales in JP region|
  |*other_sales*| The game's sales in other parts of the world|
  |*global_sales*| The game's total sales|
  |*developer*| The game's developer|

#### PUT api/v1/games/search/
  Update an existing game.
  |Parameter|Description|
  |-----------|-----------|
  |*name*|Name of the game you want to return|
  |*platform*| Platform on which the game was piblished on|
  |*year*| The game's release year|
  |*genre*| The game's genre|
  |*publisher*| The game's publisher|
  |*eu_sales*| The game's sales in EU region|
  |*na_sales*| The game's sales in NA region|
  |*JP_sales*| The game's sales in JP region|
  |*other_sales*| The game's sales in other parts of the world|
  |*global_sales*| The game's total sales|
  |*developer*| The game's developer|
 
 #### DELETE api/v1/games/search/
  Delete a game by ID
