import numpy as np
import pandas as pd
from sklearn.preprocessing import Imputer, Normalizer


out_file = "./Data/Rad_plot_all.csv"


class Data_Prep(object) :

    #####################################################################
    # If two files, that you wish to combine, but cannot be simply combined by copy paste
    # (i.e. if file1{Municipalities} does not equal file2{Municipalities}), then this routine combines the data sets
    # while maintaining file1's set of municipalities.
    # For instance if I had a data set of audit data and a separate file of census data and wanted to combine them,
    # but the census data had many entries that were not needed or included in the audit data, then setting file1 as
    # audit data and file2 as census data would add the census data only to the municipalities existing
    # in the audit data.

    def enter_pops(self, file1, file2):

        pops = pd.read_csv(file2)
        out = pd.read_csv(file1)

        out = pd.merge(out, pops, how='left', on='Municipality')

        out.to_csv(out_file)


    # enter_pops(out_file, "./Data/Ave_RE.csv")

######################################################################
#####################################################################
# It is often necessary to normalize a set of data for each entry (i.e turn it into a vector of magnitude 1).
# This routine cycles through each municipality and normalizes its set of data.

    def normalize(self, file):
        data = pd.read_csv(file)
        features = list(data.columns[1:])
        print(features)

        x = data[features]

        scalar = Normalizer().fit(x)
        normalized_x = scalar.transform(x)
        norm_data = pd.DataFrame(normalized_x)
        print(norm_data.head())

        norm_data.to_csv("./Data/Normalized_Data.csv")


########################################################################
########################################################################
    # Most data we use will contain missing values, NaN values, from the municipalities not reporting their data in the
    # audit reports, or perhaps the census data didn't include that particular town/ county/ community. This routine
    # goes about replacing these NaNs using various methods.
    # strat = 'mean' & fill = None - replace NaN with mean of field
    # strat = 'median' & fill = None - replace with median
    # strat = 'most_frequent' & fill = None - replace with mode
    # strat = 'constant' & fill = (designated value) - replace with (designated value), i.e. 0



    def replace_nan(self, f_in, f_out, strat, fill) :

        file = pd.read_csv(f_in)
        imputer = Imputer(missing_values=np.nan, strategy=strat, fill_value = fill, axis=0)
        feature = list(file.columns[1:-1])
        for f in feature :
            file[[f]] = imputer.fit_transform(file[[f]])

        file.to_csv(f_out)


#replace_nan("./Data/Munic_Data_3year_V6.csv", "./Data/Munic_Data_3year_V7.csv")