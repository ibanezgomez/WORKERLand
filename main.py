#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim :set tabstop=4 expandtab shiftwidth=4 softtabstop=4

import os, signal, time, json
from subprocess import *
from datetime import date, datetime

from utils.asciiart.art import *
from utils.logger import log
from utils.daemon import Daemon
from utils.scheduler import Job, Scheduler

CFG_FILE="config.json"

def signal_handler(signal, frame):
    # ToDo: Clean everithing
    log.debug("Exiting...")
    exit(0)

def workersChecker():
    for name in config['workers']:
        log.info("Status of %s: %s" % (workers[name]['instance'].getDisplayName(), workers[name]['instance'].getStatus()))
    return True

def workersAreWorking():
    res=False
    for name in config['workers']:
        status=workers[name]['instance'].getStatus()
        if status not in [0, 2]: 
            res=True
            break
    return res

def workersHaveFinished():
    for name in config['workers']:
        log.info("Result of %s: %s" %(workers[name]['instance'].getDisplayName(),  workers[name]['instance'].getResult()))
    return True

if __name__ == "__main__":
    with open(CFG_FILE) as c:
        config=json.load(c)
        scheduler = Scheduler()
        scheduler.start()
        signal.signal(signal.SIGINT, signal_handler)
        print(text2art('-----------------------\n    Welcome   to   ' + config['general']['name'] + "   " + config['general']['version'] + '\n-----------------------'))
        log.debug("Starting %s v%s" % (config['general']['name'], config['general']['version']))
        # Main loop waiting & polling
        workers = {}
        for worker in config['workers']:
            workers[worker] = {'import': None, 'config': None, 'instance': None}
            workers[worker]['config'] = config['workers'][worker]
            log.info("Loading worker module: %s", worker)
            log.debug("Loading worker %s config. from properties file: %s" % (worker, workers[worker]['config']))
            workers[worker]['import'] = __import__('modules.workers.' + worker, fromlist=[worker])
            workers[worker]['instance'] = workers[worker]['import'].Worker(workers[worker]['config'])
            workers[worker]['instance'].setWorkerStatus(-1)
            Daemon(workers[worker]['instance'].start).start()
        scheduler.addJob('WorkChecker', Job(workersChecker, {}, min=range(0, 60, 1)))  # se ejecuta cada 1 minuto
        while workersAreWorking(): 
            log.info("Waiting to finish...")
            time.sleep(10)  
        log.info("All the workers have finished")
        scheduler.deleteJob('WorkChecker')
        workersHaveFinished()
    exit()