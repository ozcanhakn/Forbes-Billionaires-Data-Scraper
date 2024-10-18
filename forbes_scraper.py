import requests
import pandas as pd
from collections import defaultdict

url = "https://www.forbes.com/forbesapi/person/billionaires/2024/position/true.json?filter=uri,finalWorth,age,country,source,qas,rank,category,person,personName,industries,organization,gender,firstName,lastName,squareImage,bios"
response = requests.get(url)

data = response.json()

industry_data = defaultdict(lambda: {'count': 0, 'total_worth': 0.0})

for person in data.get('personList', {}).get('personsLists', []):
    worth = person.get('finalWorth', 0.0)
    industries = person.get('industries', [])
    
    if isinstance(worth, (int, float)):
        worth_in_billion = worth / 1000.0
        for industry in industries:
            industry_data[industry]['count'] += 1
            industry_data[industry]['total_worth'] += worth_in_billion

def format_worth(value):
    billions = value
    trillions = billions // 1000
    remaining_billions = billions % 1000
    if trillions > 0:
        return f"{trillions} Trillion {remaining_billions:.0f} Billion" if remaining_billions > 0 else f"{trillions} Trillion"
    return f"{billions:.0f} Billion"

total_worth_all_industries = sum(info['total_worth'] for info in industry_data.values())

results = []

for industry, info in industry_data.items():
    count = info['count']
    total_worth = info['total_worth']
    formatted_worth = format_worth(total_worth)
    results.append({"Industry": industry, "Count": count, "Total Worth": formatted_worth})

formatted_total_worth = format_worth(total_worth_all_industries)
results.append({"Industry": "Total Wealth", "Count": "", "Total Worth": formatted_total_worth})

# Convert results to DataFrame
df = pd.DataFrame(results)

# Write to an Excel file
df.to_excel('billionaires_by_industry.xlsx', index=False)