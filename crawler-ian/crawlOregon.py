from crawler import crawler
import pandas as pd

data = pd.read_csv("CSV_1152022-131.csv")
data.fillna(0, inplace=True)
data = data.T.drop_duplicates().T
#print(data)
#print(data["unitid"])

or_data = data[["unitid","HD2021.State abbreviation", "HD2021.Institution's internet website address"]]
or_data = or_data.loc[or_data["HD2021.State abbreviation"] == "Oregon"]

site_list = or_data["HD2021.Institution's internet website address"].tolist()
print("num sites to crawl: "str(len(site_list)))


site_list.pop(0)
site_list.pop(0)
site_list.pop(0)
site_list.pop(0)

while len(site_list) > 0:
    seed = site_list.pop(0)
    print("crawling site: "+str(seed))
    seed_name = seed.replace('/','').replace(':','')
    c = crawler(seed, que_file=(seed_name+"Que.txt"), ajacency_file=(seed_name+"Ajacency.json"))
    c.crawl(10000, verbose=True)
    print("crawled site: "+str(seed))
    print()
    