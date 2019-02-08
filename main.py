import pandas as pd
from requests import get, RequestException
from bs4 import BeautifulSoup

def get_data(url:str) -> BeautifulSoup:
    """Scrape discography wikipedia page, returns html """
    try:
        website_text = requests.get(url).text
        soup = BeautifulSoup(website_text, "html5lib")
        return soup
    except RequestException as e:
        print(str(e))
    
def get_record_entries(soup:BeautifulSoup) -> list:
    """
    Extracts all headers listing the different series.
    Add each record in a series to a list. 
    """
    data_class = soup.find("div", class_= "mw-content-ltr")
    rows = []
    lista = data_class.findAll("h3")
    for each in lista:
        ul = each.findNextSibling("ul")

        for every in ul.findAll("li"):
            rows.append([each.text, every.text])
    return rows

def create_data_frame(rows:list) -> DataFrame: 
    """add list of records into a pandas dataframe """
    column_names = ["Series","Record"]

    df = pd.DataFrame(rows, columns=column_names)

    df["Series"] = df["Series"].map(lambda x: x.rstrip('series[edit]'))

    return df

def save_df_to_csv(df:DataFrame) :
    """save dataframe containing records into a csv file """
    return df.to_csv('blue_note_discography.csv')
     

def main():
    url: str = "https://en.wikipedia.org/wiki/Blue_Note_Records_discography"
    soup = get_data(url)
    rows = get_record_entries(soup)
    df = create_data_frame(rows)
    save_df_to_csv(df)

if __name__ == "__main__":
    main()

"""
TODO:

0) create virtual env 
00) try/except block for scrape
1) documentation and type hinting
2) swap for loop for list comprehension
3) extract more data for each record
4) import to Postgres DB
5) tests
"""
