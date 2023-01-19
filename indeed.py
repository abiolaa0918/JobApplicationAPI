import requests
from bs4 import BeautifulSoup

def apply_indeed_jobs(keywords, location):
    # Set the base URL for the Indeed job search
    base_url = 'https://www.indeed.com/jobs?'

    # Send an HTTP request to the Indeed job search page
    response = requests.get(base_url, params={'q': keywords, 'l': location})

    # Parse the HTML of the job search results page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all of the job listings on the page
    job_listings = soup.find_all('div', class_='jobsearch-SerpJobCard')

    # Iterate through the job listings
    for listing in job_listings:
        # Find the job title and link
        title = listing.find('h2').text
        link = listing.find('a')['href']

        # Print the job title and link
        print(f'Applying for job: {title}')
        print(f'Job description: {link}')

        # Send an HTTP request to the job application form
        form_response = requests.get(link)

        # Parse the HTML of the job application form
        form_soup = BeautifulSoup(form_response.text, 'html.parser')

        # Find the form element and the form action URL
        form = form_soup.find('form')
        form_action = form['action']

        # Find the form input elements
        inputs = form.find_all('input')

        # Create a dictionary to hold the form data
        form_data = {}

        # Iterate through the form inputs
        for input in inputs:
            # Get the input name and value
            input_name = input['name']
            input_value = input['value']

            # Add the input name and value to the form data dictionary
            form_data[input_name] = input_value

        # Add the resume and cover letter to the form data
        with open('cover_letter.pdf', 'rb') as cover_letter:
            form_data['cover_letter'] = cover_letter.read()

        # Send an HTTP request to submit the form
        submit_response = requests.post(form_action, data=form_data)

        # Print the response from the server
        print(submit_response.text)