import openai
import random
from ai_art_creation.api.api_key import api_key, chatgpt_model
import pickle

#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Generate Prompts-------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

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
    while total_words > 1500:
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
        system_prompt = random.choice([f'''You are a world class AI art prompt engineer. Please write two unique, descriptive, original, and creative word prompts
                                       for a piece of beautiful, compelling, and/or captivating art that is less than {word_count} words. 
                                       Do not use new lines for any other use than to separate prompts. Use the following prompts, which are separated by new lines, 
                                       as guides without copying them directly:
                                       ''',
                                        '''You are a world class AI art prompt engineer. Please write two unique, descriptive, original, and creative word prompts
                                       for a piece of beautiful, compelling, and/or captivating art. Do not use new lines for any other use than to separate prompts.
                                       Use the following prompts, which are separated by new lines, as guides without directly copying them:
                                       ''',
                                        '''You will now act as a prompt generator for a generative AI called "Dall-E". Dall-E AI generates images based on given prompts. 

                                        You will never alter the structure and formatting outlined below in any way and obey the following guidelines:

                                        You will not write the words "description" or use ":" in any form. 

                                        You will write each prompt in one line without using return or a new line.

                                        Structure:
                                        [1] = a concept (e.g. a person, a place, a thing, an event, a feeling, a mood, an animal, a plant, a concept, a memory, a dream, a nightmare, a fantasy, a nightmare, a bird, a fish, a reptile, a mammal, a vehicle, a building, a structure, a machine, a tool, a piece of clothing, a piece of furniture, a piece of jewelry, a piece of technology, a piece of art, a piece of music, a piece of literature, a piece of food, a piece of drink, a piece of medicine, a piece of science, a piece of math, a piece of history, a piece of philosophy, a piece of religion, a piece of politics, a piece of economics, a piece of law, a piece of nature, a piece of the universe, a piece of the cosmos, a piece of the earth, a piece of the sky, a piece of the sea, a piece of the land, a piece of the air, a piece of the water, a piece of the fire, a piece of the ice, a piece of the wind, a piece of the rain, a piece of the snow, a piece of the sun, a piece of the moon, a piece of the stars, a piece of the galaxy, a piece of the universe, a piece of the cosmos, a piece of the earth, a piece of the sky, a piece of the sea, a piece of the land, a piece of the air, a piece of the water, a piece of the fire, a piece of the ice, a piece of the wind, a piece of the rain, a piece of the snow, a piece of the sun, a piece of the moon, a piece of the stars, a piece of the galaxy, a piece of the universe, a piece of the cosmos, a piece of the earth, a piece of the sky, a piece of the sea, a piece of the land, a piece of the air, a piece of the water, a piece of the fire, a piece of the ice, a piece of the wind, a piece of the rain, a piece of the snow, a piece of the sun, a piece of the moon, a piece of the stars, a piece of the galaxy, a piece of the universe, a piece of the cosmos, a piece of the earth, a piece of the sky, a piece of the sea, a piece of the land, a piece of the air, a piece of the water, a piece of the fire, a piece of the ice, a piece of the wind, a body of water)
                                        [2] = a detailed description of [1] that will include very specific imagery details.
                                        [3] = with a detailed description describing the environment of the scene.
                                        [4] = with a detailed description describing the mood/feelings and atmosphere of the scene.
                                        [5] = A style, for example: photography, painting, illustration, sculpture, Artwork, paperwork, 3d and more). [1] 
                                        [6] = A description of how [5] will be realized. (e.g. Photography (e.g. Macro, Fisheye Style, Portrait) with camera model and appropriate camera settings, Painting with detailed descriptions about the materials and working material used, rendering with engine settings, a digital Illustration, a woodburn art (and everything else that could be defined as an output type)
                                        [v] = If [5] looks best in a Japanese art style use, "niji".

                                        Formatting: 
                                        What you write will be exactly as formatted in the structure below, including the "/" and ":"
                                        This is the prompt structure: "/imagine prompt: [1], [2], [3], [4], [5], [6], [v]".

                                        This is your task: You will generate 2 prompts for each concept [1], and each of your prompts will be a different approach in its description, environment, atmosphere, and realization.

                                        The prompts you provide will be in English.

                                        Please pay attention:
                                        - Concepts that can't be real would not be described as "Real" or "realistic" or "photo" or a "photograph". for example, a concept that is made of paper or scenes which are fantasy related.
                                        - One of the prompts you generate for each concept must be in a realistic photographic style. you should also choose a lens type and size for it. Don't choose an artist for the realistic photography prompts.
                                        - Separate the different prompts with one new line
                                        - For inspiration of concepts, please refer to the following list without directly copying:
                                        '''])
                                    
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
                model = chatgpt_model,
                messages=messages,
                temperature = 1.2,
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

    # Remove any prompts that are less than 75 characters
    api_prompts = [prompt for prompt in api_prompts if len(prompt) >= 75]
    prompts_to_add = [prompt for prompt in prompts_to_add if len(prompt) >= 75]
    
    # Print the list of API-generated prompts
    print(f'# of new prompts to add: {len(prompts_to_add)}')
    print(prompts_to_add)

    # Calculate the total number of words in the old_prompts_og list
    total_words = sum(len(prompt.split()) for prompt in old_prompts_og)

    # Check if the total number of words is greater than 1,000,000
    while total_words > 1000000:
        # If it is, find the prompt with the most words and remove it
        max_words = 0
        max_index = -1
        for i, prompt in enumerate(old_prompts_og):
            num_words = len(prompt.split())
            if num_words > max_words:
                max_words = num_words
                max_index = i
        old_prompts_og.pop(max_index)
    
    # Print the list of API-generated prompts
    print(f'# of prompts in old_prompts_og: {len(old_prompts_og)}')
    # Recalculate the total number of words in the updated old_prompts_og list
    total_words = sum(len(prompt.split()) for prompt in old_prompts_og)
    print(f'old_prompts_og total words: {total_words}')
    
    all_prompts = old_prompts_og + prompts_to_add
    print(f'new # of total old prompts: {len(all_prompts)}')
    total_words = sum(len(prompt.split()) for prompt in all_prompts)
    print(f'new # of total old words: {total_words}')
    
    # Open the pickle file to write the updated list
    with open('./ai_art_creation/api/old_prompts.pickle', 'wb') as f:
        # Use pickle.dump() to store the updated list as a pickle
        pickle.dump(all_prompts, f)
    
    print(f'Returned # of prompts: {len(api_prompts)}')
    
    return api_prompts

