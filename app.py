from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route for the home page ("/")
@app.route("/")
def hello_world():
    return "<p>Hello, Welcome to Agilisium Devops Team :) :)!</p>"

# Define a route with a dynamic part for personalized greetings
@app.route("/hello/<name>")
def hello_name(name):
    return f"<h1>Hello, Welcome to Agilisium Devops Team {name}!</h1>"

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(port=5000) # debug=True enables reloader and debugger