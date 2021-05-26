from bs4 import BeautifulSoup
import requests
import json
import os
import sys


# Random Faculty link:
scholar_url = 'https://scholar.google.com/citations?user=VMQkbCgAAAAJ&hl=en&cstart=100&pagesize=200'

#scholar_url = 'https://scholar.google.com/citations?hl=en&user=Ubvqt-kAAAAJ&cstart=0&pagesize=100'
response = requests.get(scholar_url)
print(response)
soup = BeautifulSoup(response.content, 'lxml')
publications = []
publication_results = soup.find_all('tr', class_='gsc_a_tr')

# with open("sarit_results.json", "r") as read_file:
#     if os.stat("sarit_results.json").st_size > 0:
#         print("File exists")
#         publications = json.load(read_file)

# sys.exit()
for publication in publication_results:
    # print(publication.prettify())
    article = {}
    title = publication.find('a', class_='gsc_a_at').text
    article['title'] = title
    title_link = publication.find('a')['data-href']
    publication_link = 'https://scholar.google.com/' + title_link
    #print(f"Publication link is {publication_link}")
    pub_response = requests.get(publication_link)
    pub_soup = BeautifulSoup(pub_response.content, 'lxml')

    rows = pub_soup.find_all('div', class_="gs_scl")
    # print(pub_response)
    # print(rows)

    for row in rows:
        field = row.find('div', class_="gsc_vcd_field")
        value = row.find('div', class_="gsc_vcd_value")
        #print(f"Field: {field.text}, Value: {value.text}")
        if field.text == 'Authors':
            article["authors"] = value.text
        elif field.text == 'Publication date':
            article["publication_date"] = value.text
        elif field.text == 'Journal':
            article["journal"] = value.text
        elif field.text == 'Publisher':
            article["publisher"] = value.text
        elif field.text == 'Volume':
            article['volume'] = value.text
        elif field.text == 'Issue':
            article['issue'] = value.text
        elif field.text == 'Pages':
            article['pages'] = value.text
        elif field.text == 'Description':
            article['abstract'] = value.text
        elif field.text == 'Conference':
            article['conference'] = value.text
        elif field.text == 'Book':
            article['book'] = value.text
        elif field.text == 'Institution':
            article['institution'] = value.text
        elif field.text == 'Inventors':
            article['inventors'] = value.text
        elif field.text == 'Patent office':
            article['patent_office'] = value.text
        elif field.text == 'Patent number':
            article['patent_number'] = value.text
        elif field.text == 'Application number':
            article['application_number'] = value.text

    # print(article)
    publications.append(article)
    print(len(publications))


with open('sarit_results.json', 'w') as outfile:

    json.dump(publications, outfile)
