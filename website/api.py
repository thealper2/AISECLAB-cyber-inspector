from flask import Flask, request, render_template
from flask_socketio import SocketIO
import datetime
import csv

app = Flask(__name__)
socketio = SocketIO(app)

curr_date = datetime.datetime.now().date()
print("date: ", curr_date)

@app.before_request
@app.route("/", methods=["POST"])
def test():
    q = request.url.split(request.host_url)[-1]
    with open(f"logs/{curr_date}.csv", "a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([q])

    return f"[+] Request: {q} saved.", 200

if __name__ == "__main__":
    socketio.run(app, debug=True)
