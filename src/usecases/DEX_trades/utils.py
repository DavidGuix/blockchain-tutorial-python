import requests
import pandas as pd

import typing
import time
import logging

""" import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                   ) """

MAX_NUM_OF_RECORDS_PER_REQUEST: int = (
    5000  # At October 2022, cannot be more than 25.000 (Bitquery)
)
BITQUERY_API_REQUESTS_PER_SECOND: float = 10.0 / 60.0

LAST_RUN_QUERY_TIMESTAMP: typing.Optional[float] = None  # global variable


def run_query(
    query: str, api_key: str
) -> typing.Optional[typing.Dict[str, typing.Any]]:
    global LAST_RUN_QUERY_TIMESTAMP
    if LAST_RUN_QUERY_TIMESTAMP is not None:
        sleep_between_bitquery_requests(LAST_RUN_QUERY_TIMESTAMP)
    LAST_RUN_QUERY_TIMESTAMP = time.time()

    headers = {"X-API-KEY": api_key}
    request = requests.post(
        "https://graphql.bitquery.io/",
        json={"query": query},
        headers=headers,
    )
    if request.status_code == 200:
        return request.json()  # could be None
    else:
        return {"error": {"status_code": request.status_code}}


def sleep_between_bitquery_requests(last_query_timestamp: float) -> None:
    time_to_sleep = 1.0 / BITQUERY_API_REQUESTS_PER_SECOND - (
        time.time() - last_query_timestamp
    )
    if time_to_sleep > 0:
        if time_to_sleep > 1:
            logging.warn(
                "        - Waiting for {} seconds until next request to the Bitquery Api due to free plan limits.".format(
                    round(time_to_sleep, 1)
                )
            )
        time.sleep(time_to_sleep)


def get_dextrades_protocols_by_date_range_df(
    api_key: str, start_date_str: str, end_date_str: str
) -> pd.DataFrame:
    query = """
        query CountDexTradesByProtocol {
                ethereum(network: ethereum) {
                    dexTrades {
                        count(date: {since: "%s", till: "%s"})
                        protocol
                    }
                }
            }
        """ % (
        start_date_str,
        end_date_str,
    )
    response = run_query(query, api_key)
    if response is not None and (
        "data" in response
        and "ethereum" in response["data"]
        and "dexTrades" in response["data"]["ethereum"]
    ):
        return pd.json_normalize(response["data"]["ethereum"]["dexTrades"])
    else:
        raise RuntimeError(
            "Unexpected response from bitquery. Please, try again it later."
        )


def get_query(
    limit: int,
    offset: int,
    start_date: str,
    end_date: str,
    taker_addresses: typing.List[str] = [],
    protocol: typing.Optional[str] = None,
) -> str:
    taker_query_line = ""
    if len(taker_addresses) > 0:
        addresses_list_str = f"{taker_addresses}"
        addresses_list_str = addresses_list_str.replace("'", '"')
        taker_query_line = "taker: {in: %s}" % (addresses_list_str)

    protocol_query_line = ""
    if protocol is not None:
        protocol_query_line = 'protocol: {is: "%s"}' % (protocol)

    query = """{
      ethereum(network: ethereum) {
        dexTrades(
          options: {limit: %d, offset: %d, asc: "timeInterval.second"}
          %s
          date: {since: "%s", till: "%s"}
          %s
        ) {
          protocol
          buyCurrency {
            address
            symbol
          }
          sellCurrency {
            address
            symbol
          }
          transaction {
            hash
            gasValue
            txFrom {
              address
            }
          }
          buyAmount
          sellAmount
          timeInterval {    
            second        
          }
         tradeAmount(in: USD)
        }
      }
    }""" % (
        limit,
        offset,
        protocol_query_line,
        start_date,
        end_date,
        taker_query_line,
    )

    return query


def build_dataset_from_protocol_and_dates(
    api_key: str,
    protocol: typing.Optional[str],
    start_date: str,
    end_date: str,
    max_iterations: int,
    page_size: int,
    taker_addresses: typing.List[str],
) -> pd.DataFrame:
    # start_date and end_date must have the Y-m-d format.
    logging.info(
        f"Retrieving DEX transactions for protocol {protocol}, from {start_date} to {end_date}..."
        if protocol is not None
        else f"Retrieving DEX transactions all available protocols, from {start_date} to {end_date}..."
    )

    def log_unexpected_response(
        msg: str, iteration: int, max_iterations: int = max_iterations
    ) -> None:
        logging.warn(
            f"    * Unexpected response json for iteration {iteration}: {msg}. Some DEX trades will be missing in the final DataFrame."
        )
        if i % 2 == 0:
            logging.info(
                "    * Iteration {} out of {} (estimated) finished.".format(
                    i, max_iterations
                )
            )

    df = pd.DataFrame()
    i = 0
    while i < max_iterations:
        offset = i * page_size + 1 if i != 0 else 0
        if protocol is None:
            query = get_query(
                page_size, offset, start_date, end_date, taker_addresses=taker_addresses
            )
        else:
            query = get_query(
                page_size,
                offset,
                start_date,
                end_date,
                taker_addresses=taker_addresses,
                protocol=protocol,
            )

        data = run_query(query, api_key)
        i += 1

        if data is None:
            log_unexpected_response("query response is None", i)
            continue
        else:
            if "data" not in data:
                log_unexpected_response(
                    f"`data` key is not present in the query response json. Received '{data}'",
                    i,
                )
                continue
            elif data["data"] is None:
                log_unexpected_response("`response['data']` is None", i)
                continue
            elif "ethereum" not in data["data"]:
                log_unexpected_response(
                    f"`ethereum` key is not present in `response['data']`. Received '{data}'",
                    i,
                )
                continue
            elif data["data"]["ethereum"] is None:
                log_unexpected_response("`response['data']['ethereum']` is None", i)
                continue
            elif "dexTrades" not in data["data"]["ethereum"]:
                log_unexpected_response(
                    f"`dexTrades` key is not present in `response['data']['ethereum']`.  Received '{data}'",
                    i,
                )
                continue
            elif data["data"]["ethereum"]["dexTrades"] is None:
                log_unexpected_response(
                    "`response['data']['ethereum']['dexTrades]` is None", i
                )
                continue
            elif not hasattr(data["data"]["ethereum"]["dexTrades"], "__len__"):
                dex_trades = data["data"]["ethereum"]["dexTrades"]
                log_unexpected_response(
                    f"`response['data']['ethereum']['dexTrades]` was expected to be a list but got '{dex_trades}' of type '{type(dex_trades)}'",
                    i,
                )
                continue

        if len(data["data"]["ethereum"]["dexTrades"]) == 0:
            break
        else:
            try:
                df_i = pd.json_normalize(data["data"]["ethereum"]["dexTrades"])
                df = pd.concat([df, df_i])
            except Exception as e:
                logging.warn(
                    (
                        f"    * In iteration {i}, could not convert `response['data']['ethereum']['dexTrades']` to DataFrame."
                        f" Some DEX trades will be missing in the final DataFrame. Error: {e}"
                    )
                )

        if i % 2 == 0:
            logging.info(
                "    * Iteration {} out of {} (estimated) finished.".format(
                    i, max_iterations
                )
            )

    logging.info("    Finished in {} iterations.".format(i))

    return df
