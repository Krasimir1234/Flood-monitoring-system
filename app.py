from flask import render_template, Flask
import folium

app = Flask(__name__)

@app.route('/')
def home():
    austria = [47.5162, 14.5501]
    map = folium.Map(location=austria,zoom_start= 7)
    folium.Circle(
        location=[48.2082, 16.3738],
        radius=1000,
        color="blue",
        fill_color="blue",
        tooltip="Vienna"
    ).add_to(map)
    map_html = map._repr_html_()
    return render_template("home.html", map_html=map_html)

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/Signup')
def signup():
    return render_template('signup.html')
if __name__ == '__main__':
    app.run(debug=True)