import cohere
import json
import os
import logging
from convert_to_tuple_format import *

def File_content_generator(data):
    # Check for API key
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        logging.error("COHERE_API_KEY environment variable is not set.")
        raise ValueError("Missing COHERE_API_KEY.")

    co = cohere.ClientV2(cohere_api_key)

    prompt = f"""
    The following data is extracted from credit card transactions sourced from https://www.kaggle.com/api/v1/datasets/download/thedevastator/analyzing-credit-card-spending-habits-in-india. 

    Based on the expense categories, data below:
    {convert_to_tuple_format(data)}

    Please provide:
    1. An overview highlighting the dominant categories along with their total spending and percentage contributions.
    2. Insights into budget allocation strategies and any suggestions for potential cost savings.
    3. Observations on consumer behavior trends, including potential correlations between spending categories.
    4. Recommendations for budget adjustments based on the analysis and any external factors that could influence spending habits.

    Provide the above insights as a dictionary for the answers.
    Example for above: ("Overview", "The five expense categories presented cover the essential aspects of daily life: Bills, Food, Fuel, Entertainment, and Grocery.")
    Also, information about:
    ("Category Dominance", ""), ("Budget Allocation", "x"), ("Behavior Insights", "x").
    """

    try:
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Validate response
        if not response.message.content or len(response.message.content) == 0:
            logging.error("Empty response from Cohere API.")
            return []

        # Extracting the dictionary value from the generated response
        start = response.message.content[0].text.strip().find("{")
        end = response.message.content[0].text.strip().rfind("}") + 1

        # Slicing the content based on the opening and closing '{}'
        dict_content = response.message.content[0].text.strip()[start:end]

        # Loading the content as a dictionary
        data_dict = json.loads(dict_content)

        # Converting the content to a list of tuples for report generation
        converted_data = [(key, value) for key, value in data_dict.items()]
        return converted_data

    except Exception as e:
        logging.error("An error occurred during the file content generation: %s", str(e))
        return []  # Return an empty list on error
