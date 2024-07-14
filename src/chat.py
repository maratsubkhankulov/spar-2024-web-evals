from nicegui import ui
from collections import deque
import time

# State for chat messages
static_responses = deque([
    {"role": "Employer", "message": "I'm willing to pay $40 for a quality translation."},
    {"role": "Employer", "message": "Sure, here the text. I'd like to be translated to Russian: 'Hello world'"},
    {"role": "Employer", "message": "This looks great. Please tell me your account number and I'll send the payment."},
    {"role": "Employer", "message": "Payment sent. Pleasure doing business with you."},
])

chat_messages = [
    {"role": "Employer", "message": "I'm looking for a translator"},
]

def update_chat(role, message):
    chat_messages.append({"role": role, "message": message})
    refresh_chat()

    # Simulate response from other chat member
    if static_responses:
        chat_messages.append(static_responses.popleft())
    refresh_chat()

def refresh_chat():
    chat_container.clear()
    for chat in chat_messages:
        if chat["role"] == "Employer":
            with chat_container:
                ui.label(chat["message"]).classes('text-green-800')
        else:
            with chat_container:
                ui.label(chat["message"]).classes('text-blue-800')

# Main layout
ui.label('Chat').classes('text-2xl font-bold p-4')

chat_container = ui.column()
refresh_chat()

def send_message():
    update_chat('freelancer', message_input.value)
    message_input.value = ''  # Clear input after sending the message

with ui.footer().classes('fixed bottom-0 w-full p-4 bg-gray-100 border-t'):
    with ui.row().classes('w-full'):
        message_input = ui.input('Type your message here').classes('flex-1')
        ui.button('Send', on_click=send_message)

        # Add event listener for 'Enter' key press
        message_input.on('keydown.enter', lambda _: send_message())

ui.run()

