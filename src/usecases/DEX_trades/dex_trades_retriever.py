import typing

import pandas as pd
import datetime
import pytz
import logging

from . import utils


# If at some point more protocols are created, we can use the following code to retrieve
# all unique protocols and update the PROTOCOLS values:

# def get_all_dextrades_protocols_df(api_key: str) -> pd.DataFrame:
#     query = """
#     query AllProtocolsFromAnyTransaction {
#           ethereum {
#             dexTrades {
#               protocol
#               count
#             }
#           }
#         }
#     """
#     response = utils.run_query(query, api_key)
#     return pd.json_normalize(response["data"]["ethereum"]["dexTrades"])
# protocols_df = get_all_dextrades_protocols_df("<insert a Bitquery api_key here>")
# protocols = protocols_df.protocol.values # variable containing all unique protocols


PROTOCOLS = typing.Literal[
    "AXNET",
    "AirSwap Exchange",
    "AirSwap v2",
    "Balancer Pool Token",
    "Bancor Network",
    "Bancor Network v2",
    "Cofix",
    "Curve",
    "DDEX Hydro v1.0",
    "DDEX Hydro v1.1",
    "DUBIex",
    "Dodo",
    "ETHERCExchange",
    "EtherDelta",
    "Ethfinex",
    "FEGex",
    "FEGex v0",
    "IDEX",
    "IDEX v2",
    "Kyber Network",
    "Kyber Network v2",
    "Kyber Network v3",
    "Kyber Network v4",
    "Matching Market",
    "Mooniswap",
    "One Inch Liquidity Pool",
    "Smart DeFi",
    "Token.Store",
    "Uniswap",
    "Uniswap v2",
    "Uniswap v3",
    "Zerox Exchange",
    "Zerox Exchange v2",
    "Zerox Exchange v3",
    "Zerox Exchange v4",
    "dYdX2",
    "dex.blue",
]


class DexTradesOutputDict(typing.TypedDict):
    DEX_Trades: pd.DataFrame
    ProtocolDexTrCounts: pd.DataFrame