#generate_prompts(how_many=2)

#--------------------------------------------------------------------------------------------------------------#
#------------------------------------------Generate Pre-prompt CSV---------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def generate_preprompt_csv():
    # Set your OpenAI API key
    openai.api_key = api_key
    
    system_prompt = '''You are a language model that outputs CSV strings with 5 unqiue rows and the headers "target audience", "theme", "style", "elements", "format", "layout". 
                        Columns are separated by commas, rows are separated by new lines, and each cell in a row is contained within quotation marks. 
                        Do not deviate from this format. Do not include comments, conversational elements, or other outputs that would disrupt the CSV format. 
                        Do not respond with empty elements in the csv.
                        Each column must contain unique responses for each row.
                        Each row must contain 6 columns.
                        Every row must contain the same number of columns.
                        Do not provide an empty string in each "target_audience" column.
                        Do not provide an empty string in each "theme" column.
                        Do not provide an empty string in each "style" column.
                        Do not provide an empty string in each "elements" column.
                        Do not provide an empty string in each "format" column.
                        Do not provide an empty string in each "layout" column.
                        Do not use punctuation, such as periods and exclamation marks, in the title column. 
                        Guidance for each column will be provided within brackets after the column name.
'''
                        
    user_input = '''Provide 5 unique rows to the CSV given the following guidance for each column. For the first three rows, use the target audiences "birders or birdwatchers", "sailors", and "boaters".:
                        Keep in mind that the success of the generated images largely depends on the quality of the prompt you provide to DALL-E. Here are some instructions with examples:
                            1) Define the target audience and theme:
                                Clearly specify the target audience and the theme of the design you want DALL-E to create. For instance, if you want a pattern for science enthusiasts, you can mention "geometric pattern inspired by science concepts."
                                Example: "Create a colorful and eye-catching geometric pattern inspired by science concepts, suitable for print on everyday items."

                            2) Describe the style and elements:
                                Mention the specific art style or elements you want DALL-E to incorporate into the pattern. This can include a particular color palette, shapes, or objects relevant to the theme.
                                Example: "Design an abstract pattern incorporating DNA helix, atoms, and chemical structures in a vibrant color palette, suitable for print on everyday items."

                            3) Specify the format and layout:
                                Inform DALL-E about the format and layout of the pattern. This can include whether you want a seamless pattern, a centered design, or a pattern that can be tiled.
                                Example: "Generate a seamless, repeating pattern featuring stylized illustrations of different dog breeds with a minimalist style, suitable for print on everyday items."

                            4) Encourage variations:
                                Ask DALL-E to provide multiple variations of the pattern to increase the chances of obtaining a design that meets your requirements.
                                Example: "Create three different abstract patterns inspired by nature, with organic shapes and earthy colors, suitable for print on everyday items."
                    Please make the first three target audiences "birders or birdwathers", "sailors", and "boaters"'''
                                
    # Define a list of styles
    style = "Comma separated values"

    #build messages payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": style},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": user_input}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 1,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    csv_string = (response['choices'][0]['message']['content'])

    return csv_string

