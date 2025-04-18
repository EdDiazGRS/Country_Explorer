# country/utils.py
import requests
from .models import Country

def refresh_country_data():
    """
    Refreshes country data from the API and returns refresh statistics.
    """
    api_url = 'https://restcountries.com/v3.1/all'
    
    # Stats tracking
    countries_created = 0
    countries_updated = 0
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        
        countries_data = response.json()
        
        for country_data in countries_data:
            # Extract data
            name = country_data.get('name', {}).get('common', '')
            
            # Skip if no name (data integrity check)
            if not name:
                continue
            
            # Get capital (handle possible empty list)
            capitals = country_data.get('capital', [])
            capital_city = capitals[0] if capitals else ''
            
            # Get population
            population = country_data.get('population', 0)
        
            # Get currency (extract first currency code)
            currencies = country_data.get('currencies', {})
            currency_code = next(iter(currencies), '') if currencies else ''
            
            # Get language (extract first language)
            languages = country_data.get('languages', {})
            language = next(iter(languages.values()), '') if languages else ''
            
            # Get flag URL
            flag = country_data.get('flags', {}).get('png', '')
            
            # Save to database - create or update
            country, created = Country.objects.update_or_create(
                name=name,
                defaults={
                    'capital_city': capital_city,
                    'population': population,
                    'currency': currency_code,
                    'language': language,
                    'flag': flag
                }
            )
            
            if created:
                countries_created += 1
            else:
                countries_updated += 1
        
        return {
            'success': True,
            'created': countries_created,
            'updated': countries_updated,
            'total': countries_created + countries_updated,
            'message': f'Imported {countries_created + countries_updated} countries ({countries_created} new, {countries_updated} updated)'
        }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}'
        }