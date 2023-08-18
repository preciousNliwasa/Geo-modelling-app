from flask import Flask,request,render_template,url_for,redirect
from dashboard import create_dash_application

app = Flask(__name__)
create_dash_application(app)

@app.route('/',methods = ["GET","POST"])
def home():
    
    if request.method == 'GET':
    
            return render_template('index.html')

    else:
    
        return redirect('/dash')  
            
    

if __name__ == '__main__':
    app.run(debug=False)
