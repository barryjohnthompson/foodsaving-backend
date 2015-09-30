"""This script sets up some test-data representing some of the use-cases in the app:

Food store
========================

Matthias and Tilmann talked with Jon who is the manager of the Alnatura organic shop in Munich. The trio would like to
start saving food from the Alnatura store, so Matthias and Tilmann create an entry for the store and gather a team to
organize the rescue: Neel and Flo will help with picking up food.
As such, on the 15th of October at 5pm, Flo will be picking up some food from the store. Neel signed up for the pick-ups
on the 13th and 14th but he hasn't been given the go-ahead yet. Unfortunately, Neel can't make the pick-up on the 12th
for which he was originally down (he told the group as much in a message) and no one volunteered to take over his slot.
If anyone has questions about the way that the group organizes pickups from the store, they decide that people should
contact Tilmann via direct message.


Food basket
========================

Tilmann wants to get rid of 5.1 kg of "super tasty" bananas and bread. He advertises the basket with a picture.
Our bestower of tastiness is very busy, meaning that the food can only be picked up on October 15th 2015. The pick up
can happen at Tilmann's office in Munich (between 5pm and 6pm) or at his home between 7pm and 8pm.
Neel and Matthias showed interest in picking up the food and Tilmann chose to give the food to Neel. The pick up went
seamlessly so Tilmann left some positive feedback on Neel.

Chat
========================

Neel chats lorem ipsum with Tilmann, while Flo, Matthias and Tilmann have a group chat discussion about lorem ipsum.

"""
from datetime import datetime
from django.utils.timezone import make_aware as add_timezone

from yunity.models import *


##################################################
# category
##################################################
category_foodsharing = Category.objects.create(name='foodsharing')
category_foodsharing_company = Category.objects.create(name='company', parent=category_foodsharing)
category_foodsharing_food = Category.objects.create(name='food', parent=category_foodsharing)
category_foodsharing_food_organic = Category.objects.create(name='Organic', parent=category_foodsharing_food)
category_foodsharing_food_bread = Category.objects.create(name='bread', parent=category_foodsharing_food)
category_foodsharing_food_banana = Category.objects.create(name='banana', parent=category_foodsharing_food)
category_foodsharing_food_basket = Category.objects.create(name='basket', parent=category_foodsharing_food)


##################################################
# location
##################################################
munich1 = Location.objects.create(latitude=48.13, longitude=11.57)
munich2 = Location.objects.create(latitude=48.161552, longitude=11.644833)
munich3 = Location.objects.create(latitude=48.161552, longitude=11.642)


##################################################
# user
##################################################
user_Tilmann = User.objects.create(name='Tilmann')
UserLocation.objects.create(user=user_Tilmann, location=munich2, type='UserLocation_type.HOME')
UserLocation.objects.create(user=user_Tilmann, location=munich3, type='UserLocation_type.WORK')

user_matthias = User.objects.create(name='Matthias')
user_neel = User.objects.create(name='Neel')
user_flo = User.objects.create(name='Flo')


##################################################
# contact
##################################################
contact_Tilmann_pm = Contact.objects.create(type=Contact.TYPE.DIRECT, value=user_Tilmann.id)
contact_Tilmann_email = Contact.objects.create(type=Contact.TYPE.EMAIL, value='Tilmann@foodsharing.de')
user_Tilmann.contact.add(contact_Tilmann_pm)
user_Tilmann.contact.add(contact_Tilmann_email)


##################################################
# metadata
##################################################
metadata_companycontact = Metadata.objects.create(key='companycontact', value='Jon +49 111 222 333')
metadata_basketweight = Metadata.objects.create(key='basketweight', value='5.1kg')


##################################################
# message
##################################################
message_neel_cantcome = Message.objects.create(type=Message.TYPE.TEXT, content="hey guys, i can't make the pickup today :(", sender=user_neel)
message_Tilmann_basketdescription = Message.objects.create(type=Message.TYPE.TEXT, content='please pick up my super tasty stuff', sender=user_Tilmann)
message_Tilmann_basketpicture = Message.objects.create(type=Message.TYPE.PICTURE, content='yunity.org/pics/mybasket.png', sender=user_Tilmann)

##################################################
# use-case: foodsharing store
##################################################

foodsharing_store = Mappable.objects.create(provenance='yunity.org', name='alnatura')
foodsharing_store.category.add(category_foodsharing_food_organic, category_foodsharing_company, category_foodsharing)
foodsharing_store.metadata.add(metadata_companycontact)
foodsharing_store.wall.add(message_neel_cantcome)
foodsharing_store.contact.add(contact_Tilmann_pm)
MappableLocation.objects.create(mappable=foodsharing_store, location=munich1)

