import datetime
import re

import emoji

'''
1 - Dispositivos Android e iOS exportam as conversas com uma formatação diferente da data e horários
das mensagens. O scrip já vem configurado para dispositivos Android (ANDROID_DEVICE = True), para
rodar arquivos exportados de iPhones alterar para ANDROID_DEVICE = False

2 - Quando você exporta uma conversa do seu telefone, alguns eventos de grupo podem vir com a palavra
"Você" ao invés do seu nome de usuário (Ex: [01/01/2000 12:00:00] Você removeu fulano).
Coloque o nome de usuário de quem exportou a conversa na variável MY_WHATSAPP_USERNAME para o script
não considerar "Você" e o seu nome de usuários como 2 usuários diferentes.

3 - Coloque o arquivo da conversa no mesmo diretório do script "whatsapp_info.py" e inisira o nome do
arquivo na variável FILE_NAME. Isira o nome do arquivo junto com a sua extensão (Ex: _chat.txt)
'''
ANDROID_DEVICE = True
MY_WHATSAPP_USERNAME = ""
FILE_NAME = ".txt"

group_chat = False
group_name = None
group_creator = None
group_creation_date = None
messages = list()


class ReportIOs:
    def __init__(self, messages: list, group: bool):
        if group:
            self.remove = dict()
            self.add = dict()
            self.name_change = dict()
            self.image_change = dict()
        self.messages = dict()
        self.emojis_total = dict()
        self.emojis_users = dict()
        self.dates = dict()
        self.audios = dict()
        self.images = dict()
        self.videos = dict()
        self.stickers = dict()
        self.gifs = dict()
        self.delete = dict()
        self.documents = dict()
        self.contacts = dict()

        for message in messages:
            if not message.group_event:
                if self.messages.__contains__(message.sender):
                    self.messages[message.sender] = self.messages.get(message.sender) + 1
                else:
                    if message.sender is not None:
                        self.messages[message.sender] = 1

            for emoticon in message.emojis:
                emo = str(emoji.demojize(emoticon.get("emoji"), use_aliases=True))
                if emo.__contains__("_sign") or emo.__contains__("fitzpatrick"):
                    pass
                else:
                    emo = str(emoticon.get("emoji"))
                    if self.emojis_total.__contains__(emo):
                        self.emojis_total[emo] = self.emojis_total.get(emo) + 1
                    else:
                        if emo is not None:
                            self.emojis_total[emo] = 1

            count = len(message.emojis)
            if count > 0:
                if self.emojis_users.__contains__(message.sender):
                    self.emojis_users[message.sender] = self.emojis_users.get(message.sender) + count
                else:
                    self.emojis_users[message.sender] = count

            if not message.group_event:
                if self.dates.__contains__(message.date):
                    self.dates[message.date] = self.dates.get(message.date) + 1
                else:
                    self.dates[message.date] = 1

            if not message.user_typed:
                if message.content.strip() == "áudio ocultado":
                    if self.audios.__contains__(message.sender):
                        self.audios[message.sender] = self.audios.get(message.sender) + 1
                    else:
                        self.audios[message.sender] = 1
                elif message.content.strip() == "imagem ocultada":
                    if self.images.__contains__(message.sender):
                        self.images[message.sender] = self.images.get(message.sender) + 1
                    else:
                        self.images[message.sender] = 1
                elif message.content.strip() == "vídeo omitido":
                    if self.videos.__contains__(message.sender):
                        self.videos[message.sender] = self.videos.get(message.sender) + 1
                    else:
                        self.videos[message.sender] = 1
                elif message.content.strip() == "figurinha omitida":
                    if self.stickers.__contains__(message.sender):
                        self.stickers[message.sender] = self.stickers.get(message.sender) + 1
                    else:
                        self.stickers[message.sender] = 1
                elif message.content.strip() == "GIF omitido":
                    if self.gifs.__contains__(message.sender):
                        self.gifs[message.sender] = self.gifs.get(message.sender) + 1
                    else:
                        self.gifs[message.sender] = 1
                elif message.content.strip() == "Essa mensagem foi apagada.":
                    if self.delete.__contains__(message.sender):
                        self.delete[message.sender] = self.delete.get(message.sender) + 1
                    else:
                        self.delete[message.sender] = 1
                elif message.content.strip() == "documento omitido":
                    if self.documents.__contains__(message.sender):
                        self.documents[message.sender] = self.documents.get(message.sender) + 1
                    else:
                        self.documents[message.sender] = 1
                elif message.content.strip() == "Cartão do contato omitido":
                    if self.contacts.__contains__(message.sender):
                        self.contacts[message.sender] = self.contacts.get(message.sender) + 1
                    else:
                        self.contacts[message.sender] = 1

                if group:
                    if message.content.__contains__("removeu"):
                        if self.remove.__contains__(message.sender):
                            self.remove[message.sender] = self.remove.get(message.sender) + 1
                        else:
                            self.remove[message.sender] = 1
                    elif message.content.__contains__("adicionou"):
                        if self.add.__contains__(message.sender):
                            self.add[message.sender] = self.add.get(message.sender) + 1
                        else:
                            self.add[message.sender] = 1
                    elif message.content.__contains__("mudou o nome do grupo para"):
                        if self.name_change.__contains__(message.sender):
                            self.name_change[message.sender] = self.name_change.get(message.sender) + 1
                        else:
                            self.name_change[message.sender] = 1
                    elif message.content.__contains__("mudou a imagem") or message.content.__contains__("apagou a imagem"):
                        if self.image_change.__contains__(message.sender):
                            self.image_change[message.sender] = self.image_change.get(message.sender) + 1
                        else:
                            self.image_change[message.sender] = 1

    def __str__(self):
        if group_chat:
            if group_name is not None:
                print("Conversa do grupo \"{}\"".format(group_name))
            if group_creator is not None and group_creation_date is not None:
                print("Grupo criado por {} em {}".format(group_creator, group_creation_date.strftime("%d/%m/%Y")))
            print("Quantidade de usuários removidos:", sorted(self.remove.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Quantidade de usuários adicionados:", sorted(self.add.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Mudança da imagem do grupo:", sorted(self.image_change.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Mudança do nome do grupo:", sorted(self.name_change.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de mensagens por usuários:", sorted(self.messages.items(), key=lambda k:(k[1], k[0]), reverse=True))
        print("Total de cada emojis:", sorted(self.emojis_total.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de emojis de cada usuário:", sorted(self.emojis_users.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Quantidade de mensagens por data:[", end="")
        for date in sorted(self.dates.items(), key=lambda k: (k[0], k[1]), reverse=False):
            print("({}, {}), ".format(date[0].strftime("%d/%m/%Y"), date[1]), end="")
        print("]")
        print("Total de áudios:", sorted(self.audios.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de imagens:", sorted(self.images.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de vídeos:", sorted(self.videos.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de figurinhas:", sorted(self.stickers.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de GIFs:", sorted(self.gifs.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de documentos:", sorted(self.documents.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de contatos:", sorted(self.contacts.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de mensagens deletadas:", sorted(self.delete.items(), key=lambda k: (k[1], k[0]), reverse=True))
        return ""


class ReportAndroid:
    def __init__(self, messages: list, group: bool):
        if group:
            self.remove = dict()
            self.add = dict()
            self.name_change = dict()
            self.image_change = dict()
        self.messages = dict()
        self.emojis_total = dict()
        self.emojis_users = dict()
        self.dates = dict()
        self.medias = dict()
        self.delete = dict()

        for message in messages:
            if not message.group_event:
                if self.messages.__contains__(message.sender):
                    self.messages[message.sender] = self.messages.get(message.sender) + 1
                else:
                    if message.sender is not None:
                        self.messages[message.sender] = 1

            for emoticon in message.emojis:
                emo = str(emoji.demojize(emoticon.get("emoji"), use_aliases=True))
                if emo.__contains__("_sign") or emo.__contains__("fitzpatrick"):
                    pass
                else:
                    emo = str(emoticon.get("emoji"))
                    if self.emojis_total.__contains__(emo):
                        self.emojis_total[emo] = self.emojis_total.get(emo) + 1
                    else:
                        if emo is not None:
                            self.emojis_total[emo] = 1

            count = len(message.emojis)
            if count > 0:
                if self.emojis_users.__contains__(message.sender):
                    self.emojis_users[message.sender] = self.emojis_users.get(message.sender) + count
                else:
                    self.emojis_users[message.sender] = count

            if not message.group_event:
                if self.dates.__contains__(message.date):
                    self.dates[message.date] = self.dates.get(message.date) + 1
                else:
                    self.dates[message.date] = 1

            if message.content.strip() == "<Arquivo de mídia oculto>":
                if self.medias.__contains__(message.sender):
                    self.medias[message.sender] = self.medias[message.sender] + 1
                else:
                    self.medias[message.sender] = 1

            if group:
                if message.content.__contains__("removeu"):
                    if self.remove.__contains__(message.sender):
                        self.remove[message.sender] = self.remove.get(message.sender) + 1
                    else:
                        self.remove[message.sender] = 1
                elif message.content.__contains__("adicionou"):
                    if self.add.__contains__(message.sender):
                        self.add[message.sender] = self.add.get(message.sender) + 1
                    else:
                        self.add[message.sender] = 1
                elif message.content.__contains__("mudou o nome de"):
                    if self.name_change.__contains__(message.sender):
                        self.name_change[message.sender] = self.name_change.get(message.sender) + 1
                    else:
                        self.name_change[message.sender] = 1
                elif message.content.__contains__("mudou a imagem") or message.content.__contains__("apagou a imagem"):
                    if self.image_change.__contains__(message.sender):
                        self.image_change[message.sender] = self.image_change.get(message.sender) + 1
                    else:
                        self.image_change[message.sender] = 1

    def __str__(self):
        if group_chat:
            if group_name is not None:
                print("Conversa do grupo \"{}\"".format(group_name))
            if group_creator is not None and group_creation_date is not None:
                print("Grupo criado por {} em {}".format(group_creator, group_creation_date.strftime("%d/%m/%Y")))
            print("Quantidade de usuários removidos:", sorted(self.remove.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Quantidade de usuários adicionados:", sorted(self.add.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Mudança da imagem do grupo:", sorted(self.image_change.items(), key=lambda k: (k[1], k[0]), reverse=True))
            print("Mudança do nome do grupo:", sorted(self.name_change.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de mensagens por usuários:", sorted(self.messages.items(), key=lambda k:(k[1], k[0]), reverse=True))
        print("Total de cada emojis:", sorted(self.emojis_total.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de emojis de cada usuário:", sorted(self.emojis_users.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Quantidade de mensagens por data:[", end="")
        for date in sorted(self.dates.items(), key=lambda k: (k[0], k[1]), reverse=False):
            print("({}, {}), ".format(date[0].strftime("%d/%m/%Y"), date[1]), end="")
        print("]")
        print("Total de mídias po usuário:", sorted(self.medias.items(), key=lambda k: (k[1], k[0]), reverse=True))
        print("Total de mensagens deletadas:", sorted(self.delete.items(), key=lambda k: (k[1], k[0]), reverse=True))
        return ""


class MessageIOs:

    def __init__(self, line: str, user_typed: bool):
        self.user_typed = user_typed
        self.sender = None
        self.content = ""
        self.date = None
        self.emojis = list()
        self.group_event = False
        try:
            if line[0] == "[":
                self.date = datetime.date(int(line[7:11]), int(line[4:6]), int(line[1:3]))
                pattern = " \".[^\"]*\""
                if re.sub(pattern, "", line[22:]).__contains__(":"):
                    offset = line[22:].index(":") + 22
                    self.sender = line[22: offset]
                    self.content = line[offset + 2:]
                else: #is a group event line
                    self.group_event = True
                    if line.__contains__("removeu"):
                        offset = line.index("removeu") - 1
                        self.sender = line[22:offset]
                        offset = offset + 1
                        self.content = line[offset:]
                    elif line.__contains__("adicionou"):
                        offset = line.index("adicionou") - 1
                        self.sender = line[22:offset]
                        offset = offset + 1
                        self.content = line[offset:]
                    elif line.__contains__("saiu"):
                        offset = line.index("saiu") - 1
                        self.sender = line[22:offset]
                        self.content = "saiu"
                    elif line.__contains__("mudou o nome do grupo para"):
                        offset = line.index("mudou o nome do grupo para") - 1
                        self.sender = line[22:offset]
                        offset = offset + 1
                        self.content = line[offset:]
                    elif line.__contains__("mudou a imagem"):
                        offset = line.index("mudou a imagem") - 1
                        self.sender = line[22:offset]
                        offset = offset + 1
                        self.content = line[offset:]
                if emoji.emoji_count(self.content) > 0:
                    self.emojis = emoji.emoji_lis(line)
        except Exception as e:
            print(e)
        if self.sender == "Você":
            self.sender = MY_WHATSAPP_USERNAME

    def __str__(self):
        return "SENDER: {}\nMESSAGE: {}".format(self.sender, self.content)


class MessageAndroid:

    def __init__(self, line: str):
        self.sender = None
        self.content = ""
        self.date = None
        self.emojis = list()
        self.group_event = False
        try:
            self.date = datetime.date(int(line[6:10]), int(line[3:5]), int(line[0:2]))
            pattern = " \".[^\"]*\""
            if re.sub(pattern, "", line[19:]).__contains__(":"):
                offset = line[19:].index(":") + 19
                self.sender = line[19: offset]
                self.content = line[offset + 2:]
            else:  # is a group event line
                self.group_event = True
                if line.__contains__("removeu"): #TODO ver o fomrtado da remoção
                    offset = line.index("removeu") - 1
                    self.sender = line[19:offset]
                    offset = offset + 1
                    self.content = line[offset:]
                elif line.__contains__("adicionou"):#TODO ver o formato de adicionar
                    offset = line.index("adicionou") - 1
                    self.sender = line[19:offset]
                    offset = offset + 1
                    self.content = line[offset:]
                elif line.__contains__("saiu"): #TODO ver o formato de sair
                    offset = line.index("saiu") - 1
                    self.sender = line[19:offset]
                    self.content = "saiu"
                elif line.__contains__("mudou o nome de"):
                    offset = line.index("mudou o nome de") - 1
                    self.sender = line[19:offset]
                    offset = offset + 1
                    self.content = line[offset:]
                elif line.__contains__("mudou a imagem"):
                    offset = line.index("mudou a imagem") - 1
                    self.sender = line[19:offset]
                    offset = offset + 1
                    self.content = line[offset:]
                elif line.__contains__("apagou a imagem"):
                    offset = line.index("apagou a imagem") - 1
                    self.sender = line[19:offset]
                    offset = offset + 1
                    self.content = line[offset:]
            if emoji.emoji_count(self.content) > 0:
                self.emojis = emoji.emoji_lis(line)
        except Exception as e:
            print(e)
        if self.sender == "Você":
            self.sender = MY_WHATSAPP_USERNAME

    def __str__(self):
        return "SENDER: {}\nMESSAGE: {}".format(self.sender, self.content)


def run_andorid_report():
    global group_chat
    global group_name
    global group_creator
    global group_creation_date
    with open(FILE_NAME, "r") as file:
        first_line = file.readline()
        if first_line is not None:
            if first_line.__contains__("As mensagens deste grupo"):  # Check if it's a group chat
                group_chat = True
                second_line = file.readline()
                if second_line.__contains__("criou o grupo"):
                    offset = second_line.index("criou") - 1
                    group_creator = second_line[19:offset]
                    if group_creator == "Você":
                        group_creator = MY_WHATSAPP_USERNAME
                    group_creation_date = datetime.date(int(second_line[6:10]), int(second_line[3:5]),
                                                        int(second_line[0:2]))
                    offset = second_line.index("\"")
                    group_name = second_line[offset + 1: len(second_line) - 1]
            for line in file.readlines():
                regex = re.search("\d\d/\d\d/\d\d\d\d \d\d:\d\d - ", line)
                if regex is not None:
                    if regex.span()[0] == 0:
                        messages.append(MessageAndroid(line))

    report = ReportAndroid(messages, group_chat)
    print(report)


def run_ios_report():
    global group_chat
    global group_name
    global group_creator
    global group_creation_date
    with open(FILE_NAME, "r") as file:
        first_line = file.readline()
        if first_line is not None:
            if first_line.__contains__("grupo"):  # Check if it's a group chat
                group_chat = True
                if first_line.__contains__(
                        "As mensagens deste grupo estão protegidas com a criptografia de ponta a ponta."):
                    offset = first_line[22:].index(":") + 22
                    group_name = first_line[22:offset]
                    second_line = file.readline()
                    if second_line.__contains__("criou"):
                        offset = second_line.index("criou") - 1
                        group_creator = second_line[22:offset]
                        group_creation_date = datetime.date(int(first_line[7:11]), int(first_line[4:6]),
                                                            int(first_line[1:3]))
                    else:
                        user_typed = True
                        if second_line.__contains__("\u200E"):
                            second_line = second_line.replace("\u200E", "")
                            user_typed = False
                        if second_line.__contains__("\u202a"):
                            second_line = second_line.replace("\u202a", "")
                        if second_line.__contains__("\xa0"):
                            second_line = second_line.replace("\xa0", " ")
                        if second_line.__contains__("\u202c"):
                            second_line = second_line.replace("\u202c", "")
                        if re.search("\[\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d]", second_line):
                            messages.append(MessageIOs(second_line, user_typed))
                elif first_line.__contains__("criou"):
                    offset = first_line.index("criou") - 1
                    group_creator = first_line[22:offset]
                    second_line = file.readline()
                    if second_line.__contains__("As mensagens deste grupo estão protegidas com a criptografia de ponta a ponta."):
                        offset = second_line[22:].index(":") + 22
                        group_name = second_line[22:offset]
                        group_creation_date = datetime.date(int(first_line[7:11]), int(first_line[4:6]),
                                                            int(first_line[1:3]))
                    else:
                        user_typed = True
                        if second_line.__contains__("\u200E"):
                            second_line = second_line.replace("\u200E", "")
                            user_typed = False
                        if second_line.__contains__("\u202a"):
                            second_line = second_line.replace("\u202a", "")
                        if second_line.__contains__("\xa0"):
                            second_line = second_line.replace("\xa0", " ")
                        if second_line.__contains__("\u202c"):
                            second_line = second_line.replace("\u202c", "")
                        if re.search("\[\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d]", second_line):
                            messages.append(MessageIOs(second_line, user_typed))
            for line in file.readlines():
                user_typed = True
                if line.__contains__("\u200E"):
                    line = line.replace("\u200E", "")
                    user_typed = False
                if line.__contains__("\u202a"):
                    line = line.replace("\u202a", "")
                if line.__contains__("\xa0"):
                    line = line.replace("\xa0", " ")
                if line.__contains__("\u202c"):
                    line = line.replace("\u202c", "")
                regex = re.search("\[\d\d/\d\d/\d\d\d\d \d\d:\d\d:\d\d]", line)
                if regex is not None:
                    if regex.span()[0] == 0:
                        messages.append(MessageIOs(line, user_typed))

    report = ReportIOs(messages, group_chat)
    print(report)

if __name__ == '__main__':
    if ANDROID_DEVICE:
        run_andorid_report()
    else:
        run_ios_report()
