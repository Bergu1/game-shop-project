# Game Shop Project

## Description

The **Game Shop Project** is a web application inspired by Steam, where users can purchase games, explore what games their friends own, and manage their gaming experience. The platform offers features like account management, friend lists, wallet integration, currency conversion, detailed game browsing, and the ability to export account history as PDF reports.

## Features
- **Account Management**: Register, log in, update account details, and delete accounts.
- **Game Store**: Browse and sort games, view detailed game descriptions, purchase games, or gift them to friends.
- **Wallet System**: Add funds, view transaction history, and export account history as a PDF.
- **Friend System**: Send and manage friend requests, view friend lists, and check games owned by friends.
- **Currency Conversion**: Transactions in PLN, USD, or EUR with real-time conversion.

## Technology Stack
- **Backend**: Python, Django framework
- **Frontend**: HTML, CSS, and Django templates
- **Database**: PostgreSQL
- **Other**: Git, Docker, Github Actions, AWS
- **Tests**: Unittests, Integration Testing
- **Documentation**: Postman
- **Currency Conversion**: Real-time conversion between supported currencies (PLN, USD, EUR).

## Running the Project with Docker
### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/game-shop-project.git
   cd game-shop-project
   ```
2. Build the Docker container:
   ```bash
   docker-compose build
   ```
3. Run the application:
   ```bash
   docker-compose up
   ```
   
## Backend Documentation
The file `GameStore_backend_documentation.postman_collection.json` contains detailed backend documentation in the Postman export format (v2.1).

To import the documentation into Postman:
1. Open Postman.
2. Select the Import option.
3. Upload the file `GameStore_backend_documentation.postman_collection.json`.

## Live Demo 
You can view the live application at this link:
[game - shop - project - Live Demo](http://ec2-52-91-102-211.compute-1.amazonaws.com/login/)
