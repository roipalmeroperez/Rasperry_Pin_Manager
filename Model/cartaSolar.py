import math
import calendar

def dayOfYear(dateStr):
    days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    txt = dateStr.split('/')
    day = int(txt[0])
    month = int(txt[1])
    year = int(txt[2])
    if calendar.isleap(year) and month > 2:
        return days[month - 1] + day + 1
    else:
        return days[month - 1] + day

def carta(lat, lon, date):
    print("Lat: " + str(lat) + ", Lon: " + str(lon))
    horaMedicion = 10.5
    day = dayOfYear(date)
    #Latitud en radianes
    latRad = lat*math.pi/180
    # Calculo de la variable auxiliar
    x = 2 * math.pi * (day - 1 + (horaMedicion - 12) / 24) / 365
    # Calculo de declinación en radianes
    declinationRad = (0.006918-0.399912*math.cos(x)+0.070257*math.sin(x)
                    -0.006758*math.cos(2*x)+0.000907*math.sin(2*x)
                    -0.002697*math.cos(3*x)+0.001480*math.sin(3*x))
    declinationDec = declinationRad * 180 / math.pi
    # Cálculo de ascensión recta a la hora medida
    omegaRad = horaMedicion * math.pi / 12 - math.pi
    omegaDec = omegaRad * 180 / math.pi
    # Cálculo de altura y acimut
    elevationRad = math.asin(math.cos(latRad)*math.sin(omegaRad)*math.cos(declinationRad)
                             +math.sin(latRad)*math.sin(declinationRad))
    elevationDec = elevationRad * 180 / math.pi
    azimuthRad = math.acos((math.cos(latRad)*math.sin(declinationRad)
                          -math.cos(omegaRad)*math.sin(latRad)*math.cos(declinationRad))
                         /math.cos(elevationRad))
    azimuthDec = azimuthRad * 180 / math.pi
    
    print('Declinación: ' + str(declinationDec))
    print('Ascensión recta: ' + str(omegaDec))
    print('Elevación: ' + str(elevationDec))
    print('Acimut: ' + str(azimuthDec))
    


if __name__ == '__main__':
    #latitudeStr = input("Introduzca la latitud: ")
    #longitudeStr = input("Introduzca la longitud: ")
    dateStr = input("Introduzca el día a medir (dd/mm/yyyy): ")
    #print(dayOfYear(dateStr))
    #carta(float(latitudeStr), float(longitudeStr), dateStr)
    carta(43.35, -8.42, dateStr)