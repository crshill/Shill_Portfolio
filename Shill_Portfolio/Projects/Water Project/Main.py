from Supervised_Methods import S_Models
from Unsupervised_Methods import US_Models
import warnings
#from Data_prep import Data_Prep

warnings.filterwarnings("ignore")
def main() :

    #file_name = './Data/Modeling_Data/Munic_Data_New.csv'
    #file_name = './Data/Rates/Munic_Data_wRatings_Years_V11.csv'
    file_name = './Data/Rates/Munic_Data_RE_NextYear.csv'

    # prep = Data_Prep()
    classifier = S_Models()
    #classifier.classifier_step(file_name, 55, 1)
    classifier.regression_step(file_name,1,1)
    #classifier.voter(file_name, 100)
    #classifier.svm_class(file_name, 100)


if __name__ == '__main__' :

    main()