#print(generate_preprompt_csv())


#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Generate Font CSV------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def generate_font_csv(target_audience="science enthusiasts",
                                theme="science concepts"):
    
    # Set your OpenAI API key
    openai.api_key = api_key
    
    system_prompt = '''You are a language model that outputs CSV strings with 3 unique rows and the headers "text", "font", "font_color", "title", "description", "tags". 
                        Columns are separated by commas, rows are separated by new lines, and each cell in a row is contained with quotation marks. 
                        Do not deviate from this format. Do not include comments, conversational elements, or other outputs that would disrupt the csv format.
                        Do not respond with empty elements in the csv. 
                        Each row must have 6 columns.
                        Every row must contain the same number of columns.
                        Each column must contain unique responses for each row.
                        Do not use punctuation, such as periods and exclamation marks, in the title column.
                        Guidance for each column with be provided within brackets after the column name.'''
                        
    user_input = f'''provide 3 unique rows to the csv given the following guidance for each column:
                        "text" column - [Do not provide an empty string in the "text" column. Generate unique, original, creative expressions suitable for best-selling t-shirts or mugs.
                        There are no limits on word count, but the text must reasonably fit on a t-shirt or mug. 
                        Do NOT use trademarked or copyrighted phrases.
                        Do use clever, witty, funny, thought-provoking, inspirational, motivational, or otherwise interesting phrases.
                        Do use unique, original, and creative phrases. 
                        Do not use phrases that are already in use or that are commonly used.
                        incorporate the following guidance:
                            -target audience: {target_audience}
                            -theme: {theme}]
                        "font" column - [Do not provide an empty string in the font column. Suggest a single font that is suitable for the target audience and theme.]
                        "font_color" column - [Do not provide an empty string in the font color column. Use a sing font color in hex format that is suitable for the target audience and theme.]
                        "title" column: [You are a world class search engine optimization (SEO) expert. 
                            Do not mention anything about SEO or SEO experts in the title column.
                            Do not mention anything about AR or aspect ratio.
                            Do not provide comments or anything conversational in the title column.
                            Do not include periods or exclamation marks in the title column.
                            Provide unique titles for each row.
                            Do not provide an empty string in the title column.
                            Use a title identical or very similar to th text column.
                            Do not reference any products, such as t-shirts or mugs in the title column. Only reference the "text" expression itself.
                            If you are unsure of how to generate the title based on the description, please use a title related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                            Please write a search engine optimized title of the "text" column at less than 50 characters]
                        "description" column: [You are a world class search engine optimization (SEO) expert and marketer. 
                            Do not mention anything about AR or aspect ratio.
                            Do not provide anything conversational.
                            Do not provide an introductory label such as "Optimized description:".
                            Do not use first person pronouns such as "I" or "we" or "us" or "our".
                            Do not provide an empty string in the description column.
                            Do not speak about creating or generating the "text" expression.
                            Speak only about the "text" expression itself by describing it with excitement.
                            Provide unique descriptions for each row.
                            Do not reference any products, such as t-shirts or mugs in the description column. Only reference the "text" expression itself.
                            Please write a unique, search engine optimized, witty, funny, clever, exciting description in the description column with punctuation, such as exclamation points, inspired by the "text" column generated above at less than 400 characters]
                        "tags" column: [You are a world class search engine optimization (SEO) expert.
                            Do not mention anything about AR or aspect ratio.
                            Do not provide comments or anything conversational in the tags column.
                            Do not use any punctuation other than commas.
                            Do not use any numbered lists.
                            Do not use any new lines in the tags column.
                            Do not use periods.
                            Do not start the list of tags in the tags column with a label.
                            Do not mention SEO or SEO experts in the tags column.
                            Do not provide an empty string in the tags column.
                            Do not reference any products, such as t-shirts or mugs in the tags column. Only reference the "text" expression itself.
                            Please provide only the tags separated by commas.
                            Provide unique tags for each row.
                            If you are unsure of how to generate the tags based on the target audience, theme, or "description" column generated above, please use tags related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                            Please provide 25 search engine optimized tags separated by commas]'''
                                
    # Define a list of styles
    style = "Comma separated values"

    #build messages payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": style},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": user_input}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = 1,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text

