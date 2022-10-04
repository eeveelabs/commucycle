
from this import d
from flask import Flask, request, Request, Response
from flask_sqlalchemy import SQLAlchemy

from mqtt import request_cycle, return_cycle

app = Flask(__name__)
# DB config
app.config["SQLALCHEMY_DB_URI"] = "sqlite3:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class cycles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    isIssued = db.Column(db.Integer)
    isTxInProgress = db.Column(db.Integer)
    disp_id = db.Column(db.Integer)


@app.route("/", methods=["GET"])
def basehit():
    return "Server online"

@app.route("/request/<disp_id>/<cycle_id>", methods=["GET", "POST"])
async def requestCycle(disp_id, cycle_id):
    isCycleAtDisp = db.first_or_404(db.select(cycles).filter_by(disp_id=disp_id))
    request_cycle(cycle_id, disp_id)




if __name__ == "__main__":
    app.run()