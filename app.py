from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# username and password
valid_username = 'user'
valid_password = 'password'

# Sample domain records 
domain_records = [
    # Add as many as required
]


@app.route('/home')
def home():
    filter_value = request.args.get('filter', '')

    filtered_records = [record for record in domain_records if not filter_value or record['domain_type'] == filter_value];

    return render_template('home.html', records=filtered_records)


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == valid_username and password == valid_password:
            # Successful login
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        domain_type = request.form['domain_type']
        name = request.form['name']
        address = request.form['address']
        other = request.form['other']

        domain_records.append({
            'domain_type': domain_type,
            'name': name,
            'address': address,
            'other': other
        })

        return redirect('/home')
    else:
        return render_template('insert.html')

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    if request.method == 'POST':
        domain_type = request.form['domain_type']
        name = request.form['name']
        address = request.form['address']
        other = request.form['other']

        domain_records[index] = {
            'domain_type': domain_type,
            'name': name,
            'address': address,
            'other': other
        }

        return redirect('/home')
    else:
        record = domain_records[index]
        return render_template('edit.html', index=index, record=record)

@app.route('/delete/<int:index>')
def delete(index):
    del domain_records[index]
    return redirect('/home')

@app.route('/logout')
def logout():
    global logged_in
    logged_in = False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
