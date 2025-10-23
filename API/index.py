from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# 2018-2020 ka old database
OLD_SIM_DATABASE = {
    '03001234567': {'name': 'Muhammad Ali', 'address': 'House 45, Model Town, Lahore', 'cnic': '35201-1234567-8', 'network': 'Mobilink', 'reg_date': '2018-03-15'},
    '03111234567': {'name': 'Ayesha Khan', 'address': 'Flat 23, Gulshan-e-Iqbal, Karachi', 'cnic': '42301-7654321-9', 'network': 'Ufone', 'reg_date': '2019-07-22'},
    '03211234567': {'name': 'Ahmed Raza', 'address': 'Sector F-8/4, Islamabad', 'cnic': '37405-5554444-3', 'network': 'Telenor', 'reg_date': '2020-01-10'},
    '03331234567': {'name': 'Fatima Bibi', 'address': 'Cantt Area, Rawalpindi', 'cnic': '36602-8889999-1', 'network': 'Zong', 'reg_date': '2018-11-30'},
    '03451234567': {'name': 'Bilal Ahmed', 'address': 'Johar Town, Lahore', 'cnic': '35202-1112222-4', 'network': 'Warid', 'reg_date': '2019-05-14'}
}

def generate_old_data(phone_number):
    networks_old = ['Mobilink', 'Ufone', 'Telenor', 'Zong', 'Warid']
    
    cities = {
        'Lahore': ['Model Town', 'Gulberg', 'Johar Town', 'Cantt', 'DHA'],
        'Karachi': ['Gulshan-e-Iqbal', 'North Nazimabad', 'DHA', 'Saddar', 'Clifton'],
        'Islamabad': ['Sector F-8', 'G-9', 'Blue Area', 'I-8'],
        'Rawalpindi': ['Saddar', 'Cantt', 'Sixth Road', 'Bahria Town']
    }
    
    city = random.choice(list(cities.keys()))
    area = random.choice(cities[city])
    
    year = random.randint(2018, 2020)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    
    return {
        'name': random.choice(['Muhammad Ali', 'Ayesha Khan', 'Ahmed Raza', 'Fatima Bibi', 'Bilal Ahmed']),
        'address': f"House {random.randint(1,999)}, {area}, {city}",
        'cnic': f"{random.randint(35000,43000)}-{random.randint(1000000,9999999)}-{random.randint(0,9)}",
        'network': random.choice(networks_old),
        'reg_date': f"{year}-{month:02d}-{day:02d}",
        'data_source': '2018-2020_Public_Records'
    }

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🔍 SBL HACKER - SIM Database</title>
        <style>
            body { font-family: Arial; background: #0d1117; color: #58a6ff; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: #161b22; padding: 30px; border-radius: 10px; border: 1px solid #30363d; }
            .header { text-align: center; border-bottom: 2px solid #58a6ff; padding-bottom: 20px; margin-bottom: 30px; }
            input, button { padding: 12px; margin: 5px; border: 1px solid #30363d; border-radius: 5px; }
            input { background: #0d1117; color: white; width: 200px; }
            button { background: #238636; color: white; cursor: pointer; }
            .result { background: #0d1117; padding: 15px; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 SBL HACKER - SIM DATABASE</h1>
                <p>2018-2020 SIM Records Lookup</p>
            </div>
            
            <div>
                <h3>📞 Enter Phone Number:</h3>
                <input type="text" id="number" placeholder="e.g., 03001234567" maxlength="11">
                <button onclick="search()">Search Records</button>
                
                <div id="result" class="result">
                    <pre id="resultData">Enter number and click search...</pre>
                </div>
            </div>
        </div>

        <script>
            function search() {
                const number = document.getElementById('number').value;
                const resultData = document.getElementById('resultData');
                
                if (!number) {
                    alert('Please enter phone number');
                    return;
                }
                
                resultData.innerHTML = 'Searching database...';
                
                fetch('/api/sim-info?number=' + number)
                    .then(r => r.json())
                    .then(data => {
                        resultData.innerHTML = JSON.stringify(data, null, 2);
                    })
                    .catch(err => {
                        resultData.innerHTML = 'Error: ' + err;
                    });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/api/sim-info', methods=['GET'])
def sim_info():
    number = request.args.get('number', '')
    
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
