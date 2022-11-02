# DEXTradesRetriever

## Description

`DEXTradesRetriever` class allows  to retrieve DEX (swap) transactions (from the ethereum network) data for a given list of protocols or for all available protocols, and between a range of dates. Additionally, an extra output DataFrame with the count of dex trades per protocol is returned in the `ProtocolDexTrCounts` output DataFrame.

At least, the following fields are obtained in the `DEX_Trades` output DataFrame:

-   `transaction_from_address`: usually the wallet address from which the swap transaction has been performed.
-   `datetime`: date of the transaction (datetime format).
-   `protocol`: transaction swap protocol (ex: `Uniswap v3`)
-   `total_trade_amount_usd`: amount of USD that quantifies the transaction.
-   `sold_token_symbol`: symbol of the token that is sold.
-   `sold_tokens`: number of sold tokens (ex: `20 SOLANA`)
-   `bought_tokens`: number of bought tokens (ex: `1 WETH`).
-   `bought_token_symbol`: symbol of the token that is bought.
-   `transaction_gas_value`: amount of gas (in ETH) wasted in the transaction (transaction fee).
-   `bought_token_address`: contract address of the bought token.
-   `sold_token_address`: contract address of the sold token.
-   `transaction_hash`: hash of the transaction.

For the `ProtocolDexTrCounts` output DataFrame, the columns are just two:

-   `protocol`: protocol name.
-   `count`: number of dex transactions, in the specified range of dates, that have been done via the given protocol.

**Note**: whether or not `wallet_addresses` parameter is specified, the `ProtocolDexTrCounts`  dataframe will contain the counts over all DEX transactions, not only transactions for the specified address, for the specified date range.

**Tip**: To convert the column `transaction_gas_value` from ETH to USD in order to know the value in USD of the gas at the time of the transactions, it is necessary to know the price of ETH in USD at the time of the transaction. 

**Warning**: When the `protocols` parameter is not specified (i.e., left empty), all available protocols at the time of running the `transform` method of the retriever will be considered. For this case, keep in mind that the running time can be huge, although specifying just a cuple of days via the `start_date` and `end_date` parameters.

## Class Parameters

-   **api_key**: Your Bitquery API key. Type: string.
-   **protocols**: Optional. List of DEX swap protocols to be considered when retrieving transactions. If not specified, all available protocols at the time of running the button will be considered. Type: list of strings.
-   **start_date**: Initial date to start retrieving dex transactions from (the specified date is included). Type: datetime.datetime object.
-   **end_date**: Final date to stop retrieving dex transactions (the specified date is included). Type: datetime.datetime object.
-   **wallet_addresses**: Optional. List of wallet addresses to retrieve DEX transactions from. Type: list of strings.
