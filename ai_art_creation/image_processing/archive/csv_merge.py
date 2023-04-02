import os
import glob
import pandas as pd
import datetime

def merge_csv():
    # Task 1: Import all CSV files from the specified folder
    csv_path = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv/'
    all_csv_files = glob.glob(os.path.join(csv_path, "*.csv"))

    # Task 2: Merge the data
    dataframes = [pd.read_csv(f, encoding='ISO-8859-1') for f in all_csv_files]
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Task 3: Retrieve all PNG file names and remove the extension
    images_path = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/images_raw/'
    png_files = glob.glob(os.path.join(images_path, "*.png"))
    file_names = [os.path.splitext(os.path.basename(f))[0] for f in png_files]

    # Task 4: Filter the merged CSV data for matching IDs
    filtered_df = merged_df[merged_df['ID'].isin(file_names)].copy()

    # Task 5: Replace ".png" with "-scaled.png" in the "Image Path" column
    filtered_df.loc[:, 'Image Path']  = filtered_df['Image Path'].str.replace('.png', '-scaled.png', regex = True)

    # Task 6: Write the merged CSV file with the specified columns and format
    output_path = 'C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv_merged/'
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    upload_filename = f"{current_time}-upload.csv"
    upload_columns = ["Title", "Description", "Tags", "Price", "Image Path"]
    filtered_df.to_csv(os.path.join(output_path, upload_filename), columns=upload_columns, index=False)

    # Task 7: Write the merged CSV file with the specified columns and format
    reference_filename = f"{current_time}-reference.csv"
    reference_columns = ["ID", "Prompt", "Title", "Description", "Tags", "Price", "Image Path"]
    filtered_df.to_csv(os.path.join(output_path, reference_filename), columns=reference_columns, index=False)

    # Task 8: Delete the original CSV files
    for csv_file in all_csv_files:
        os.remove(csv_file)
    
    # Task 9: Delete the PNG files that do not exist in the ID column of the merged data
    for file_name, png_file in zip(file_names, png_files):
        if file_name not in merged_df['ID'].values:
            os.remove(png_file)
    
merge_csv()