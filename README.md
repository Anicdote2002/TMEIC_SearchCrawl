# TMEIC_SearchCrawl
This is a mini search engine which basically traverses a Bugzilla database for TMEIC that has retreived using the Bugzilla API.
The basic algorithm for now is, filter out common words using a Python Script, make note of all the keywords, get a number of how many
times each bug popped up and then use that to make a priority.
