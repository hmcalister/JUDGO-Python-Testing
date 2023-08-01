# JUDGO Implementation for Testing

A quick implementation of the [JUDGO](https://dl.acm.org/doi/pdf/10.1145/3539618.3591801) preference algorithm to assess the average number of steps required to rank a set of documents.

## Running the Experiments

First, install the requirements using `pip install -r requirements.txt`.

Next, run the script using `python main.py`. A plot will appear after a short time detailing the trend of number of steps vs number of documents. An annotation is also programmed that can be updated using the variables `X_VAL, Y_VAL` on lines 79 and 80 of `main.py`.