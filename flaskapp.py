from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    with open('emission.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        r = csv.reader(csvfile)

        countries = []
    
        for i in range(4):
            next(r)
        
        for row in readCSV:
            if row[0] != "Country Name" :
                countries.append(row[0])
        
    return jsonify({'countries': countries})


@app.route('/api/imdeadinside', methods=['GET'])
def get_death():
    with open('emission.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        r = csv.reader(csvfile)

        countries = []
    
        for i in range(4):
            next(r)
        
        for row in readCSV:
            countries.append(row)
        
    return jsonify({'countries': countries})

#COUNTRY'S EMISSIONS
@app.route('/api/countries/<country>', methods=['GET', 'POST'])
def get_countryid(country):
    #indexes
    yeari = 4
    headeri = 0
    countryi = 4
    populationi = 4
    percapitai = 0

    #arrays
    headers = []
    emissions = []
    years = []
    populations = []
    percapitas = []

    #get years, headers and emissions
    with open('emission.csv') as emissionfile:
        readEmissions = csv.reader(emissionfile, delimiter=',')
        for i in range(4):
            next(emissionfile)

        for row in readEmissions:
            if row[0] == "Country Name" :
                last = len(row)-1
                for i in range(4,last):
                    years.append(row[yeari])
                    yeari = yeari + 1
            if row[0] == country :
                for i in range(0,4):
                    headers.append(row[headeri])
                    headeri = headeri + 1
                for x in range(4,last):
                    emissions.append(row[countryi])
                    countryi = countryi + 1

    #get populations
    with open('population.csv') as populationfile:
        readPopulations = csv.reader(populationfile, delimiter=',')
        for i in range(4):
            next(populationfile)

        for row in readPopulations:
            if row[0] == country :
                last = len(row)-1
                for y in range(4,last):
                    populations.append(row[populationi])
                    populationi = populationi + 1

    #emissions per capita
    while percapitai < len(populations):
        pop = populations[percapitai]
        ems = emissions[percapitai]
        if ems != "" and pop != "":
            percapitanumber = float(ems) / int(pop)
            percapitanumber = format(percapitanumber, ".5f")
            print(percapitanumber)
            percapitas.append(percapitanumber)
        else:
            percapitas.append("")
            
        percapitai = percapitai + 1

    return jsonify({'emissions': emissions, 'years': years, 'headers': headers, 'populations': populations, 'percapitas': percapitas})

#COUNTRY'S EMISSIONS PER YEAR
@app.route('/api/countries/<country>/<year>', methods=['GET'])
def get_countryidyear(country, year):
    yeari = 0
    
    countries = []
    emissions = []
    years = []
    headers = []

    with open('emission.csv') as emissionfile:
        readEmissions = csv.reader(emissionfile, delimiter=',')
        for i in range(4):
            next(emissionfile)

        for row in readEmissions:
            if row[0] == "Country Name" :
                while row[yeari] != year :
                    yeari = yeari + 1
                if row[yeari] == year :
                    years.append(row[yeari])
            if row[0] == country :
                countries.append(row[0])
                emissions.append(row[yeari])

    return jsonify({'country': countries, 'emissions': emissions, 'years': years})


if __name__ == '__main__':
    app.run()
