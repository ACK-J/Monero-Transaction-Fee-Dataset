import requests
import pickle

API_URL = "https://xmrchain.net/api"


def get_tx_data():
    data = []
    starting_block = 2566273
    num_transactions = 0
    skipped_transactions = 0
    while num_transactions < 100000:
        try:
            response = requests.get(API_URL + "/block/" + str(starting_block))
            if response.status_code == 200 and 'application/json' in response.headers.get('Content-Type', ''):
                txs = response.json()["data"]["txs"]
                for tx in txs:
                    if tx["coinbase"] is not True:
                            tx_response = requests.get(API_URL + "/transaction/" + str(tx["tx_hash"])).json()["data"]
                            transaction = {}
                            transaction["timestamp"] = tx_response["timestamp"]
                            transaction["tx_fee"] = tx_response["tx_fee"]
                            transaction["tx_size"] = tx_response["tx_size"]
                            transaction["tx_hash"] = tx_response["tx_hash"]
                            transaction["num_inputs"] = len(tx_response["inputs"])
                            transaction["num_outputs"] = len(tx_response["outputs"])
                            num_transactions += 1
                            print(transaction)
                            print("Transactions:", num_transactions)
                            print()
        except Exception as e:
            skipped_transactions += 1
            print("Skipped Transaction:", skipped_transactions)
        starting_block -= 1
        print("Block: ", starting_block)
        print()
    with open("data.pkl", "wb") as fp:
        pickle.dump(data, fp)


def make_csv():
    with open("data.pkl", "rb") as fp:
        data = pickle.load(fp)
    with open("data.csv", "a") as fp:
        fp.write("tx_fee,tx_size,num_inputs,num_outputs,fee_per_kB\n")
        for tx in data:
            fp.write(str(tx['tx_fee']) + "," + \
                     str(tx['tx_size']) + "," + \
                     str(tx['num_inputs']) + "," + \
                     str(tx['num_outputs']) + "," + \
                     str(tx['fee_per_kB']) + "," + "\n")


def main():
    get_tx_data()
    make_csv()


if __name__ == '__main__':
    main()
