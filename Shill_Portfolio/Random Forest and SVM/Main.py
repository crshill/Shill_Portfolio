from Supervised_Methods import Models
from Data_prep import Data_Prep


def main() :

    file_name = './Data/Munic_Data_3year_V8.csv'

    # prep = Data_Prep()
    classifier = Models()
    classifier.feature_select(file_name)


if __name__ == '__main__' :

    main()