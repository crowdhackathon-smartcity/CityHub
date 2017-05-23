# -*- coding: utf-8 -*-
from flask import Flask, request
from pymessenger.bot import Bot
from pymessenger import Element, Button
import sys
import rules
import time
import sys
import orchestrator, history, globals

app = Flask(__name__)

ACCESS_TOKEN = ''
VERIFY_TOKEN = ''
merchant = 0

@app.route("/", methods=['GET', 'POST'])
def parse_request():
    global ACCESS_TOKEN
    global VERIFY_TOKEN
    global bot
    global merchant

    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    if request.method == 'POST':
        print str(request)
        output = request.get_json()
        print str(output)
        if (output['entry'][0]['messaging'][0].get('postback')):
            recipient_id = output['entry'][0]['messaging'][0]['sender']['id']
            message = output['entry'][0]['messaging'][0]['postback']['payload']
            if (message.startswith('2')) and (merchant == 1):
                bot.send_text_message(recipient_id, 'Τέλεια! Που να τα στείλω;')
            elif (message.startswith('Λεπτομέρειες')) and (merchant == 1):
                bot.send_text_message(recipient_id, 'Αυτά είναι όντως πανέμορφα λουλούδια.')
            elif (message.startswith('Λεπτομέρειες')) and (merchant == 2):
                bot.send_text_message(recipient_id, 'Το παρόν σας δίνει την δυνατότητα στάθμευσης στα όρια του δήμου Μοσχάτου-Ταύρου.')
            elif (message.startswith('2')) and (merchant == 2):
                              buttons = []
                              button = Button(title='PayPal', type='postback', payload='4')
                              buttons.append(button)
                              button = Button(title='Πιστωτική Κάρτα', type='postback', payload='4')
                              buttons.append(button)
                              button = Button(title='Digital Wallet', type='postback', payload='4')
                              buttons.append(button)
                              text = 'Πως θες να πληρώσεις;'
                              result = bot.send_button_message(recipient_id, text, buttons)
            elif (message.startswith('4')):
                time.sleep(1)
                bot.send_text_message(recipient_id, 'Η συναλλαγή ολοκληρώθηκε! Σύντομα θα λάβεις e-mail με την παραγγελία σου.')
                merchant = 0
            else:
                print 'ha'
        elif (output['entry'][0]['messaging'][0]['message'].get('attachments')):
                if (output['entry'][0]['messaging'][0]['message']['attachments'][0]['payload'].get('coordinates')):
                              recipient_id = output['entry'][0]['messaging'][0]['sender']['id']
                              bot.send_text_message(recipient_id, 'Βρίσκεσαι κοντά στον Δήμο Μοσχάτου-Ταύρου')
                              image_url1 = 'http://buddythebot.com/images/demo/park11.jpg'
                              image_url2 = 'http://buddythebot.com/images/demo/park12.jpg'
                              image_url3 = 'http://buddythebot.com/images/demo/park13.jpg'
                              
                              title1 = "1 ώρα"
                              title2 = "2 ώρες"
                              title3 = "3 ώρες"
                              
                              subtitle1 = "Δήμος Μοσχάτου-Ταύρου"
                              subtitle2 = "Δήμος Μοσχάτου-Ταύρου"
                              subtitle3 = "Δήμος Μοσχάτου-Ταύρου"
                              
                              price1 = "Αγορά (1€)"
                              price2 = "Αγορά (2€)"
                              price3 = "Αγορά (3€)"
                              
                              payload = {
                                          'recipient': {
                                                  'id': recipient_id
                                          },
                                          'notification_type': 'REGULAR',
                                          'message': {
                                                'attachment': {
                                                  'type': 'template',
                                                  'payload': {
                                                      'template_type': 'generic',
                                                      'elements': [
                                                                    {
                                                                     "title":title1,
                                                                     "image_url":image_url1,
                                                                     "subtitle":subtitle1,
                                                                     "item_url":"https://dimosmoschatou-tavrou.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price1,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    },
                                                                    {
                                                                     "title":title2,
                                                                     "image_url":image_url2,
                                                                     "subtitle":subtitle2,
                                                                     "item_url":"https://dimosmoschatou-tavrou.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price2,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    },
                                                                    {
                                                                     "title":title3,
                                                                     "image_url":image_url3,
                                                                     "subtitle":subtitle3,
                                                                     "item_url":"https://dimosmoschatou-tavrou.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price3,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    }
                                                                  ]
                                                  }
                                                }
                                          }
                              }
                              bot.send_raw(payload)
        else:
            for event in output['entry']:
                messaging = event['messaging']
                for x in messaging:
                    if x.get('message'):
                        recipient_id = x['sender']['id']
                        if x['message'].get('text'):
                            message = x['message']['text']
                            print message
            
                            if (('λουλούδια' in message) or ('λουλουδια' in message) or ('Λουλούδια' in message) or ('Λουλουδια' in message)):
                              image_url1 = 'http://buddythebot.com/images/demo/tulips2.jpg'
                              image_url2 = 'http://buddythebot.com/images/demo/pink.jpg'
                              image_url3 = 'http://buddythebot.com/images/demo/chamomile.jpg'
                              merchant = 1
                              
                              title1 = "Πολύχρωμες τουλίπες"
                              title2 = "Ροζ τριαντάφυλλα"
                              title3 = "Μαργαρίτες"
                              
                              subtitle1 = "Δωρεάν έξοδα αποστολής"
                              subtitle2 = "Δωρεάν έξοδα αποστολής"
                              subtitle3 = "Δωρεάν έξοδα αποστολής"
                              
                              price1 = "Αγορά (15€)"
                              price2 = "Αγορά (20€)"
                              price3 = "Αγορά (11€)"
                              
                              payload = {
                                          'recipient': {
                                                  'id': recipient_id
                                          },
                                          'notification_type': 'REGULAR',
                                          'message': {
                                                'attachment': {
                                                  'type': 'template',
                                                  'payload': {
                                                      'template_type': 'generic',
                                                      'elements': [
                                                                    {
                                                                     "title":title1,
                                                                     "image_url":image_url1,
                                                                     "subtitle":subtitle1,
                                                                     "item_url":"http://thewhitelilly.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price1,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    },
                                                                    {
                                                                     "title":title2,
                                                                     "image_url":image_url2,
                                                                     "subtitle":subtitle2,
                                                                     "item_url":"http://thewhitelilly.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price2,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    },
                                                                    {
                                                                     "title":title3,
                                                                     "image_url":image_url3,
                                                                     "subtitle":subtitle3,
                                                                     "item_url":"http://thewhitelilly.gr",
                                                                     "buttons":[
                                                                       {
                                                                         "type":"postback",
                                                                         "payload":"Λεπτομέρειες",
                                                                         "title":"Λεπτομέρειες"
                                                                       },{
                                                                         "type":"postback",
                                                                         "title":price3,
                                                                         "payload":"2"
                                                                       }
                                                                     ]
                                                                    }
                                                                  ]
                                                  }
                                                }
                                          }
                              }
                              bot.send_raw(payload)
                            elif (('παρκάρω' in message) or ('παρκαρω' in message) or ('parking' in message) or ('parking' in message) or ('παρκινγκ' in message) or ('πάρκινγκ' in message)):
                              payload = {
                                         "recipient":{
                                           "id":recipient_id
                                         },
                                         "message":{
                                           "text":"Φυσικά. Που βρίσκεσαι τώρα;",
                                           "quick_replies":[
                                             {
                                               "content_type":"location",
                                             }
                                           ]
                                         }
                                       }
                              merchant = 2
                              bot.send_raw(payload)
                            elif ((message.startswith('Στη') or message.startswith('Στην') or message.startswith('Στο') or message.startswith('Στον'))) and (merchant == 1):
                              buttons = []
                              button = Button(title='PayPal', type='postback', payload='4')
                              buttons.append(button)
                              button = Button(title='Πιστωτική Κάρτα', type='postback', payload='4')
                              buttons.append(button)
                              button = Button(title='Digital Wallet', type='postback', payload='4')
                              buttons.append(button)
                              text = 'Πως θες να πληρώσεις;'
                              result = bot.send_button_message(recipient_id, text, buttons)
                            else:
                              bot.send_text_message(recipient_id, 'Δεν είμαι σίγουρος πως καταλαβαίνω...')
                            #bot.send_generic_message(recipient_id, elements)
                            #bot.send_text_message(recipient_id, 'nothing')
                        if x['message'].get('attachment'):
                            data['request']['type'] = 'attachment'
                            bot.send_attachment_url(recipient_id, x['message']['attachment']['type'],
                                                    x['message']['attachment']['payload']['url'])
                    else:
                        pass
        return "Success"

if (__name__ == '__main__'):
  #rules.init()
  #globals.init()
  #history.init()
  reload(sys)  
  sys.setdefaultencoding('utf8')
  ACCESS_TOKEN = ''
  #ACCESS_TOKEN = ''
  VERIFY_TOKEN = ''
  bot = Bot(ACCESS_TOKEN)
  print 'Facebook is listening...'
  app.run(port=5003, debug=True)
