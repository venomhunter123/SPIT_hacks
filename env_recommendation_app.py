import requests
import pandas as pd
import streamlit as st

# Function to fetch data from the API and handle JSON format
def get_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = pd.json_normalize(response.json())
        return data
    else:
        return None

# Function to filter and recommend refrigerators/freezers
def recommend_refrigerator_freezer(product_name, api_url):
    data = get_data_from_api(api_url)
    if data is None:
        st.write("Failed to fetch data from API.")
        return []

    # Filter based on product type (use available column instead of 'product_type')
    filtered_data = data[data['lab_grade_refrigerators_and_freezers_product_type'].str.contains(product_name, case=False, na=False)]

    # Sort by energy consumption and peak temperature variance
    filtered_data = filtered_data.sort_values(by=['daily_energy_consumption', 'peak_temperature_variance_c'])

    # Limit to top 10 environmentally friendly products
    filtered_data = filtered_data.head(10)

    recommendations = []
    for _, row in filtered_data.iterrows():
        recommendation = {
            'brand_name': row['brand_name'],
            'model_name': row['model_name'],
            'product_type': row['lab_grade_refrigerators_and_freezers_product_type'],
            'daily_energy_consumption': row['daily_energy_consumption'],
            'peak_temperature_variance': row['peak_temperature_variance_c'],
            'reason': f"Low daily energy consumption ({row['daily_energy_consumption']} kWh) and low peak temperature variance ({row['peak_temperature_variance_c']}°C)."
        }
        recommendations.append(recommendation)

    return recommendations

# Function to filter and recommend air conditioners

def recommend_air_conditioner(product_name, api_url_ac):
    # Fetch the data
    data = get_data_from_api(api_url_ac)  # Use the api_url_ac to fetch the data
    if data is None:
        st.write("Failed to fetch data from API.")
        return []

    # Debugging: Print the first few rows of the data to inspect the structure
    st.write("recommendations:", data.head())
    st.write("Best Environment Friendly Product:")


    # Convert relevant columns to numeric values (handling errors gracefully)
    data['cooling_capacity_btu_hour'] = pd.to_numeric(data['cooling_capacity_btu_hour'], errors='coerce')
    data['annual_energy_use_kwh_yr'] = pd.to_numeric(data['annual_energy_use_kwh_yr'], errors='coerce')
    data['combined_energy_efficiency_ratio_ceer'] = pd.to_numeric(data['combined_energy_efficiency_ratio_ceer'], errors='coerce')

    # Relaxed filter: Show products that meet at least one of the criteria perfectly.
    def evaluate_product(row):
        match = False
        reason = ""
        
        # Check for "meets_most_efficient_criteria" flag first
        if row['meets_most_efficient_criteria'] == "Yes":
            match = True
            reason = f"Product meets 'Most Efficient Criteria' for energy efficiency."
        
        # If not already matched, check other conditions
        elif row['cooling_capacity_btu_hour'] >= 12000:
            match = True
            reason = f"Product has a high cooling capacity of {row['cooling_capacity_btu_hour']} BTU/hr."

        elif row['annual_energy_use_kwh_yr'] <= 600:
            match = True
            reason = f"Product has a low annual energy use of {row['annual_energy_use_kwh_yr']} kWh/year."

        elif row['low_noise'] == "Yes":
            match = True
            reason = f"Product operates at a low noise level."

        # Add additional checks as needed (e.g., energy efficiency ratio)
        elif row['combined_energy_efficiency_ratio_ceer'] >= 15:
            match = True
            reason = f"Product has a high CEER of {row['combined_energy_efficiency_ratio_ceer']}."

        return match, reason

    # Filter products based on relaxed matching conditions
    filtered_data = data[data.apply(lambda row: evaluate_product(row)[0], axis=1)]

    # Prepare recommendations
    recommendations = []
    for _, row in filtered_data.iterrows():
        match, reason = evaluate_product(row)
        recommendation = {
            'brand_name': row['brand_name'],
            'model_number': row['model_number'],
            'cooling_capacity': row['cooling_capacity_btu_hour'],
            'voltage': row['voltage_volts'],
            'product_class': row['product_class'],
            'low_noise': row['low_noise'],
            'annual_energy_use_kwh_yr': row['annual_energy_use_kwh_yr'],
            'meets_efficient_criteria': row['meets_most_efficient_criteria'],
            'reason': reason
        }
        recommendations.append(recommendation)

    return recommendations



# Streamlit UI elements
st.title("Environmentally Friendly Product Recommendations")

# Input fields for user search
product_name = st.text_input("Enter product name (e.g., refrigerator, freezer, air conditioner):")

# API URLs for datasets
api_url_rf = 'https://data.energystar.gov/resource/g242-ysjw.json'
api_url_ac = 'https://data.energystar.gov/resource/5xn2-dv4h.json'

# Initialize the recommendations variable
recommendations = []

# Fetch recommendations based on product type
if product_name:
    st.write("Fetching recommendations...")

    if 'refrigerator' in product_name.lower() or 'freezer' in product_name.lower():
        recommendations = recommend_refrigerator_freezer(product_name, api_url_rf)
    elif 'air conditioner' in product_name.lower():
        recommendations = recommend_air_conditioner(product_name, api_url_ac)
    else:
        st.write("Sorry, no recommendations available for this product type.")

    # Display the recommendations
    if recommendations:
        for rec in recommendations:
            st.write(f"**Brand:** {rec['brand_name']}")
            st.write(f"Available keys in rec: {rec.keys()}")

# Get either 'model_name' or 'model_number', if present
            model = rec.get('model_name') or rec.get('model_number') or 'Unknown Model'
            st.write(f"**Model:** {model}")
            # st.write(f"**Model:** {rec['model_name']}")
            st.write(f"**Product Type:** {rec['product_type']}")
            st.write(f"**Reason:** {rec['reason']}")
            st.write("---")
    else:
        st.write("No products found matching your criteria.")
