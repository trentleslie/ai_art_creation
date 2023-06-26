import openai
import random
import time
import os
import random
import sqlite3
import pickle
import pandas as pd
from datetime import datetime
from ai_art_creation.api.api_key import api_key
from ai_art_creation.prompts.prompt_path_info import portrait_pickle_file_path, sqlite_db_path, starting_keywords_path, portrait_products_path, base_prompt_output_path, keywords_folder_path

# Function for getting the list of relevant keywords and products
def get_keywords_list(starting_folder_path, 
                      starting_keywords_path, 
                      portrait_products_path,
                      file_type=".csv"):
    
    # if generating prompts from archived keywords, use this path
    #starting_keywords_path = r'C:\Users\trent\OneDrive\Documents\GitHub\ai_art_creation\ai_art_creation\keywords\starting_keywords_archive.txt'
    
    # Load starting keywords
    with open(starting_keywords_path, 'r') as f:
        # Read lines into a list
        starting_keywords = f.read().splitlines()

    # Load products
    with open(portrait_products_path, 'r') as f:
        # Read lines into a list
        all_products = f.read().splitlines()
    
    # Get list of all files
    files = os.listdir(starting_folder_path)

    # Sort list of files based on their modified time
    files.sort(key=lambda x: os.path.getmtime(os.path.join(starting_folder_path, x)))

    # The latest file would be the last file in the sorted list
    latest_file = files[-1]

    # Ensure the file is a CSV file
    if latest_file.endswith(file_type):
        # Full file path
        file_path = os.path.join(starting_folder_path, latest_file)
    else:
        print(f"The latest file in the directory is not a {file_type} file.")
        
    df = pd.read_csv(file_path)
    
    # Create keywords_to_run list
    keywords_to_run = [keyword for keyword in starting_keywords if any(keyword.lower() in element.lower() for element in df['starting_keyword'].values)]

    # Create products_to_record list
    products_to_record = [product for product in all_products if any(product.lower() in element.lower() for element in df['starting_keyword'].values)]
    
    return (keywords_to_run, products_to_record)

# Function for getting random gpt params
def get_random_gpt_params():
    models = ['gpt-3.5-turbo', 'gpt-4']
    rand_model = random.choice(models)
    rand_temperature = round(random.uniform(0.3, 0.9), 2)
    rand_top_p = round(random.uniform(0.3, 0.9), 2)
    rand_presence_penalty = round(random.uniform(0.3, 0.9), 2)
    rand_frequency_penalty = round(random.uniform(0.3, 0.9), 2)

    params = {
        "model": rand_model,
        "temperature": rand_temperature,
        "top_p": rand_top_p,
        "presence_penalty": rand_presence_penalty,
        "frequency_penalty": rand_frequency_penalty,
    }

    return params

#--------------------------------------------------------------------------------------------------------------#
#--------------------------------------------GPT Prompt Function-----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def generate_portrait_prompts(keyword, 
                           model="gpt-4", 
                           temperature=0.5, 
                           top_p=0.5, 
                           presence_penalty=0.5, 
                           frequency_penalty=0.5):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    system_prompt = f'''As a prompt generator for a generative AI called "Midjourney", you will create image prompts for the AI to visualize. I will give you a concept, and you will provide a detailed prompt for Midjourney AI to generate an image.

                        Please adhere to the structure and formatting below, and follow these guidelines:

                        - Do not use the words "description" or ":" in any form.
                        - Write each prompt in one line without using return.

                        Structure:
                        [1] = {keyword}
                        [2] = a detailed description of [1] with specific imagery details.
                        [3] = a detailed description of the scene's environment.
                        [4] = a detailed description of the scene's mood, feelings, and atmosphere.
                        [5] = A style (e.g. watercolor, geometric, abstract, painting, illustration, artwork, 3D, etc.) for [1].
                        [6] = A description of how [5] will be executed (e.g. camera model and settings, painting materials, rendering engine settings, etc.)

                        Formatting: 
                        Follow this prompt structure: "/imagine prompt: [1], [2], [3], [4], [5], [6]".

                        Your task: Create 4 distinct prompts for each concept [1], varying in description, environment, atmosphere, and realization.

                        - Write your prompts in English.
                        - Do not describe unreal concepts as "real" or "photographic".
                        - Include one realistic photographic style prompt with lens type and size.
                        - Separate different prompts with two new lines.
                        - The generated images are intended to be used for merchandise, such as posters, t-shirts, and mugs, so try to specify trendy, cute, and/or cool concepts.

                        Example Prompts:
                        Prompt 1:
                        /imagine prompt: A stunning Halo Reach landscape with a Spartan on a hilltop, lush green forests surround them, clear sky, distant city view, focusing on the Spartan's majestic pose, intricate armor, and weapons, Artwork, oil painting on canvas

                        Prompt 2:
                        /imagine prompt: A captivating Halo Reach landscape with a Spartan amidst a battlefield, fallen enemies around, smoke and fire in the background, emphasizing the Spartan's determination and bravery, detailed environment blending chaos and beauty, Illustration, digital art
                        '''
                                
    # Define a list of styles
    style = f'''Incorporate a few of the following key phrases in your prompt:
                "Watercolor",
                "Geometric",
                "Cute",
                "Trendy",
                "Cool",
                "Stylish",
                "Vibrant",
                "Abstract",
                "Minimalist",
                "Pencil Drawing",
                "Ink Drawing",
                "Vectorized cartoon style on a white #000000 background"
            '''

    #build messages payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": style},
    ]
    
    max_retries = 10
    retry_count = 0
    retry_flag = True
            
    while retry_flag and retry_count < max_retries:
        newline_count = 0 #count the number of newlines in the generated text
        try:
            #call the ChatCompletion end
            counter = 0
            while newline_count < 6 and counter <= 5:
                print("Generating prompts...")
                response = openai.ChatCompletion.create(
                        model = model,
                        messages=messages,
                        temperature = temperature,
                        top_p = top_p, 
                        presence_penalty = presence_penalty,
                        frequency_penalty = frequency_penalty            
                    )
                
                time.sleep(3)
                
                newline_count = response['choices'][0]['message']['content'].count('\n')
                print("Newline count:", newline_count)
                
                counter += 1
                
            retry_flag = False
            
        except Exception as e:
            print(f"Exception occurred in OpenAI API call: '{e}' Retrying...")
            retry_count += 1
            
        if retry_count == max_retries - 1:
            print("Max retries reached. Skipping this prompt...")
            return []

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    # If it does, split the string into a list of prompts
    prompts_list = generated_text.split("\n")

    # Remove any empty or whitespace elements from the list, and any that start with "Prompt"
    prompts_list = [prompt.strip() for prompt in prompts_list if prompt.strip() and not prompt.startswith("Prompt")]
    
    prompts_list = [s + " On a white #000000 background" if "Vectorized cartoon style" in s else s for s in prompts_list]
        
    print(len(prompts_list) , "more prompts generated!")
    
    return prompts_list