MappableResponsibility.objects.create(responsible=user_Tilmann, mappable=foodsharing_store, status=MappableResponsibility.STATUS.GRANTED, type=MappableResponsibility.TYPE.OWNER)
MappableResponsibility.objects.create(responsible=user_matthias, mappable=foodsharing_store, status=MappableResponsibility.STATUS.GRANTED, type=MappableResponsibility.TYPE.OWNER)
MappableResponsibility.objects.create(responsible=user_neel, mappable=foodsharing_store, status=MappableResponsibility.STATUS.GRANTED, type='MappableResponsibility_type.TEAM')
MappableResponsibility.objects.create(responsible=user_flo, mappable=foodsharing_store, status=MappableResponsibility.STATUS.GRANTED, type='MappableResponsibility_type.TEAM')
MappableResponsibility.objects.create(responsible=user_flo, mappable=foodsharing_store, status=MappableResponsibility.STATUS.GRANTED, type='MappableResponsibility_type.PICKER', date=add_timezone(datetime.strptime('2015-10-15 17:00', '%Y-%m-%d %H:%M')))
MappableResponsibility.objects.create(responsible=user_neel, mappable=foodsharing_store, status=MappableResponsibility.STATUS.REQUESTED, type='MappableResponsibility_type.PICKER', date=add_timezone(datetime.strptime('2015-10-14 17:00', '%Y-%m-%d %H:%M')))
MappableResponsibility.objects.create(responsible=user_neel, mappable=foodsharing_store, status=MappableResponsibility.STATUS.REQUESTED, type='MappableResponsibility_type.PICKER', date=add_timezone(datetime.strptime('2015-10-13 17:00', '%Y-%m-%d %H:%M')))
MappableResponsibility.objects.create(responsible=None, mappable=foodsharing_store, status=MappableResponsibility.STATUS.PENDING, type='MappableResponsibility_type.PICKER', date=add_timezone(datetime.strptime('2015-10-12 17:00', '%Y-%m-%d %H:%M')))


##################################################
# use-case: food basket
##################################################

foodsharing_basket = Mappable.objects.create(provenance='foodsharing.de', name='super tasty bananas and bread')
foodsharing_basket.category.add(category_foodsharing_food_bread, category_foodsharing_food_banana, category_foodsharing_food_basket, category_foodsharing)
foodsharing_basket.metadata.add(metadata_basketweight)
foodsharing_basket.wall.add(message_Tilmann_basketdescription, message_Tilmann_basketpicture)
foodsharing_basket.contact.add(contact_Tilmann_email)
MappableLocation.objects.create(mappable=foodsharing_basket, location=munich2, startTime=add_timezone(datetime.strptime('2015-10-15 17:00', '%Y-%m-%d %H:%M')), endTime=add_timezone(datetime.strptime('2015-10-15 18:00', '%Y-%m-%d %H:%M')))
MappableLocation.objects.create(mappable=foodsharing_basket, location=munich3, startTime=add_timezone(datetime.strptime('2015-10-15 19:00', '%Y-%m-%d %H:%M')), endTime=add_timezone(datetime.strptime('2015-10-15 20:00', '%Y-%m-%d %H:%M')))

MappableResponsibility.objects.create(responsible=user_Tilmann, mappable=foodsharing_basket, status=MappableResponsibility.STATUS.GRANTED, type=MappableResponsibility.TYPE.OWNER)

ItemRequest.objects.create(requester=user_neel, requested=foodsharing_basket, feedback=ItemRequest.FEEDBACK.OK)
ItemRequest.objects.create(requester=user_matthias, requested=foodsharing_basket, feedback=ItemRequest.FEEDBACK.NOT_GRANTED)

##################################################
# use-case: chat
##################################################

chat_pair = Chat.objects.create()
chat_pair.participants.add(user_neel, user_Tilmann)

for i in range(100):
    m = Message.objects.create(content="Hi Neel, lorem ipsum %i" %i, type=Message.TYPE.TEXT, sender=user_Tilmann)
    chat_pair.messages.add(m)
    m = Message.objects.create(content="Hi Tilmann, lorem ipsum %i" %i, type=Message.TYPE.TEXT, sender=user_neel)
    chat_pair.messages.add(m)

chat_group = Chat.objects.create()
chat_group.participants.add(user_matthias, user_flo, user_Tilmann)

for i in range(100):
    m = Message.objects.create(content="Hi all, lorem ipsum %i" %i, type=Message.TYPE.TEXT, sender=user_matthias)
    chat_group.messages.add(m)
    m = Message.objects.create(content="Hi too, lorem ipsum %i" %i, type=Message.TYPE.TEXT, sender=user_flo)
    chat_group.messages.add(m)
    m = Message.objects.create(content="Bla, lorem ipsum %i" %i, type=Message.TYPE.TEXT, sender=user_Tilmann)
    chat_group.messages.add(m)
