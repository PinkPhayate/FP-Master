import bug_process_merger as bg
import sys
import configparser

# set environment lab or home
inifile = configparser.SafeConfigParser()
inifile.read('./../../config.ini')
ENV = inifile.get('env', 'locale')
METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/'
derby_version = ['10.8.1.2', '10.9.1.0', '10.10.1.1', '10.11.1.1']
solr_version = ['4.1.0', '4.2.0', '4.3.0', '4.4.0', '4.5.0']

if __name__ == '__main__':
    # args = sys.argv
    # if 1 < len(args):
    #     target = metrics_dir[1]
    # else:
    #     return
    for elm in solr_version:
        filename = METRICS_DIR + 'Solr/bug/slr_' + elm + '_bgmd.csv'
        bug_list = bg.get_bug_list_solr(filename)
        print('version : ' + elm)
        print('numOfBug: ' + str(len(bug_list)))

    for elm in derby_version:
        filename = METRICS_DIR + 'Derby/bug/' + elm + '-buglist.csv'
        bug_list = bg.get_bug_list_derby(filename)
        print('version : ' + elm)
        print('numOfBug: ' + str(len(bug_list)))
