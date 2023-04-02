import pandas as pd
import os
import datetime
import shutil

def csv_merge():
    csv_folder = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv/'
    png_folder = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/images_raw/'
    png_special_folder = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/images_raw/special/'
    merged_df = pd.DataFrame()
    png_to_delete = []
    png_files = []
    png_files_special = []
    
    # Task 1: Import all CSV files (assume they have headers) from csv_folder
    for file in os.listdir(csv_folder):
        if file.endswith('.csv'):
            file_path = os.path.join(csv_folder, file)
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
            merged_df = merged_df.append(df, ignore_index=True)
            os.remove(file_path)
    
    # Task 2: Merge the data using encoding='ISO-8859-1' into a dataframe called 'merged_df' 
    # and save a list of png files not in merged_df to a list called 'png_to_delete'
    for file in os.listdir(png_folder):
        if file.endswith('.png') and file not in merged_df['Image Path'].values:
            png_to_delete.append(file)
    for file in os.listdir(png_special_folder):
        if file.endswith('.png') and file not in merged_df['Image Path'].values:
            png_to_delete.append(file)
    
    # Task 3: Retrieve all PNG file names from png_folder, remove the extension, and store in a list called 'png_files'
    for file in os.listdir(png_folder):
        if file.endswith('.png'):
            png_files.append(os.path.splitext(file)[0])
    
    # Task 4: Retrieve all PNG file names from png_special_folder, remove the extension, and store in a list called 'png_files_special'
    for file in os.listdir(png_special_folder):
        if file.endswith('.png'):
            png_files_special.append(os.path.splitext(file)[0])
    
    # Task 5: Filter the merged CSV data for matching IDs, where IDs are the PNG file names (with the extension removed) in 'png_files'
    merged_df = merged_df[merged_df['Image Path'].apply(lambda x: os.path.splitext(os.path.basename(x))[0] in png_files)]
    
    # Task 6: In 'merged_df', replace ".png" with "-scaled.png" in the "Image Path" column, set regex = True
    merged_df['Image Path'] = merged_df['Image Path'].str.replace(".png", "-scaled.png", regex=True)
    
    # Task 7: Duplicate 'merged_df' to a separate dataframe called 'merged_df_rounded' and add " (rounded)" to the end of the string in each row of the "Title" column
    merged_df_rounded = merged_df.copy()
    merged_df_rounded['Title'] = merged_df_rounded['Title'] + ' (rounded)'
    
    # Task 8: In 'merged_df_rounded', replace "-scaled.png" with "-scaled-rounded.png" in the "Image Path" column, set regex = True 
    merged_df_rounded['Image Path'] = merged_df_rounded['Image Path'].str.replace("-scaled.png", "-rounded-scaled.png", regex=True)
    
    # Task 9: Duplicate 'merged_df' to a separate dataframe called 'merged_df_special' 
    # and filter 'merged_df_special' by the ID column with values that are in 'png_files_special'
    merged_df_special = merged_df.copy()
    merged_df_special = merged_df_special[merged_df_special['ID'].isin(png_files_special)]
    
    # Task 10: In 'merged_df_special', replace "-scaled.png" with "-scaled-rounded.png" in the "Image Path" column, set regex = True 
    merged_df_special['Image Path'] = merged_df_special['Image Path'].str.replace("-scaled.png", "-rounded-scaled.png", regex=True)
    
    # Task 11: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_circle' 
    # and add " (circle)" to the end of the string in each row of the "Title" column
    merged_df_circle = merged_df_special.copy()
    merged_df_circle['Title'] = merged_df_circle['Title'] + ' (circle)'
    
    # Task 12: In 'merged_df_circle', replace "-scaled.png" with "-scaled-circle.png" in the "Image Path" column, set regex = True 
    merged_df_circle['Image Path'] = merged_df_circle['Image Path'].str.replace("-scaled.png", "-circle-scaled.png", regex=True)
    
    # Task 13: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_diamond' 
    # and add " (diamond)" to the end of the string in each row of the "Title" column
    merged_df_diamond = merged_df_special.copy()
    merged_df_diamond['Title'] = merged_df_diamond['Title'] + ' (diamond)'
    
    # Task 14: In 'merged_df_diamond', replace "-scaled.png" with "-scaled-diamond.png" in the "Image Path" column, set regex = True 
    merged_df_diamond['Image Path'] = merged_df_diamond['Image Path'].str.replace("-scaled.png", "-diamond-scaled.png", regex=True)
    
    # Task 15: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_triangle' 
    # and add " (triangle)" to the end of the string in each row of the "Title" column
    merged_df_triangle = merged_df_special.copy()
    merged_df_triangle['Title'] = merged_df_triangle['Title'] + ' (triangle)'
    
    # Task 16: In 'merged_df_triangle', replace "-scaled.png" with "-scaled-triangle.png" in the "Image Path" column, set regex = True 
    merged_df_triangle['Image Path'] = merged_df_triangle['Image Path'].str.replace("-scaled.png", "-triangle-scaled.png", regex=True)
    
    # Task 17: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_randpoly' 
    # and add " (randpoly)" to the end of the string in each row of the "Title" column
    merged_df_randpoly = merged_df_special.copy()
    merged_df_randpoly['Title'] = merged_df_randpoly['Title'] + ' (randpoly)'
    
    # Task 18: In 'merged_df_randpoly', replace "-scaled.png" with "-scaled-randpoly.png" in the "Image Path" column, set regex = True 
    merged_df_randpoly['Image Path'] = merged_df_randpoly['Image Path'].str.replace("-scaled.png", "-randpoly-scaled.png", regex=True)
    
    # Task 19: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_randpolycircle' 
    # and add " (randpolycircle)" to the end of the string in each row of the "Title" column
    merged_df_randpolycircle = merged_df_special.copy()
    merged_df_randpolycircle['Title'] = merged_df_randpolycircle['Title'] + ' (randpolycircle)'
    
    # Task 20: In 'merged_df_randpolycircle', replace "-scaled.png" with "-scaled-randpolycircle.png" in the "Image Path" column, set regex = True 
    merged_df_randpolycircle['Image Path'] = merged_df_randpolycircle['Image Path'].str.replace("-scaled.png", "-randpolycircle-scaled.png", regex=True)
    
    # Task 21: Duplicate 'merged_df_special' to a separate dataframe called 'merged_df_star' 
    # and add " (star)" to the end of the string in each row of the "Title" column
    merged_df_star = merged_df_special.copy()
    merged_df_star['Title'] = merged_df_star['Title'] + ' (star)'
    
    # Task 22: In 'merged_df_star', replace "-scaled.png" with "-scaled-star.png" in the "Image Path" column, set regex = True 
    merged_df_star['Image Path'] = merged_df_star['Image Path'].str.replace("-scaled.png", "-star-scaled.png", regex=True)
    
    # Task 23: Append 'merged_df_rounded', 'merged_df_circle', 'merged_df_diamond', 'merged_df_triangle', 'merged_df_randpoly', and 'merged_df_randpolycircle' to 'merged_df' 
    merged_df = merged_df.append([merged_df_rounded, merged_df_circle, merged_df_diamond, merged_df_triangle, merged_df_randpoly, merged_df_randpolycircle, merged_df_star], ignore_index=True)
    
    # Task 24: Write columns "Title", "Description", "Tags", "Price", "Image Path" from 'merged_df' 
    # to a CSV file to csv_merged/[timestamp]-upload.csv where [timestamp] is datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    upload_file_name = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv_merged/' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '-upload.csv'
    merged_df[['Title', 'Description', 'Tags', 'Image Path']].to_csv(upload_file_name, index=False)
    
    # Task 25: Write columns "ID", "Prompt", "Title", "Description", "Tags", "Price", "Image Path" from 'merged_df' 
    # to a CSV file to csv_merged/[timestamp]-reference.csv where [timestamp] is datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    reference_file_name = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv_merged/' + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '-reference.csv'
    merged_df.to_csv(reference_file_name, index=False)
    
    # Task 26: Delete the original CSV files from csv_folder
    #for file in os.listdir(csv_folder):
    #    if file.endswith('.csv'):
    #        os.remove(os.path.join(csv_folder, file))
    
    # Task 27: Delete the PNG files from 'png_to_delete'
    for file in png_to_delete:
        os.remove(os.path.join(png_folder, file))
    
    # Task 28: Duplicate png files from png_files, adding '-rounded' to the existing filename (before the extension)
    for file in png_files:
        if os.path.isfile(os.path.join(png_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_folder, file + '.png')} {os.path.join(png_folder, file + '-rounded.png')}")
    
    # Task 29: Duplicate png files from png_files_special, adding '-circle' to the existing filename (before the extension)
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-circle.png')}")
    
    # Task 30: Duplicate png files from png_files_special, adding '-triangle' to the existing filename (before the extension)
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-triangle.png')}")
    
    # Task 31: Duplicate png files from png_files_special, adding '-diamond' to the existing filename (before the extension)
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-diamond.png')}")
    
    # Task 32: Duplicate png files from png_files_special, adding '-randpoly' to the existing filename (before the extension) 
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-randpoly.png')}")
    
    # Task 33: Duplicate png files from png_files_special, adding '-randpolycircle' to the existing filename (before the extension) 
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-randpolycircle.png')}")
            
    # Task 34: Duplicate png files from png_files_special, adding '-randpolycircle' to the existing filename (before the extension) 
    for file in png_files_special:
        if os.path.isfile(os.path.join(png_special_folder, file + '.png')):
            os.system(f"cp {os.path.join(png_special_folder, file + '.png')} {os.path.join(png_special_folder, file + '-star.png')}")
    
    # Task 35: Copy all the png images from png_folder_special to png_folder (overwriting is fine) and then delete the files in png_folder_special
    for file in os.listdir(png_special_folder):
        if file.endswith('.png'):
            shutil.copy(os.path.join(png_special_folder, file), os.path.join(png_folder, file))
            os.remove(os.path.join(png_special_folder, file))

csv_merge()