#print(generate_prompt_csv())

#--------------------------------------------------------------------------------------------------------------#
#-----------------------------------------Generate Dall-E Prompt CSV-------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def generate_prompt_csv(target_audience="science enthusiasts",
                                theme="science concepts",
                                style="geometric",
                                elements="DNA helix, atoms, and chemical structures",
                                format="seamless",
                                layout="repeating"):
    
    # Set your OpenAI API key
    openai.api_key = api_key
    
    # Create an empty list to store the API responses
    api_prompts = []
    prompts_to_add = []
    
    system_prompt = '''You are a language model that outputs CSV strings with 5 unique rows and the headers "prompt", "title", "description", "tags". 
                        Columns are separated by commas, rows are separated by new lines, and each cell in a row is contained with quotation marks. 
                        Do not deviate from this format. Do not include comments, conversational elements, or other outputs that would disrupt the csv format.
                        Do not respond with empty elements in the csv. 
                        Each row must have 4 columns.
                        Every row must contain the same number of columns.
                        Each column must contain unique responses for each row.
                        Do not use punctuation, such as periods and exclamation marks, in the title column.
                        Guidance for each column with be provided within brackets after the column name.
                        You are to act as an independent language model based on the guidance within the brackets provided for each column.'''
                        
    user_input = f'''provide 5 unique rows to the csv given the following guidance for each column:
                        "prompt" column - [Do not provide an empty string in the prompt column. Generate unique, original, creative dall-e prompts to provide best-selling patterns for t-shirts and mugs, specifying to NOT include t-shirts or mugs in the illustration. use 20-100 words for the prompt column. incorporate the following guidance:
                            -target audience: {target_audience}
                            -theme: {theme}
                            -style: {style}
                            -elements: {elements}
                            -format: {format}
                            -layout: {layout}]
                        "title" column: [You are a world class search engine optimization (SEO) expert. 
                            Do not mention anything about SEO or SEO experts in the title column.
                            Do not mention anything about AR or aspect ratio.
                            Do not provide comments or anything conversational in the title column.
                            Do not include periods or exclamation marks in the title column.
                            Provide unique titles for each row.
                            Do not provide an empty string in the title column.
                            If you are unsure of how to generate the title based on the description, please use a title related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                            Please write a search engine optimized title of the prompt used above at less than 50 characters]
                        "description" column: [You are a world class search engine optimization (SEO) expert and marketer. 
                            Do not mention anything about AR or aspect ratio.
                            Do not provide anything conversational.
                            Do not provide an introductory label such as "Optimized description:".
                            Do not use first person pronouns such as "I" or "we" or "us" or "our".
                            Do not provide an empty string in the description column.
                            Do not speak about creating or generating the design.
                            Speak only about the design itself by describing it with excitement.
                            Provide unique descriptions for each row.
                            Please write a unique, search engine optimized, witty, funny, clever, exciting description in the description column with punctuation, such as exclamation points, inspired by the prompt column generated above at less than 400 characters]
                        "tags" column: [You are a world class search engine optimization (SEO) expert.
                            Do not mention anything about AR or aspect ratio.
                            Do not provide comments or anything conversational in the tags column.
                            Do not use any punctuation other than commas.
                            Do not use any numbered lists.
                            Do not use any new lines in the tags column.
                            Do not use periods.
                            Do not start the list of tags in the tags column with a label.
                            Do not mention SEO or SEO experts in the tags column.
                            Do not provide an empty string in the tags column.
                            Please provide only the tags separated by commas.
                            Provide unique tags for each row.
                            If you are unsure of how to generate the tags based on the description generated above, please use tags related to AI, artificial intelligence, deep learning, digital art, digital art design, or any adjectives or nouns that are included in or related to the description.
                            Please provide 25 search engine optimized tags separated by commas]'''
                                
    # Define a list of styles
    style = "Comma separated values"

    #build messages payload
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": style},
        {"role": "assistant", "content": "On what topic?"},
        {"role": "user", "content": user_input}
    ]
    
    #call the ChatCompletion end
    response = openai.ChatCompletion.create(
            model = chatgpt_model,
            messages=messages,
            temperature = .7,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    return generated_text

#print(generate_prompt_csv())




