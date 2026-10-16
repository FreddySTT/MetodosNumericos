import cv2
from modules.alertas_fatiga.detector import analizar_frame

def iniciar_camara():
    cap = cv2.VideoCapture(0)
    print("Iniciando cámara... Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        cv2.putText(frame, "Monitoreo de Fatiga Activo", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Detector de Fatiga - Camara", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    iniciar_camara()