import os
import datetime
from PIL import Image, ImageDraw, ImageFont

def generate_text_image(width, height, text, font_name, font_color, border_color): 
    def hex_to_rgb(hex_string):
        try:
            # Check if the input string is already in RGB format
            if hex_string.startswith("(") and hex_string.endswith(")"):
                # Remove the parentheses and split the string into three values
                r, g, b = map(int, hex_string[1:-1].split(","))
                return (r, g, b)
            
            # If the input string is not in RGB format, convert it from hex
            hex_string = hex_string.lstrip("#")
            r, g, b = tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
            return (r, g, b)
        except:
            # If there was an error, return white
            return (255, 255, 255)
    
    font_color = hex_to_rgb(font_color)
    
    img = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    font_size = 1
    font = ImageFont.truetype(font_name, font_size)

    while True:
        text_width, text_height = draw.textsize(text, font)
        if text_width < width and text_height < height:
            font_size += 1
            font = ImageFont.truetype(font_name, font_size)
        else:
            break

    font = ImageFont.truetype(font_name, font_size - 1)
    text_width, text_height = draw.textsize(text, font)

    x = (width - text_width) // 2
    y = (height - text_height) // 2

    for border_x in range(-1, 2):
        for border_y in range(-1, 2):
            draw.text((x + border_x, y + border_y), text, font=font, fill=border_color)
    draw.text((x, y), text, font=font, fill=font_color)

    return img

def generate_fonts_dictionary(fonts_directory):
    fonts_available = {}

    for file in os.listdir(fonts_directory):
        if file.endswith(".otf") or file.endswith(".ttf"):
            file_name_without_extension = os.path.splitext(file)[0]
            file_path = os.path.join(fonts_directory, file)
            fonts_available[file_name_without_extension] = file_path

    return fonts_available

def process_fonts_images(ongoing_tshirt_df, fonts_directory, output_path):
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
            
    return fonts_to_install








font_library = ['Open Sans', 'Lobster', 'Impact', 'Comfortaa', 'Amatic SC', 'Pacifico', 'Source Sans Pro', 'Playfair Display', 'Lato', 'Oswald', 
                'Catamaran', 'Bangers', 'Raleway', 'Archivo Narrow', 'Indie Flower', 'Anton', 'Tangerine', 'Old Standard TT', 'Righteous', 'Cabin', 
                'Bitter', 'Poppins', 'Montserrat', 'Ubuntu', 'Roboto', 'Bebas Neue', 'Bungee', 'ChunkFive', 'Cooper Hewitt', 'Dosis', 
                'Exo', 'Frutiger', 'Garamond', 'Gill Sans', 'Gotham', 'Helvetica Neue', 'ITC Franklin Gothic', 'Josefin Sans', 'Kabel', 'League Gothic', 
                'Lobster Two', 'Maven Pro', 'Merriweather', 'Neutraface', 'Nexa', 'Norwester', 'Ostrich Sans', 'Pacifico Alternate', 'Panton', 'Proxima Nova', 
                'Raleway Dots', 'Rockwell', 'Sanchez', 'SF Sports Night', 'Signika', 'Sofia Pro', 'Titillium Web', 'Trade Gothic', 'Ubuntu Condensed', 'Ultra', 
                'Uni Sans', 'Varela Round', 'Vollkorn', 'Walkway', 'Yanone Kaffeesatz', 'Zilla Slab', 'Abril Fatface', 'Arvo', 'Barlow Condensed', 'Baumans', 
                'Cooper Black Pro', 'Eames Century Modern', 'Futura PT', 'HVD Comic Serif', 'Klinic Slab', 'Adelle Sans', 'Aileron', 'Akrobat', 'Aleo', 'Apex Sans', 
                'Baloo Tammudu', 'Beon', 'Bodoni XT', 'Brandon Grotesque', 'Century Gothic', 'Clarendon', 'Code Pro', 'Comfortaa Sans', 'Copperplate', 'Couture', 
                'Cutive Mono', 'District Pro', 'FF DIN', 'Franklin Gothic', 'Gidole', 'Hammersmith One', 'Headliner No. 45', 'Jura', 'Kelson Sans', 'Lemon/Milk']

