from bs4 import BeautifulSoup
import re
import os

def extract_claim_text(html_file, patent_info):
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    if "Patent Not Issued For This Number" in html_content:
        patent_info['type'] = "Patent Not Issued For This Number"
        return
    
    soup = BeautifulSoup(html_content, 'html.parser')

    # Patent title
    patent_info['title'] = soup.find(class_='table_data', attrs={'style':"text-transform: uppercase"}).get_text()

    # CPC codes
    try:
        cpc_list = re.split(r'\[|\]', re.sub(r'\([^)]*\)', '', soup.find(class_='table_data', attrs={'align':"left"}).get_text()).replace('CPC', ''))
        patent_info['cpc_main'] = cpc_list[0].strip()
        if len(cpc_list) > 2:
            patent_info['cpc_sub'] = [x.strip() for x in cpc_list[1].split(';')]
    except:
        patent_info['cpc_main'] = soup.find(class_='table_data', attrs={'colspan':"2"}).get_text().strip()
        patent_info['type'] = "Design"
        return
    
    # Claim text
    if soup.find(class_='claim_text_root'):
        patent_info['claims'] = soup.find(class_='claim_text_root').get_text()
    elif soup.find(class_='para_text'):
        patent_info['claims'] = soup.find(class_='para_text').get_text()

    claim_texts = soup.find_all(class_='claim_text')

    for claim_text in claim_texts:
        patent_info['claims'] += re.sub(r'\s+', ' ', claim_text.get_text()).strip()
    
    return patent_info
    #print(patent_info)

def list_subdirectories(directory):
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d)) and d != "json"]
    return subdirectories

# Usage
for yrs in range(2010, 2025):
    # giving directory name
    mainDir = './patentZip/' + str(yrs)
    subdirs = list_subdirectories(mainDir)
    
    # giving file extension
    ext = ('.html')

    pCount = 0
    eCount = 0
    # iterating over all files
    for subdir in subdirs:
        dirname = mainDir + "/" + subdir + "/"
        weeklyPatent = []
        for files in os.listdir(dirname):
            if files.endswith(ext):
                pCount += 1
                try:
                    patent_info = {}
                    patent_info['id'] = files.split("-")[0]
                    row = extract_claim_text(dirname + files, patent_info)
                    if row:
                        weeklyPatent.append(row)
                except Exception as e:
                    eCount += 1
            else:
                continue
        filename = mainDir + "/json/" + subdir + ".txt"
        print(filename)
        with open(filename, 'w') as f:
            for patent in weeklyPatent:
                f.write(str(patent) + '\n')
        

                        