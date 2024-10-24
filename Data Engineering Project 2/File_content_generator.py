import cohere
import json
import os
from convert_to_tuple_format import *

def File_content_generator(data):

    co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))

    prompt = f"""
    The following data is extracted from credit card transactions sourced from https://www.kaggle.com/api/v1/datasets/download/thedevastator/analyzing-credit-card-spending-habits-in-india. 

    Based on the expense categories and data below:
    {convert_to_tuple_format(data)}

    Please provide:
    1. An overview highlighting the dominant categories along with their total spending and percentage contributions.
    2. Insights into budget allocation strategies and any suggestions for potential cost savings.
    3. Observations on consumer behavior trends, including potential correlations between spending categories.
    4. Recommendations for budget adjustments based on the analysis and any external factors that could influence spending habits.

    Provide the above insights as  dictionary for the answers for above.
    example for above: ("Overview","The five expense categories presented cover the essential aspects of daily life: Bills, Food, Fuel, Entertainment, and Grocery.")
    also information about
    ("Category Dominance", ""),("Budget Allocation", "x"),("Behavior Insights",'x'). like for category dominace its findings based on data and will it  in place of 'x'. x should mention the findings of the title . example:
    ("Category Dominance", "Housing and utilities are significant parts of most budgets.")
    """

    response = co.chat(
        model="command-r-plus",
        messages=[
            {
                "role": "user",
                "content": {prompt}
            }
        ]
    )

    
    # Extracting only dictinary value from the generated response
    start = response.message.content[0].text.strip().find("{")
    end = response.message.content[0].text.strip().rfind("}") + 1
    # slicing the content based on the opening and closing '{}'
    dict_content = response.message.content[0].text.strip()[start:end]

    # Loading the content as a dictionary
    data_dict = json.loads(dict_content)
    
    # converting the content as a list of tuples to create a .docx and .pdf report using the content in a separate function.
    converted_data = [(key, value) for key, value in data_dict.items()]
    return converted_data