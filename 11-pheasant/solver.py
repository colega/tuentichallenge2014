
from random import randrange
from random import sample
from pheasant import pheasant
from aescrypt import bruteforce

import fileinput

allowed_chars = [chr(i) for i in range(ord('A'), ord('Z')+1) + range(ord('a'), ord('z')+1)]
files_path = 'data/'
 
def get_encrypted_user_feed(user_id, key):
	return parse_encrypted_feed_file(user_id, key)

def parse_encrypted_feed_file(user_id, key):
	partition = str(user_id)[-2:]
	f = open(files_path + 'encrypted/' + partition + '/' + str(user_id) + '.feed', 'r')
	encrypted = f.read()
	f.close()

	contents = bruteforce(encrypted, allowed_chars, key, 32 - len(key))

	feed = []
	for row in contents.split('\n'):
		if len(row.split()) == 3:
			data = row.split()
			feed.append((int(data[0]), int(data[1]), int(data[2])))

	return feed

for line in fileinput.input():
	arguments = line.split('; ')
	if len(arguments) < 2:
		continue
	num_events = int(arguments.pop(0))
	requested_users_data = arguments

	requested_users = []
	user_keys = dict()
	for user_data in requested_users_data:
		(user_id, user_key) = user_data.split(',')
		user_id = int(user_id)
		requested_users.append(user_id)
		user_keys[user_id] = user_key.strip()

	last_times = []
	for user_id in requested_users:
		partition = str(user_id)[-2:]
		f = open(files_path + 'last_times/' + partition + '/' + str(user_id) + '.timestamp')
		last_time = f.read()
		last_times.append((int(user_id), int(last_time)))

	last_times = sorted(last_times, key=lambda lt: lt[1], reverse=True)
	users = [lt[0] for lt in last_times]

	feed = pheasant(users[:], user_keys, num_events, parse_encrypted_feed_file)

	for event in feed:
		print event[2],
	print
