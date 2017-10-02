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

rep = ex01
def wrapper_exp(arg1, arg2):
    rep.exp(arg1, arg2)

def main():
    start = time.time()
    derby_tuple = (('10.8', '10.9'), ('10.9', '10.10'))
    solr_tuple  = (('4.1.0', '4.2.0'),
                   ('4.2.0', '4.3.0'),
                   ('4.3.0', '4.4.0'),
                   ('4.4.0', '4.5.0'))
    rep.PRED_TYPE = 'rf'
    rep.ITER = 5
    jobs = []

    rep.TARGET = 'Derby'
    rep.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Derby/all'
    for t in derby_tuple:
        job = Process(target=wrapper_exp, args=t)
        jobs.append(job)
        job.start()

    rep.TARGET = 'Solr'
    rep.METRICS_DIR = '/Users/'+ENV+'/Dropbox/STUDY/Metrics/Solr/all'
    for t in solr_tuple:
        job = Process(target=wrapper_exp, args=t)
        jobs.append(job)
        job.start()

    [job.join() for job in jobs]
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

if __name__ == '__main__':
    main()
    # start = time.time()
    # ex01.PRED_TYPE = 'rf'
    # ex01.ITER = 5
    # jobs = []
    # job = Process(target=apply_derby_ex01)
    # jobs.append(job)
    # job.start()
    #
    # job = Process(target=apply_solr_ex01)
    # jobs.append(job)
    # job.start()
    #
    # [job.join() for job in jobs]
    #
    # elapsed_time = time.time() - start
    # print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
