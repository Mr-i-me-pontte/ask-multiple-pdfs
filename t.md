# NovaDAX API

Welcome to the NovaDAX API
--------------------------

NovaDAX provides a series of API documents aiming to deliver a faster, more secure and professional trading experience
to customers. You can use our API to access all market data, trading, order history and account management endpoints.

NovaDAX API endpoints can be accessed by customers in an easy and practical way and we are optimizing our SDK
continuously.


Get One Supported Trading Symbol
--------------------------------

This endpoint returns one NovaDAX's supported trading symbol

> Response Body

```
{
    "code": "A10000",
    "data": {
        "symbol": "BTC_BRL",
        "baseCurrency": "BTC",
        "quoteCurrency": "BRL",
        "amountPrecision": 4,
        "pricePrecision": 2,
        "valuePrecision": 4,
        "minOrderAmount": "0.001",
        "minOrderValue": "5"
    },
    "message": "Success"
}

```

### Request URL

`GET /v1/common/symbol`

### Weight: 1

### Request Parameter

| Field  | Mandatory | Data Type | Description    |
|--------|-----------|-----------|----------------|
| symbol | true      | string    | Trading symbol |

### Response Details

| Field           | Data Type | Description                        |
|-----------------|-----------|------------------------------------|
| symbol          | string    | Trading symbol                     |
| baseCurrency    | string    | Base currency in a trading symbol  |
| quoteCurrency   | string    | Quote currency in a trading symbol |
| pricePrecision  | number    | Price precision                    |
| amountPrecision | number    | Amount precision                   |
| valuePrecision  | number    | Value precision                    |
| minOrderAmount  | string    | Minimum order amount               |
| minOrderValue   | string    | Minimum order value                |

Get All Supported Trading Symbol
--------------------------------

