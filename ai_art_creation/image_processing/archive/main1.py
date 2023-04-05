# main.py

from ai_art_creation.api import chatgpt, dall_e
#from ai_art_creation.image_processing import csv_merge3 as csv_merge
#from ai_art_creation.image_processing import lighting, topaz_gigapixel
#from ai_art_creation.store_integration import etsy, redbubble

def main():
    for i in range(3):
        # Generate prompts for DALL-E
        prompts = chatgpt.generate_prompts(how_many=1)
        
        # Retrieve images from DALL-E API
        images = dall_e.generate_images(prompts)
        
        print(f'GENERATED {len(images)} IMAGES IN ITERATION {i}.')
    
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
