import os

SENDY_API_KEY = os.getenv('SENDY_API_KEY')

SENDY_USERNAME = os.getenv('SENDY_USERNAME')

SENDY_SENDER_DETAILS = {
    'name': 'Daniel Waruo',
    'email': 'waruodaniel@gmail.com',
    'phone': '+254797792447'
}

SENDY_LOCATION_DETAILS = {
    'name': 'Ruai Near Embakasi Ranching',
    'description': 'First Right After Arriving at Embakasi Ranching',
    'lat': '-1.275872',
    'long': '36.9908555'
}

# TODO: automate delivery location to find several locatin based on where the goods are collected
