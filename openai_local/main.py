from text_example import TEXT
from openai import OpenAI
from refrence_dictionaries.target_fields import expropriation_data
from utils import get_field_from_text ,setup_openai
import pandas as pd



# Initialize OpenAI client with API key
client = OpenAI(api_key=setup_openai())

# Create an empty list to store the results
results = []

# Loop over the dictionary values and get the response for each field
for field in expropriation_data.keys():
    response = get_field_from_text(client, TEXT, field)
    results.append({'Champs': field, 'Valeur': response})

# Convert the results into a DataFrame
df = pd.DataFrame(results)

# Print the DataFrame
print(df)

# Export the DataFrame to an Excel file
df.to_excel('expropriation_data_results.xlsx', index=False)

print("Data has been exported to 'expropriation_data_results.xlsx'.")



