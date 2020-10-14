import requests
import json
import datetime

class HorairesLouvre(object):
        def fistDayPossible():
                now = datetime.datetime.now()
                fistDayPossible = now + datetime.timedelta(days=1)
                fistDayPossible_formated = fistDayPossible.strftime('%Y-%m-%d')
                return fistDayPossible_formated


        def getHoraires_BilletGroupLouvre(selectedDate=None):
                if not selectedDate:
                        selectedDate = fistDayPossible()

                url = 'https://www.ticketlouvre.fr/louvre/b2c/RemotingService.cfc'

                headers = {'User-Agent':'Mozilla/5.0',
                #'Connection':'keep-alive',
                'Referer':'https://www.ticketlouvre.fr/louvre/b2c/index.cfm/calendar/eventCode/GA'
                }

                params = {'method':'doJson'}

                payload = {'eventName':'performance.read.nt',
                'performanceId':'',
                'selectedDate':selectedDate,
                'index':'',
                'eventCode':'GA',
                'eventAk':'LVR.EVN21'
                }

                response = requests.post(url,headers=headers,params=params,data=payload)

                resultDict_request = response.json()

                resultHoraires = resultDict_request['api']['result']['performanceList']

                return resultHoraires


        def printHoraires(resultDict_horaires):
                for horaire in resultDict_horaires:
                        print('date - {date} | horaire - {heure} | nb_places_dispo - {nb}/{nb_total}'.format(date=horaire['perfDate'],heure=horaire['perfTime'], nb=horaire['available'], nb_total=horaire['total']))


        def saveInFile_getHoraires(resultDict_horaires,mode='a+'):
                dateNow = datetime.datetime.now().strftime('%Y_%m_%d')
                timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                filename = 'results_get_at_' + dateNow + '.txt'
                insertTime = timeNow + ':\n'

                file = open(filename,mode)
                file.write(insertTime)
                for horaire in resultDict_horaires:
                        file.write('date - {date} | horaire - {heure} | nb_places_dispo - {nb}/{nb_total}\n'.format(date=horaire['perfDate'],heure=horaire['perfTime'], nb=horaire['available'], nb_total=horaire['total']))

                file.close()


        def getListDates(date,nb_days):
                BeginDate = datetime.datetime.strptime(date,'%Y-%m-%d')
                now = datetime.datetime.now()
                if BeginDate <= now:
                        print('bad date')
                        return

                listDates = [date,]
                i = 1
                nextDay = BeginDate

                while i < nb_days:
                        nextDay = nextDay + datetime.timedelta(days=1)
                        listDates.append(nextDay.strftime('%Y-%m-%d'))
                        i = i + 1        

                return listDates


if __name__ == "__main__": 
        listDates = getListDates('2020-10-08',3)
        for date in listDates:
                resultDict_horaires = getHoraires_BilletGroupLouvre(date)
                saveInFile_getHoraires(resultDict_horaires,'a+')

