import pandas as pd
# path= "C:\\Users\\yraja\\LogicBot\\rasa"
# create_files_path = "C:\\Users\\yraja\\LogicBot\\rasa\\data"
def create_rasa_files(path, create_files_path):
    create_files_path = "C:/Users/yraja/LogicBot/rasa/data/nlu.yml"
    path = "C:/Users/yraja/LogicBot/rasa/nlu_sample_format_for_conversion.csv"
    print("hi")
    """
    Converts a CSV file created with the specified format to RASA accepted nlu.md format
    :param path: path where the CSV file is present
    :param create_files_path: path where the nlu.md file needs to be created
    :return: None. Files are created in the path specified via create_files_path
    """
    df = pd.read_csv(path)
    file = open(f"{create_files_path}", "w")
    intents = list(df.columns)
    for item in intents:
        file.write("- intent: {intent_name}\n".format(intent_name=item))
        for sent in df[item]:
            file.write("- {}\n".format(sent))
    file.close()
    return None

create_files_path = "C:/Users/yraja/LogicBot/rasa/data/nlu.yml"
path = "C:/Users/yraja/LogicBot/rasa/nlu_sample_format_for_conversion.csv"
out = create_rasa_files(path, create_files_path)
print(out)
            