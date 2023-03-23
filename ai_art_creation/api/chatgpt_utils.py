import openai
from ai_art_creation.api.api_key import api_key

def get_title(prompt):
    
    # Set your OpenAI API key
    openai.api_key = api_key

    #build messages payload
    messages = [
        {"role": "system", "content": "You are a world class search engine optimization expert. Avoiding anything about AR or aspect ratio, please write a short title less than 10 words of the following digital art design description:"},
        {"role": "user", "content": "Descriptive title"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
        {"role": "system", "content": "You are a world class search engine optimization expert. Avoiding anything about AR or aspect ratio, please write a short description less than 200 words of the following digital art design description:"},
        {"role": "user", "content": "Casual description"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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
        {"role": "system", "content": "You are a world class search engine optimization expert. Avoiding anything about AR or aspect ratio, please provide only 15 tags separated by commas (no numbered lists, no newlines) of the following digital art design description:"},
        {"role": "user", "content": "Casual description"},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": prompt}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature = 0.8,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text
