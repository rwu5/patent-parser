import os
import requests

def download_url(url, directory):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Extract the filename from the URL
        filename = url.split('/')[-1]
        
        # Create the subdirectory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the content to a file in the subdirectory
        with open(os.path.join(directory, filename), 'wb') as f:
            f.write(response.content)
        
        print(f"File saved: {filename}")
    else:
        print(f"Failed to download {url}. Status code:", response.status_code)

if __name__ == "__main__":
    for yrs in range(2017, 2025):
        with open("./patentZip/" + str(yrs) + ".txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                # Strip newline characters and whitespace
                url = line.strip()
                # Download the URL and save it to the subdirectory
                print("printing: " + url)

                download_url(url, "./patentZip/" + str(yrs))
