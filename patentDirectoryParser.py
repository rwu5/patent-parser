import requests
from bs4 import BeautifulSoup

def save_table_info_to_file(url, filename):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all table tags in the HTML
        tables = soup.find_all('table')

        # Open the file for writing
        with open(filename, 'w') as f:
            # Write the information under each table to the file
            for i, table in enumerate(tables):
                if i == 0:
                        continue
                rows = table.find_all('tr')
                for row in rows:
                    # Find all the cells (td tags) in this row
                    cells = row.find_all(['th', 'td'])
                    row_data = [cell.text.strip() for cell in cells]
                    f.write((url + row_data[0]) + '\n')

        print(f"Table information saved to {filename}")

    else:
        print("Failed to retrieve webpage. Status code:", response.status_code)

if __name__ == "__main__":
    
    # Example usage:
    for yrs in range(2010, 2025):
        url = "https://bulkdata.uspto.gov/data/patent/officialgazette/" + str(yrs)+ "/"
        filename = "./patentZip/" + str(yrs) + ".txt"
        save_table_info_to_file(url, filename)
