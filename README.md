# ScottBot
This is a very old and disorganized project I made to answer questions from the game show app HQ Trivia. It was named after the games original host.

It sets up a websocket to intercept the traffic coming to your app's account where it will parse out when a question has been received.
It then scrapes google, bing, and wikipedia for potential answers.
A machine learning model, trained on a large dataset from wikipedia, is used to vectorize the scraped text, the question, and the answer choices.
This, along with some additional data is fed into a second machine learning model that had been trained on past questions to predict the actual answer.
The answer was pushed to your phone as a notification using an app that I don't believe is supported any longer.
This was accomplished in well under 10 seconds and was accurate about 65% of the time.

To run the program you would simply run the hq_main.py file.
However, all trained models have been removed from this project as well as supporting text and json files.
In addition, tokens to access your app's HQ Trivia account would need to be filled in along with API access tokens.
