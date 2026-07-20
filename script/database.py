import json
import os
import re
import sys
import pandas as pd


class Database:

    def __init__(self):
        # PyInstaller base path handling
        if getattr(sys, "frozen", False):
            BASE_DIR = sys._MEIPASS
        else:
            BASE_DIR = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

        csv_path = os.path.join(BASE_DIR, "Data", "clean_cutoff.csv")
        json_path = os.path.join(BASE_DIR, "Data", "alias.json")

        self.df = pd.read_csv(csv_path)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                self.alias = json.load(f)
        except Exception:
            self.alias = {}

        self.df["Search"] = self.df["Institute"].apply(self.normalize)

    # ==========================================================
    # Normalize
    # ==========================================================

    def normalize(self, text):

        text = str(text).lower()

        text = text.replace("&", "and")

        text = re.sub(r"[(),.-]", " ", text)

        text = " ".join(text.split())

        return text

    # ==========================================================
    # College Search
    # ==========================================================

    def search_colleges(self, keyword):

        keyword = keyword.strip().lower()

        if keyword in self.alias:
            keyword = self.alias[keyword]

        keyword = self.normalize(keyword)

        result = self.df[
            self.df["Search"].str.contains(keyword, na=False)
        ]

        return sorted(
            result["Institute"]
            .drop_duplicates()
            .tolist()
        )

    # ==========================================================
    # All Colleges
    # ==========================================================

    def get_colleges(self):

        return sorted(
            self.df["Institute"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

    # ==========================================================
    # Quotas
    # ==========================================================

    def get_quotas(self, college):

        df = self.df[
            self.df["Institute"] == college
        ]

        return sorted(
            df["Quota"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

    # ==========================================================
    # Categories
    # ==========================================================

    def get_categories(self, college, quota):

        df = self.df[
            (self.df["Institute"] == college) &
            (self.df["Quota"] == quota)
        ]

        return sorted(
            df["Category"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

    # ==========================================================
    # Seat Gender
    # ==========================================================

    def get_genders(self, college, quota, category):

        df = self.df[
            (self.df["Institute"] == college) &
            (self.df["Quota"] == quota) &
            (self.df["Category"] == category)
        ]

        return sorted(
            df["Seat Gender"]
            .dropna()
            .drop_duplicates()
            .tolist()
        )

    # ==========================================================
    # Pivot Cutoff Table
    # ==========================================================

    def search(self, college, quota, category, gender):

        df = self.df[
            (self.df["Institute"] == college) &
            (self.df["Quota"] == quota) &
            (self.df["Category"] == category) &
            (self.df["Seat Gender"] == gender)
        ]

        if df.empty:
            return df

        pivot = pd.pivot_table(
            df,
            index="Program",
            columns="Round",
            values="Closing Rank",
            aggfunc="first"
        )

        pivot = pivot.fillna("-")

        pivot.reset_index(inplace=True)

        return pivot