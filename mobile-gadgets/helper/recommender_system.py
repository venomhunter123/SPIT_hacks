
# def recommender(product,name_list,similarity_metrix):
#     recommendations = []
#     product_index = name_list[name_list == product].index[0]
    
#     similarity_list = list(enumerate(similarity_metrix[product_index]))
#     top_10_similar_product = sorted(similarity_list,key=lambda x:x[1],reverse=True)[1:11]

#     print(top_10_similar_product)
#     return list(map(lambda x:x[0], top_10_similar_product))
def recommender(product_index,similarity_matrix):
    """_summary_

    Args:
        product_index (_type_): int
        similarity_matrix (_type_):  array

    Returns:
        _type_: return Indexes of top 10 Similar type of products
    """
    return similarity_matrix[product_index]