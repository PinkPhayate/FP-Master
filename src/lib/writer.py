import datetime
import locale
METRICS_DIR = '/Users/phayate/Dropbox/STUDY/Euromicro'
def write_report( list ):
    d = datetime.datetime.today()
    with open(METRICS_DIR + '/result10000.csv', mode = 'a', encoding = 'utf-8') as fh:
        fh.write( d.strftime("%x %X") + '\n' )
        for line in list:
            print(line)
            fh.write(line + ',')
        fh.write( '\n' )
