import tweepy
import random
import time
from interactive_conditional_samples import interact_model
#import gpt_2_simple as gpt2
from textblob import TextBlob

def pick_topic():
	topic = random.choice(['evolution', 'abortion', 'gun control', 'gay marriage', 'existence of god', 'healthcare'
						  , 'climate change', 'communism', '#christian'])
	return topic

def search(topic, api):
	results = api.search(q=topic, lang='en', result_type='recent', count=1, tweet_mode='extended')
#     for res in results:
#         if 
	return results
	
def generate_responses(text):#,sess, gpt2):
	print('Generating responses')
	responses = interact_model(text+' ||| ', top_k = 40, temperature = 0.8, nsamples = 10, model_name='355M')
#     responses = gpt2.generate(sess,
#                               length=280,
#                               temperature=0.8,
#                               prefix=text+' ||| ',
#                               nsamples=10,
#                               batch_size=5,
#                               return_as_list=True)
	print(responses)
	return responses

def select_response(responses):
	parsed = []
	for response in responses:
		response = response.split(' ||| ')[1]
		response = response[:240]
		response = response.split('<endoftext>')[0]
		before, sep, after = response.rpartition('.')
		response = before + sep
		parsed += [response]

	parsed = [x for x in parsed if 'emoticon' not in x and 'forum' not in x and x != '']
	sent_parsed = [[x,TextBlob(x).sentiment.polarity] for x in parsed]
	parsed.sort(key = lambda x: x[1], reverse = True)

	return parsed[0]

def reply(tweet, api):#,sess, gpt2):
	user = tweet._json['user']['screen_name']
	tweet_id = tweet._json['id_str']
	text = tweet._json['full_text']
	responses = generate_responses(text)#,sess, gpt2)
	reply_text = select_response(responses)
	
	#api.update_status('@' + user + ' ' + reply, in_reply_to_status_id=tweet_id)
	return text, reply_text

def main():
	auth = tweepy.OAuthHandler('5W4GMKnmBPmz73ofTbMSrBX5O', 'v3liOsP8k73qnqasUUbJAD0VaXyHJN6zy6tr2xdjdmuIgrjj0D')
	auth.set_access_token('977955567846281216-8YsIaPvhBtk3vQSZ5thkEvbiTTm39ro', 'h7JcHEceUN5PX8NuKYFA9f665DLMUSKpNizT1ZqFod2ei')

	api = tweepy.API(auth)
#     sess = gpt2.start_tf_sess()
#     gpt2.load_gpt2(sess, run_name='run1')
	while True:
		try:
			topic = pick_topic()
			tweet = search(topic, api)[0]
			text, reply_text = reply(tweet, api)#,sess, gpt2)
			print(topic)
			print('tweet: ', text)
			print('##########################')
			print('reply: ', reply_text)
			time.sleep(int(random.random()*120+300))
		except KeyboardInterrupt:
			break
		except:
			continue
		
if __name__ == "__main__":
	main()