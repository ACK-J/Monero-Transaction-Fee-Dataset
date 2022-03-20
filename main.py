import requests
import pickle
from time import sleep
from typing import List, Dict, Any

# Parameters
API_URL: str = "https://xmrchain.net/api"
desired_transaction_count: int = 5
exception_sleep_time: float = 1.0
success_sleep_time: float = 0.5


# Transaction scraper
def get_tx_data():
    data: List[Dict[str, Any]] = []
    starting_block: int = 2566275
    skipped_transactions: int = 0
    while len(data) < desired_transaction_count:
        try:
            # Retrieve the next block and confirm that the response is good
            response: requests.Response = requests.get(API_URL + "/block/" + str(starting_block))
            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                txs = response.json()["data"]["txs"]
                print(f"\nRetrieved block {starting_block} containing {len(txs)} transactions...")
            else:
                print(f"\nIssue retrieving block {starting_block}... Continuing")
                continue

            # Loop over non-coinbase transactions
            non_coinbase_transactions: List[Dict[str, Any]] = [t for t in txs if not t["coinbase"]]
            for tx in non_coinbase_transactions:
                tx_response: requests.Response = requests.get(f"{API_URL}/transaction/{tx['tx_hash']})").json()["data"]
                sleep(success_sleep_time)

                # Copy direct fields
                transaction: Dict[str, Any] = {f: tx_response[f] for f in ['timestamp', 'tx_fee', 'tx_size', 'tx_hash']}

                # Feature engineering
                transaction["num_inputs"] = len(tx_response["inputs"])
                transaction["num_outputs"] = len(tx_response["outputs"])

                # Add to the data and log
                data.append(transaction)
                print(f"\n[Collected {len(data)} of {desired_transaction_count} total]\nNew entry: {transaction}")

        except Exception as e:
            skipped_transactions += 1
            print(f"Encountered exception {e}\nTotal skip count: {skipped_transactions}\n")
            sleep(exception_sleep_time)

        starting_block -= 1

    with open("data.pkl", "wb") as fp:
        pickle.dump(data, fp)


def make_csv():
    with open("data.pkl", "rb") as fp:
        data: List[Dict[str, Any]] = pickle.load(fp)
    with open("data.csv", "w") as fp:
        fp.write("tx_fee,tx_size,num_inputs,num_outputs,tx_fee/tx_size\n")
        for tx in data:
            fp.write(f"{int(tx['tx_fee']) * 0.000000000001},{tx['tx_size']},{tx['num_inputs']},{tx['num_outputs']}," +
                     f"{(int(tx['tx_fee']) * 0.000000000001) / int(tx['tx_size'])}\n")


def main():
    get_tx_data()
    make_csv()


if __name__ == '__main__':
    main()
