import os

if __name__ == "__main__":
    os.system(
        "wget https://owncloud.tuwien.ac.at/index.php/s/xtvAkFbtDEvcB6Y/download -O src/nlp/models/NER_model.zip"
    )
    os.system("unzip -n src/nlp/models/NER_model.zip -d src/nlp/models/")
    os.system("rm src/nlp/models/NER_model.zip")
    os.system("rm -rf src/nlp/models/__MACOSX")