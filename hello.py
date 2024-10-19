from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
    first_name = "Dennis Wu 99, i'm super cool"
    safe_test = "Safe test every thing is Safe"
    cars = ["BMW", "Audi", "Benz", "Toyota",40708]
    return render_template('index.html', 
                           fn=first_name,
                           st=safe_test,
                           cars=cars)


@app.route('/user/<name>')

def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)

#they use a lot the safe and striptags.
# title for capitalizing the first letter of the string