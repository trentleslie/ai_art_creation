import openai
from ai_art_creation.api.api_key import api_key, chatgpt_model

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
