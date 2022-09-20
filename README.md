# Project Instructions
Suppose you have 3 different APIs you can call with `member_id` as a parameter.

so example API calls would be:

```
https://api1.com?member_id=1
https://api2.com?member_id=1
https://api3.com?member_id=1
```

and you'll get responses from these apis with similar responses:

- API1: `{deductible: 1000, stop_loss: 10000, oop_max: 5000}`
- API2: `{deductible: 1200, stop_loss: 13000, oop_max: 6000}`
- API3: `{deductible: 1000, stop_loss: 10000, oop_max: 6000}`

As you can see above the APIs don't always agree. The task is to build an API that calls these APIs and coalesces the responses with a strategy.

An example strategy could be the average of the response fields. With the average strategy, your coalesce API would respond with:
`{deductible: 1066, stop_loss: 11000, oop_max: 5666}`

Your API should:

- Take in the member_id as a parameter
- Make the calls to the different APIs
- Coalesce the data returned by the APIs
- As a bonus challenge: allow for the coalescing strategy to be configurable

### How to run the application

The application is a Fastapi application that runs in a Docker container. To run the application you have to:

1. Build the Docker image: `docker compose build app`.
2. Launch the Docker container: `docker compose up -d app`.
3. Open `http://localhost:8000/docs` in your favorite web browser.

### Running the test suite

The application has a test suite that uses `pytest`, you can run it with the following command: 
`docker compose run app pytest`, you should and output similar to this:

```
docker compose run app pytest
========================================================================================================= test session starts =========================================================================================================
platform linux -- Python 3.10.2, pytest-7.1.3, pluggy-1.0.0
rootdir: /code
plugins: anyio-3.6.1, asyncio-0.19.0
asyncio: mode=strict
collected 10 items                                                                                                                                                                                                                    

app/tests/test_main.py ..........                                                                                                                                                                                               [100%]

========================================================================================================= 10 passed in 0.24s ==========================================================================================================
```

## Solution Overview

To make the call to the different APIs we leverage on the `aiohttp.ClientSession` class to make the calls asynchronous.
When all the tasks have finished processing we pass the results to the `coalesce_data` function that receives both the list
of results and the strategy to be used to coalesce the data. To implement the different coalesce strategies a simplification
of the plugin pattern is used, every strategy is a function that is mapped into a dictionary that then is used inside the 
`coalesce_data` function, adding a new strategy only requires adding the function that implements the new strategy and add
a new key/value pair to the `STRATEGIES_MAPPING` dictionary that way the `coalesce_data` function is open for extension
but closed to modifications, if and invalid key is passed to the `coalesce_data` function, the `average_coalesce_strategy`
function is returned by default.