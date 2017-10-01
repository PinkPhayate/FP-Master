import ex01
import ex01_threshold
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

def apply_derby_ex01_threshold():
    ex01_threshold.TARGET = 'Derby'
    ex01_threshold.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
    ex01_threshold.exp_derby()

def apply_solr_ex01_threshold():
    ex01_threshold.TARGET = 'Solr'
    ex01_threshold.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
    ex01_threshold.exp_solr()

if __name__ == '__main__':
    start = time.time()
    ex01_threshold.PRED_TYPE = 'rf'
    ex01_threshold.ITER = 100
    jobs = []
    # job = Process(target=apply_derby_ex01)
    job = Process(target=apply_derby_ex01_threshold)
    jobs.append(job)
    job.start()

    # job = Process(target=apply_solr_ex01)
    job = Process(target=apply_solr_ex01_threshold)
    jobs.append(job)
    job.start()

    [job.join() for job in jobs]

    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
