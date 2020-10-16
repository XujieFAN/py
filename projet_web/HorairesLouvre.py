from flask import Flask
from flask import render_template
from flask import request
#from getHorairesDispo_Louvre import getListDates
#from getHorairesDispo_Louvre import getHoraires_BilletGroupLouvre
from getHorairesDispo_Louvre import HorairesLouvre
import numpy

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1> welcome to my web </h1>'

@app.route('/helloworld')
def helloworld():
    return render_template('helloworld.html')


@app.route('/horaires_louvre', methods=['POST','GET'])
def getHorairesLouvre():
    template_HTML = 'horaires_louvre.html'
    #template_HTML = '/home/xfan/mysite/horaires_louvre.html'

    date = '2020-10-17'
    nb_days = 1

    if request.method == 'POST':
        date = request.form['selectedDate']
        nb_days = int(request.form['selectedNbDays'])

        listDates = HorairesLouvre.getListDates(date,nb_days)
        resultDict_horaires = dict()

        for date in listDates:
            resultDict_horaires[date] = HorairesLouvre.getHoraires_BilletGroupLouvre(date)

        return render_template(template_HTML, hasSelectedDateAndNb=1, listDates=listDates, resultDict_horaires=resultDict_horaires)
    else:
        return render_template(template_HTML, hasSelectedDateAndNb=0)

'''
@app.errorhandler(Exception)
def page_not_found(error):
    return render_template('error.html')
'''

if __name__ == '__main__':
    app.run(debug=True)