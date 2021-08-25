import numpy as np
import pandas as pd
import numpy as np
import math
import os

import pickle
from config.service_utils.constants import SENTIMENT_TOEKNS


class PreFetchData:
    ASKED_AMOUNT_CAP = 500000

    def __init__(self, data):
        self.data = data

    def fetch(self):
        """
        Fetch required data
        :return: All required data
        """
        mortality_band = self.get_mortality_band()
        return mortality_band

    def get_mortality_band(self):

        xgb_1 = pickle.load(open(
            os.path.dirname(os.path.abspath(__file__)) +
            "/../../../data_files/model_files/zomato_reviews.pickle.dat",
            "rb"))

        # files = os.listdir(w_dir2 + 'Review files/')
            # for k in range(1) :
            # self.data = self.data['_source']['details']['restaurantInfo']
        restInfo = self.data
        rf = pd.DataFrame(restInfo['reviews'])
        for token in SENTIMENT_TOEKNS:
            rf.loc[:, str(token)] = rf['reviewText'].str.lower().str.count(str(token))
        rf['sentiment_score'] = [x[1] for x in xgb_1.predict_proba(rf[SENTIMENT_TOEKNS])]
        rf.loc[:, 'sentiment_score'] = np.where(rf["reviewText"] == "", 0.13161,
                                                rf['sentiment_score'])
        sentiment_count = 0;
        sentiment_sum = 0;
        for i in range(len(rf)):
            if (rf.loc[i, "reviewTimeInMonth"] <= 6):
                sentiment_count = sentiment_count + 1
                sentiment_sum = sentiment_sum + rf.loc[i, "sentiment_score"]
        if (sentiment_count == 0):
            sentiment_count = sentiment_count + 1
        rf.loc[:, "sentiment_sum"] = sentiment_sum
        rf.loc[:, "sentiment_count"] = sentiment_count
        rf.loc[:, "review_last_12m"] = restInfo["review_last_12m"]
        rf.loc[:, "zomato_vintage"] = restInfo["zomato_vintage"]
        rf.loc[:, "rest_id"] = restInfo["restId"]
        avg_score = (sentiment_sum / sentiment_count)
        if (sentiment_count <= 5):
            avg_score = 1

        logit = -1.7483 - 0.0061 * restInfo["review_last_12m"] - 0.0136 * \
                restInfo["zomato_vintage"] + 1.1298 * avg_score
        mortality_score = math.exp(logit) / (1 + math.exp(logit))
        rf.loc[:, "mortality_score"] = mortality_score
        rf.loc[:, 'band_10m'] = np.where(rf["mortality_score"].between(0, 0.0493),
                "1",np.where(rf["mortality_score"].between(0.0493, 0.0599),
                "2", np.where(rf["mortality_score"].between(0.0599, 0.0704),
                "3",np.where(rf["mortality_score"].between(0.0704, 0.0829),
                "4", np.where(rf["mortality_score"].between(0.0829,0.0963),
                "5", np.where(rf["mortality_score"].between(0.0963, 0.1193),
                "6",np.where(rf['mortality_score'].between(0.1193, 0.1647),
                "7",np.where(rf['mortality_score'].between(0.1647, 0.1983),
                "8",np.where(rf['mortality_score'].between(0.1983,0.2315),
                "9",np.where(rf['mortality_score'].between(0.2315,1),
                "10","NA"))))))))))
        return rf.loc[0,'band_10m']
