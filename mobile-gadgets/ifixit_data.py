import pandas as pd
import random
import glob

# Load all the ifixit data files and combine them into a single DataFrame
def load_ifixit_data():
    files = glob.glob("ifixit_data/*.csv")
    dataframes = []
    for file in files:
        df = pd.read_csv(file)
        df = df.iloc[:, :3]  # Keep only the first 3 columns
        df.columns = ['OEM', 'Device', 'Repairability Score']
        dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

# Create a dictionary of repairability scores
def create_ifixit_score_dict():
    ifixit_df = load_ifixit_data()
    ifixit_scores = {}

    # Normalize OEM names (lowercase and remove extra spaces)
    ifixit_df['OEM'] = ifixit_df['OEM'].str.lower().str.strip()
    ifixit_df['Device'] = ifixit_df['Device'].str.lower().str.strip()

    for _, row in ifixit_df.iterrows():
        key = (row['OEM'], row['Device'])
        ifixit_scores[key] = row['Repairability Score']

    return ifixit_scores

# Function to get the repairability score with randomization for missing scores
def get_repairability_score(oem, device, ifixit_scores):
    oem = oem.lower().strip()
    device = device.lower().strip()
    key = (oem, device)

    # Check if the score exists in the dictionary
    if key in ifixit_scores:
        score = ifixit_scores[key]
        return score if pd.notna(score) else generate_random_score(oem)

    # If not found, generate a random score based on OEM
    return generate_random_score(oem)

# Helper function to generate random scores
def generate_random_score(oem):
    if 'apple' in oem:
        return random.randint(6, 9)
    elif 'samsung' in oem:
        return random.randint(7, 9)
    elif 'google' in oem:
        return random.randint(4, 7)
    elif 'xiaomi' in oem:
        return random.randint(5, 8)
    elif 'oneplus' in oem:
        return random.randint(6, 8)
    else:
        # For other brands, return a general range
        return random.randint(4, 8)

