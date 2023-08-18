from pusher_push_notifications import PushNotifications

pn_client = PushNotifications(
    instance_id='XXXXX',
    secret_key='XXXXX')

def notify(title, message, status):
	response = pn_client.publish(
	  interests=['ScottBot'],
	  publish_body={
	    'fcm': {
	    	'data': {
	    		'title': title,
	    		'message': message,
	    		'status': status
	    		}}})

def update(status):
	response = pn_client.publish(
	  interests=['ScottBot'],
	  publish_body={
	    'fcm': {
	    	'data': {
	    		'status': status
	    		}}})