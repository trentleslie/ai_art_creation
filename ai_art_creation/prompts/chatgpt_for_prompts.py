import openai
import random
import time
import os
from datetime import datetime
from ai_art_creation.api.api_key import api_key

# Folder where the CSV files are stored
folder_path = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\prompts\\prompt_generation_keywords\\"

# Get list of all files
files = os.listdir(folder_path)

# Sort list of files based on their modified time
files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

# The latest file would be the last file in the sorted list
latest_file = files[-1]

# Ensure the file is a CSV file
if latest_file.endswith(".txt"):
    # Full file path
    file_path = os.path.join(folder_path, latest_file)
else:
    print("The latest file in the directory is not a text file.")

# Open and read the file, and split the content into a list
with open(file_path, 'r') as file:
    keywords_list = file.read().splitlines()

#--------------------------------------------------------------------------------------------------------------#
#---------------------------------------------Generate Prompts-------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------#

def generate_prompts_tiled(keyword):
    
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
                        [5] = A style (e.g. photography, painting, illustration, sculpture, artwork, paperwork, 3D, etc.) for [1].
                        [6] = A description of how [5] will be executed (e.g. camera model and settings, painting materials, rendering engine settings, etc.)

                        Formatting: 
                        Follow this prompt structure: "/imagine prompt: [1], [2], [3], [4], [5], [6]".

                        Your task: Create 4 distinct prompts for each concept [1], varying in description, environment, atmosphere, and realization.

                        - Write your prompts in English.
                        - Do not describe unreal concepts as "real" or "photographic".
                        - Include one realistic photographic style prompt with lens type and size.
                        - Separate different prompts with two new lines.

                        Example Prompts:
                        Prompt 1:
                        /imagine prompt: A stunning Halo Reach landscape with a Spartan on a hilltop, lush green forests surround them, clear sky, distant city view, focusing on the Spartan's majestic pose, intricate armor, and weapons, Artwork, oil painting on canvas

                        Prompt 2:
                        /imagine prompt: A captivating Halo Reach landscape with a Spartan amidst a battlefield, fallen enemies around, smoke and fire in the background, emphasizing the Spartan's determination and bravery, detailed environment blending chaos and beauty, Illustration, digital art
                        '''
                                
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
    ]
    
    #call the ChatCompletion end
    print("Generating prompts...")
    response = openai.ChatCompletion.create(
            model = 'gpt-4',
            messages=messages,
            temperature = 0.5,
            top_p = 1, 
            presence_penalty = 0.5,
            frequency_penalty = 0.4            
        )
    
    time.sleep(3)

    # Extract the generated text from the API response
    generated_text = (response['choices'][0]['message']['content'])

    # Check if the generated_text string contains newlines
    if "\n" in generated_text:
        # If it does, split the string into a list of prompts
        prompts_list = generated_text.split("\n")

        # Remove any empty or whitespace elements from the list
        prompts_list = [prompt.strip() for prompt in prompts_list if prompt.strip()]
        
    print(len(prompts_list) , "more prompts generated!")
    
    return prompts_list

def get_tiled_prompts():
    # Create a timestamp
    timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M')

    # Specify the path for the output text file
    output_path = f"C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\prompts\\all_prompts_tiled_{timestamp}.txt"

    # Open the file in write mode
    with open(output_path, 'w') as file:

        # Iterate over the keywords list
        for i, keyword in enumerate(keywords_list, 1):
            print(f"Processing keyword {i} of {len(keywords_list)}: {keyword}")
            # Generate prompts for the current keyword
            prompts = generate_prompts_tiled(keyword)
        
            # Write prompts to the file as they are generated
            for prompt in prompts:
                if not prompt.startswith("Prompt"):
                    file.write("%s\n" % prompt)

    print("Prompt generation completed!")
