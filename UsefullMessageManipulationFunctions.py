import json


def replace_special_romanian_characters(message):
    message = message.replace(u"\u00c8\u0099", "s")
    message = message.replace(u"\u00c8\u009b", "t")
    message = message.replace("u\u00c4\u0083", "a")
    message = message.replace(u"\u00c3\u00ae", "i")
    message = message.replace(u"\u00c3\u00a2", "a")
    message = message.replace(u"\u00c8\u0099", "s")
    message = message.replace(u"\u00c4\u0083", "a")
    message = message.replace(u"\u00f3\u00be\u008c\u00a7", "hearteyemojy ")
    message = message.replace(u"\u00f0\u009f\u0098\u0089", "WinkEmojy ")
    message = message.replace(u"\u00f0\u009f\u0098\u0098", "KissEmojy ")
    message = message.replace(u"\u00f0\u009f\u0098\u0082", "LaughEmojy ")
    message = message.replace(u"\u00f0\u009f\u0098\u00b1", "Shockedemojy ")
    message = message.replace(u"\u00c5\u0084", "n")
    message = message.replace(u"\u00f3\u00be\u008c\u00b5", "smileEmojy ")

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

            if "http" in message:
                continue

            if sender == old_sender and timestamp-old_timestap < 3600000 and (len(old_message.split(" ")) < 20):
                old_message += message + " "
            elif len(old_message.split(" ")) < 50:
                lista_mesaje.append(old_message)
                lista_authors.append(old_sender)
                old_sender = sender
                old_message = message + " "
                old_timestap = timestamp

    return [lista_authors, lista_mesaje]