This endpoint returns all NovaDAX's supported trading symbols

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "symbol": "BTC_BRL",
            "baseCurrency": "BTC",
            "quoteCurrency": "BRL",
            "amountPrecision": 4,
            "pricePrecision": 2,
            "valuePrecision": 4,
            "minOrderAmount": "0.001",
            "minOrderValue": "5",
        },
        {
            "symbol": "ETH_BRL",
            "baseCurrency": "ETH",
            "quoteCurrency": "BRL",
            "amountPrecision": 4,
            "pricePrecision": 2,
            "valuePrecision": 4,
            "minOrderAmount": "0.01",
            "minOrderValue": "5"
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/common/symbols`

### Weight: 1

### Request Parameters

No parameter is needed for this endpoint.

### Response Details

| Field           | Data Type | Description                        |
|-----------------|-----------|------------------------------------|
| symbol          | string    | Trading symbol                     |
| baseCurrency    | string    | Base currency in a trading symbol  |
| quoteCurrency   | string    | Quote currency in a trading symbol |
| pricePrecision  | number    | Price precision                    |
| amountPrecision | number    | Amount precision                   |
| valuePrecision  | number    | Value precision                    |
| minOrderAmount  | string    | Minimum order amount               |
| minOrderValue   | string    | Minimum order value                |

Get Current System Time
-----------------------

This endpoint returns the current system time in milliseconds adjusted to UTC time zone.

> Response Body

```
{
    "code": "A10000",
    "data": 1565080348983,
    "message": "Success"
}

```

### Request URL

`GET /v1/common/timestamp`

### Weight: 1

### Request Parameters

No parameter is needed for this endpoint.

### Response Details

System time milliseconds adjusted to UTC time zone.

Get Latest Tickers for All Trading Pairs
----------------------------------------

This endpoint returns the latest ticker for all supported trading pairs with important 24h aggregated market data.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "ask": "34708.15",
            "baseVolume24h": "34.08241488",
            "bid": "34621.74",
            "high24h": "35079.77",
            "lastPrice": "34669.81",
            "low24h": "34330.64",
            "open24h": "34492.08",
            "quoteVolume24h": "1182480.09502814",
            "symbol": "BTC_BRL",
            "timestamp": 1571112216346
        }
    ],
    "message": "Success"
}


```

### Request URL

`GET /v1/market/tickers`

### Weight: 5

### Request Parameters

No parameters are needed for this endpoint.

### Response Details

| Field          | Data Type | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| symbol         | string    | Trading symbol                                        |
| lastPrice      | string    | The price of last trade                               |
| bid            | string    | The current best bid price                            |
| ask            | string    | The current best ask price                            |
| open24h        | string    | The opening price of last 24 hours                    |
| high24h        | string    | The highest price of last 24 hours                    |
| low24h         | string    | The lowest price of last 24 hours                     |
| baseVolume24h  | string    | The trading volume in base currency of last 24 hours  |
| quoteVolume24h | string    | The trading volume of quote currency of last 24 hours |
| timestamp      | number    | The current system time in UTC time zone              |

Get Latest Ticker for Specific Pair
-----------------------------------

The endpoint retrieves the latest ticker of a specific trading pair.

> Response Body

```
{
    "code": "A10000",
    "data": {
        "ask": "34708.15",
        "baseVolume24h": "34.08241488",
        "bid": "34621.74",
        "high24h": "35079.77",
        "lastPrice": "34669.81",
        "low24h": "34330.64",
        "open24h": "34492.08",
        "quoteVolume24h": "1182480.09502814",
        "symbol": "BTC_BRL",
        "timestamp": 1571112216346
    },
    "message": "Success"
}

```

### Request URL

`GET /v1/market/ticker`

### Weight: 1

### Request Parameter

| Field  | Mandatory | Data Type | Description    |
|--------|-----------|-----------|----------------|
| symbol | true      | string    | Trading symbol |

### Response Details

| Field          | Data Type | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| symbol         | string    | Trading symbol                                        |
| lastPrice      | string    | The price of last trade                               |
| bid            | string    | The current best bid price                            |
| ask            | string    | The current best ask price                            |
| open24h        | string    | The opening price of last 24 hours                    |
| high24h        | string    | The highest price of last 24 hours                    |
| low24h         | string    | The lowest price of last 24 hours                     |
| baseVolume24h  | string    | The trading volume in base currency of last 24 hours  |
| quoteVolume24h | string    | The trading volume of quote currency of last 24 hours |
| timestamp      | number    | The current system time in UTC time zone              |

Get Market Depth
----------------

This endpoint retrieves the current order book of a specific pair.

> Response Body

```
{
    "code": "A10000",
    "data": {
        "asks": [
            ["43687.16", "0.5194"],
            ["43687.2", "1.3129"]
        ],
        "bids": [
            ["43657.57", "0.6135"],
            ["43657.46", "0.0559"]
        ],
        "timestamp": 1565057338020
    },
    "message": "Success"
}

```

### Request URL

`GET /v1/market/depth`

### Weight: 1

### Request Parameters

| Field  | Mandatory | Data Type | Description                                    |
|--------|-----------|-----------|------------------------------------------------|
| symbol | true      | string    | Trading symbol                                 |
| limit  | false     | number    | The number of asks and bids to return , max 50 |

### Response Details

| Field     | Data Type | Description                              |
|-----------|-----------|------------------------------------------|
| asks      | array     | All current asks                         |
| asks[][0] | string    | Sell price                               |
| asks[][1] | string    | Sell amount                              |
| bids      | array     | All current bids                         |
| bids[][0] | string    | Buy price                                |
| bids[][1] | string    | Buy amount                               |
| timestamp | number    | The current system time in UTC time zone |

Get Recent Trades
-----------------

This endpoint returns most recent trades data.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "price": "43657.57",
            "amount": "1",
            "side": "SELL",
            "timestamp": 1565007823401
        },
        {
            "price": "43687.16",
            "amount": "0.071",
            "side": "BUY",
            "timestamp": 1565007198261
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/market/trades`

### Weight: 5

### Request Parameters

| Field  | Mandatory | Data Type | Description                                  |
|--------|-----------|-----------|----------------------------------------------|
| symbol | true      | string    | Trading symbol                               |
| limit  | false     | number    | The number of trades to return , default 100 |

### Response Details

| Field     | Data Type | Description                         |
|-----------|-----------|-------------------------------------|
| price     | string    | The trading price                   |
| amount    | string    | The trading volume                  |
| side      | string    | The trading direction (SELL or BUY) |
| timestamp | number    | The time when the trade occurred    |

Get Kline Data
--------------

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "amount": 8.25709100,
            "closePrice": 62553.20,
            "count": 29,
            "highPrice": 62592.87,
            "lowPrice": 62553.20,
            "openPrice": 62554.23,
            "score": 1602501480,
            "symbol": "BTC_BRL",
            "vol": 516784.2504067500
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/market/kline/history`

### Weight: 5

### Request Parameters

| Field  | Mandatory | Data Type | Description                                                             |
|--------|-----------|-----------|-------------------------------------------------------------------------|
| symbol | true      | string    | Trading symbol                                                          |
| unit   | true      | string    | ONE_MIN,FIVE_MIN, FIFTEEN_MIN,HALF_HOU,ONE_HOU,ONE_DAY,ONE_WEE,ONE_MON; |
| from   | true      | number    | The start time  All time units only save the latest 3000 data           |
| to     | true      | number    | The end time   All time units only save the latest 3000 data            |
|        |           |           |                                                                         |

### Response Details

| Field      | Data Type | Description          |
|------------|-----------|----------------------|
| unit       | string    | Time unit            |
| amount     | string    | The trading amount   |
| count      | string    | The trading count    |
| openPrice  | string    | The open Price       |
| closePrice | string    | The close Price      |
| highPrice  | string    | The high Price       |
| lowPrice   | string    | The low Price        |
| symbol     | string    | The  trading  symbol |
| score      | string    | The time             |
| vol        | string    | The trading volume   |

Order Introduction
------------------

#### Order type(order.type)

* **LIMIT**: Limit order
* **MARKET**: Market order
* **STOP\_LIMIT**: The order will be put into matching queue at limit price only when the market price reaches the
  trigger price.
* **STOP\_MARKET**: The order will be put into matching queue at market price only when the market price reaches the
  trigger price.

#### Operator of stop order （order.operator）

* **GTE**: More than or equal to
* **LTE**: Less than or equal to

#### Order direction(order.side)

* **BUY**: Buy
* **SELL**: Sell

#### Order status(order.status)

* **SUBMITTED**: The order has been submitted but not processed, not in the matching queue yet. The order is unfinished.
* **PROCESSING**: The order has been submitted and is in the matching queue, waiting for deal. The order is unfinished.
* **PARTIAL\_FILLED**: The order is already in the matching queue and partially traded, and is waiting for further
  matching and trade. The order is unfinished
* **PARTIAL\_CANCELED**: The order has been partially traded and canceled by the user and is no longer in the matching
  queue. This order is finished.
* **PARTIAL\_REJECTED**: The order has been rejected by the system after being partially traded. Now it is finished and
  no longer in the matching queue.
* **FILLED**: This order has been completely traded, finished and no longer in the matching queue.
* **CANCELED**: This order has been canceled by the user before being traded. It is finished now and no longer in the
  matching queue.
* **REJECTED**: This order has been rejected by the user before being traded. It is finished now and no longer in the
  matching queue.
* **CANCELING**: This order is being canceled, but it is unfinished at the moment and still in the matching queue.

#### Order’s role(order.role)

* **MAKER**: Brings liquidity
* **TAKER**: Takes liquidity

Place A New Order
-----------------

This endpoint places a new order and submits it to the exchange to be matched.

> Response Body

```
{
    "code": "A10000",
    "data": {
        "id": "633679992971251712",
        "clientOrderId": "client_order_id_123456",
        "symbol": "BTC_BRL",
        "type": "MARKET",
        "side": "SELL",
        "price": null,
        "averagePrice": "0",
        "amount": "0.123",
        "filledAmount": "0",
        "value": null,
        "filledValue": "0",
        "filledFee": "0",
        "stopPrice": null,
        "operator": null,
        "status": "REJECTED",
        "timestamp": 1565165945588
    },
    "message": "Success"
}

```

### Request URL

`POST /v1/orders/create`

### Weight: 5

### Request Parameters

* Field: clientOrderId
    * Mandatory: false
    * Data Type: string
    * Description: Customer-customized unique order ID, not exceeding 30 characters in length.
* Field: symbol
    * Mandatory: true
    * Data Type: string
    * Description: The trading symbol to trade, like BTC_BRL
* Field: type
    * Mandatory: true
    * Data Type: string
    * Description: The type of order, single option: LIMIT
* Field: side
    * Mandatory: true
    * Data Type: string
    * Description: The direction of order, single option: BUY
* Field: price
    * Mandatory: true
    * Data Type: string
    * Description: Buy price
* Field: amount
    * Mandatory: true
    * Data Type: string
    * Description: The amount of base currency, like BTC amount for buy of BTC_BRL
* Field: value
    * Mandatory: true
    * Data Type: string
    * Description: The amount of quote currency, like BRL amount for buy of BTC_BRL
* Field: operator
    * Mandatory: true
    * Data Type: string
    * Description: Operator of stop order, can be found in order introduction
* Field: stopPrice
    * Mandatory: true
    * Data Type: string
    * Description: Stop price

Based on the order type and side, certain parameters are required to be enforced:

| type + side      | Required Parameters             |
|------------------|---------------------------------|
| LIMIT BUY        | price,amount                    |
| LIMIT SELL       | price,amount                    |
| MARKET BUY       | value                           |
| MARKET SELL      | amount                          |
| STOP_LIMIT BUY   | price,amount,operator,stopPrice |
| STOP_LIMIT SELL  | price,amount,operator,stopPrice |
| STOP_MARKET BUY  | value,operator,stopPrice        |
| STOP_MARKET SELL | amount,operator,stopPrice       |

### Response Details

| Field         | Data Type | Description                                             |
|---------------|-----------|---------------------------------------------------------|
| id            | string    | Order ID                                                |
| clientOrderId | string    | Customer-customized unique order ID                     |
| symbol        | string    | The trading symbol                                      |
| type          | string    | The type of order                                       |
| side          | string    | The direction of order                                  |
| price         | string    | The price of order                                      |
| averagePrice  | string    | The average price of order                              |
| amount        | string    | The amount of base currency                             |
| filledAmount  | string    | The executed amount of base currency                    |
| value         | string    | The amount of quote currency                            |
| filledValue   | string    | The executed amount of quote currency                   |
| filledFee     | string    | Transaction fee paid                                    |
| status        | string    | The status of order, can be found in order introduction |
| timestamp     | number    | The time when the order was created                     |

Bulk Place Orders
-----------------

Batch create new orders, supporting the simultaneous submission of up to 20 orders at a time.

> Response Body

```
{
    "code": "A10000",
    "data": [{
        "id": "633679992971251712",
        "clientOrderId": "client_order_id_123456",
        "symbol": "BTC_BRL",
        "type": "MARKET",
        "side": "SELL",
        "price": null,
        "averagePrice": "0",
        "amount": "0.123",
        "filledAmount": "0",
        "value": null,
        "filledValue": "0",
        "filledFee": "0",
        "stopPrice": null,
        "operator": null,
        "status": "REJECTED",
        "timestamp": 1565165945588
    }, {
        "clientOrderId": "client_order_id_123456",
        "code": "A10001",
        "message": "Params error"
    }],
    "message": "Success"
}

```

### Request URL

`POST /v1/orders/batch-create`

### Weight: 50

### Request Parameters

* Field: clientOrderId
    * Mandatory: false
    * Data Type: string
    * Description: Customer-customized unique order ID, not exceeding 30 characters in length.
* Field: symbol
    * Mandatory: true
    * Data Type: string
    * Description: The trading symbol to trade, like BTC_BRL
* Field: type
    * Mandatory: true
    * Data Type: string
    * Description: The type of order, single option: LIMIT
* Field: side
    * Mandatory: true
    * Data Type: string
    * Description: The direction of order, single option: BUY
* Field: price
    * Mandatory: true
    * Data Type: string
    * Description: Buy price
* Field: amount
    * Mandatory: true
    * Data Type: string
    * Description: The amount of base currency, like BTC amount for buy of BTC_BRL
* Field: value
    * Mandatory: true
    * Data Type: string
    * Description: The amount of quote currency, like BRL amount for buy of BTC_BRL
* Field: operator
    * Mandatory: true
    * Data Type: string
    * Description: Operator of stop order, can be found in order introduction
* Field: stopPrice
    * Mandatory: true
    * Data Type: string
    * Description: Stop price

Based on the order type and side, certain parameters are required to be enforced:

| type + side      | Required Parameters             |
|------------------|---------------------------------|
| LIMIT BUY        | price、amount                    |
| LIMIT SELL       | price、amount                    |
| MARKET BUY       | value                           |
| MARKET SELL      | amount                          |
| STOP_LIMIT BUY   | price、amount、operator、stopPrice |
| STOP_LIMIT SELL  | price、amount、operator、stopPrice |
| STOP_MARKET BUY  | value、operator、stopPrice        |
| STOP_MARKET SELL | amount、operator、stopPrice       |

### Response Details

| Field          | Data Type | Description                                             |
|----------------|-----------|---------------------------------------------------------|
| data           | array     | Order List                                              |
| >id            | string    | Order ID                                                |
| >clientOrderId | string    | Customer-customized unique order ID                     |
| >symbol        | string    | The trading symbol                                      |
| >type          | string    | The type of order                                       |
| >side          | string    | The direction of order                                  |
| >price         | string    | The price of order                                      |
| >averagePrice  | string    | The average price of order                              |
| >amount        | string    | The amount of base currency                             |
| >filledAmount  | string    | The executed amount of base currency                    |
| >value         | string    | The amount of quote currency                            |
| >filledValue   | string    | The executed amount of quote currency                   |
| >filledFee     | string    | Transaction fee paid                                    |
| >status        | string    | The status of order, can be found in order introduction |
| >timestamp     | number    | The time when the order was created                     |

Cancel Order ID
---------------

This endpoint submits a request to cancel an order.

> Response Body

```
{
    "code": "A10000",
    "data": {
        "result": true
    },
    "message": "Success"
}

```

### Request URL

`POST /v1/orders/cancel`

### Weight: 1

### Request Parameters

| Field         | Mandatory | Data Type | Description                         |
|---------------|-----------|-----------|-------------------------------------|
| id            | false     | string    | Order ID                            |
| clientOrderId | false     | string    | Customer-customized unique order ID |

### Response Details

| Field  | Data Type | Description                      |
|--------|-----------|----------------------------------|
| result | string    | The result of the cancel request |

Bulk Cancel Orders by ID
------------------------

Batch submission of order cancellation requests, supporting up to 20 orders to be submitted simultaneously.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "id": "608695623247466496",
            "result": true,
            "code": "A10000",
            "message": "Success"
        },
        {
            "clientOrderId": "client_order_id_123457",
            "result": true,
            "code": "A10000",
            "message": "Success"
        },
        {
            "clientOrderId": "client_order_id_123458",
            "result": false,
            "code": "A30001",
            "message": "Order not found",
        }
    ],
    "message": "Success"
}

