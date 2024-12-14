from flask import Flask , jsonify
    # a simple page that says hello
app = Flask(__name__)
@app.route('/')
def hello():
        return 'Hello, World!'

@app.route("/armstrong/<int:n>")
def armstrong (n):

    sum = 0
    order = len(str(n))
    copy_num = n
    while(n > 0):
        digit = n % 10
        sum += digit ** order
        n = n //10

    if(sum == copy_num):
        print(F"{copy_num} is a armstrong number")
        result = {
             "number" : copy_num,
             "armstrong" : True
        }
    else:
        print(F"{copy_num} is not armstrong number")
        result = {
             "number" : copy_num,
             "armstrong" : False
        }
    return jsonify(result)    
app.run(debug=True)