import numpy as np
import pandas as pd
import numpy as np
import math
import os

import pickle
from mortality_band_service.computation.constants import SENTIMENT_TOEKNS,\
    EMPTY_SENTIMENT_SCORE, MORTALITY_BAND_RANGE


class CalculateMortalityBand:

    def __init__(self, data):
        self.data = data

    def calculate(self):
        """
        Fetch required data
        :return: All required data
        """
        mortality_band = self.get_mortality_band()
        return mortality_band

    def get_mortality_band(self):
        # Read pickle file
        xgb_1 = pickle.load(open(
            os.path.dirname(os.path.abspath(__file__)) +
            "/../../../data_files/model_files/zomato_reviews.pickle.dat",
            "rb"))

        restInfo = self.data
        # Get reviews from data
        reviews = pd.DataFrame(restInfo['reviews'])
        for token in SENTIMENT_TOEKNS:
            reviews.loc[:, str(token)] = reviews['reviewText'].str.lower().str.count(str(token))
        # Predict sentiment score using model
        reviews['sentiment_score'] = [x[1] for x in
                                      xgb_1.predict_proba(reviews[SENTIMENT_TOEKNS])]
        # set sentiment score
        reviews.loc[:, 'sentiment_score'] = np.where(reviews["reviewText"] == "",
                                    EMPTY_SENTIMENT_SCORE, reviews['sentiment_score'])
        sentiment_count = 0
        sentiment_sum = 0
        #Count sentiment only for reviews within 6 months
        for i in range(len(reviews)):
            if (reviews.loc[i, "reviewTimeInMonth"] <= 6):
                sentiment_count = sentiment_count + 1
                sentiment_sum = sentiment_sum + reviews.loc[i, "sentiment_score"]
        if (sentiment_count == 0):
            sentiment_count = sentiment_count + 1
        reviews.loc[:, "sentiment_sum"] = sentiment_sum
        reviews.loc[:, "sentiment_count"] = sentiment_count
        reviews.loc[:, "review_last_12m"] = restInfo["review_last_12m"]
        reviews.loc[:, "zomato_vintage"] = restInfo["zomato_vintage"]
        reviews.loc[:, "rest_id"] = restInfo["restId"]
        avg_score = (sentiment_sum / sentiment_count)
        if (sentiment_count <= 5):
            avg_score = 1
        #Calcualte mortality score acording to formula
        logit = -1.7483 - 0.0061 * restInfo["review_last_12m"] - 0.0136 * \
                restInfo["zomato_vintage"] + 1.1298 * avg_score
        mortality_score = math.exp(logit) / (1 + math.exp(logit))
        reviews.loc[:, "mortality_score"] = mortality_score
        #calculate band in which mortality score lies
        reviews.loc[:, 'band_10m'] = np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[0][0], MORTALITY_BAND_RANGE[0][1]),
                "1",np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[1][0], MORTALITY_BAND_RANGE[1][1]),
                "2", np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[2][0], MORTALITY_BAND_RANGE[2][1]),
                "3",np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[3][0], MORTALITY_BAND_RANGE[3][1]),
                "4", np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[4][0], MORTALITY_BAND_RANGE[4][1]),
                "5", np.where(reviews["mortality_score"].between(MORTALITY_BAND_RANGE[5][0], MORTALITY_BAND_RANGE[5][1]),
                "6",np.where(reviews['mortality_score'].between(MORTALITY_BAND_RANGE[6][0], MORTALITY_BAND_RANGE[6][1]),
                "7",np.where(reviews['mortality_score'].between(MORTALITY_BAND_RANGE[7][0], MORTALITY_BAND_RANGE[7][1]),
                "8",np.where(reviews['mortality_score'].between(MORTALITY_BAND_RANGE[8][0], MORTALITY_BAND_RANGE[8][1]),
                "9",np.where(reviews['mortality_score'].between(MORTALITY_BAND_RANGE[9][0], MORTALITY_BAND_RANGE[9][1]),
                "10","NA"))))))))))
        return reviews.loc[0,'band_10m']
