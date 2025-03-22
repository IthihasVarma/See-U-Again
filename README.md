# See-U-Again

## Description
See U Again is a powerful OSINT (Open-Source Intelligence) tool designed to gather, analyze, and correlate publicly available information to identify and track individuals. By leveraging multiple data sources, web scraping, image recognition, and automated data aggregation, See U Again provides comprehensive intelligence reports.

The accuracy of the results improves significantly with the amount and specificity of the input data provided by the user. The more details given—such as name, location, images, online usernames, or email addresses—the more precise and effective the search becomes.

Core Features:
✔ Multi-Source Data Aggregation – Collects data from social media, public records, and online databases.
✔ Facial Recognition & Image Processing – Matches target images with publicly available photos.
✔ Automated Web Scraping – Retrieves real-time data from static and dynamic websites.
✔ API Integration – Uses third-party OSINT APIs for enhanced results.
✔ Ethical & Legal Compliance – Designed for responsible use while respecting privacy laws.

Libraries & Technologies Used:
🔹 Web Scraping: requests, BeautifulSoup, selenium
🔹 Automated Data Search: Various OSINT APIs
🔹 Image Processing & Facial Recognition: face_recognition, OpenCV, Pillow
🔹 Database Management: MongoDB
🔹 Data Aggregation & Pattern Matching: pandas, re (Regular Expressions)
🔹 Automation & Deployment: Flask for the backend, Task schedulers for automation

See U Again is built for investigators, cybersecurity professionals, and researchers who need a reliable OSINT tool for tracking digital footprints.

## Installation Instructions
To set up the project locally, follow these steps:
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required libraries using:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python app.py
```
Access the application in your web browser at `http://localhost:5005`.

## Library Explanations
- **requests**: For making HTTP requests.
- **beautifulsoup4**: For parsing HTML and XML documents.
- **selenium**: For automating web browser interaction.
- **webdriver-manager**: For managing browser drivers for Selenium.
- **Flask**: The web framework used for building the application.
- **flask-jwt-extended**: For handling JSON Web Tokens (JWT) for authentication.
- **pymongo**: For interacting with MongoDB.

## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

## License
This project is licensed under the Apache 2.0 License.

## Project Overview
The See-U-Again project is a Flask application designed to provide a web interface for searching data using a scraping function. The application utilizes JWT for authentication and has several routes for different functionalities, including user management and data retrieval.

The back end is built using Flask, which handles requests and responses, while the data scraping functionality is implemented using libraries such as BeautifulSoup and Selenium. The application is structured to allow for easy expansion and integration of additional features.

## Current Status
While the back end is functional, the front end is not yet fully developed. The following components are still missing:
- Integration of the front end and back end: The user interface (UI) is not yet connected to the back end services.
- Development of HTML and UI/UX: The HTML templates and user experience design have not been created, which means that users currently interact with the application through a basic interface.

Contributors are welcome to help with the development of the front end, including creating HTML templates and ensuring a seamless integration with the back end services.
