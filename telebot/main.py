# -*- coding: utf-8 -*-

import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
import random


TOKEN = '151950361:AAGcOuZWBymSLXm_nir2TgmUJkbJtf1WYYs' #Token mio
TOKEN = '239992585:AAG3iAzFMXPcZQ5__-HQYk_8BgyaxHopX3w' #Token bot tdrc

#IDs favoritas:

MI_ID = 21888782

#Las almacenamos en un array:
ID_favs=[MI_ID]

#Definimos el bot al que vamos a llamar:
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

#Variables globales necesarias para el bot

opciones_menu=['Surprise','Imagen','Iniciar Juego','About']
pad={'delante':'Avanzo adelante','derecha':'Giro a la derecha','izquierda':'Giro a la izquierda','mediavuelta':'Doy media vuelta', 'reboot':'Reiniciar Juego', 'salir':'Salir del juego'}
mapa=[pad['derecha'],pad['derecha'], pad['izquierda'], pad['delante'], pad['delante'], pad['derecha']] #Solución al laberinto
pasos={} #Guardamos el paso por el que va el jugador
posibles_respuestas_muerte=['Te encuentras un gato y lo sigues, al final terminas perdida',
                            'Si es que no paras de liarla..., anda Reinicia otra vez',
                            'Escuchas una llamada de socorro, cuando vas, era una trampa, te capturan como esclava',
                            'Te encuentras con tu cantante favorito cantando, te encandila y te quedas tan embobada que el tiempo pasa y olvidas tu cometido',
                            'Aparece Taylor Swift liándose con Justin Bieber.\nDe repente tienes un báte, y no dudas en usarlo.\nTe pillan y vas a la cárcel',
                            'Esto es, cómo no, un juego muy troll, mueres.\n...\n¿Por qué dices?¿Denunciar?\nEmmmm...Ummmm...Veamos...\nAh, sí, vaya..., te acaba de caer un rayo, lo sentimos mucho.\nAtentamente: El presidente de la empresa'
                            ]
posibles_respuestas_vida=['Te encuentras en una bonita habitación con maravillosas vistas',
                            'Te encuentras en una habitación con 3 puertas',
                            'Encuentras una imagen que te resulta familiar.\nTe paras a mirarla y te gusta.\nContinuas con tu camino.',
                            'Hay un cartel en el que pone un número\n22...\n¿Qué significará?','Estás leyendo esto esperando a que te describa una situación, pero esta vez la tendrás que poner tú, ya que estás en el mejor sitio del mundo para ti',
                            'Esta habitación no es buena, pero aún tienes escapatoria, el techo lleno de pinchos está bajando, corre.',
                            'Oyes un mensaje: \n"¿Aún sigues vivo?, no estarás haciendo trampas... ¿no?"'
                            ]

#############################################
#Funciones auxiliares





#Funcion disegnada para orientar el juego, viendo que ocurre en cada paso
#Es la funcion que parsea las opciones
#Si el usuario no esta dentro del registro, lo metemos y ponemos el juego a cero
def process_menu_step(message):
    global pasos
    try:
        chat_id = message.chat.id #Coger el identificador del chat, es único
        texto = message.text
        """
        if (texto == opciones_menu[0]) :    #Surprise
            command_noly(message)
        elif (texto == opciones_menu[1]):   #Imagen
            command_imagen(message)
        el
        """
        #Cojo el texto y lo compruebo
        if (texto == opciones_menu[2]):   #Game
            if not (chat_id in pasos):
                pasos[chat_id]=0
            command_game(message)
        elif (texto == opciones_menu[3]):
            command_about(message)
        """
        else:
            raise Exception()
        """
    except Exception as e:
        bot.reply_to(message, 'oooops')













