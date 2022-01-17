# DSCryptoMonitor
Made for the project assignment for the Data Science master course on the University of Twente.

## Prerequisites
- Docker and Docker Compose
- Python (>3.9)
- (Recommended) Virtualenv
- Google Chrome
- [ChromeDriver](https://chromedriver.chromium.org/home) (accesible from PATH)

## Installation
1. Clone the repository: `git clone https://github.com/Drevanoorschot/DSCryptoMonitor.git`
2. Change directories: `cd DSCryptoMonitor`
4. Run the docker compose: `docker-compose up -d`
5. (Recommended) Create virtualenv: `virtualenv crypto && source crypto/bin/activate`
6. Install dependencies: `pip install -r requirements.txt`
7. Apply migrations: `./manage.py migrate`
8. Run development server: `./manage.py runserver localhost:8000`

5. Run the docker-compose: `docker-compose up -d`