```

### Request URL

`POST /v1/orders/batch-cancel`

### Weight: 10

### Request Parameters

| Field          | Mandatory | Data Type | Description                         |
|----------------|-----------|-----------|-------------------------------------|
| >id            | false     | string    | 订单ID                                |
| >clientOrderId | false     | string    | Customer-customized unique order ID |

### Response Details

| Field          | Data Type | Description                         |
|----------------|-----------|-------------------------------------|
| data           | array     | Canceled Order List                 |
| >id            | string    | Order ID                            |
| >clientOrderId | string    | Customer-customized unique order ID |
| >result        | boolean   | The result of the cancel request    |

Cancel order by symbol
----------------------

Cancel order based on trading symbol.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "id": "608695623247466496",
            "clientOrderId": "client_order_id_123456",
            "result": true,
            "code": "A10000",
            "message": "Success"
        },
        {
            "id": "608695623247466497",
            "clientOrderId": "client_order_id_123457",
            "result": true,
            "code": "A10000",
            "message": "Success"
        }
    ],
    "message": "Success"
}

```

### Request URL

`POST /v1/orders/cancel-by-symbol`

### Weight: 10

### Request Parameters

| Field  | Mandatory | Data Type | Description                               |
|--------|-----------|-----------|-------------------------------------------|
| symbol | true      | string    | The trading symbol to trade, like BTC_BRL |