#Función de desarrollo del juego. El propio juego
def process_game_step(message):
    global pasos
    #Respuestas posibles al usuario
    r_muerte=random.choice(range(len(posibles_respuestas_muerte)))
    r_vida=random.choice(range(len(posibles_respuestas_vida)))
    try:
        chat_id = message.chat.id
        texto = message.text
        #Aumento el numero de pasos
        pasos[chat_id]+=1
        #print str(pasos[chat_id])+'\n'
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for arrow in pad:
            markup.add(pad[arrow])

        # Winner
        if pasos[chat_id]==len(mapa)+1:
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Recoger premio')
            msg = bot.send_message( chat_id, '¡Enhorabuena!\nHas superado el juego.\nRecoge tu premio.', reply_markup=markup)
            bot.register_next_step_handler(msg, premio)
        # Good Answer or reboot
        #Filtramos la respuesta
        elif(texto == mapa[pasos[chat_id]-1] or texto == pad['reboot'] or texto == pad['salir']):
            if (texto == pad['delante']):
                msg = bot.send_message( chat_id, 'Has avanzado hacia delante\n'+posibles_respuestas_vida[r_vida]+'\n¿Hacia dónde irás?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_game_step)
            elif (texto == pad['derecha']):
                msg = bot.send_message( chat_id, 'Has girado a la derecha\n'+posibles_respuestas_vida[r_vida]+'\n¿Hacia dónde irás?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_game_step)
            elif (texto == pad['izquierda']):
                msg = bot.send_message( chat_id, 'Has girado a la izquierda\n'+posibles_respuestas_vida[r_vida]+'\n¿Hacia dónde irás?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_game_step)
            elif (texto == pad['mediavuelta']):
                msg = bot.send_message( chat_id, 'Has vuelto atrás\n'+posibles_respuestas_vida[r_vida]+'\n¿Hacia dónde irás?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_game_step)
            elif (texto == pad['reboot']):
                pasos[chat_id]=0
                msg = bot.send_message( chat_id, 'Juego Reiniciado\n'+posibles_respuestas_vida[r_vida]+'\n¿Hacia dónde irás?', reply_markup=markup)
                bot.register_next_step_handler(msg, process_game_step)
            elif (texto == pad['salir']):
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.add('Volver al menú')
                msg = bot.send_message( chat_id, 'Has salido del juego', reply_markup=markup)
            else:
                raise Exception()
                #Lanza excepcion si el texto no esta en las opciones
        # Bad answer
        elif texto in pad.values():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add(pad['reboot'])
            pasos[chat_id]=0
            msg = bot.send_message( chat_id, posibles_respuestas_muerte[r_muerte], reply_markup=markup)
            bot.register_next_step_handler(msg, process_game_step)

    except Exception as e:
        bot.reply_to(message, 'Te has salido del juego')

#############################################
#Listener
def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        cid = m.chat.id # Almacenaremos el ID de la conversación.
        print "[" + str(cid) + "]: " + m.text # Y haremos que imprima algo parecido a esto -> [52033876]: /start

bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.



#############################################
#Funciones que encontramos en el menú


#@bot.message_handler(commands=['imagen']) # Indicamos que lo siguiente va a controlar el comando '/imagen'.
def command_imagen(m): # Definimos una función que resuelva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_photo( cid, open( '../imagenes/imagen.png', 'rb')) # Con la función 'send_photo()' del bot, enviamos al ID de la conversación que hemos almacenado previamente la foto de nuestro querido :roto2:

#@bot.message_handler(commands=['noly']) # Indicamos que lo siguiente va a controlar el comando '/noly'
def command_noly(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    bot.send_message( cid, 'Buenas preciosa') # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.

# Función encargada de Iniciar el juego, dando las instrucciones.
def command_game(m):
    cid = m.chat.id
    #Genero el teclado
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    #markup.add('Surprise','Imagen')
    for arrow in pad:
        markup.add(pad[arrow])
    #Le explico al usuario el juego en la linea siguiente
    msg = bot.send_message( cid, 'Estás en un lugar desconocido.\nTu misión es encontrar el tucán mágico, el cual te concederá un deseo.\n¿Hacia dónde irás?', reply_markup=markup)

    bot.register_next_step_handler(msg, process_game_step)

# Función que nos da información del creador.
def command_about(m):
    cid = m.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Volver al menú')
    msg = bot.send_message( cid, 'Este juego ha sido creado y desarrollado por @neon_520\nInspirado en una persona muy especial\nversión 22.3.16', reply_markup=markup)


# Si ganas el juego ejecutas esto:
def premio(m):
    cid = m.chat.id
    pasos[cid]=0
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Volver al menú')#Para que empiece todo otra vez
    bot.send_photo(cid, open( '../imagenes/imagen.png', 'rb'),'Enséñaselo al que te proporcionó el juego',reply_markup=markup)
    #El premio del juego es una imagen

#############################################
#Función menú

#Listener que cuando le escribo algo que pasa con ese filtro me responde
@bot.message_handler(func=lambda message: not (message.text == 'Recoger premio') and not (message.text in opciones_menu) and not (message.text in pad.keys()) and not (message.text in pad.values())) #dejamos que acepte todo, menos las opciones del menú
#@bot.message_handler(commands=['menu','start'])
def command_menu(m):
    cid = m.chat.id
    #Cambio el teclado por el teclado de telegram
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(opciones_menu[-2])
    markup.add(opciones_menu[-1])
    """
    for opcion in opciones_menu:
        markup.add(opcion)
    """
    #Con la siguiente linea puedo enviar un mensaje
    msg = bot.send_message( cid, 'Hola buenas '+str(m.chat.username)+'.\n¿Deseas comenzar tu aventura?', reply_markup=markup)
    #Con la siguiente linea hacemos que la respuesta anterior se procesa en la función process_menu_step
    bot.register_next_step_handler(msg, process_menu_step)



#############################################
#Peticiones
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.
