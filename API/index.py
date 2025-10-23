from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "SBL HACKER API IS WORKING!"

@app.route('/api/sim-info')
def sim_info():
    return jsonify({
        "status": "success",
        "message": "API is working!",
        "test_number": "03001234567"
    })

def handler(request, context):
    return app(request, context)

if __name__ == '__main__':
    app.run()    
    if not number or len(number) != 11:
        return jsonify({
            "status": "error",
            "message": "Valid 11-digit phone number required"
        }), 400
    
    if number in OLD_SIM_DATABASE:
        return jsonify({
            "status": "success",
            "data": OLD_SIM_DATABASE[number],
            "database": "2018-2020_Records"
        })
    else:
        fake_data = generate_old_data(number)
        return jsonify({
            "status": "success", 
            "data": fake_data,
            "database": "2018-2020_Records",
            "note": "Simulated data based on 2018-2020 patterns"
        })

# Vercel serverless function handler
def handler(request, context):
    return app(request, context)

if __name__ == '__main__':
    app.run(debug=True)
