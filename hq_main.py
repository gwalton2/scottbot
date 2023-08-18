from datetime import datetime
from vector import Vector
from scott import Scott
from save_json import Save_Json
import notify
import time
import asyncio
import pickle
import push
import re
import json
import aiohttp
from unidecode import unidecode
from threading import Thread

DATA = None
SOCKET = None

BEARER_TOKEN = 'XXXXX'
USER_ID = 'XXXXX'

main_url = f"https://api-quiz.hype.space/shows/now?type=hq&userId={USER_ID}"
headers = {"Authorization": f"Bearer {BEARER_TOKEN}", "x-hq-client": "Android/1.3.0"}

game_time = time.strftime('%m/%d/%y %I')
gamedata = Save_Json(game_time)

vector = Vector()
model = pickle.load(open('hqscribe_results/thenew_model.dat', "rb"))
methods = ['qtext_ans', 'atext_ans', 'atext_wiki_vec_ans', 'bing_qtext_vec_ans', 'wiki_vec_ans', 'bingwiki_vec_ans', 'vec_qa_text_ans']

push.update()

print('connecting...\n')

async def get_json_response(url, timeout, headers):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, timeout=timeout) as response:
            while True:
                data = await response.json(content_type=None)

                if type(data) is dict:
                    json_data = data
                    break

                elif type(data) is bytes:
                    string_data = data.decode("utf8").replace("'", '"')
                    json_data = json.loads(string_data)
                    break

                else:
                    print(f'Data type is {type(data)}. Retrying...')

            return json_data

async def websocket_handler(uri, headers):
    global DATA
    async with aiohttp.ClientSession() as session:

        async with session.ws_connect(uri, headers=headers, heartbeat=5, timeout=30) as ws:
            print("Connected")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    message = msg.data
                    message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)

                    message_data = json.loads(message)

                    print(message_data) #TESTING

                    if "error" in message_data and message_data["error"] == "Auth not valid":
                        raise RuntimeError("Connection settings invalid")

                    elif message_data["type"] != "interaction":

                        if message_data["type"] == "question":
                            question_str = unidecode(message_data["question"])
                            answers = [unidecode(ans["text"]) for ans in message_data["answers"]]

                            DATA = message_data['questionNumber'], question_str, answers

                            print("\n" * 5)
                            print("Question detected.")
                            print(f"Question {message_data['questionNumber']}")

    print("Socket closed. Waiting for question...\n")

def websocket_thread_starter():
    loop_data = asyncio.new_event_loop()
    asyncio.set_event_loop(loop_data)
    loop_data.run_until_complete(websocket_handler(SOCKET, headers))

def question_watcher():
    global DATA
    while SOCKET != None:
        if DATA != None:
            start = time.time()

            ques_num, question, answers = DATA
            myscott = Scott(vector, question, answers)

            myscott.get_text_threads()
            myscott.get_answer_threads()

            answer_array = myscott.answer_dict_array(methods)

            ans = round(model.predict(answer_array)[0])
            notify.notify(f'Q{ques_num}', answers[ans - 1], 'Live!')
            push.push(f'Q{ques_num}: {answers[ans - 1]}')

            end = time.time()
            print(end - start)

            q_data = {'question': question, 'answers': answers, 'answer_dict': myscott.answer_dict, 'myanswer': answers[ans - 1], 'theanswer': '', 'text': myscott.text_dict}
            gamedata.append(q_data, 'gamedata.json')

            print(question)
            print(answers)
            print(answer_array)
            print(f'{answers[ans - 1]}\n')

            time.sleep(5)
            DATA = None

def question_handler():
    process = Thread(target=question_watcher)
    process.start()

    while SOCKET != None:
        process = Thread(target=websocket_thread_starter)
        process.start()

        time.sleep(5)

        process = Thread(target=websocket_thread_starter)
        process.start()

        time.sleep(25)

def connection_handler():
    global SOCKET
    while True:

        loop_response = asyncio.new_event_loop()
        asyncio.set_event_loop(loop_response)
        try:
            response_data = loop_response.run_until_complete(get_json_response(main_url, timeout=1.5, headers=headers))
        except TimeoutError:
            print('Encountered major with json response. Please fix before continuing.')
            time.sleep(5)
            continue

        if "broadcast" not in response_data or response_data["broadcast"] is None:
            if "error" in response_data and response_data["error"] == "Auth not valid":
                raise RuntimeError("Connection settings invalid")

            else:
                SOCKET = None
                print("Show not on.")
                next_time = datetime.strptime(response_data["nextShowTime"], "%Y-%m-%dT%H:%M:%S.000Z")
                now = time.time()
                offset = datetime.fromtimestamp(now) - datetime.utcfromtimestamp(now)

                print(f"Next show time: {(next_time + offset).strftime('%Y-%m-%d %I:%M %p')}")
                print("Prize: " + response_data["nextShowPrize"])
                print()

                notify.update(f"Live at: {(next_time + offset).strftime('%I:%M%p')} PDT")

                time.sleep(60)

        else:
            if SOCKET == None:
                SOCKET = response_data["broadcast"]["socketUrl"]
                print(f"Show active, connecting to socket at {SOCKET}")

                question_handler()

                time.sleep(30)

            
connection_handler()
