#First file for extracting any good given information by amazon in a fashion that I can use for a further data visualization on google datastudio.

#Using this github repo: https://github.com/ian-kerins/amazon-python-scrapy-scraper
#It recommends to use Scrappy API.

#First Template:

import requests
import json
import pandas as pd
import numpy as np

def get_book_info(asin):
    with open("config.json", "r") as file:
        access_token = json.load(file)

    api_access = access_token["access_token"]
    country = "amazon.com.br"
    tld= ".com.br"
    payload = {'api_key': api_access, 'asin': asin, 'country': country, 'tld': tld}
    url = 'https://api.scraperapi.com/structured/amazon/product'
    try:
        response = requests.get(url, params=payload)
    except Exception as e:
        print(e)
        continue
    return response.json()

def get_books_asin():
    with open("books.json", "r") as file:
        books_json = json.load(file)
        
    books_url = books_json["books_url"]
    books_asin = [ book.split('/')[5] for book in books_url ]
    #Fazemos isto pois cometi um erro na listagem das urls, contendo um duplicado, este método é o mais simples para tratar isto.
    return list(set(books_asin))

fields_json = ["name",
          "product_information",
          "brand",
          "full_description",
          "pricing",
          "list_price",
          "shipping_price",
          "availability_status",
          "product_category",
          "average_rating",
          "total_reviews"]

columns = ["nome",
            "editora",
            "idioma",
            "capa_comum",
            "isbn_10",
            "isbn_13",
            "dimensoes",
            "ranking_dos_mais_vendidos",
            "avaliacoes_dos_clientes",
            "brand",            
            "pricing",
            "list_price",
            "shipping_price",
            "availability_status",
            "product_category",
            "average_rating",
            "total_reviews"]

books_df = []
for book in get_books_asin():
    books_info = get_book_info(asin)
        #colocar a chave e o valor. Passar como dicionario para ja montar o dataframe
    book_df_list = { field : book[field] for field in fields_json }
    books_df.append(book_df_list)
    
for book in books_df:
    for keys,values in book["product_information"].items():
        print(keys, values)
        book[keys] = values
    del book["product_information"]

df_final = pd.DataFrame(books_df)

#Treating Dataframe:
df_final.drop(["idade_de_leitura", "pricing", "list_price", "dimensoes", "asin"], axis=1, inplace=True)
df_final = df_final.astype(object).replace(np.nan, 'None')
columns = [ column.replace("_", " ").title().replace(" ", "_") for column in df_final.columns.tolist() ]
df_final.columns = columns


df_final.rename(columns={"Capa_Comum":"Paginas", "Shipping_Price":"Preco_De_Embarcacao"},inplace=True)
ship_price = df_final["Preco_De_Embarcacao"].tolist()
ship_price = [ c.lower() for c in ship_price ]
df_final["Preco_De_Embarcacao"] = ship_price

prd_cat = df_final["Product_Category"].tolist()
prd_cat = [ prd.split("livros")[2:] for prd in prd_cat ]

df_final["Average_Rating"] = df_final["Average_Rating"].astype(float)
df_final["Total_Reviews"] = df_final["Total_Reviews"].astype(int)

editora = df_final["Editora"].tolist()
editoras = [ edit.split(";")[0] for edit in editora ]
df_final["Editoras"] = editoras

def convert_ordinal_num(data_edicao):
    for i in range(len(data_edicao)):
        for j in range(len(data_edicao[i])):
            if data_edicao[i][j].endswith("ª"):
                try:
                    order = int(data_edicao[i][j][:-1])
                    data_edicao[i][j] = f"{order}th"
                    
                except ValueError:
                    pass
    return data_edicao

data_edicao_completo = [ edit.split(";")[-1].strip().split() for edit in editora ]
data_edicao_completo = convert_ordinal_num(data_edicao_completo)
data_edicao_completo = [ " ".join(data) for data in data_edicao_completo ]
data_edicao = [ "-".join(data.split()[2:]).replace("(", "").replace(")","").title() for data in data_edicao_completo ]

def correct_date(data_edicao=data_edicao):
    meses = {
    "Janeiro": "01",
    "Fevereiro": "02",
    "Março": "03",
    "Abril": "04",
    "Maio": "05",
    "Junho": "06",
    "Julho": "07",
    "Agosto": "08",
    "Setembro": "09",
    "Outubro": "10",
    "Novembro": "11",
    "Dezembro": "12"
    }
    
    corrected_dates = []
    for date in data_edicao:
        date_ = date.split("-")
        if len(date_) > 3:
            date_ = date_[-3:]
        for i in range(len(date_)):
            if date_[i] in list(meses.keys()):
                    date_[i] = meses[date_[i]]
                    clean_date =  "-".join(date_)
                    corrected_dates.append(clean_date)

    return corrected_dates

df_final["Data_Edicao"] = correct_date()
df_final['Data_Edicao'] = pd.to_datetime(df_final['Data_Edicao'], format='%d-%m-%Y')

num_edicao = [ " ".join(data.split()[:2]).replace("edição", "edition") for data in data_edicao_completo ]
df_final["Numero_Edicao"] = num_edicao

paginas = df_final["Paginas"].tolist()
paginas = [ pagina.split()[0].split("\u200e")[-1] for pagina in paginas ]
df_final["Paginas"] = paginas
df_final["Paginas"] = df_final["Paginas"].astype(int)

