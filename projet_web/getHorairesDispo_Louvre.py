import requests
import json
import datetime

class HorairesLouvre(object):
        def fistDayPossible(self):
                now = datetime.datetime.now()
                fistDayPossible = now + datetime.timedelta(days=1)
                fistDayPossible_formated = fistDayPossible.strftime('%Y-%m-%d')
                return fistDayPossible_formated


        def getHoraires_BilletGroupLouvre(self,selectedDate=None):
                if not selectedDate:
                        selectedDate = self.fistDayPossible()

                url = 'https://www.ticketlouvre.fr/louvre/b2c/RemotingService.cfc'

                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
                'Referer':'https://www.ticketlouvre.fr/louvre/b2c/index.cfm/calendar/eventCode/GA'
                #,'Connection':'keep-alive',
                #'Accept':'application/json, text/javascript, */*; q=0.01',
                #'Accept-Encoding':'gzip, deflate, br',
                #'Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
                #'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                #'charset':'UTF-8',
                #'Host':'www.ticketlouvre.fr',
                #'Origin':'https://www.ticketlouvre.fr',
                #'Sec-Fetch-Dest':'empty',
                #'Sec-Fetch-Mode':'cors',
                #'Sec-Fetch-Site':'same-origin',
                #'X-Requested-With':'XMLHttpRequest',
                #'Cookie':'Application_STICKY=sticky.node1; visid_incap_2189377=Civn7wOITl2hb4q1U+d2JZXlq18AAAAAQUIPAAAAAADw9caFVg9tx91c/ISDNkl+; _ga=GA1.2.1675765201.1605100952; _gid=GA1.2.1735062989.1605100952; DisplayDivasCookiesBanner=yes; _tlp=874:4619815; CFID=37188412; CFTOKEN=89046886; incap_ses_466_2189377=J2kHPNYoiAl55GrcxpB3BmZHrF8AAAAAqArTdfw5GqcU8L0EwUSZyA==; _tlc=www.google.com%2F:1605125991:www.ticketlouvre.fr%2Flouvre%2Fb2c%2Findex.cfm%2Fhome:ticketlouvre.fr; QueueITAccepted-SDFrts345E-V3_louvreprd=EventId%3Dlouvreprd%26QueueId%3D06ec0c26-a899-4651-8f52-a6caa47b943d%26RedirectType%3Dsafetynet%26IssueTime%3D1605125991%26Hash%3Db98a3ba73613e93175e273b0e62d9e95187de49bcda0b087f7d8408b62805eaf; _gat=1; _tls=*.666521,666523..8991435802738993200; _tlv=3.1605100952.1605121669.1605126002.8.2.3'
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

                if 'result' in resultDict_request['api']:
                        resultHoraires = resultDict_request['api']['result']['performanceList']
                else:
                        resultHoraires = 'Error'

                return resultHoraires


        def printHoraires(self,resultDict_horaires):
                for horaire in resultDict_horaires:
                        print('date - {date} | horaire - {heure} | nb_places_dispo - {nb}/{nb_total}'.format(date=horaire['perfDate'],heure=horaire['perfTime'], nb=horaire['available'], nb_total=horaire['total']))


        def saveInFile_getHoraires(self,resultDict_horaires,mode='a+'):
                dateNow = datetime.datetime.now().strftime('%Y_%m_%d')
                timeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                filename = 'results_get_at_' + dateNow + '.txt'
                insertTime = timeNow + ':\n'

                file = open(filename,mode)
                file.write(insertTime)

                if resultDict_horaires == 'Error':
                        file.write('Error to get data for this date, Check : There is no more ticket for this date or Louvre is closed ?\n')
                else :
                        for horaire in resultDict_horaires:
                                file.write('date - {date} | horaire - {heure} | nb_places_dispo - {nb}/{nb_total}\n'.format(date=horaire['perfDate'],heure=horaire['perfTime'], nb=horaire['available'], nb_total=horaire['total']))

                file.close()


        def getListDates(self,date,nb_days):
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

                print(listDates)

                return listDates


if __name__ == "__main__": 
        print('input a date(format aaaa-mm-dd):')
        selectedDate = input()
        print('input nb days:')
        nb_days = int(input())

        h = HorairesLouvre()
        listDates = h.getListDates(date=selectedDate,nb_days=nb_days)
        for date in listDates:
                resultDict_horaires = h.getHoraires_BilletGroupLouvre(date)
                h.saveInFile_getHoraires(resultDict_horaires,'a+')
