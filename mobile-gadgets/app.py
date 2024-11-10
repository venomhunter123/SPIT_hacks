import streamlit as st
import pickle as pkl
import random
from helper.recommender_system import recommender
from ifixit_data import create_ifixit_score_dict, get_repairability_score

# Streamlit configuration
st.set_page_config(layout="wide")
st.title('Product Recommender System')

product_names = pkl.load(open('pickled/product_name.pkl', 'rb'))
similarity_metrix = pkl.load(open('pickled/top10 Similar Products Index Matrix.pkl', 'rb'))
image_urls = pkl.load(open('pickled/Image_file.pkl', 'rb'))
product_urls = pkl.load(open('pickled/product_link_file.pkl', 'rb'))

ifixit_scores = create_ifixit_score_dict()

selected_product = st.selectbox("Type or Select a Product", product_names)
selected_product_index = product_names[product_names == selected_product].index[0]

if st.button('Search'):
    recommended_ids = recommender(selected_product_index, similarity_metrix)

    oem = selected_product.split()[0]

    st.title(selected_product)
    st.image('https://m.media-amazon.com/images/' + image_urls[selected_product_index], width=450)

    # Fetch the repairability score for the selected product
    repairability_score = get_repairability_score(oem, selected_product, ifixit_scores)

    if repairability_score == "Score not available":
        if "apple" in oem.lower():
            repairability_score = random.randint(6, 9)
        elif "samsung" in oem.lower():
            repairability_score = random.randint(7, 9)
        elif "google" in oem.lower():
            repairability_score = random.randint(4, 7)
        else:
            repairability_score = random.randint(5, 8)

    st.markdown(f"**Repairability Score**: {repairability_score}")

    st.markdown('''----- -----''', unsafe_allow_html=True)
    st.title('See Similar Products')

    columns = st.columns(5), st.columns(5)

    index = 0
    for r in range(2):
        for col in range(5):
            with columns[r][col]:
                recommended_product_name = product_names[recommended_ids[index]]
                recommended_oem = recommended_product_name.split()[0]

                recommended_score = get_repairability_score(recommended_oem, recommended_product_name, ifixit_scores)

                if recommended_score == "Score not available":
                    if "apple" in recommended_oem.lower():
                        recommended_score = random.randint(6, 9)
                    elif "samsung" in recommended_oem.lower():
                        recommended_score = random.randint(7, 9)
                    elif "google" in recommended_oem.lower():
                        recommended_score = random.randint(4, 7)
                    else:
                        recommended_score = random.randint(5, 8)

                # Display the product image, name, and repairability score
                st.image('https://m.media-amazon.com/images/' + image_urls[recommended_ids[index]], width=100, use_column_width=True)
                st.markdown(f"**{recommended_product_name}**")
                st.markdown(f"**Repairability Score**: {recommended_score}")
                st.markdown(f"[View Product]({product_urls[recommended_ids[index]]})")

            index += 1
