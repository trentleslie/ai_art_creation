import openai
import random
from ai_art_creation.api.api_key import api_key
import pickle

def generate_prompts(how_many=2):
    
    # Set your OpenAI API key
    openai.api_key = api_key
    
    # Open the pickle file for reading
    with open('./ai_art_creation/api/old_prompts.pickle', 'rb') as f:
        # Use pickle.load() to load the pickle into a list
        old_prompts = pickle.load(f)
        
    f.close()

    old_prompts_og = old_prompts
    
    #print(old_prompts_og)
    
    # Calculate the total number of words in the old_prompts list
    total_words = sum(len(prompt.split()) for prompt in old_prompts)
    print(f'starting total words: {total_words}')

    # Check if the total number of words is greater than 3000
    while total_words > 2500:
        # If it is, randomly remove an element from the old_prompts list
        remove_index = random.randint(0, len(old_prompts)-1)
        old_prompts.pop(remove_index)
        
        # Recalculate the total number of words in the updated old_prompts list
        total_words = sum(len(prompt.split()) for prompt in old_prompts)
    
    print(f'final starting words for prompt: {total_words}')

    # Create an empty string to store the numbered list
    numbered_list = ""

    # Iterate over the styles list and add each item to the numbered list string
    for prompt in old_prompts:
        # Add a new line and the numbered item to the string
        numbered_list += f"{prompt}\n"
    
    #print(numbered_list)

    # Create an empty list to store the API responses
    api_prompts = []
    prompts_to_add = []
    
    # Iterate through the prompts list and submit each prompt to the API
    for i in range(how_many):
        word_count = str(random.randint(20, 125))
        system_prompt = random.choice([f'You are a world class AI art prompt engineer. Please write a word prompt for a piece of beautiful, compelling, and/or captivating art that is less than {word_count} words. Use the following prompts separated by newlines as guides (without copying them), and generate unique, descriptive, and creative prompts:',
                                        f'You are a world class AI art prompt engineer. Please write one, single short prompt for a piece of beautiful, compelling, and/or captivating artwork. Use the following prompts separated by newlines as guides (without copying them), and generate unique and creative prompts:'])
        
        # Define a list of styles
        style = random.choice([
            "Poetic prose",
            "Humorous description",
            "Romantic love letter",
            "Horror movie plot summary",
            "Stream-of-consciousness",
            "Surrealism",
            "Romanticism",
            "Imagism",
            "Ekphrastic writing",
            "Nature poetry",
            "Impressionism",
            "Prose poetry",
            "Nature journaling",
            "Magical realism",
            "Minimalism",
            "Futurism",
            "Folklore",
            "Mythology",
            "Science fiction",
            "Horror",
            "Realism",
            "Symbolism",
            "Absurdism"
            ]
        )
    
        #build messages payload
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": style},
            {"role": "assistant", "content": "On what topic?"},
            {"role": "user", "content": numbered_list}
        ]
        
        #call the ChatCompletion end
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                #model="gpt-4-0314",
                messages=messages,
                temperature = 1.4,
                #temperature = 0.5,
                top_p = 1, 
                presence_penalty = 0.5,
                frequency_penalty = 0.4            
            )

        # Extract the generated text from the API response
        generated_text = (response['choices'][0]['message']['content'])

        # Check if the generated_text string contains newlines
        if "\n" in generated_text:
            # If it does, split the string into a list of prompts
            prompts_list = generated_text.split("\n")

            # Remove any empty or whitespace elements from the list
            prompts_list = [prompt.strip() for prompt in prompts_list if prompt.strip()]

            # Append the non-empty prompts to the api_prompts list
            api_prompts.extend(prompts_list)
            
            # add a new prompt to the prompts_to_add list
            prompts_to_add.extend(prompts_list)
        else:
            # Add the generated text to the api_prompts list
            api_prompts.append(generated_text)
        
            # add a new prompt to the prompts_to_add list
            prompts_to_add.append(generated_text)

    # Print the list of API-generated prompts
    print(f'# of new prompts to add: {len(prompts_to_add)}')
    #print(prompts_to_add)

    # Calculate the total number of words in the old_prompts_og list
    total_words = sum(len(prompt.split()) for prompt in old_prompts_og)

    # Check if the total number of words is greater than 1,000,000
    #while total_words > 1000000:
    #    # If it is, find the prompt with the most words and remove it
    #    max_words = 0
    #    max_index = -1
    #    for i, prompt in enumerate(old_prompts_og):
    #        num_words = len(prompt.split())
    #        if num_words > max_words:
    #            max_words = num_words
    #            max_index = i
    #    old_prompts_og.pop(max_index)
    
    # Recalculate the total number of words in the updated old_prompts_og list
    #total_words = sum(len(prompt.split()) for prompt in old_prompts_og)
    #print(f'old_prompts_og total words: {total_words}')
    
    #all_prompts = old_prompts_og + prompts_to_add
    #print(f'new # of total old prompts: {len(all_prompts)}')
    #total_words = sum(len(prompt.split()) for prompt in all_prompts)
    #print(f'new # of total old words: {total_words}')
    
    # Open the pickle file to write the updated list
    #with open('./ai_art_creation/api/old_prompts.pickle', 'wb') as f:
    #    # Use pickle.dump() to store the updated list as a pickle
    #    pickle.dump(all_prompts, f)
    
    print(f'Returned # of prompts: {len(api_prompts)}')
    
    return api_prompts

#generate_prompts(how_many=2)