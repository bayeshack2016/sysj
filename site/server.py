from flask import Flask, render_template
import os

app = Flask(__name__, template_folder='views')
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.debug = True

# templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views')

@app.route("/")
@app.route('/<city>')
def hello(city=None):
    return render_template('index.jade', city=city)

if __name__ == "__main__":
    app.run()
