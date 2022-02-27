import pickle
import random


def main():
    with open("data.pkl", "rb") as fp:
        data = pickle.load(fp)
        # 1 0.00000005
        # 2 0.00000015
        # 3 0.00000025
        # 4 0.0000086500
        rand_idx = random.randrange(0, len(data)-1)
        xmr_per_byte = (data[rand_idx]['tx_fee'] * 0.000000000001) / data[rand_idx]['tx_size']
        if xmr_per_byte <= 0.00000005:
            print("1")
        elif xmr_per_byte <= 0.00000015:
            print("2")
        elif xmr_per_byte <= 0.00000025:
            print("3")
        else:
            print("4")


if __name__ == '__main__':
    main()
