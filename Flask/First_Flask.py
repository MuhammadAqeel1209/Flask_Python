from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    temp =  render_template('index.html')
    return temp
@app.route('/about')
def Aqeel():
    name = "Aqeel"
    return render_template('about.html',name = name)

@app.route('/boost')
def Boost():
    return render_template('boosttrap.html')

app.run(debug=True)



# https://pythonbasics.org/what-is-flask-python/
# https://jinja.palletsprojects.com/en/3.1.x/