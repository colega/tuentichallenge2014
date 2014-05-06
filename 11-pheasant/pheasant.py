def pheasant(users, user_keys, num_events, get_user_feed_callback):
	event_feed = []
	event_list_array = []
	event_list_position = 0

	while len(event_feed) < num_events:
		if len(event_list_array) <= event_list_position + 1 and len(users) > 0:
			user_to_request_feed = users.pop(0)
			user_feed = get_user_feed_callback(user_to_request_feed, user_keys[user_to_request_feed])

			if len(user_feed) > 0:
				event_list_array.append(user_feed)

		if len(event_list_array) == 0 and len(users) == 0:
			break;

		first_events = get_first_event_from_each_list(event_list_array)

		event_list_position = get_position_of_max_timestamp(first_events)

		event = event_list_array[event_list_position].pop(0)

		event_feed.append(event)

		if len(event_list_array[event_list_position]) == 0:
			event_list_array.pop(event_list_position)

	return event_feed

def get_first_event_from_each_list(event_list_array):
	first_events = []
	for event_list in event_list_array:
		first_events.append(event_list[0])
	return first_events

def get_position_of_max_timestamp(events):
	max_pos = -1
	max_val = -1

	for index, event in enumerate(events):
		if event[1] > max_val:
			max_val = event[1]
			max_pos = index
	
	return max_pos	