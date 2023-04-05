import openai
from ai_art_creation.api.api_key import api_key, chatgpt_model
import csv
from io import StringIO
import time
import pandas as pd

def is_csv_format(s):
    s = s.strip()
    lines = s.split('\n')

    if len(lines) < 2:
        print("CSV must have at least 2 lines")
        return False

    num_columns = None

    csv_reader = csv.reader(StringIO(s), delimiter=',', quotechar='"')
    for row in csv_reader:
        if num_columns is None:
            num_columns = len(row)
        elif num_columns != len(row):
            print("CSV must have the same number of columns on each line")
            return False

        # Check for empty elements in the row
        for element in row:
            if element.strip() == "":
                print("CSV must not have empty elements")
                return False

    return True

def generate_valid_csv(generator_function):
    attempts = 0
    start_time = time.time()

    while True:
        attempts += 1
        csv_string = generator_function()
        print("Attempt", attempts, "completed.")
        print(csv_string)
        if is_csv_format(csv_string):
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Successful CSV generated after {attempts} attempts and {elapsed_time:.2f} seconds")
            
            # Convert the CSV string to a CSV object
            csv_reader = csv.reader(StringIO(csv_string), delimiter=',', quotechar='"')
            csv_object = [row for row in csv_reader]
            return csv_object

def generate_valid_csv_as_df(generator_function):
    attempts = 0
    start_time = time.time()

    while True:
        attempts += 1
        csv_string = generator_function()
        print("Attempt", attempts, "completed.")
        print(csv_string)
        if is_csv_format(csv_string):
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Successful CSV generated after {attempts} attempts and {elapsed_time:.2f} seconds")
            
            # Convert the CSV string to a DataFrame
            csv_df = pd.read_csv(StringIO(csv_string), delimiter=',', quotechar='"')
            return csv_df

def save_valid_csv_to_file(valid_csv, filename="valid_csv.csv"):
    with open(filename, "w") as f:
        f.write(valid_csv)
        
def save_df_to_file(valid_csv_df, filename="valid_csv.csv"):
    valid_csv_df.to_csv(filename, index=False)

def join_and_append(original_row, generated_df, ongoing_df):
    # Repeat the original row values for the same number of rows as in the generated_df
    original_row_repeated = pd.DataFrame([original_row] * len(generated_df), columns=original_row.index)

    # Reset the index for both DataFrames
    original_row_repeated.reset_index(drop=True, inplace=True)
    generated_df.reset_index(drop=True, inplace=True)

    # Join the columns of the original row with the generated DataFrame
    joined_df = pd.concat([original_row_repeated, generated_df], axis=1)

    # Append the joined DataFrame to the ongoing DataFrame
    ongoing_df = ongoing_df.append(joined_df, ignore_index=True)

    return ongoing_df

def get_title(prompt):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    #build messages payload
    messages = [
        {"role": "system", "content": '''You are a world class search engine optimization (SEO) expert. 
                                            Do not mention anything about AR or aspect ratio.
                                            Do not provide anything conversational.
                                            Do not end the title with a period.
                                            If you are unsure of how to generate the title based on the description, please use a title related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                                            Please write a search engine optimized title less than 50 characters of the following digital art design description:
                                            '''},
        {"role": "user", "content": "Descriptive title"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 0.8,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text

def get_description(prompt):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    #build messages payload
    messages = [
        {"role": "system", "content": '''You are a world class search engine optimization (SEO) expert. 
                                            Do not mention anything about AR or aspect ratio.
                                            Do not provide anything conversational.
                                            Do not provide an introductory label such as "Optmized description:".
                                            Do not use first person pronouns such as "I" or "we" or "us" or "our".
                                            If you are unsure of how to generate the description based on the description, please use tags related to AI art, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                                            Please write a search engine optimized description less than 400 characters of the following digital art design description:'''},
        {"role": "user", "content": "Casual description"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 0.8,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text

def get_tags(prompt):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    #build messages payload
    messages = [
        {"role": "system", "content": '''You are a world class search engine optimization (SEO) expert.
                                            Do not mention anything about AR or aspect ratio.
                                            Do not provide anything conversational.
                                            Do not use any punctuation other than commas.
                                            Do not use any numbered lists.
                                            Do not use any new lines.
                                            Do not use periods.
                                            Do not start the list of tags with a label.
                                            Do not mention SEO.
                                            Please provide only the tages separated by commas.
                                            If you are unsure of how to generate the tags based on the description, please use tags related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                                            Please provide 25 search engine optimized tags separated by commas for the following digital art design description:'''},
        {"role": "user", "content": "Casual description"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 0.8,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text
