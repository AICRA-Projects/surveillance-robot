import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_PWM_1 = 12
GPIO_PWM_2 = 13
GPIO_IN1 = 23
GPIO_IN2 = 16
GPIO_IN3 = 20
GPIO_IN4 = 21
#GPIO.setwarnings(False)
GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)
GPIO.setup(GPIO_IN3, GPIO.OUT)
GPIO.setup(GPIO_IN4, GPIO.OUT)
GPIO.setup(GPIO_PWM_1, GPIO.OUT)
GPIO.setup(GPIO_PWM_2, GPIO.OUT)

pi_pwm_1 = GPIO.PWM(GPIO_PWM_1,1000)
pi_pwm_1.start(0)
pi_pwm_2 = GPIO.PWM(GPIO_PWM_2,1000)
pi_pwm_2.start(0)
while True:
    for i in range(0,100,1):
        pi_pwm_1.ChangeDutyCycle(i)
        pi_pwm_2.ChangeDutyCycle(i)
        GPIO.output(GPIO_IN1, True)
        GPIO.output(GPIO_IN2, False)
        GPIO.output(GPIO_IN3, True)
        GPIO.output(GPIO_IN4, False)

GPIO.cleanup()
