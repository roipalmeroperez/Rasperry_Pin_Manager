# Imports
import utils

# Configuration
conf = utils.getGeneralConfiguration()

# Implementation
cameraImpl = __import__(conf["CAMERA_IMPL_NAME"])

def takeFoto(route, name):
	cameraImpl.takeFoto(route, name)

if __name__ == '__main__':
	takeFoto('./', 'foto.jpg')
