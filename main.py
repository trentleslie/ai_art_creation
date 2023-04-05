from ai_art_creation.api.chatgpt import generate_preprompt_csv, generate_prompt_csv, generate_font_csv
from ai_art_creation.api.chatgpt_utils import generate_valid_csv_as_df, join_and_append
from ai_art_creation.api.dall_e import generate_images_from_df
from ai_art_creation.image_processing.font_processing import generate_fonts_dictionary, generate_text_image
import pandas as pd
import datetime
import os

#to load ai_art_creation.api module via the powershell console, run the following command:
#$env:PYTHONPATH = "$env:PYTHONPATH;C:\Users\trent\OneDrive\Documents\GitHub\ai_art_creation"
#
#to load ai_art_creation.api module into the interactive (python) console, run the following commands:
#import sys
#sys.path.append('C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation')

def main():
    
    valid_preprompt_csv_df = generate_valid_csv_as_df(generate_preprompt_csv)

    print(valid_preprompt_csv_df)
    
    #for i in range(1):
        
    # Initialize an ongoing DataFrame with the column names from both valid_csv_df and the new DataFrames generated from generate_prompt_csv_with_args()
    ongoing_prompt_df = pd.DataFrame(columns=valid_preprompt_csv_df.columns.tolist() + ["prompt", "title", "description", "tags"])

    # Iterate through the rows of valid_csv_df
    for _, row in valid_preprompt_csv_df.iterrows():
        # Create a wrapper function that takes no arguments and returns the output of generate_prompt_csv with the required arguments
        def wrapper_function():
            return generate_prompt_csv(
                target_audience=row["target audience"],
                theme=row["theme"],
                style=row["style"],
                elements=row["elements"],
                format=row["format"],
                layout=row["layout"],
            )

        # Call generate_valid_csv_as_df() with the wrapper_function as an argument
        generated_df = generate_valid_csv_as_df(wrapper_function)
        
        # Initialize an empty set to store unique tags
        unique_tags = set()

        # Iterate through the "tags" column and add tags to the unique_tags set
        for tags in generated_df['tags']:
            unique_tags.update(tag.strip() for tag in tags.split(','))

        # Join the unique_tags set with commas and update the "tags" column
        unique_tags_str = ', '.join(unique_tags)
        generated_df['tags'] = unique_tags_str

        # Join the original row with the generated DataFrame and append it to the ongoing DataFrame
        ongoing_prompt_df = join_and_append(row, generated_df, ongoing_prompt_df)
        
    # Get the current date and time as a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    ongoing_prompt_df.to_csv(f'prompts_for_dalle-{timestamp}.csv', index=False)

    print(generate_images_from_df(ongoing_prompt_df))
    
    # Initialize an ongoing DataFrame with the column names from both valid_csv_df and the new DataFrames generated from generate_prompt_csv_with_args()
    ongoing_tshirt_df = pd.DataFrame(columns=valid_preprompt_csv_df.columns.tolist() + ["text", "title", "description", "tags"])

    # Iterate through the rows of valid_csv_df
    for _, row in valid_preprompt_csv_df.iterrows():
        # Create a wrapper function that takes no arguments and returns the output of generate_prompt_csv with the required arguments
        def wrapper_function():
            return generate_font_csv(
                target_audience=row["target audience"],
                theme=row["theme"]
            )

        # Call generate_valid_csv_as_df() with the wrapper_function as an argument
        generated_df = generate_valid_csv_as_df(wrapper_function)
        
        # Initialize an empty set to store unique tags
        unique_tags = set()

        # Iterate through the "tags" column and add tags to the unique_tags set
        for tags in generated_df['tags']:
            unique_tags.update(tag.strip() for tag in tags.split(','))

        # Join the unique_tags set with commas and update the "tags" column
        unique_tags_str = ', '.join(unique_tags)
        generated_df['tags'] = unique_tags_str

        # Join the original row with the generated DataFrame and append it to the ongoing DataFrame
        ongoing_tshirt_df = join_and_append(row, generated_df, ongoing_tshirt_df)

    # Get the current date and time as a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    ongoing_tshirt_df.to_csv(f'text_for_tshirts-{timestamp}.csv', index=False)
    
    fonts_directory = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\image_processing\\Fonts"
    fonts_available = generate_fonts_dictionary(fonts_directory)
    fonts_to_install = []
    
    for _, row in ongoing_tshirt_df.iterrows():        
        output_path = "C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/images_raw/"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}-font.png"

        if row["font"] in fonts_available.keys():
            image = generate_text_image(
                width=1024,
                height=1024,
                text=row["text"],
                font_name=fonts_available[row["font"]],
                font_color=row["font color"],
                border_color=(0, 0, 0, 255)
            )
            
            image.save(os.path.join(output_path, filename))
        else:
            fonts_to_install.append(row["font"])
            
    print("Fonts to install:")
    for font in fonts_to_install:
        print(font)
    
    # UNTIL I FIGURE OUT HOW TO AUTOMATE THE SELECTION OF "SPECIAL" IMAGES, THIS IS AS FAR AS I CAN GO.
    # UNTIL THEN, MANUALLY DELETE THE IMAGES YOU DON'T WANT TO KEEP, COPY "SPECIAL" IMAGES TO THE "SPECIAL" FOLDER,
    # AND RUN CSV_MERGE2.PY. THEN SCALE UP USING TOPAZ GIGAPIXEL AND UPLOAD TO REDBUBBLE.
        
    # Merge CSV files
    #csv_merge.merge_csv()
    
    # Process images: adjust lighting, and scale up using Topaz Gigapixel
    #processed_images = []
    #for image in images:
    #    tuned_image = lighting.adjust_lighting(image)
    #    scaled_image = topaz_gigapixel.scale_image(tuned_image)
    #    processed_images.append(scaled_image)
    
    # Upload images to Etsy and RedBubble
    #etsy.upload_images(processed_images)
    #redbubble.upload_images(processed_images)

if __name__ == "__main__":
    main()
