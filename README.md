# inspirobot
**Inspirobot: A Customizable Quote Inspiration App**  

Inspirobot is a web application designed to provide users with inspirational quotes based on their interests or desired mode. It leverages the Zen Quotes API to retrieve quotes and allows users to select keywords (tags) to personalize their experience. 

## Features
* Keyword selection for targeted inspiration
* Author selection for specific author's quotes
* Integration with Zen Quotes API for a vast quote collection
* User-friendly interface with Tailwind CSS for clean styling
* Built with Django for a robust web framework
* Interactive elements powered by HTMX

## Technologies
* Django (Python web framework)
* Tailwind CSS (utility CSS framework)
* HTML
* HTMX for interactive elements
* Zen Quotes API (external quote source)

## Zen Quotes API Information
This application uses the Zen Quotes API, which offers:
* **Free Tier**: 5 requests per 30 seconds with attribution requirement
* **Paid Tier**: Unlimited requests, CORS support, no attribution required

**Note**: If using the free tier, attribution with a link to zenquotes.io is required. Consider implementing local caching to optimize API usage and stay within rate limits.

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your Zen Quotes API key (if using paid tier) in settings
4. Run migrations: `python manage.py migrate`
5. Start the development server: `python manage.py runserver`

## Rate Limiting & Best Practices
* Free tier: Maximum 5 requests per 30 seconds
* Implement local quote caching to reduce API calls
* Use batch API calls when possible for better efficiency

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2024 Nuru Umar Mohammed

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.