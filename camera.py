import picamera


def takeFoto(route, name):
	camera = picamera.PiCamera()
	camera.resolution = (1024, 768)
	camera.capture('' + route + name)
	camera.close()

if __name__ == '__main__':
	takeFoto('./', 'foto.jpg')