#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------Generate portrait Prompts----------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def get_prompts(keywords_list, 
                      products_list, 
                      sqlite_db_path, 
                      pickle_file_path, 
                      generate_func):
    try:
        with open(pickle_file_path, 'rb') as pickle_file:
            completed_keywords = pickle.load(pickle_file)
    except FileNotFoundError:
        completed_keywords = []  # initialize as an empty list if the file doesn't exist

    # Create a timestamp
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M')

    # Specify the path for the output text file
    output_path = f"{base_prompt_output_path}portrait\\all_prompts_portrait_{timestamp}.txt"

    with sqlite3.connect(sqlite_db_path) as conn:
        c = conn.cursor()
        # Open the file in write mode
        with open(output_path, 'w') as file:

            # Iterate over the keywords list
            for i, keyword in enumerate(keywords_list, 1):                
                try:
                    # Attempt to split the string and get the second element
                    keyword_for_gpt = keyword.split(":")[1]
                except IndexError:
                    # If there is no ":" in the string, just use the whole string as the keyword
                    keyword_for_gpt = keyword
                    
                # If the keyword has already been processed, skip it
                if keyword_for_gpt not in completed_keywords:
                    print(f"Processing keyword {i} of {len(keywords_list)}: {keyword_for_gpt}")
                    
                    params = get_random_gpt_params()
                    
                    # Generate prompts for the current keyword
                    prompts = generate_func(keyword=keyword_for_gpt, 
                                                    model=params['model'],
                                                    temperature=params['temperature'], 
                                                    top_p=params['top_p'], 
                                                    presence_penalty=params['presence_penalty'],
                                                    frequency_penalty=params['frequency_penalty'])
                
                    if len(prompts) > 0:
                        # Write prompts to the file as they are generated
                        for prompt in prompts:
                            file.write("%s\n" % str(prompt))
                            
                            for product in products_list:
                                # insert a record
                                c.execute('''
                                    INSERT INTO prompts_and_images (
                                        starting_keyword, 
                                        gpt_model, 
                                        gpt_keyword, 
                                        temperature, 
                                        top_p, 
                                        presence_penalty, 
                                        frequency_penalty, 
                                        prompt,
                                        product,
                                        keyword_product
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    ''', (keyword.split(":")[0], 
                                        params['model'], 
                                        keyword_for_gpt, 
                                        params['temperature'], 
                                        params['top_p'], 
                                        params['presence_penalty'], 
                                        params['frequency_penalty'], 
                                        prompt,
                                        product,
                                        f'{keyword_for_gpt} {product}'))
                                
                                conn.commit()
                                
                        # keyword is completed, add it to the list
                        completed_keywords.append(keyword_for_gpt)

                        # update the pickle file
                        with open(pickle_file_path, 'wb') as pickle_file:
                            pickle.dump(completed_keywords, pickle_file)
                    else:
                        print(f"No prompts generated for this keyword: {keyword_for_gpt}. Moving on to the next one...")
                else:
                    print(f"Keyword {keyword_for_gpt} has already been processed. Moving on to the next one...")

    print("Prompt generation completed!")
    
    return completed_keywords

print("Getting keywords and products...")

# Get the list of keywords to run and the list of products to record
keywords_to_run, products_to_record = get_keywords_list(keywords_folder_path,
                                        starting_keywords_path,
                                        portrait_products_path,
                                        file_type=".csv")

print("Keywords and products retrieved! Starting Run 1...")

num_runs = 10 # you can change this to the number of runs you need

for i in range(num_runs):
    print(f"Starting Run {i+1}...")
    
    completed_keywords_check = [] 

    while len(completed_keywords_check) < len(keywords_to_run):
        # Get the prompts
        completed_keywords_check = get_prompts(keywords_to_run, 
                                                     products_list=products_to_record, 
                                                     sqlite_db_path=sqlite_db_path,
                                                     pickle_file_path=portrait_pickle_file_path,
                                                     generate_func=generate_portrait_prompts)

        # Delete the pickle file if all went well
        if len(completed_keywords_check) == len(keywords_to_run):
            print("All keywords have been processed! Deleting the pickle file...")
            os.remove(portrait_pickle_file_path)

    print(f"Run {i+1} completed!")

print("All runs completed!")