### Response Details

| Field          | Data Type | Description                         |
|----------------|-----------|-------------------------------------|
| data           | array     | Canceled Order List                 |
| >id            | string    | Order ID                            |
| >clientOrderId | string    | Customer-customized unique order ID |
| >result        | boolean   | The result of the cancel request    |

Get Order Details
-----------------

This endpoint returns the latest status and details of an order. Orders created through API cannot be found after being
cancelled for two hours.

> Response Body

```
{
    "code": "A10000",
    "data": {
        "id": "608695623247466496",
        "clientOrderId": "client_order_id_123456",
        "symbol": "BTC_BRL",
        "type": "MARKET",
        "side": "SELL",
        "price": null,
        "averagePrice": "0",
        "amount": "0.123",
        "filledAmount": "0",
        "value": null,
        "filledValue": "0",
        "filledFee": "0",
        "stopPrice": null,
        "operator": null,
        "status": "REJECTED",
        "timestamp": 1565165945588
    },
    "message": "Success"
}

```

### Request URL

`GET /v1/orders/get`

### Weight: 1

### Request Parameters

| Field         | Mandatory | Data Type | Description                         |
|---------------|-----------|-----------|-------------------------------------|
| id            | false     | string    | Order ID                            |
| clientOrderId | false     | string    | Customer-customized unique order ID |

