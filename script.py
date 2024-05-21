import schedule
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuración del cliente de Slack con tu token de acceso
slack_token = "token-bot-slack"
client = WebClient(token=slack_token)

# Menús por día y horario
menus = {
    "Lunes": {
        "08:00": "Yakult",
        "09:00": "Desayuno: 2/3 pzas de huevo, 2 rebanadas de jamón, Salsa, 2 tortillas de maíz",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Cortadillo de res, 2C/5 cortadillo, 300 gr, Salsa/cebolla/champiñones/chile morrón, 3 tortillas de maíz",
        "16:30": "Colación: 1 taza piña",
        "18:00": "Colación: Té canela, Crisp Kellogs",
        "20:00": "Cena: Tostadas de cortadillo, 3 tostadas horneadas, 3C cortadillo, Salsa/cebolla"
    },
    "Martes": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Pan tostado, 1 rebanada de pan, mantequilla/mermelada, Café, 1/2 taza leche light",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Pescado empapelado, 2 filetes de pescado, 1C mantequilla, Mostaza/pimienta, calabacitas, 3 papa salmas",
        "15:30": "Colación: 1 taza sandía",
        "18:00": "Colación: Té canela, Crisp Kellogs",
        "20:00": "Cena: Queso en salsa, 80 gr queso panela, Salsa/cebolla/chile morrón/cilantro/pimienta, 3 tostadas horneadas"
    },
    "Miércoles": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Huevo, 2/3 pzas de huevo, Chorizo, Salsa, 2 tortillas de maíz",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Bistec a la mexicana, Carne de res magra 250-300 gr, Salsa/cebolla/champiñones/chile morrón, 3 tortillas de maíz",
        "16:30": "Colación: 1 taza piña",
        "18:00": "Colación: Té canela, Crisp Kellogs",
        "20:00": "Cena: Tostadas de pollo, 3 tostadas horneadas, 80 gr pollo deshebrado, 1C crema, Lechuga/cebolla"
    },
    "Jueves": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Pan tostado, 1 rebanada de pan, mantequilla/mermelada, Café, 1/2 taza leche light",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Tostada de atún, 3 tostadas horneadas, 80 gr atún en agua, Verdura al gusto, 1C mayonesa, 3 tortillas de maíz",
        "16:30": "Colación: 1 taza sandía",
        "18:00": "Colación: Té canela, Crisp Kellogs",
        "20:00": "Cena: Chilaquiles, 80 gr queso panela, 3 tostadas horneadas, Salsa/cebolla/chile morrón"
    },
    "Viernes": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Migas con huevo, 3 tortillas de maíz, 2/3 pzas de huevo",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Bistec a la mexicana, Carne de res magra 250-300 gr, Salsa/cebolla/champiñones/chile morrón, 3 tortillas de maíz",
        "16:30": "Colación: 1 taza piña",
        "18:00": "Colación: Té canela, Crisp Kellogs",
        "20:00": "Cena: Tostadas de pollo, 3 tostadas horneadas, 80 gr pollo deshebrado, 1C crema, Lechuga/cebolla"
    },
    "Sábado": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Pan tostado, 1 rebanada de pan blanco, 1 rebanada de pan integral, 3/3 pzas de huevo, Salsa, 3 rebanadas de jamón",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Tostada a la Siberia, Sin consomé en el poste",
        "16:30": "Colación: 1 mandarina",
        "18:00": "Colación: 1 puño de Sabritas",
        "20:00": "Cena: Tacos de bistec, 4 piezas, 1 sola tortilla en taco, Sin papa galeana",
        "23:00": "Colación: Pastilla"
    },
    "Domingo": {
        "08:00": "Yakult",
        "09:00": "Desayuno: Pan tostado, 1 rebanada de pan blanco, 5 tacos de barbacoa",
        "11:30": "Colación: 1 paleta coronado",
        "13:30": "Colación: 1 mandarina",
        "14:00": "Comida: Alitas, 1 papa",
        "16:30": "Colación: 1 mandarina",
        "18:00": "Colación: 1 puño de Sabritas",
        "20:00": "Cena: Tacos de bistec, 4 piezas, 1 sola tortilla en taco, Sin papa galeana",
        "23:00": "Colación: Pastilla"
    }
}

def send_message(channel, text):
    try:
        response = client.chat_postMessage(channel=channel, text=text)
        print(f"Mensaje enviado: {text}")
    except SlackApiError as e:
        print(f"Error enviando mensaje: {e.response['error']}")

def schedule_messages():
    for day, times in menus.items():
        for time_str, menu in times.items():
            if day == "Lunes":
                schedule.every().monday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")
            elif day == "Martes":
                schedule.every().tuesday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")
            elif day == "Miércoles":
                schedule.every().wednesday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")
            elif day == "Jueves":
                schedule.every().thursday.at(time_str).do(send_message, channel="#prueba", text=f"{day} {time_str} - {menu}")
            elif day == "Viernes":
                schedule.every().friday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")
            elif day == "Sábado":
                schedule.every().saturday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")
            elif day == "Domingo":
                schedule.every().sunday.at(time_str).do(send_message, channel="#nombre-canal-slack", text=f"{day} {time_str} - {menu}")

schedule_messages()

while True:
    schedule.run_pending()
    time.sleep(1)
