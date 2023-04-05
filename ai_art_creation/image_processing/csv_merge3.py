import pandas as pd
import os
import datetime
import shutil

def csv_merge():
    # Task 1
    csv_directory = "C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv/"
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

    # Task 2
    merged_df = pd.DataFrame()
    for csv_file in csv_files:
        file_path = os.path.join(csv_directory, csv_file)
        df = pd.read_csv(file_path, encoding="ISO-8859-1")
        merged_df = merged_df.append(df)

    # Task 3
    png_directory = "C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/images_raw/ready_to_scale/"
    png_files = [os.path.splitext(file)[0] for file in os.listdir(png_directory) if file.endswith(".png")]

    # Task 4
    png_dict = {}
    for png_file in png_files:
        key = png_file[:19]
        value = png_file[20:]
        if len(value) > 0:
            if key in png_dict:
                png_dict[key].append(value)
            else:
                png_dict[key] = [value]

    # Task 5
    matching_ids = set(merged_df['ID']) & set(png_dict.keys())
    merged_df = merged_df[merged_df['ID'].isin(matching_ids)]

    # Task 6
    png_dict_rev = {}
    for key, values in png_dict.items():
        for value in values:
            if value in png_dict_rev:
                png_dict_rev[value].append(key)
            else:
                png_dict_rev[value] = [key]
    
    # Helper function for duplicating and updating DataFrame
    def duplicate_and_update_df(df, title_suffix, search_suffix, replace_suffix):
        new_df = df.copy()
        new_df['Title'] = new_df['Title'] + title_suffix
        new_df['Image Path'] = new_df['Image Path'].replace(search_suffix, replace_suffix, regex=True)
        return new_df

    # Task 7
    merged_df['Image Path'] = merged_df['Image Path'].replace(".png", "-scaled.png", regex=True)

    # Task 8 and 9
    merged_df_rounded = duplicate_and_update_df(merged_df, " (rounded)", "-scaled.png", "-rounded-scaled.png")

    # Task 10
    if "rounded" in png_dict_rev:
        merged_df_rounded = merged_df_rounded[merged_df_rounded['ID'].isin(png_dict_rev["rounded"])]

    # Task 11 and 12
    merged_df_circle = duplicate_and_update_df(merged_df, " (circle)", "-scaled.png", "-circle-scaled.png")

    # Task 13
    if "circle" in png_dict_rev:
        merged_df_circle = merged_df_circle[merged_df_circle['ID'].isin(png_dict_rev["circle"])]

    # Task 14 and 15
    merged_df_triangle = duplicate_and_update_df(merged_df, " (triangle)", "-scaled.png", "-triangle-scaled.png")

    # Task 16
    if "triangle" in png_dict_rev:
        merged_df_triangle = merged_df_triangle[merged_df_triangle['ID'].isin(png_dict_rev["triangle"])]

    # Task 17 and 18
    merged_df_diamond = duplicate_and_update_df(merged_df, " (diamond)", "-scaled.png", "-diamond-scaled.png")

    # Task 19
    if "diamond" in png_dict_rev:
        merged_df_diamond = merged_df_diamond[merged_df_diamond['ID'].isin(png_dict_rev["diamond"])]

    # Task 20 and 21
    merged_df_star = duplicate_and_update_df(merged_df, " (star)", "-scaled.png", "-star-scaled.png")

    # Task 22
    if "star" in png_dict_rev:
        merged_df_star = merged_df_star[merged_df_star['ID'].isin(png_dict_rev["star"])]

    # Task 23 and 24
    merged_df_randpoly = duplicate_and_update_df(merged_df, " (randpoly)", "-scaled.png", "-randpoly-scaled.png")

    # Task 25
    if "randpoly" in png_dict_rev:
        merged_df_randpoly = merged_df_randpoly[merged_df_randpoly['ID'].isin(png_dict_rev["randpoly"])]

    # Task 26 and 27
    merged_df_randpolycircle = duplicate_and_update_df(merged_df, " (randpolycircle)", "-scaled.png", "-randpolycircle-scaled.png")

    # Task 28
    if "randpolycircle" in png_dict_rev:
        merged_df_randpolycircle = merged_df_randpolycircle[merged_df_randpolycircle['ID'].isin(png_dict_rev["randpolycircle"])]

    # Task 29
    merged_df = merged_df.append([merged_df_rounded, merged_df_circle, merged_df_triangle, merged_df_diamond, merged_df_star, merged_df_randpoly, merged_df_randpolycircle])

    # Task 30 and 31
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_directory = "C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv_merged/"

    merged_df[["Title", "Description", "Tags", "Image Path"]].to_csv(os.path.join(output_directory, f"{timestamp}-upload.csv"), index=False)
    merged_df[["ID", "Prompt", "Title", "Description", "Tags", "Image Path"]].to_csv(os.path.join(output_directory, f"{timestamp}-reference.csv"), index=False)
    
    # Task 32
    archive_directory = "C:/Users/trent/OneDrive/Documents/GitHub/ai_art_creation/ai_art_creation/image_processing/csv/archive/"
    for csv_file in csv_files:
        file_path = os.path.join(csv_directory, csv_file)
        archive_path = os.path.join(archive_directory, csv_file)
        shutil.move(file_path, archive_path)

csv_merge()