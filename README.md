
# Wikipedia Search Engine

### How to run code
    
    - To create index, run script -
        bash index.sh <path to xml dump> <path where you want to store index and title file> <index_stat_file_name>

    - To run Search query, run script -
        bash search.sh <path where the index and title file> <one word query>

### Note -
    
    - Please provide absolute path only.
    - For now only single word search is supported.
    - Inverted index will be stored inside temp folder on mentioned path and title files will be stored inside title folder on given path.
    - The submission contains -
        - 3 python3 files i.e. index.py, pre_processing.py and search.py
        - 2 bash script files i.e. index.sh and search.sh
        - 1 text file for stopwords
        - 1 readme file

### Requirements -
    Following python3 libraries will be required for running the code
        - PyStemmer
        - nltk
        - re
        - os
        - sys
        - time
        - collections
        - xml.sax


