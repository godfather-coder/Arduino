import pyautogui
import serial




serial_port = serial.Serial('COM3', 9600)  # Replace 'COM3' with your Arduino port


ball_speed=40

# Move the mouse to coordinates (x, y)
x = 100
y = 100
while True:
    if serial_port.in_waiting > 0:
        try:
            data = serial_port.readline().decode('utf-8').strip()
            x1, y1, sw, _, _, _ = map(int, data.split(','))
            x += x1 * ball_speed
            y += y1 * ball_speed
            pyautogui.moveTo(x, y)
            print(x,y)
            if sw == 0:
                break
        except:
            continue
