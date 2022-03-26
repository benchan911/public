import base64
from io import BytesIO
import io 

from flask import Flask
from matplotlib.figure import Figure
import requests

app = Flask(__name__)

def display(fig):
    # Save it to a temporary buffer.
    buf = BytesIO()

    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

@app.route("/basic")
def basic():
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 3, 2], [0.1, 0.2, 0.3])

    return display(fig)

@app.route("/fetch")
def fetch():
    import pandas as pd
    import matplotlib.pyplot as plt

    # READ
    df = pd.read_csv('local.csv').to_dict()
    fig = Figure()
    ax = fig.subplots()

    # PLOT
    ax.plot(list(df['DATE'].values()),list(df['TAVG'].values()))

    # ADDING LABELS
    ax.set(xlabel='Date', ylabel='Average Temperature')

    ## Adding Title
    ax.set_title("New York")
    
    # RETURN
    return display(fig)

@app.route("/scatter")
def scatter():
    import pandas as pd
    import matplotlib.pyplot as plt

    # READ
    df = pd.read_csv('local.csv').to_dict()
    fig = Figure()
    ax = fig.subplots()

    # PLOT
    ax.scatter(list(df['DATE'].values()),list(df['TAVG'].values()), s=2)

    # ADDING LABELS
    ax.set(xlabel='Date', ylabel='Average Temperature')

    ## Adding Title
    ax.set_title("New York")
    
    # RETURN
    return display(fig)

@app.route("/live")
def live():
    import pandas as pd
    import matplotlib.pyplot as plt

    # READ
    url = 'http://raw.githubusercontent.com/benchan911/public/main/local.csv'
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content)).to_dict()

    # df = pd.read_csv().to_dict()
    fig = Figure()
    ax = fig.subplots()

    # PLOT
    ax.scatter(list(df['DATE'].values()),list(df['TAVG'].values()), s=2)

    # ADDING LABELS
    ax.set(xlabel='Date', ylabel='Average Temperature')

    ## Adding Title
    ax.set_title("New York")
    
    # RETURN
    return display(fig)
    
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)