# World of Tanks Clan Data Collector

This Python application is designed to fetch and store data related to World of Tanks clans. It leverages the World of Tanks API to gather the data and subsequently stores it in a database for further use and analysis.

## Features

- **Clan Details Collection**: The application fetches detailed information about clans based on the clan name. This includes clan creation date, number of members, clan rating, and more.

- **Player Statistics Collection**: The application fetches and stores player statistics. This includes data such as battles fought, wins, losses, survival rate, and more.

- **Player's Tanks Collection**: The application fetches and stores data about each player's tanks. This includes data such as the tank's nation, type, tier, and more.

- **Interactive Dashboard**: The collected data is used to fuel an interactive dashboard. This dashboard provides a visual representation of the data, making it easier to understand and analyze.


## How to Use

1. Clone the repository.
2. Install the required Python packages.
3. Set up your database.
4. Run the application and mention the clan name for which you want to collect the statistics.
5. You can then use the data from your db in any other scope, but for me, it serves as data for a Tableau dashboard.