font_library = ['ChunkFive', 'Cooper Hewitt', 'Frutiger', 'Garamond', 'Gill Sans', 'Gotham', 'Helvetica Neue', 'ITC Franklin Gothic', 'Kabel', 'Neutraface', 'Nexa', 
                'Norwester', 'Ostrich Sans', 'Pacifico Alternate', 'Panton', 'Proxima Nova', 'Rockwell', 'SF Sports Night', 'Sofia Pro', 'Trade Gothic', 'Uni Sans', 
                'Walkway', 'Cooper Black Pro', 'Eames Century Modern', 'Futura PT', 'HVD Comic Serif', 'Klinic Slab', 'Adelle Sans', 'Aileron', 'Akrobat', 'Apex Sans', 
                'Baloo Tammudu', 'Beon', 'Bodoni XT', 'Brandon Grotesque', 'Century Gothic', 'Clarendon', 'Code Pro', 'Comfortaa Sans', 'Copperplate', 'Couture', 
                'District Pro', 'FF DIN', 'Franklin Gothic', 'Gidole', 'Headliner No. 45', 'Kelson Sans', 'Lemon/Milk']

available_fonts = ['Arial', 'Arial Bold', 'Arial Bold Italic', 'Arial Italic', 'Arial Black', 'Bahnschrift', 'Calibri', 'Calibri Bold', 'Calibri Italic', 'Calibri Light', 
                   'Calibri Light Italic', 'Calibri Bold Italic', 'Cambria Bold', 'Cambria Italic', 'Cambria Bold Italic', 'Candara', 'Candara Bold', 'Candara Italic', 
                   'Candara Light', 'Candara Light Italic', 'Candara Bold Italic', 'Comic Sans MS', 'Comic Sans MS Bold', 'Comic Sans MS Italic', 'Comic Sans MS Bold Italic', 
                   'Consolas', 'Consolas Bold', 'Consolas Italic', 'Consolas Bold Italic', 'Constantia', 'Constantia Bold', 'Constantia Italic', 'Constantia Bold Italic', 
                   'Corbel', 'Corbel Bold', 'Corbel Italic', 'Corbel Light', 'Corbel Light Italic', 'Corbel Bold Italic', 'Courier New', 'Courier New Bold', 
                   'Courier New Bold Italic', 'Courier New Italic', 'Ebrima', 'Ebrima Bold', 'Franklin Gothic Medium', 'Franklin Gothic Medium Italic', 'Gabriola', 'Gadugi', 
                   'Gadugi Bold', 'Georgia', 'Georgia Bold', 'Georgia Italic', 'Georgia Bold Italic', 'Microsoft Himalaya', 'HoloLens MDL2 Assets', 'Impact', 'Ink Free', 
                   'Javanese Text', 'Lato Bold', 'Lato Bold Italic', 'Lato Italic', 'Lato Light', 'Lato Light Italic', 'Lato Regular', 'Lato Semibold', 'Lato Semibold Italic', 
                   'Leelawadee UI Bold', 'Leelawadee UI', 'Leelawadee UI Semilight', 'Lucida Console', 'Lucida Sans Unicode', 'Malgun Gothic', 'Malgun Gothic Bold', 
                   'Malgun Gothic Semilight', 'Microsoft Sans Serif', 'Myanmar Text', 'Myanmar Text Bold', 'Mongolian Baiti', 'Microsoft Yi Baiti', 'MV Boli', 'Nirmala UI', 
                   'Nirmala UI Bold', 'Nirmala UI Semilight', 'Microsoft New Tai Lue', 'Microsoft New Tai Lue Bold', 'Palatino Linotype', 'Palatino Linotype Bold', 
                   'Palatino Linotype Bold Italic', 'Palatino Linotype Italic', 'Microsoft PhagsPa', 'Microsoft PhagsPa Bold', 'Sans Serif Collection', 'Segoe MDL2 Assets', 
                   'Segoe Fluent Icons', 'Segoe Print', 'Segoe Print Bold', 'Segoe Script', 'Segoe Script Bold', 'Segoe UI', 'Segoe UI Bold', 'Segoe UI Italic', 'Segoe UI Light', 
                   'Segoe UI Semilight', 'Segoe UI Bold Italic', 'Segoe UI Black', 'Segoe UI Black Italic', 'Segoe UI Emoji', 'Segoe UI Historic', 'Segoe UI Light Italic', 
                   'Segoe UI Semibold', 'Segoe UI Semibold Italic', 'Segoe UI Semilight Italic', 'Segoe UI Symbol', 'Segoe UI Variable', 'SimSun-ExtB', 'Sitka Text Italic', 
                   'Sitka Text', 'Sylfaen', 'Tahoma', 'Tahoma Bold', 'Microsoft Tai Le', 'Microsoft Tai Le Bold', 'TeamViewer15', 'Times New Roman', 'Times New Roman Bold', 
                   'Times New Roman Bold Italic', 'Times New Roman Italic', 'Trebuchet MS', 'Trebuchet MS Bold', 'Trebuchet MS Bold Italic', 'Trebuchet MS Italic', 'Verdana', 
                   'Verdana Bold', 'Verdana Italic', 'Verdana Bold Italic']


