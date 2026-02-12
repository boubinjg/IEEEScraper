import os
import requests
import pandas as pd
import time

import os
import requests
import pandas as pd
import time

API_KEY = os.getenv("IEEE_API_KEY") #Add your key as an environment variable
BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"

#SEARCH_TERM = '((AI OR LLM OR GAI OR "generative AI" OR "language model") AND (align* OR RAG OR "retrieval augmented generation” ) AND ("social robotics" OR anthropomorphism OR companion* OR “mind perception”))'
SEARCH_TERM = "generative AI"
MAX_RECORDS_PER_CALL = 200                # IEEE max is usually 200

def fetch_all_metadata(query):
    all_records = []
    start_record = 1
    total_records = None

    while True:
        params = {
            "apikey": API_KEY,
            "format": "json",
            "querytext": query,
            "max_records": MAX_RECORDS_PER_CALL,
            "start_record": start_record
        }

        #response = requests.get(BASE_URL, params=params)
        #response.raise_for_status()
        #data = response.json()

        if total_records is None:
            #total_records = int(data.get("total_records", 0))
            print(f"Total records found: {total_records}")
            print("Your Daily API Limit is at most 40,000 papers from 200 API calls. Do you wish to scrape these records?")
            user_resp = input("Type Y|y to continue, or anything else to exit: ")
            if(user_resp != "Y" and user_resp != "y"):
                print("Exiting")
                exit()
            else:
                print("Scraping...")
        
        articles = data.get("articles", [])
        if not articles:
            break

        for article in articles:
            record = {
                "title": article.get("title"),
                "authors": ", ".join(
                    [a.get("full_name", "") for a in article.get("authors", {}).get("authors", [])]
                ),
                "abstract": article.get("abstract"),
                "publication_title": article.get("publication_title"),
                "publication_year": article.get("publication_year"),
                "volume": article.get("volume"),
                "issue": article.get("issue"),
                "start_page": article.get("start_page"),
                "end_page": article.get("end_page"),
                "doi": article.get("doi"),
                "publisher": article.get("publisher"),
                "isbn": article.get("isbn"),
                "issn": article.get("issn"),
                "pdf_url": article.get("pdf_url"),
                "html_url": article.get("html_url"),
                "content_type": article.get("content_type")
            }
            all_records.append(record)

        start_record += len(articles)
        print(f"Fetched {start_record - 1} / {total_records}")

        # Respect API rate limits
        time.sleep(0.5) 

        if start_record > total_records:
            break

    return all_records


if __name__ == "__main__":
    if not API_KEY:
        raise ValueError("IEEE_API_KEY environment variable not set")

    records = fetch_all_metadata(SEARCH_TERM)

    df = pd.DataFrame(records)
    df.to_csv("ieee_metadata.csv", index=False)

    print(f"Saved {len(df)} records to ieee_metadata.csv")
