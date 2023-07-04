import json

#conf_file = open('config.json')
#conf = json.loads(pin_conf_file.read())

if __name__ == '__main__':
    # Tests
    conf_file = open('../config.json')
    conf = json.loads(conf_file.read())
    
    historicDao=__import__(conf["HISTORIC_DAO_NAME"])
    
    historicDao.doSelect()