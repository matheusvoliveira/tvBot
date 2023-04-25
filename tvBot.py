# # import requests
# # import json
# #
# # url = "https://online-movie-database.p.rapidapi.com/auto-complete"
# #
#
# # # These are my keywords I'd like to search for
# # searchTerms = ["spider"]
# #
# # # I store all the responses in a list
# # responses = []
# #
# # # Here I loop through the search terms
# # for x in range(len(searchTerms)):
# #   # Update the searchterm in the url parameters
# #   querystring = {"q": searchTerms[x]}
# #
# #   # Query the API and save the result
# #   response = requests.request("GET", url, headers=headers, params=querystring)
# #
# #   # Turn the json text from the response into a useful json python object
# #   data = json.loads(response.text)
# #
# #   # Format the json to be more readable this is mostly for viewing raw
# #   # response data when debugging
# #
# #   formattedData = json.dumps(data, indent=4)
# #   # Uncomment the following line to see the raw response from the api
# #   # print(formattedData)
# #
# #   # Load the json data into a dictionary
# #   dataDict = json.loads(formattedData)
# #
# #   # Save the most important data in our list
# #   responses.append(dataDict["d"])
# #
# # # Print out the results
# # for x in range(len(searchTerms)):
# #   print("\n\nSearch Term: \"" + str(searchTerms[x]) + "\"")
# #   for movie in responses[x]:
# #     # I used try/except here to keep going just incase a movie doesn't have
# #     # the data I'm asking for.
# #     try:
# #       print("Título: " + movie["l"])
# #       print("Imagem: " + movie["i"]["imageUrl"])
# #       print("Tipo: " + movie["qid"])
# #       print("Ano: " + movie["y"])
# #       print("Elenco: " + movie["s"])
# #
# #
# #
# #     except:
# #       pass
#
# import requests
# import json
#
# url = "https://online-movie-database.p.rapidapi.com/auto-complete"
#

# # Solicita ao usuário o termo de pesquisa
# searchTerm = input("Digite o termo de pesquisa: ")
#
# # Query the API and save the result
# response = requests.get(url, headers=headers, params={"q": searchTerm})
#
# # Verifica se a resposta foi bem-sucedida (código de resposta 200)
# if response.status_code == 200:
#     # Transforma o texto JSON da resposta em um objeto Python
#     data = json.loads(response.text)
#
#     # Formata o JSON para ser mais legível
#     formattedData = json.dumps(data, indent=4)
#     # Descomente a linha abaixo para ver a resposta bruta da API
#     # print(formattedData)
#
#     # Carrega os dados JSON em um dicionário
#     dataDict = json.loads(formattedData)
#
#     # Salva os dados mais importantes em uma lista
#     responses = dataDict["d"]
#
#     # Imprime os resultados
#     print("\n\nTermo de pesquisa: \"" + searchTerm + "\"")
#     for movie in responses:
#         # Utiliza try/except para lidar com casos em que o filme não possui determinados dados
#         try:
#             print("Título: " + movie["l"])
#             print("Imagem: " + movie["i"]["imageUrl"])
#             print("Tipo: " + movie["qid"])
#             print("Ano: " + movie["y"])
#             print("Elenco: " + movie["s"])
#
#         except:
#             pass
# else:
#     # print("Não foi possível obter resultados. Verifique sua conexão com a internet e tente novamente.")

from telegram.ext import *
import keys
import requests
import json

# info api IMDB
url = "https://online-movie-database.p.rapidapi.com/auto-complete"


searchTerm = ''

print('Starting up bot ...')

def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. Nice to meet you!')


def help_command(update, context):
    update.message.reply_text('Try typping anything and i will respond!')

def custom_command(update, context):
    update.message.reply_text('This is a custom command!')

def handle_response(text: str) -> str:
    split = text.split()
    searchTerm = split[1]
    if split[0] == 'search' \
            and len(searchTerm) > 2:
        response = requests.get(url, headers=keys.headers, params={"q": searchTerm})
        data = json.loads(response.text)
        formattedData = json.dumps(data, indent=4)
        dataDict = json.loads(formattedData)
        responses = dataDict["d"]
        # return 'searching for ' + split[1] + ' ...'
        for movie in responses:
            return "Título: " + movie["l"] + "\n" + "Imagem: " + movie["i"]["imageUrl"] + "\n" + \
                "Tipo: " + movie["qid"] + "Tipo: " + movie["yr"]

        # for movie in responses:
        #     print("Título: " + movie["l"])
        #     print("Imagem: " + movie["i"]["imageUrl"])
        #     print("Tipo: " + movie["qid"])
        #     print("Ano: " + movie["y"])
        #     print("Elenco: " + movie["s"])



def handle_message(update, context):
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    if message_type == 'group':
        if '@mrxangbot' in text:
            new_text = text.replacec('@mrxangbot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    update.message.reply_text(response)

def error(update, context):
    print(f'Update {update} caused error: {context.error}')



if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    #Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('custom', custom_command))

    # o handler é um objeto que define como seu bot deve
    # responder uma mensagem especifica como por exemplo start_command

    #Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    #Errors
    dp.add_error_handler(error)

    #Run bot
    updater.start_polling(1.0)
    updater.idle()
