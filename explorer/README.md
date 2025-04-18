# Countries Explorer

A Django web application for exploring and displaying information about countries around the world.

## Overview

Countries Explorer is a web-based application that fetches and displays information about countries using the RestCountries API. The application allows users to browse countries, search by name, filter by population size, leave a rating and review as well adding to a favorites list, while viewing detailed information about each country including their flag, capital, population, currency, and language.

## Features

- Browse a list of all countries
- Search countries by name
- Filter by population size
- View detailed information about each country
- Manually refresh country data from the API
- Add to favorite list and leave review
- Register/Login authentication
- Responsive design using Bootstrap

## Technologies Used

- **Backend**: Django 5.1.7
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5.3
- **API**: RestCountries API
- **Styling**: CSS
- **Deployment**: Local development server

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL
- pip (Python package manager)
- Poetry (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd explorer
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or if using Poetry:
   ```bash
   poetry install
   ```

4. Configure PostgreSQL:
   ```bash
   # Login to PostgreSQL
   psql -U postgres

   # Create database and user
   CREATE DATABASE explorer_db;
   CREATE USER explorer_user WITH PASSWORD 'your_password';
   ALTER ROLE explorer_user SET client_encoding TO 'utf8';
   ALTER ROLE explorer_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE explorer_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE explorer_db TO explorer_user;
   GRANT USAGE ON SCHEMA public TO explorer_user;
   GRANT CREATE ON SCHEMA public TO explorer_user;
   \q
   ```

5. Update database settings in `explorer/settings.py` with your credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'explorer_db',
           'USER': 'explorer_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

6. Apply migrations:
   ```bash
   python manage.py migrate
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Visit http://127.0.0.1:8000/ in your browser to access the application.
9. Click on "Update Countries Data" to fetch country data from the API for the first time.

## API Details

### External API
The application uses the RestCountries API to fetch country data:

- https://restcountries.com/v3.1/all - Fetches all countries

### Internal App Structure

#### Models:
- **Country**: Stores country information (name, capital, population, currency, language, flag)

#### Views:
- **HomeView**: Displays the homepage
- **CountryListView**: Lists all countries
- **CountryDetailView**: Shows detailed information about a specific country
- **CountrySearchView**: Handles search functionality
- **FetchCountryDataView**: Refreshes country data from the API

#### URLs:
- `/` - Home page
- `/countries/` - List of all countries
- `/countries/<id>/` - Detail view for a specific country
- `/search/` - Search page
- `/fetch-countries/` - Endpoint to refresh country data
- `/my-favorites/` - Favorites page
- `/add-review/` - Review page

## Usage Guidelines

### Browsing Countries
- Visit the homepage and click "Browse Countries" to see all countries in the database
- Use the pagination controls at the bottom to navigate through multiple pages

### Searching
- Use the search page to find countries by name
- Enter a search term in the text box and click "Search"
- Results will show matching countries with their basic information

### Viewing Country Details
- Click on the "View" button next to any country to see its detailed information
- The detail page shows comprehensive information including:
  - Flag
  - Capital city
  - Population
  - Currency
  - Official language

### Refreshing Data
- Click the refresh button (circular arrow icon) in the bottom-right corner of any page to update all country data from the API
- The system will display a confirmation message showing how many countries were created or updated

## Customization

### Styling
The application uses Bootstrap 5.3 for styling. To customize the appearance:

- Edit the CSS in `country/static/country/css/country.css`
- Or modify the Bootstrap CDN link in `base.html` to use a different theme

### Adding Features
To extend the application with more features:

- Add new fields to the Country model in `country/models.py`
- Update `utils.py` to fetch and process additional data
- Modify templates to display new information

## Troubleshooting

### Database Connection Issues
If you encounter database connection errors:

- Verify PostgreSQL is running
- Check database credentials in `settings.py`
- Ensure the database user has proper permissions

### API Fetch Errors
If country data isn't loading:

- Check your internet connection
- Verify the RestCountries API is operational
- Look for error messages in the Django console