### Response Details

| Field         | Data Type | Description                                             |
|---------------|-----------|---------------------------------------------------------|
| id            | string    | Order ID                                                |
| clientOrderId | string    | Customer-customized unique order ID                     |
| symbol        | string    | The trading symbol                                      |
| type          | string    | The type of order                                       |
| side          | string    | The direction of order                                  |
| price         | string    | The price of order                                      |
| averagePrice  | string    | The average price of order                              |
| amount        | string    | The amount of base currency                             |
| filledAmount  | string    | The executed amount of base currency                    |
| value         | string    | The amount of quote currency                            |
| filledValue   | string    | The executed amount of quote currency                   |
| filledFee     | string    | Transaction fee paid                                    |
| status        | string    | The status of order, can be found in order introduction |
| timestamp     | number    | The time when the order was created                     |

Get Order History
-----------------

This endpoint returns the order history based on a certain search filter. Orders created through API cannot be found
after being cancelled for two hours.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "id": "608695678650028032",
            "clientOrderId": "client_order_id_123456",
            "symbol": "BTC_BRL",
            "type": "MARKET",
            "side": "SELL",
            "price": null,
            "averagePrice": "0",
            "amount": "0.123",
            "filledAmount": "0",
            "value": null,
            "filledValue": "0",
            "filledFee": "0",
            "stopPrice": null,
            "operator": null,
            "status": "REJECTED",
            "timestamp": 1565165958796
        },
        {
            "id": "608695623247466496",
            "clientOrderId": "client_order_id_123457",
            "symbol": "BTC_BRL",
            "type": "MARKET",
            "side": "SELL",
            "price": null,
            "averagePrice": "0",
            "amount": "0.123",
            "filledAmount": "0",
            "value": null,
            "filledValue": "0",
            "filledFee": "0",
            "stopPrice": null,
            "operator": null,
            "status": "REJECTED",
            "timestamp": 1565165945588
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/orders/list`

### Weight: 10

### Request Parameters

* Field: symbol
    * Mandatory: false
    * Data Type: string
    * Description: The trading symbol, like BTC_BRL
* Field: status
    * Mandatory: false
    * Data Type: string
    * Description: The status of orders(can be found in order introduction, use comma to separate different status). You
      can also use 'FINISHED' to find finished orders and use 'UNFINISHED' to find unfinished orders.
* Field: fromId
    * Mandatory: false
    * Data Type: string
    * Description: Search order id to begin with
* Field: toId
    * Mandatory: false
    * Data Type: string
    * Description: Search order id to end up with
* Field: fromTimestamp
    * Mandatory: false
    * Data Type: string
    * Description: Search order creation time to begin with, in milliseconds
* Field: toTimestamp
    * Mandatory: false
    * Data Type: string
    * Description: Search order creation time to end up with, in milliseconds
* Field: limit
    * Mandatory: false
    * Data Type: string
    * Description: The number of orders to return, default 100, max 100

### Response Details

| Field         | Data Type | Description                                             |
|---------------|-----------|---------------------------------------------------------|
| id            | string    | Order ID                                                |
| clientOrderId | string    | Customer-customized unique order ID                     |
| symbol        | string    | The trading symbol                                      |
| type          | string    | The type of order                                       |
| side          | string    | The direction of order                                  |
| price         | string    | The price of order                                      |
| averagePrice  | string    | The average price of order                              |
| amount        | string    | The amount of base currency                             |
| filledAmount  | string    | The executed amount of base currency                    |
| value         | string    | The amount of quote currency                            |
| filledValue   | string    | The executed amount of quote currency                   |
| filledFee     | string    | Transaction fee paid                                    |
| status        | string    | The status of order, can be found in order introduction |
| timestamp     | number    | The time when the order was created                     |

Get Order Match Details
-----------------------

This endpoint returns the match result of an order.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "id": "608717046691139584",
            "orderId": "608716957545402368",
            "symbol": "BTC_BRL",
            "side": "BUY",
            "amount": "0.0988",
            "price": "45514.76",
            "fee": "0.0000988 BTC",
            "feeAmount": "0.0000988",
            "feeCurrency": "BTC",
            "role": "MAKER",
            "timestamp": 1565171053345
        },
        {
            "id": "608717065729085441",
            "orderId": "608716957545402368",
            "symbol": "BTC_BRL",
            "side": "BUY",
            "amount": "0.0242",
            "price": "45514.76",
            "fee": "0.0000242 BTC",
            "feeAmount": "0.0000988",
            "feeCurrency": "BTC",
            "role": "MAKER",
            "timestamp": 1565171057882
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/orders/fills`

### Weight: 10

### Request Parameters

| Field         | Mandatory | Data Type | Description                                            |
|---------------|-----------|-----------|--------------------------------------------------------|
| orderId       | true      | string    | Order ID                                               |
| symbol        | false     | string    | The trading symbol, like BTC_BRL                       |
| fromId        | false     | string    | Search fill id to begin with                           |
| toId          | false     | string    | Search fill id to end up with                          |
| fromTimestamp | false     | string    | Search order fill time to begin with, in milliseconds  |
| toTimestamp   | false     | string    | Search order fill time to end up with, in milliseconds |
| limit         | false     | string    | The number of fills to return, default 100, max 100    |

### Response Details

| Field       | Data Type | Description                                    |
|-------------|-----------|------------------------------------------------|
| id          | string    | Order match ID                                 |
| orderId     | string    | Order ID                                       |
| symbol      | string    | The trading symbol                             |
| side        | string    | The direction of order, options: BUY or SELL   |
| price       | string    | The matched price                              |
| amount      | string    | The matched amount                             |
| fee         | string    | Transaction fee paid                           |
| feeCurrency | string    | Transaction fee paid currency                  |
| feeAmount   | string    | Transaction fee paid amount                    |
| role        | string    | The role of transaction，option: TAKER or MAKER |
| timestamp   | false     | string                                         |

Get Account Balance
-------------------

This endpoint returns the account balance.

> Response Body

```
{
    "code": "A10000",
    "data": [
        {
            "available": "1.23",
            "balance": "0.23",
            "currency": "BTC",
            "hold": "1"
        }
    ],
    "message": "Success"
}

```

### Request URL

`GET /v1/account/getBalance`

### Weight: 1

### Request Parameters

No parameter is needed for this endpoint

### Response Details

| Field     | Data Type | Description                  |
|-----------|-----------|------------------------------|
| currency  | string    | The currency of this balance |
| balance   | string    | The balance of this currency |
| hold      | string    | The balance in order         |
| available | string    | The available balance        |

Get Sub Account Balance
-----------------------

This endpoint returns the balance of sub account.

> Response Body

```
{
    "code":"A10000",
    "data":[
        {
            "balance":"7.22",
            "currency":"BTC"
        }
    ],
    "message":"Success"
}

```

### Request URL

`GET /v1/account/subs/balance`

### Weight: 1

### Request Parameters

| Field | Mandatory | Data Type | Description    |
|-------|-----------|-----------|----------------|
| subId | ture      | string    | Sub account ID |

### Response Details

| Field    | Data Type | Description              |
|----------|-----------|--------------------------|
| balance  | string    | Balance of sub account   |
| currency | string    | Currency of this balance |

Get Sub Account Transfer Record
-------------------------------

This endpoint returns the transfer record of sub account

> Response Body

```
{
    "code": "A10000",
    "data": [{
        "subId": "CA648855702269333504",
        "amount": "103.22",
        "currency": "BRL",
        "state": "success",
        "type": "master-transfer-out"
    }, {
        "subId": "CA648855702269333504",
        "amount": "3.5",
        "currency": "BRL",
        "state": "success",
        "type": "master-transfer-in"
    }],
    "message": "Success"
}

```

### Request URL

`GET /v1/account/subs/transfer/record`

### Weight: 10

### Request Parameters

| Field | Mandatory | Data Type | Description    |
|-------|-----------|-----------|----------------|
| subId | ture      | string    | Sub account ID |

### Response Details

* Field: subId
    * Data Type: string
    * Description: Sub account ID
* Field: amount
    * Data Type: string
    * Description: Transfer amount
* Field: currency
    * Data Type: string
    * Description: Transfer currency
* Field: state
    * Data Type: string
    * Description: Transfer state: success/fail
* Field: type
    * Data Type: string
    * Description: Type: master-transfer-in (transfer into master account) or master-transfer-out (transfer from master
      account)

Get Sub Account Transfer
------------------------

The endpoint submits a transfer request of sub account

> Response Body

```
{
  "code":"A10000",
  "message":"Success",
  "data":40
}

```

### Request URL

`POST /v1/account/subs/transfer`

### Weight: 5

### Request Parameters

| Field          | Mandatory | Data Type | Description                                    |
|----------------|-----------|-----------|------------------------------------------------|
| subId          | true      | string    | Sub account ID                                 |
| currency       | true      | string    | Transfer currency                              |
| transferAmount | true      | string    | Transfer amount                                |
| transferType   | true      | string    | Type，master-transfer-in or master-transfer-out |
|                |           |           |                                                |

### Response Details

Data field returns the transfer record ID.

Wallet Records of Deposits and Withdraws
----------------------------------------

The endpoint returns the records of deposits and withdraws.

> Response Body

```
{
    "code": "A10000",
    "data": [{
        "id": "DR562339304588709888",
        "type": "COIN_IN",
        "currency": "XLM",
        "chain": "XLM",
        "address": "GCUTK7KHPJC3ZQJ3OMWWFHAK2OXIBRD4LNZQRCCOVE7A2XOPP2K5PU5Q",
        "addressTag": "1000009",
        "amount": 1.0,
        "state": "SUCCESS",
        "txHash": "39210645748822f8d4ce673c7559aa6622e6e9cdd7073bc0fcae14b1edfda5f4",
        "createdAt": 1554113737000,
        "updatedAt": 1601371273000
    }...],
    "message": "Success"
}

```

### Request URL

`GET /v1/wallet/query/deposit-withdraw`

### Weight: 10

### Request Parameters

| Field    | Data Type | Required | Description                           | Default Value        |
|----------|-----------|----------|---------------------------------------|----------------------|
| currency | string    | false    | The currency code. e.g. BTC           | NA                   |
| type     | string    | false    | default record type to search         | coin_in and coin_out |
| direct   | string    | false    | the order of records,e.g. asc or desc | asc                  |
| size     | int       | false    | the number of iterms to return        | 100                  |
| start    | string    | false    | the id of record,                     | NA                   |

### Response Details

* Field: id
    * Data Type: string
    * Description: the id of record
* Field: type
    * Data Type: string
    * Description: the type of record
* Field: currency
    * Data Type: string
    * Description: the currency code of record
* Field: txHash
    * Data Type: string
    * Description: the txid of chain
* Field: address
    * Data Type: string
    * Description: the dst address of txHash
* Field: addressTag
    * Data Type: string
    * Description: the tag of txHash
* Field: chain
    * Data Type: string
    * Description: Block chain name,internal means transfer through novadax inside rather than chain
* Field: amount
    * Data Type: decimal
    * Description: the amount of txHash
* Field: state
    * Data Type: string
    * Description: the state of record
* Field: createdAt
    * Data Type: long
    * Description: The timestamp in milliseconds for the transfer creation
* Field: updatedAt
    * Data Type: long
    * Description: The timestamp in milliseconds for the transfer's latest update

#### List of possible record state

| State          | Description                                                  |
|----------------|--------------------------------------------------------------|
| Pending        | the record is wait broadcast to chain                        |
| x/M confirming | the comfirming state of tx,the M is total confirmings needed |
| SUCCESS        | the record is success full                                   |
| FAIL           | the record failed                                            |

Send Cryptocurrencies
---------------------

> Response Body

```
{
  "code":"A10000",
  "data": "DR123",
  "message":"Success"
}

```

### Request URL

`POST /v1/wallet/withdraw/coin`

### Weight: 600

### Request Parameters

| Field      | Mandatory | Data Type | Description                                                        |
|------------|-----------|-----------|--------------------------------------------------------------------|
| code       | ture      | string    | Crypto symbol, like BTC                                            |
| amount     | true      | string    | Amount to send                                                     |
| wallet     | true      | string    | Wallet address to receive                                          |
| chainAlias | true      | string    | Wallet address to receive with chainAlias,default nova first chain |
| tag        | false     | string    | Tag, required when sending XLM, XRP, EOS                           |

### Response Details

The data field will return the withdrawal id.

Chain Network Search
--------------------

### Request URL

`GET /crypto/chain/{code}`

### Weight: 5

### Request parameters

| parm r name | param type | param note                                |
|-------------|------------|-------------------------------------------|
| code        | String     | crypto accout code,default value is "ALL" |

### Response parameters

| param name       | param type | param note                             |
|------------------|------------|----------------------------------------|
| accountCode      | String     | code account                           |
| accountType      | String     | code account type:DIGITAL,LEGAL        |
| accountPrecision | Integer    | code account precision                 |
| accountOrder     | Integer    | code account order                     |
| accountState     | Integer    | code account state,1:in-use，0: off-use |
| tokens           | List       | crypro network List                    |

List of tokens

| parame name       | param type | param note                                                      |
|-------------------|------------|-----------------------------------------------------------------|
| codeAccount       | String     | Code account                                                    |
| chainAlias        | String     | crypto chain alias, use for send crypto                         |
| chainName         | String     | crypto chain name, just for reading                             |
| mainAddr          | String     | main address for memo crypto,default value is null              |
| useMemo           | Integer    | use memo or not,1:using，0:not using                             |
| useDynamicSendFee | String     | using dynamic sent fee,1:using，0:not using                      |
| minConf           | Integer    | min confirmations of chain                                      |
| useFirst          | Integer    | default chain choosed in novadax when chainAlias is null in api |
| state             | Integer    | chain is useful，1:in-use，0:off-use                              |
| chainURL          | String     | chain url                                                       |
| chainAddressURL   | String     | chain address url                                               |
| chainHashURL      | String     | chain hash url                                                  |
| officialURL       | String     | chain official url                                              |

Access
------

NovaDAX WebSocket API is based on Socket.io. You can find more information about Socket.io on their official website.

### Address

`wss://api.novadax.com`

```
// Socket.IO example of establishing connection
const io = require("socket.io-client");

const socket = io("wss://api.novadax.com", {
transports: ['websocket']
});

// Socket.IO example of subscription
socket.emit("SUBSCRIBE", ["MARKET.BTC_USDT.TICKER", "MARKET.BTC_USDT.TRADE"])
socket.on("MARKET.BTC_USDT.TICKER", (ticker) => {
    console.log(ticker)
})
socket.on("MARKET.BTC_USDT.TRADE", (trade) => {
    console.log(trade)
})

// Socket.IO example of cancelling subscription
socket.emit("UNSUBSCRIBE", ["MARKET.BTC_USDT.DEPTH.LEVEL0"])

```

### Limit

* Only supports `websocket` transports of Socket.io
* One IP can only establish 10 WebSocket connections

### Subscribe topics

When you subscribe a topic, you can receive all the notifications about it. Subscription format:

`socket.emit("SUBSCRIBE", ["XXX"])`

### Cancel subscription

After subscribing a topic, you can cancel the subscription if you don’t want to receive notifications about the topic
anymore. Format of canceling the subscription:

`socket.emit("UNSUBSCRIBE", ["XXX"])`

Subscribe Ticker Data of All Trading Pairs
------------------------------------------

After subscription, the system will send ticker data of all trading pairs once a second.

> Data

```
[
  {
      "ask": "34708.15",
      "baseVolume24h": "34.08241488",
      "bid": "34621.74",
      "high24h": "35079.77",
      "lastPrice": "34669.81",
      "low24h": "34330.64",
      "open24h": "34492.08",
      "quoteVolume24h": "1182480.09502814",
      "symbol": "BTC_BRL",
      "timestamp": 1571112216346
  }
]

```

### Subscription Topic

`MARKET.TICKERS`

### Request Parameters

No parameters are needed for this endpoint.

### Response Details

| Field          | Data Type | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| symbol         | string    | Trading symbol                                        |
| lastPrice      | string    | The price of last trade                               |
| bid            | string    | The current best bid price                            |
| ask            | string    | The current best ask price                            |
| open24h        | string    | The opening price of last 24 hours                    |
| high24h        | string    | The highest price of last 24 hours                    |
| low24h         | string    | The lowest price of last 24 hours                     |
| baseVolume24h  | string    | The trading volume in base currency of last 24 hours  |
| quoteVolume24h | string    | The trading volume of quote currency of last 24 hours |
| timestamp      | number    | The current system time in UTC time zone              |

Subscribe Ticker Data of a Single Trading Pair
----------------------------------------------

After subscription, the system will send ticker data of the chosen trading pair once a second.

> Data

```
{
    "ask": "34708.15",
    "baseVolume24h": "34.08241488",
    "bid": "34621.74",
    "high24h": "35079.77",
    "lastPrice": "34669.81",
    "low24h": "34330.64",
    "open24h": "34492.08",
    "quoteVolume24h": "1182480.09502814",
    "symbol": "BTC_BRL",
    "timestamp": 1571112216346
}

```

### Subscription Topic

`MARKET.{{symbol}}.TICKER`

### Request Parameter

| Field  | Mandatory | Data Type | Description    |
|--------|-----------|-----------|----------------|
| symbol | true      | string    | Trading symbol |

### Response Details

| Field          | Data Type | Description                                           |
|----------------|-----------|-------------------------------------------------------|
| symbol         | string    | Trading symbol                                        |
| lastPrice      | string    | The price of last trade                               |
| bid            | string    | The current best bid price                            |
| ask            | string    | The current best ask price                            |
| open24h        | string    | The opening price of last 24 hours                    |
| high24h        | string    | The highest price of last 24 hours                    |
| low24h         | string    | The lowest price of last 24 hours                     |
| baseVolume24h  | string    | The trading volume in base currency of last 24 hours  |
| quoteVolume24h | string    | The trading volume of quote currency of last 24 hours |
| timestamp      | number    | The current system time in UTC time zone              |

Subscribe Depth Data
--------------------

After subscription, the system will send the depth data of the chosen trading pairs once a second.

> Data

```
{
    "asks": [
        ["43687.16", "0.5194"],
        ["43687.2", "1.3129"]
    ],
    "bids": [
        ["43657.57", "0.6135"],
        ["43657.46", "0.0559"]
    ],
    "timestamp": 1565057338020
}

```

### Subscription Topic

`MARKET.{{symbol}}.DEPTH.LEVEL0`

### Request Parameters

| Field  | Mandatory | Data Type | Description    |
|--------|-----------|-----------|----------------|
| symbol | true      | string    | Trading symbol |

### Response Details

| Field     | Data Type | Description                              |
|-----------|-----------|------------------------------------------|
| asks      | array     | All current asks                         |
| asks[][0] | string    | Sell price                               |
| asks[][1] | string    | Sell amount                              |
| bids      | array     | All current bids                         |
| bids[][0] | string    | Buy price                                |
| bids[][1] | string    | Buy amount                               |
| timestamp | number    | The current system time in UTC time zone |

Subscribe Order Execution Data
------------------------------

After subscription, the system will send notification about the latest executed orders.

> Data

```
[
    {
        "price": "43657.57",
        "amount": "1",
        "side": "SELL",
        "timestamp": 1565007823401
    },
    {
        "price": "43687.16",
        "amount": "0.071",
        "side": "BUY",
        "timestamp": 1565007198261
    }
]

```

### Subscription Topic

`MARKET.{{symbol}}.TRADE`

### Request Parameters

| Field  | Mandatory | Data Type | Description    |
|--------|-----------|-----------|----------------|
| symbol | true      | string    | Trading symbol |

### Response Details

| Field     | Data Type | Description                         |
|-----------|-----------|-------------------------------------|
| price     | string    | The trading price                   |
| amount    | string    | The trading volume                  |
| side      | string    | The trading direction (SELL or BUY) |
| timestamp | number    | The time when the trade occurred    |
