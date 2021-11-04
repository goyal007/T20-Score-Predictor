from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predictScore():
    if request.method=="POST":
        BattingTeam=request.form["BattingTeam"]
        BowlingTeam=request.form["BowlingTeam"]
        city=request.form["city"]
        Innings=int(request.form["Innings"])
        Over=int(request.form["Over"])
        Ball=int(request.form["Ball"])
        Score=float(request.form["Score"])
        WicketsLeft=int(request.form["WicketsLeft"])
        RunsInLastFive=int(request.form["RunsInLastFive"])
        WicketsInLastFive=int(request.form["WicketsInLastFive"])
        
        print(BattingTeam,type(BattingTeam))
        print(BowlingTeam,type(BowlingTeam))
        print(city,type(city))
        print(Innings,type(Innings))
        print(Over,type(Over))
        print(Ball,type(Ball))
        print(Score,type(Score))
        print(WicketsLeft,type(WicketsLeft))
        print(RunsInLastFive,type(RunsInLastFive))
        print(WicketsInLastFive,type(WicketsInLastFive))
        
        pp=powerplay(Over)
        average=avr(city,Innings)
        left=deliveryLeft(Over,Ball)
        crr=currentRunRate(Score,Over,Ball)
        
        
        li=[pp,average,BattingTeam,BowlingTeam,city,left,Score,crr,WicketsLeft,RunsInLastFive,WicketsInLastFive,Innings]
        i=['powerPlay','AverageScore','battingTeam', 'bowlingTeam', 'city', 'delivery_left', 'score', 'CurrentRunRate', 'wicketsLeft', 'Run_In_Last5', 'Wickets_In_Last5', 'innings']
        inp=pd.DataFrame([li],columns=i)
        inp.head()
        pipe= pickle.load(open('temp.pkl','rb'))
        
        t=pipe.predict(inp)
        #print(t)
        n=t
        return render_template("predict.html",n=n,BattingTeam=BattingTeam,BowlingTeam=BowlingTeam,
                               city=city,Innings=Innings,Over=Over,Ball=Ball,Score=Score,
                                WicketsLeft=WicketsLeft,RunsInLastFive=RunsInLastFive,
                              WicketsInLastFive=WicketsInLastFive
                              )

@app.route("/")
def hello():
    return render_template("index.html")

averages = pickle.load(open('average.pkl','rb'))

city = ['Wellington', 'Colombo', 'Christchurch', 'Harare', 'Auckland',
       'Hyderabad', 'Durban', 'Pallekele', 'Abu Dhabi', 'Mirpur', 'Dhaka',
       'Lauderhill', 'Kimberley', 'Adelaide', 'Cape Town', 'Coolidge',
       'Chandigarh', 'Pune', 'Canberra', 'Port Elizabeth', 'Delhi',
       'Antigua', 'Hambantota', 'Barbados', 'Sharjah', 'Kolkata',
       "St George's", 'Dubai', 'Bready', 'St Kitts', 'Sylhet', 'Sydney',
       'London', 'Cardiff', 'Visakhapatnam', 'Lahore', 'Basseterre',
       'Centurion', 'Nagpur', 'Johannesburg', 'Manchester', 'St Lucia',
       'Melbourne', 'Mumbai', 'Gros Islet', 'Hamilton', 'Napier',
       'Chattogram', 'Karachi', 'Dominica', 'Dharamsala', 'Birmingham',
       'Nottingham', 'Dublin', 'Rotterdam', 'Al Amarat',
       'Mount Maunganui', 'Bristol', 'Chester-le-Street', 'Ranchi',
       'Cuttack', 'Greater Noida', 'Perth', 'Brisbane', 'Guyana',
       'Lucknow', 'Bulawayo', 'Nelson', 'Dehradun', 'Southampton',
       'Rajkot', 'Belfast', 'Thiruvananthapuram', 'Dunedin', 'Guwahati',
       'Nairobi', 'Indore', 'Hobart', 'Jamaica', 'Edinburgh', 'Bengaluru',
       'St Vincent', 'Paarl', 'Khulna', 'Trinidad', 'Chennai', 'Derry',
       'King City', 'The Hague', 'Ahmedabad', 'Providence', 'Leeds',
       'Kandy', 'Rawalpindi', 'Kanpur', 'Victoria', 'Potchefstroom',
       'Bridgetown', 'Bloemfontein', 'Taunton', 'Carrara']


bat = ['New Zealand', 'Sri Lanka', 'India', 'Bangladesh', 'Netherlands',
       'Pakistan', 'West Indies', 'Zimbabwe', 'Australia', 'England',
       'South Africa', 'Afghanistan', 'Ireland']

bowl = ['Australia', 'Pakistan', 'Zimbabwe', 'Sri Lanka', 'West Indies',
       'South Africa', 'Ireland', 'England', 'Bangladesh', 'Afghanistan',
       'New Zealand', 'India', 'Netherlands']
def powerplay(over):
    if over<=6:
        return 1
    return 0

def avr(city,innings):
    average = averages[(averages['city']== city) & (averages['innings']==innings)]['AverageScore']
    average=average[average.index[0]]
    return average

def deliveryLeft(over,ball):
    deliv = int(over)*6 + int(ball)
    deliv1 = 120 - deliv
    if deliv1 < 0:
        return 0
    else:
        return deliv1

def currentRunRate(score,over,ball):
    deliv = int(over)*6 + int(ball)
    return (score)/(deliv/6)

if __name__ == '__main__':
	app.run()