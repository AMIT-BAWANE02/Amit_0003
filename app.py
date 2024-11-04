import os
import MySQLdb
import smtplib
import random
import string
from datetime import datetime
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash, send_file
from database import db_connect,owner_reg,owner_login,te_act,vtrack,g_act,vgoal,g1_act
from database import db_connect

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline



# def db_connect():
#     _conn = MySQLdb.connect(host="localhost", user="root",
#                             passwd="root", db="assigndb")
#     c = _conn.cursor()

#     return c, _conn


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def FUN_root():
    return render_template("index.html")
    


@app.route("/user.html")
def user():
    return render_template("user.html")

@app.route("/cs.html")
def cs():
    return render_template("cs.html")

@app.route("/reg.html")
def reg():
    return render_template("reg.html")


@app.route("/uhome.html")
def uhome():
    return render_template("uhome.html")

@app.route("/pr.html")
def pr():
    return render_template("pr.html")

@app.route("/index")
def index():
    return render_template("index.html") 


@app.route("/te.html")
def te():
    username = session['username']
    data = vtrack(username)
    print(data)
    return render_template("te.html",data = data)

@app.route("/goal.html")
def goal():
    username = session['username']
    data = vgoal(username)
    print(data)
    return render_template("goal.html",data = data)


@app.route("/vu2", methods = ['GET','POST'])
def vu2():
    b = request.args.get('b')
    c = request.args.get('c')
    d = request.args.get('d')
    e = request.args.get('e')
    return render_template("g1.html", b=b,c=c,d=d,e=e)




        

@app.route("/oregact", methods = ['GET','POST'])
def oregact():
   if request.method == 'POST':    
      
      status = owner_reg(request.form['username'],request.form['password'],request.form['email'],request.form['mobile'],request.form['address'])
      
      if status == 1:
       return render_template("user.html",m1="sucess")
      else:
       return render_template("reg.html",m1="failed")
      

      
@app.route("/teact", methods = ['GET','POST'])
def teact():
   if request.method == 'POST':    
      
      status = te_act(request.form['username'],request.form['income'],request.form['expenses'],request.form['dt'])
      
      if status == 1:
       return render_template("te.html",m1="sucess")
      else:
       return render_template("te.html",m1="failed")
      

@app.route("/gact", methods = ['GET','POST'])
def gact():
   if request.method == 'POST':    
      
      status = g_act(request.form['username'],request.form['gname'],request.form['tamount'],request.form['camount'])
      
      if status == 1:
       return render_template("goal.html",m1="sucess")
      else:
       return render_template("goal.html",m1="failed")
      
@app.route("/g1act", methods = ['GET','POST'])
def g1act():
   if request.method == 'POST':    
      


      username = request.form['username']
      gname = request.form['gname']
      tamount = request.form['tamount']
      camount = request.form['camount']
      eamount = request.form['eamount']

      ca = int(camount)
      ea = int(eamount)
      fa = ca+ea



      status = g1_act(username,gname,tamount,fa)
      
      if status == 1:
       return render_template("goal.html",m1="sucess")
      else:
       return render_template("goal.html",m1="failed")
      
@app.route("/csact", methods = ['GET','POST'])
def csact():
   if request.method == 'POST':    
      


      income = request.form['income']
      rent = request.form['rent']
      gro = request.form['gro']
      uti = request.form['uti']
      others = request.form['others']

      inc = int(income)
      re = int(rent)
      gr = int(gro)
      ut = int(uti)
      ot = int(others)

      t1 = re + gr + ut + ot

      t2 = inc - t1

      
      return render_template("cs.html",m1="sucess",t2 = t2)
      