[
'arial', 'arialbd', 'arialbi', 'ariali', 'ariblk', 'calibri', 'calibrib', 'calibrii', 'calibril', 'calibrili', 'calibriz', 'cambriab', 'cambriai', 'cambriaz', 'Candara', 'Candarab', 'Candarai', 'Candaral', 'Candarali', 'Candaraz', 'comic', 'comicbd', 'comici', 'comicz', 'consola', 'consolab', 'consolai', 'consolaz', 'corbel', 'corbelb', 'corbelb_0', 'corbeli', 'corbeli_0', 'corbell', 'corbelli', 'corbelz', 'corbelz_0', 'corbel_0', 'cour', 'courbd', 'courbi', 'couri', 'ebrima', 'ebrimabd', 'gadugi', 'gadugib', 'gadugib_0', 'Gabriola', 'bauhaus-93', 'BebasNeue', 'BrushScriptStd', 'Champagne & Limousines Bold', 'Champagne & Limousines', 'Chunkfive', 'Cocaine sans', 'Copper Canyon WBW', 'Couture-Bold', 'Dense-Regular', 'DHF Story Brush', 'Diavlo_BOLD_II', 'Diavlo_BOOK_II', 'Diavlo_LIGHT_II', 'Diavlo_MEDIUM_II', 'DouarOutline', 'Elektra', 'Elianto-Regular', 'Estrangelo Edessa', 'Evergreen', 'Fabulous', 'Futura', 'Futura-Bold', 'Futura-Condensed', 'Futura-CondensedBold', 'Futura-CondensedLight', 'Futura-Light', 'Futura-Medium', 'Futura-MediumItalic', 'Futura-Oblique', 'Gabba_All_Caps', 'Garamond', 'Garamond-Bold', 'Garamond-Italic', 'Garamond-SemiBold', 'GillSans', 'GillSans-Bold', 'GillSans-BoldItalic', 'GillSans-Italic', 'GillSans-Light', 'GillSans-LightItalic', 'GillSans-SemiBold', 'GillSans-SemiBoldItalic', 'GillSans-UltraBold', 'Helvetica', 'Helvetica-Bold', 'Helvetica-BoldOblique', 'Helvetica-Light', 'Helvetica-LightOblique', 'Helvetica-Oblique', 'Impact', 'Lobster', 'Montserrat-Bold', 'Montserrat-Light', 'Montserrat-Regular', 'MyriadPro-Bold', 'MyriadPro-Regular', 'OpenSans-Bold', 'OpenSans-Light', 'OpenSans-Regular', 'Roboto-Bold', 'Roboto-Light', 'Roboto-Regular', 'TimesNewRoman', 'TimesNewRoman-Bold', 'TimesNewRoman-BoldItalic', 'TimesNewRoman-Italic'
]