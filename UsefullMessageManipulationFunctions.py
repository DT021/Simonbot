import json


def replace_special_romanian_characters(message):
    message = message.replace(u"\u00c8\u0099", "s")
    message = message.replace(u"\u00c8\u009b", "t")
    message = message.replace("u\u00c4\u0083", "a")
    message = message.replace(u"\u00c3\u00ae", "i")
    message = message.replace(u"\u00c3\u00a2", "a")
    message = message.replace(u"\u00c8\u0099", "s")
    message = message.replace(u"\u00c4\u0083", "a")
    message = message.replace(u"\u00f3\u00be\u008c\u00a7", "heart eye emojy")
    message = message.replace(u"\u00f0\u009f\u0098\u0089", ";)")
    message = message.replace(u"\u00f0\u009f\u0098\u0098", ":*")
    message = message.replace(u"\u00f0\u009f\u0098\u0082", ":))")
    message = message.replace(u"\u00f0\u009f\u0098\u00b1", ":o")
    message = message.replace(u"\u00c5\u0084", "n")
    message = message.replace(u"\u00f3\u00be\u008c\u00b5", ":)")

    #    message = message.replace(u"", "")
    return message

def return_messages_from_json_file(file):
    data = json.load(open(file))
    message_list = data['messages']
    message_list.reverse()

    lista_mesaje = []
    lista_authors = []
    old_sender = message_list[0]['sender_name']
    old_message = ""
    old_timestap = int(message_list[0]['timestamp_ms'])

    for mesaj in message_list:
        if "content" in mesaj:
            sender = mesaj['sender_name']
            message = replace_special_romanian_characters(mesaj['content'])
            timestamp = int(mesaj['timestamp_ms'])

            if sender == old_sender and timestamp-old_timestap < 3600000:
                old_message += message + " "

            else:
                lista_mesaje.append(old_message)
                lista_authors.append(old_sender)
                old_sender = sender
                old_message = message + " "
                old_timestap = timestamp

    return [lista_authors, lista_mesaje]

message_file = "C:/Users/sular/Desktop/message_1.json"
for message in zip(return_messages_from_json_file(message_file)[0],return_messages_from_json_file(message_file)[1]):
    print(message)