@app.route("/ologin", methods=['GET', 'POST'])       
def ologin():
    if request.method == 'POST':
        status = owner_login(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']
            return render_template("uhome.html", m1="sucess")
        else:
            return render_template("user.html", m1="Login Failed")

# # -------------------------------Loginact End-----------------------------------------------------------------



@app.route('/')
def home():
    return render_template('index.html')



# predict-------------------------------------------
data = {
    'monthly_income': [
        10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000,
        10500, 20500, 30500, 40500, 50500, 60500, 70500, 80500, 90500, 100500,
        11000, 21000, 31000, 41000, 51000, 61000, 71000, 81000, 91000, 101000,
        11500, 21500, 31500, 41500, 51500, 61500, 71500, 81500, 91500, 101500,
        12000, 22000, 32000, 42000, 52000, 62000, 72000, 82000, 92000, 102000
    ],
    'monthly_expenses': [
        5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000,
        5200, 10200, 15200, 20200, 25200, 30200, 35200, 40200, 45200, 50200,
        5400, 10400, 15400, 20400, 25400, 30400, 35400, 40400, 45400, 50400,
        5600, 10600, 15600, 20600, 25600, 30600, 35600, 40600, 45600, 50600,
        5800, 10800, 15800, 20800, 25800, 30800, 35800, 40800, 45800, 50800
    ],
    'savings': [
        4000, 8000, 12000, 16000, 20000, 24000, 28000, 32000, 36000, 40000,
        4300, 8300, 12300, 16300, 20300, 24300, 28300, 32300, 36300, 40300,
        4600, 8600, 12600, 16600, 20600, 24600, 28600, 32600, 36600, 40600,
        4900, 8900, 12900, 16900, 20900, 24900, 28900, 32900, 36900, 40900,
        5200, 9200, 13200, 17200, 21200, 25200, 29200, 33200, 37200, 41200
    ]
}

df = pd.DataFrame(data)

# Splitting the data into features and target
X = df[['monthly_income', 'monthly_expenses']]
y = df['savings']

# Splitting into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creating a pipeline with scaling and the Random Forest model
pipeline = Pipeline([
    ('scaler', StandardScaler()),  # Scaling the features
    ('model', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Training the model
pipeline.fit(X_train, y_train)

def get_investment_suggestions(savings):
    if savings < 1000:
        return (
            "Start by building a small emergency fund in a basic savings account. Prioritize accumulating a few hundred dollars before exploring investments."
        )
    elif 1000 <= savings < 2000:
        return (
            "Focus on building an emergency fund with a high-yield savings account. Keep your savings easily accessible and consider starting a small, low-risk investment."
        )
    elif 2000 <= savings < 3000:
        return (
            "Continue to build your emergency fund. Explore low-risk investment options like short-term fixed deposits or a low-risk savings account."
        )
    elif 3000 <= savings < 4000:
        return (
            "With a growing emergency fund, consider starting with low-risk investments like government bonds or a Certificate of Deposit (CD)."
        )
    elif 4000 <= savings < 5000:
        return (
            "Diversify slightly with low-risk investments such as fixed deposits or short-term government bonds. Keep your emergency fund well-established."
        )
    elif 5000 <= savings < 7000:
        return (
            "Consider expanding your investments to include low-risk mutual funds or ETFs. Continue to maintain a strong emergency fund."
        )
    elif 7000 <= savings < 9000:
        return (
            "Explore medium-risk investments like balanced mutual funds or sector-specific ETFs. Ensure your emergency fund is fully funded."
        )
    elif 9000 <= savings < 11000:
        return (
            "Invest in a diversified portfolio including both low-risk and medium-risk investments. Consider starting a small equity investment or a systematic investment plan (SIP)."
        )
    elif 11000 <= savings < 13000:
        return (
            "Increase your exposure to medium-risk investments such as equity mutual funds. Start exploring higher-risk options like growth stocks."
        )
    elif 13000 <= savings < 15000:
        return (
            "Diversify further with a combination of medium-risk mutual funds, ETFs, and a portion in equities. Maintain a solid emergency fund."
        )
    elif 15000 <= savings < 20000:
        return (
            "Consider a mix of medium-risk investments, including blue-chip stocks and balanced funds. Explore starting a small investment in real estate or REITs."
        )
    elif 20000 <= savings < 25000:
        return (
            "Expand your portfolio with a mix of equities, mutual funds, and REITs. Consider adding some higher-risk investments for potential higher returns."
        )
    elif 25000 <= savings < 30000:
        return (
            "Diversify further with international mutual funds and ETFs. Consider investing in commercial real estate or other high-growth opportunities."
        )
    elif 30000 <= savings < 35000:
        return (
            "Focus on a balanced portfolio with a mix of equities, fixed income, and real estate. Explore advanced investment vehicles like structured products or hedge funds."
        )
    elif 35000 <= savings < 40000:
        return (
            "Invest in a diverse range of asset classes including equities, bonds, real estate, and alternative investments. Consider professional portfolio management services."
        )
    elif 40000 <= savings < 50000:
        return (
            "Allocate funds to a diversified portfolio including direct equities, mutual funds, ETFs, and commercial real estate. Explore higher-risk investments such as venture capital."
        )
    elif 50000 <= savings < 60000:
        return (
            "Leverage your savings for significant investment opportunities including international equities, high-yield bonds, and high-growth real estate projects."
        )
    elif 60000 <= savings < 70000:
        return (
            "Expand into alternative investments such as private equity or collectibles. Diversify further with international real estate or advanced structured investments."
        )
    elif 70000 <= savings < 80000:
        return (
            "Consider a comprehensive investment strategy with a mix of equities, bonds, real estate, and alternative investments. Explore philanthropy or impact investing."
        )
    elif 80000 <= savings < 90000:
        return (
            "Focus on maximizing returns through a balanced and diversified portfolio. Consider investing in commercial real estate, private equity, and high-yield bonds."
        )
    elif 90000 <= savings < 100000:
        return (
            "Invest in a broad range of assets including international equities, high-yield investments, and private equity. Explore advanced wealth management strategies."
        )
    elif 100000 <= savings < 120000:
        return (
            "With substantial savings, consider a diversified investment approach including high-risk, high-reward opportunities like start-ups and venture capital."
        )
    elif 120000 <= savings < 150000:
        return (
            "Leverage significant savings for extensive diversification. Invest in global markets, commercial real estate, and alternative assets such as private equity and hedge funds."
        )
    else:
        return (
            "With significant wealth, focus on advanced investment strategies. Diversify across multiple asset classes, including international real estate, private equity, hedge funds, and impact investments. Consider working with a wealth management advisor for personalized strategies."
        )


@app.route('/predict', methods=['POST'])
def predict():
    income = float(request.form['income'])
    expenses = float(request.form['expenses'])

    # Make prediction
    prediction = pipeline.predict([[income, expenses]])
    predicted_savings = round(prediction[0], 2)

    # Get investment suggestions
    suggestions = get_investment_suggestions(predicted_savings)

    return render_template('result.html', prediction=predicted_savings, suggestions=suggestions)
   
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
