from flask import Flask, render_template, json, request
import pandas as pd

app = Flask(__name__)
data = pd.read_csv('salary_dataset.csv')
data = data.drop('Unnamed: 0', axis = 'columns')
for i in data.columns: data.rename(columns = {i: i.replace(' ', '_')}, inplace = True)

@app.route('/', methods = ['GET','POST'])
def homepage():
    locations = data['Location'].unique().tolist()
    jobtitles = data['Job_Title'].unique().tolist()
    location = locations[0]

    if request.method == 'POST':
        if request.form['location-home'] != '':
            location = request.form['location-home']

    companies = data.query(f"Location == '{location}'")['Company_Name'].tolist()
    salreport = data.query(f"Location == '{location}'")['Salaries_Reported'].tolist()
    salaries = data.query(f"Location == '{location}'")['Salary'].tolist()

    loc_salary = []
    loc_company = []
    loc_salrept = []
    job_title = []

    for i in jobtitles:
        if len(data.query(f"Location == '{location}' and Job_Title == '{i}'")['Job_Title'].tolist()) != 0:
            job_title.append(i)
            k = data.query(f"Location == '{location}' and Job_Title == '{i}'")['Salary'].tolist()
            loc_salary.append('{:,}'.format(round(sum(k) / len(k))))
            loc_company.append('{:,}'.format(len(data.query(f"Location == '{location}' and Job_Title == '{i}'")['Company_Name'])))
            loc_salrept.append('{:,}'.format(sum(data.query(f"Location == '{location}' and Job_Title == '{i}'")['Salaries_Reported'])))

    return render_template(
        template_name_or_list = 'cities.html',
        location_cities = locations,
        init_location = location,
        total_companies = '{:,}'.format(len(companies)),
        salary_report = '{:,}'.format(sum(salreport)),
        avg_salary = '{:,}'.format(round(sum(salaries) / len(salaries))),
        jobtl = job_title,
        salry = loc_salary,
        compn = loc_company,
        slrpt = loc_salrept
    )

@app.route('/position', methods = ['GET','POST'])
def salarydata():
    cities = data['Location'].unique().tolist()
    positions = data['Job_Title'].unique().tolist()
    position = positions[0]

    if request.method == 'POST':
        if request.form['position-level'] != '':
            position = request.form['position-level']
    
    pavgsal = []
    psalrpt = []
    company = []

    for i in cities:
        sumval = data.query(f"Location == '{i}' and Job_Title == '{position}'")['Salary'].tolist()
        if len(sumval) == 0: pavgsal.append(0)
        else: pavgsal.append(sum(sumval) / len(sumval))
        salrpt = data.query(f"Location == '{i}' and Job_Title == '{position}'")['Salaries_Reported'].tolist()
        psalrpt.append(sum(salrpt))
        compny = data.query(f"Location == '{i}' and Job_Title == '{position}'")['Company_Name'].unique().tolist()
        company.append(len(compny))

    return render_template(
        template_name_or_list = 'poslevel.html',
        location_cities = json.dumps(cities),
        position_level = positions,
        init_position = position,
        mean_salaries = json.dumps(pavgsal),
        sal_report = json.dumps(psalrpt),
        companies = json.dumps(company),
        total_pos_count = len(data.query(f"Job_Title == '{position}'"))
    )

if __name__ == '__main__': app.run(debug = True)