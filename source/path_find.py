import os # Get the directory of the current Python script
# script_directory = os.path.dirname(os.path.abspath(__file__))
# print(f"The directory of the current script is: {script_directory}")

keywords_list = [ "Maxview", "maxview", "MAXview", "MaxVIEw", "helloe"]

# for i in range(0, len(keywords_list)):   
#     for j in range(i+1, len(keywords_list)):
#         if (keywords_list[i].lower() == keywords_list[j].lower()):
#             keywords_list.remove(j)
#             #print(keywords_list[j])

unique_keywords = []

# Iterate over the original keywords_list
for keyword in keywords_list:
    # Convert the keyword to lowercase for case-insensitive comparison
    lowercase_keyword = keyword.lower()

    # Check if the lowercase keyword is not already in the unique_keywords list
    if lowercase_keyword not in (k.lower() for k in unique_keywords):
        unique_keywords.append(keyword)

print(unique_keywords)


 # unique_keyword_list = []
    # for keywords in keywords_list:
    #     is_unique = True
    #     for unique_keywords in unique_keyword_list:
    #         if keywords.lower() == unique_keywords.lower():
    #             is_unique = False
    #             break
    #     if is_unique:
    #         unique_keyword_list.append(keywords)

    # unique_keyword_list = {}
    # for keywords in keywords_list:
    #     is_unique = True
    #     for unique_keywords in unique_keyword_list:
    #         if keywords.lower() == unique_keywords.lower():
    #             is_unique = False
    #             break
    #     if is_unique:
    #         unique_keyword_list.append(keywords)


    # unique_keyword_list = {}       
    # for i in keywords_list: 
    #     count = 0
    #     is_Unique = True
    #     for j in keywords_list:
    #         if (i.lower() == j.lower() and is_Unique== True):             
    #             count = count + 1          
    #             is_Unique = False
    #         elif (i.lower() == j.lower() and is_Unique == False):
    #             count = count + 1   
    #     if (is_Unique == False):
    #         unique_keyword_list[i] = count 
    #     else:
    #         unique_keyword_list[i] = 1 


    # print(unique_keyword_list)