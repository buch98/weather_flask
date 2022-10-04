import requests
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=="POST":
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
            
    cities = City.query.all()
    url="http://api.weatherapi.com/v1/current.json?key=2161153760a04e278ad53200220410&q={}&aqi=no"

    weather_data = []

    for city in cities:
        res = requests.get(url.format(city.name)).json()

        weather = {
            "city":res['location']['name'],
            "temperature":res['current']['temp_c'],
            "description":res['current']['condition']['text'],
            "icon":res['current']['condition']['icon'],
            "id":city.id

        }
        weather_data.append(weather)

    return render_template('index.html',weather_data=weather_data)

@app.route('/delete/<id>')
def delete(id):
    try:    
        del_city = City.query.filter_by(id=id).first()
        db.session.delete(del_city)
        db.session.commit()
    except Exception as e:
        return {"Error":"Id does not exist to delete"}
    
    return redirect('/')

if __name__=="__main__": 
    app.run(debug=True)