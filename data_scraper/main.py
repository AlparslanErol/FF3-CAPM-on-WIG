import pandas as pd
from .utils.utils import get_wig_list


def main(args=None):
    # megde dataset
    wig_stocks = pd.read_csv("./data_scraper/output/wig_stocks.csv")
    wig_df = pd.read_csv("./data_scraper/output/wig_df.csv")
    wig_list = get_wig_list()
    wig_data_clean = pd.read_csv("./data_scraper/output/wig_data.csv")

    final_df = wig_stocks.merge(wig_df, how="inner", on="period", suffixes=("", "_wig"))
    final_df = pd.merge(
        final_df, wig_list, how="inner", left_on=["Ticker"], right_on=["Ticker"]
    )
    final_df = pd.merge(
        final_df,
        wig_data_clean,
        how="inner",
        left_on=["Nazwa", "period"],
        right_on=["symbol", "Date"],
    )
    final_df.to_csv("./data_scraper/output/final_data/final_df_long.csv", index=False)

    final_df_sorted = final_df.loc[
        final_df["Currency"] == "PLN",
    ]
    final_df_sorted.loc[final_df_sorted["Assets"] == 0, "Assets"] = None
    final_df_sorted.dropna(inplace=True)

    final_df_short = final_df_sorted.loc[
        :,
        [
            "Ticker",
            "period",
            "close",
            "perc_change",
            "close_wig",
            "perc_change_wig",
            "Assets",
            "Number of shares",
        ],
    ]
    final_df_short.to_csv(
        "./data_scraper/output/final_data/final_df_short_ret.csv", index=False
    )

    miss_data = ["BNP"]
    final_df_short = final_df_short.loc[
        -final_df_short["Ticker"].isin(miss_data),
    ]
    final_df_short.to_csv(
        "./data_scraper/output/final_data/final_df_short_ret_clean.csv",
        index=False,
    )


if __name__ == "__main__":
    main()
