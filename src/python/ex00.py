import ex01
import configparser
import time
from multiprocessing import Process
from multiprocessing import Pool
inifile = configparser.SafeConfigParser()
inifile.read('./config.ini')
ENV = inifile.get('env', 'locale')


def apply_derby_ex01():

    ex01.TARGET = 'Derby'
    ex01.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
    ex01.exp_derby()

def apply_solr_ex01():
    ex01.TARGET = 'Solr'
    ex01.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
    ex01.exp_solr()

if __name__ == '__main__':
    start = time.time()
    ex01.PRED_TYPE = 'rf'
    ex01.ITER = 5
    jobs = []
    job = Process(target=apply_derby_ex01)
    jobs.append(job)
    job.start()

    job = Process(target=apply_solr_ex01)
    jobs.append(job)
    job.start()

    [job.join() for job in jobs]

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
