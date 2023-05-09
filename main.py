from ai_art_creation.api.chatgpt import generate_preprompt_csv
from ai_art_creation.api.chatgpt_utils import generate_valid_csv_as_df, generate_ongoing_prompt_df, generate_ongoing_tshirt_df
from ai_art_creation.api.dall_e import generate_images_from_df
from ai_art_creation.image_processing.font_processing import process_fonts_images
import datetime

# Constants
FONTS_DIRECTORY = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\image_processing\\Fonts"
OUTPUT_PATH = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\image_processing\\images_raw"

def main():

    # Generate concepts for DALL-E prompts
    valid_preprompt_csv_df = generate_valid_csv_as_df(generate_preprompt_csv)
    print(valid_preprompt_csv_df)
    
    # Generate prompts for DALL-E
    #ongoing_prompt_df = generate_ongoing_prompt_df(valid_preprompt_csv_df)
    
    # Save prompts for DALL-E as a CSV file
    #timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #ongoing_prompt_df.to_csv(f'prompts_for_dalle-{timestamp}.csv', index=False)
    
    # Generate text for t-shirts
    ongoing_tshirt_df = generate_ongoing_tshirt_df(valid_preprompt_csv_df)

    # Save text for t-shirts as a CSV file
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ongoing_tshirt_df.to_csv(f'text_for_tshirts-{timestamp}.csv', index=False)

    # Generate images from text for t-shirts and get fonts to install
    fonts_to_install = process_fonts_images(ongoing_tshirt_df, FONTS_DIRECTORY, OUTPUT_PATH)
    
    # Print fonts to install
    print("Fonts to install:")
    for font in fonts_to_install:
        print(font)
    
    # Generate images from prompts for DALL-E and print filenames
    #print(generate_images_from_df(ongoing_prompt_df))
    
if __name__ == "__main__":
    main()



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