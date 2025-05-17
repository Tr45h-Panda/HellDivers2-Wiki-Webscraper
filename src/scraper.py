import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Mapping of input code images to directions
INPUT_CODE_MAP = {
    'Up Arrow.png': 'U',
    'Left Arrow.png': 'L',
    'Down Arrow.png': 'D',
    'Right Arrow.png': 'R'
}

def sanitize_filename(filename):
    """Remove invalid characters from the filename."""
    return re.sub(r'[<>:"/\\|?*]', '', filename)  # Remove invalid characters

def download_image(url, group_name, filename):
    """Download an image and save it to the appropriate group folder."""
    # Simplify the group name to avoid invalid characters
    group_folder = os.path.join('data', 'images', group_name)  # Save images in 'data/images'
    os.makedirs(group_folder, exist_ok=True)

    # Sanitize the filename
    sanitized_filename = sanitize_filename(filename)

    # Full path to save the image
    file_path = os.path.join(group_folder, sanitized_filename)

    # Download the image
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded: {sanitized_filename} to {group_folder}")
    else:
        print(f"Failed to download {sanitized_filename} from {url}")

def scrape_helldivers2_wiki():
    url = 'https://helldivers.fandom.com/wiki/Stratagem_Codes'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    stratagems = []
    stratagem_id = 1  # Start ID at 1

    # Find all groups of stratagems
    groups = soup.select('table.wikitable')
    if not groups:
        print("No tables with the specified class found.")
        return []

    for group in groups:
        # Extract the group name
        group_name_tag = group.find('th', colspan="6")
        if not group_name_tag:
            group_name_tag = group.find('span', style=True)
            if group_name_tag:
                full_group_name = group_name_tag.text.strip()
            else:
                print("No group name found for a table. Skipping...")
                continue
        else:
            full_group_name = group_name_tag.text.strip()

        # Simplify the group name to the first word
        group_name = full_group_name.split(':')[0]
        print(f"Processing group: {group_name}")

        # Determine the border color based on the group
        if group_name == "Offensive":
            border_color = "RED"
        elif group_name == "Supply":
            border_color = "BLUE"
        elif group_name == "Defensive":
            border_color = "GREEN"
        elif group_name == "Mission":
            border_color = "GOLD"
        else:
            border_color = "UNKNOWN"

        # Extract all stratagems within the group
        rows = group.select('tbody tr')
        if not rows:
            print(f"No rows found in group: {group_name}")
            continue

        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 3:  # Ensure there are enough columns
                print("Skipping a row with insufficient columns.")
                continue

            # Extract stratagem name
            name_tag = columns[1].find('a')
            name = name_tag.text.strip() if name_tag else "Unknown"
            print(f"Found stratagem: {name}")

            # Extract input code
            input_code_images = columns[2].find_all('img')
            if not input_code_images:
                print(f"No input code images found for stratagem: {name}")
                input_code = "?";
            else:
                input_code = ''
                for img in input_code_images:
                    data_image_name = img.get('data-image-name', '')
                    if data_image_name:
                        direction = INPUT_CODE_MAP.get(data_image_name, '?')
                        input_code += direction
            print(f"Input code for {name}: {input_code}")

            # Extract the correct image filename and URL
            image_tag = columns[0].find('img')
            if image_tag and 'data-image-name' in image_tag.attrs:
                filename = image_tag['data-image-name']
                filename = sanitize_filename(filename)  # Sanitize the filename
                
                # Check for the actual image URL in 'data-src' or fallback to 'src'
                image_url = image_tag.get('data-src', image_tag.get('src', ''))

                # Check if the URL is valid (starts with http or https)
                if image_url.startswith('http'):
                    # Download the image
                    download_image(image_url, group_name, filename)
                elif image_url.startswith('data:image'):
                    print(f"Skipping image with base64 data URL: {image_url}")
                else:
                    print(f"Skipping image with invalid URL: {image_url}")
            else:
                filename = 'unknown.png'  # Fallback if no image is found
                image_url = None
            print(f"Image filename for {name}: {filename}")

            # Append the stratagem data
            stratagems.append({
                'ID': stratagem_id,
                'Group': group_name,
                'Name': name,
                'Command': input_code,  # Renamed from stratagem_code
                'foldername': group_name,  # Same as the group name
                'filename': filename,
                'Border': border_color
            })

            stratagem_id += 1  # Increment the ID

    return stratagems

def save_to_csv(data):
    if not data:
        print("No data to save.")
        return
    # Reorder the columns as specified
    df = pd.DataFrame(data, columns=['ID', 'Name', 'Border', 'Command', 'foldername', 'filename'])
    os.makedirs('data', exist_ok=True)  # Ensure the 'data' directory exists
    df.to_csv('data/Stratagems.csv', index=False)
    print("Data saved to data/Stratagems.csv")

if __name__ == '__main__':
    stratagem_data = scrape_helldivers2_wiki()
    # Remove the 'Group' column from the data
    for stratagem in stratagem_data:
        stratagem.pop('Group', None)  # Remove the 'Group' key
    save_to_csv(stratagem_data)