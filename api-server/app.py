
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
    '''
    Endpoint to request a cycle, return is the cycle was issued, or not
    Contains a async call to request_cycle(), that does mqtt, and return a list of messages in the cyclereqeuest/<disp_id>/response topic
    '''
    isCycleAtDisp = db.first_or_404(db.select(cycles).filter_by(disp_id=disp_id))
    responses = request_cycle(cycle_id, disp_id)
    for response in responses:
        if(cycle_id in response):
            return "Cycle issued :{}".format(cycle_id)
    return "Cycle issue failed"




if __name__ == "__main__":
    app.run()