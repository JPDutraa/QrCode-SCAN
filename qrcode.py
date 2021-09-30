from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
import pygame


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="resultado.csv", help="")
args = vars(ap.parse_args())


print("[INFO] Iniciando...")
vs = VideoStream(src=0).start()

time.sleep(2.0)


csv = open(args["output"], "w")
found = set()

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=800)


    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        if barcodeData not in found:
            pygame.mixer.init()
            pygame.mixer.music.load('success.mpeg')
            pygame.mixer.music.play()
            print('QRCode Capturado')

            csv.write("{};{}\n".format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M'), barcodeData))
            csv.flush()

            found.clear()
            found.add(barcodeData)

    cv2.imshow("Registro de Ponto", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

print("[INFO] Finalizando...")
csv.close()
cv2.destroyAllWindows()
vs.stop()