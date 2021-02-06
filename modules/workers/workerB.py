from utils.logger import log
import os, time, random

name         = 'workerA'
display_name = 'Worker A'

class Worker:
    baseurl = "https://www.workerX.com/api/"
    desc    = "Generic description"
    status  = -1
    result  = ""

    def __init__(self, *kwargs):
        try:
            if "baseurl" in kwargs[0]: self.baseurl = str(kwargs[0]['baseurl'])
            if "desc" in kwargs[0]: self.desc = str(kwargs[0]['desc'])
            log.info("Loaded worker: %s Worker with values: name=%s, display_name=%s, desc=%s baseurl=%s" % (self.getName(), self.getName(), self.getDisplayName(), self.getDescription(), self.getBaseUrl()))
        except Exception as e:
            log.error("Error loadding Worker", exc_info=e)

    def getName(self):
        return name
    
    def getDisplayName(self):
        return display_name
    
    def getDescription(self):
        return self.desc
    
    def getStatus(self):
        return self.status

    def getBaseUrl(self):
        return self.baseurl

    def getResult(self):
        return self.result

    def start(self):
        if self.onStartWork():
            if self.onWork():
                if self.setResult(): return self.onWorkFinished()
        return self.onFailureWork()

    def setResult(self):
        log.debug('[setResult] %s' % self.getDisplayName())
        self.result = "Work finished, time for a beer ;-)"
        return True

    def onStartWork(self):
        log.debug('[onStartWork] %s' % self.getDisplayName())
        return True

    def onWork(self):
        log.debug('[onWork] %s' % self.getDisplayName())
        self.setWorkerStatus(1)
        tasks=random.randrange(60, 80, 2)
        log.info("Worker %s has %s taks" % (self.getName(), str(tasks)))
        for task in range(0, tasks):
            log.info("Doing task #%s" % (str(task)))
            time.sleep(random.randrange(1, 4))
        return True
    
    # Status values:
    #   -1 - Configuring job
    #    0 - Finished with error
    #    1 - In progresss
    #    2 - Finished with success
    def setWorkerStatus(self, status):
        log.debug('[setWorkerStatus] %s' % self.getDisplayName())
        self.status=status
        return True

    def onWorkFinished(self):
        log.info('[onFinishedScan] %s' % display_name)
        self.setWorkerStatus(2)
        return True

    def onFailureWork(self):
        log.error('[onFailureScan] %s' % display_name)
        self.setWorkerStatus(0)
        return True