class DEXTradesRetriever:
    api_key: str
    protocols: typing.Optional[typing.List[PROTOCOLS]]
    start_date: datetime.datetime
    end_date: datetime.datetime

    def __init__(
        self,
        api_key: str,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        protocols: typing.Optional[typing.List[PROTOCOLS]] = None,
        wallet_addresses: typing.List[str] = [],
    ):
        super().__init__()
        self.api_key = api_key
        self.protocols = protocols

        self.start_date = start_date
        self.end_date = end_date

        self.wallet_addresses = wallet_addresses

        if self.end_date.timestamp() < self.start_date.timestamp():
            logging.error(f"end_date must be greater than start_date")
            logging.error(
                f"end_date: {datetime.datetime.fromtimestamp(self.end_date.timestamp(),pytz.utc).isoformat()}"
            )
            logging.error(
                f"start_date: {datetime.datetime.fromtimestamp(self.start_date.timestamp(),pytz.utc).isoformat()}"
            )
            raise ValueError("end_date must be greater than start_date")

    def _get_df_if_protocols_is_none(
        self,
        start_date_str: str,
        end_date_str: str,
        max_iterations: int,
        wallet_addresses: typing.List[str],
    ) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            df = utils.build_dataset_from_protocol_and_dates(
                self.api_key,
                None,
                start_date_str,
                end_date_str,
                max_iterations,
                utils.MAX_NUM_OF_RECORDS_PER_REQUEST,
                wallet_addresses,
            )
            if df.shape[0] == 0:
                logging.info(
                    f" * No DEX trades found for dates between '{start_date_str}' and '{end_date_str}'."
                )
        except Exception as e:
            logging.warn(
                f" * An error occurred when retrieving dex transactions. Error: {e}."
            )
        return df

    def _get_df_if_protocols_is_not_none(
        self,
        start_date_str: str,
        end_date_str: str,
        max_protocol_iterations_dict: dict,
        protocols: typing.List[PROTOCOLS],
        wallet_addresses: typing.List[str],
    ) -> pd.DataFrame:
        df = pd.DataFrame()
        for protocol in protocols:
            try:
                df_protocol = utils.build_dataset_from_protocol_and_dates(
                    self.api_key,
                    protocol,
                    start_date_str,
                    end_date_str,
                    max_protocol_iterations_dict[protocol],
                    utils.MAX_NUM_OF_RECORDS_PER_REQUEST,
                    wallet_addresses,
                )
                if df_protocol.shape == (0, 0):
                    logging.info(
                        f" * No DEX trades found for protocol '{protocol}' between '{start_date_str}' and '{end_date_str}'."
                    )
            except Exception as e:
                df_protocol = pd.DataFrame()
                logging.warn(
                    f" * An error occurred when retrieving dex transactions for protocol {protocol}, it will not be included in the output DataFrame. Error: {e}."
                )

            df = df.append(df_protocol)
        return df

    def transform(self) -> DexTradesOutputDict:
        start_date_str = datetime.datetime.fromtimestamp(
            self.start_date.timestamp()
        ).strftime("%Y-%m-%d")
        end_date_str = datetime.datetime.fromtimestamp(
            self.end_date.timestamp()
        ).strftime("%Y-%m-%d")

        # Protocols info
        try:
            logging.info("Retrieving number of DEX transactions per protocol data...")

            protocols_df = utils.get_dextrades_protocols_by_date_range_df(
                self.api_key, start_date_str=start_date_str, end_date_str=end_date_str
            )
            protocols_df = protocols_df[["protocol", "count"]]
            protocols = protocols_df.protocol.values
            counts = protocols_df["count"].values
            protocol_to_number_of_pages_to_request_data_from_dict = dict(
                zip(
                    protocols,
                    [
                        int(count / utils.MAX_NUM_OF_RECORDS_PER_REQUEST) + 1
                        for count in counts
                    ],
                )
            )
        except Exception as e:
            raise RuntimeError(
                f"An error occurred when retrieving protocols data with the bitquery api: {e}"
            )

        # Build output dataframe iterating over protocols

        if self.protocols is None or (
            self.protocols is not None and len(self.protocols) == 0
        ):
            number_of_pages_to_request_data_from = (
                int(sum(counts) / utils.MAX_NUM_OF_RECORDS_PER_REQUEST)
            ) + 1
            df = self._get_df_if_protocols_is_none(
                start_date_str,
                end_date_str,
                number_of_pages_to_request_data_from,
                self.wallet_addresses,
            )
        else:
            df = self._get_df_if_protocols_is_not_none(
                start_date_str,
                end_date_str,
                protocol_to_number_of_pages_to_request_data_from_dict,
                self.protocols,
                self.wallet_addresses,
            )

        if "timeInterval.second" in df.columns.tolist():
            df["timeInterval.second"] = pd.to_datetime(df["timeInterval.second"])

        # Rename columns

        if df.shape[0] != 0:
            df = df.rename(
                columns={
                    "buyAmount": "bought_tokens",
                    "sellAmount": "sold_tokens",
                    "tradeAmount": "total_trade_amount_usd",
                    "buyCurrency.address": "bought_token_address",
                    "sellCurrency.address": "sold_token_address",
                    "buyCurrency.symbol": "bought_token_symbol",
                    "sellCurrency.symbol": "sold_token_symbol",
                    "transaction.hash": "transaction_hash",
                    "transaction.gasValue": "transaction_gas_value",
                    "transaction.txFrom.address": "transaction_from_address",
                    "timeInterval.second": "datetime",
                }
            )

            ordered_first_columns = [
                "transaction_from_address",
                "datetime",
                "protocol",
                "total_trade_amount_usd",
                "sold_token_symbol",
                "sold_tokens",
                "bought_tokens",
                "bought_token_symbol",
                "transaction_gas_value",
                "bought_token_address",
                "sold_token_address",
                "transaction_hash",
            ]

            df = df[
                ordered_first_columns
                + [
                    col
                    for col in df.columns.tolist()
                    if col not in ordered_first_columns
                ]
            ]

            df = df.reset_index(drop=True)
        else:
            logging.warn("Output DataFrame is empty.")

        return {
            "DEX_Trades": df,
            "ProtocolDexTrCounts": protocols_df,
        }
