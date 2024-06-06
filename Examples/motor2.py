# from MSPy import MSPy
from yamspy import MSPy
import redis
import time
import signal
import sys 
import threading

redis_host = 'localhost'
redis_port = 6379
redis_channel = 'motors:speed'

# Définir le port série correspondant à votre contrôleur de vol
serial_port = 'COM3'  # Remplacez par votre port série

# Connexion à REDIS
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
pubsub = redis_client.pubsub()
pubsub.subscribe(redis_channel, "motors:stop")


# Initialiser la connexion MSPy avec le contrôleur de vol
board = MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200)

print(f"Listening for messages on channel: {redis_channel}")


with board:
  # Initialiser la connexion MSPy avec le contrôleur de vol
  
  # Lire les informations du contrôleur de vol pour vérifier la connexion
  # board.send_RAW_msg(MSPy.MSPCodes['MSP_API_VERSION'], data=[])
  # response = board.receive_msg()
  # if response:
  #     print(f"API Version: {response['API_VERSION']}")
  
  # Écouter les messages publiés sur le canal 'motors'
  for message in pubsub.listen():
    
    print(f"Received message: {message}")
    
    if message['type'] == 'message':

      if message['channel'] == 'motors:stop':
        print("Received stop command. Exiting the app.")

        motor_values = list(map(int, "1000,1000,1000,1000".split(',')))
        print(f"Sending STOP motor values: {motor_values}")
        
        # Préparer les données pour la commande MSP_SET_MOTOR
        motor_data = []
        for value in motor_values:
            motor_data.append(value & 0xFF)
            motor_data.append((value >> 8) & 0xFF)
        
        # Envoyer les valeurs des moteurs
        board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_MOTOR'], data=motor_data)
        response = board.receive_msg()
        if response:
            print("Motor values set successfully")
        else:
            print("Failed to set motor values")
                
        sys.exit()
      else:
      
        if message['type'] == 'message':
            motor_values = list(map(int, message['data'].split(',')))
            print(f"Received motor values: {motor_values}")
            
            # Préparer les données pour la commande MSP_SET_MOTOR
            motor_data = []
            for value in motor_values:
                motor_data.append(value & 0xFF)
                motor_data.append((value >> 8) & 0xFF)
            
            # Envoyer les valeurs des moteurs
            board.send_RAW_msg(MSPy.MSPCodes['MSP_SET_MOTOR'], data=motor_data)
            response = board.receive_msg()
            if response:
                print("Motor values set successfully")
            else:
                print("Failed to set motor values")
                