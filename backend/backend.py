
from flask import Flask, request
import schedule
from threading import Thread
import json
from webscraper import Webscraper
import time
import os
from datetime import datetime
import asyncio
from telegram_bot import Telebot

flask_api = Flask(__name__)
telebot = Telebot("INSERT_BOT_TOKEN")

# not used by default as the auto cookie accept ext can only be used with head, otherwise supply to WebScraper
ext_id = 'fihnjjcciajhdojfnbdddfaoknhalnja'
ext_url = 'https://clients2.google.com/service/update2/crx?response=redirect&prodversion=31.0.1609.0&acceptformat=crx2,crx3&x=id%3D' + ext_id + '%26uc'
plugin_cache_json = None

@flask_api.route('/getplugins', methods = ['GET'])
def get_plugins():
    plugins_json = fetch_plugins(False)
    return plugins_json, 200
  
@flask_api.route('/editplugins', methods = ['POST'])
def edit_plugins():
    plugins_json = fetch_plugins(False)
    plugins = json.loads(plugins_json)
    initial_hash = hash(plugins_json)
    edit_plugin = request.json
    plugins[edit_plugin['name']] = edit_plugin
    plugins_json = json.dumps(plugins, indent=4, sort_keys=True)
    rewrite_plugins(plugins_json)
    later_hash = hash(plugins_json)
    if initial_hash != later_hash:
        return "Success", 200
    else:
        return "Failure or nothing has changed", 400

def rewrite_plugins(plugins_json):
    f = open('./plugins.json', 'w+')
    f.write(plugins_json)
    f.close()

def fetch_plugins(parse_json=True):
    global plugin_cache_json
    fetch_file = False
    if os.path.isfile('./plugins.json'):
        global current_lastedit
        global previous_lastedit
        current_lastedit = os.path.getmtime('./plugins.json')
        if not 'previous_lastedit' in globals():
            fetch_file = True
            previous_lastedit = current_lastedit
        if not previous_lastedit == current_lastedit:
            fetch_file = True
    else:
        fetch_file = True 
    if fetch_file:
        f = open('./plugins.json', 'r+')
        plugins_json = f.read()
        f.close()
        plugin_cache_json = plugins_json
        if len(plugin_cache_json) == 0:
            plugin_cache_json = '{}'
    return json.loads(plugin_cache_json) if parse_json else plugin_cache_json
    
def recreate_necessary(plugin):
    recreate = False
    global plugins_running
    if plugin['name'] in plugins_running:
        if not plugins_running[plugin['name']] == plugin['hash']:
            recreate = True
    else:
        recreate = True
    return recreate

# wrap workaround to execute async in procedurally
# https://stackoverflow.com/questions/59645272/how-do-i-pass-an-async-function-to-a-thread-target-in-python
def execute_scrape(plugin):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(exec_scrape(plugin))
    loop.close()
    
async def exec_scrape(plugin):
    if recreate_necessary(plugin):
        global plugins_running
        print('deregistered plugin ' + plugin['name'] + ' (' + str(plugin['hash']) + ')')
        return schedule.CancelJob
    try:
        scraper = Webscraper()
        result = scraper.check_site(plugin['website'], plugin['script'])
        print('checked plugin ' + plugin['name'] + ' (' + str(plugin['hash']) + '), state: ' + ('success' if result else 'failure'))
        plugins = fetch_plugins()
        tele_msg = 'plugin ' + plugin['name'] + ' (' + str(plugin['hash'])
        if not result:
            await telebot.send_message(tele_msg + ') alert. Script returned False!')
        else:
            if not plugins[plugin['name']]['state']:
                await telebot.send_message(tele_msg + ') recovered. Script returned True!')
        plugins[plugin['name']]['state'] = result
        plugins[plugin['name']]['lastChecked'] = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        plugins_json = json.dumps(plugins, indent=4, sort_keys=True)
        rewrite_plugins(plugins_json)
    except Exception as e:
        print('deregistered plugin ' + plugin['name'] + ' (' + str(plugin['hash']) + ')')
        return schedule.CancelJob

def register_plugins():
    plugins = fetch_plugins()
    global plugins_running
    if not 'plugins_running' in globals():
        plugins_running = {}
    for name in list(plugins_running.keys()):
        if not name in plugins.keys() and name in plugins_running:
            plugins_running.pop(name)
    for plugin in plugins.values():
        plugin_to_execute = plugin.copy()
        if 'lastChecked' in plugin_to_execute:
            plugin_to_execute.pop('lastChecked')
        if 'state' in plugin_to_execute:
            plugin_to_execute.pop('state')
        plugin_to_execute['hash'] = hash(json.dumps(plugin_to_execute))
        recreate = recreate_necessary(plugin_to_execute)
        if recreate:
            print('registered plugin ' + plugin_to_execute['name'] + ' (' + str(plugin_to_execute['hash']) + ')')
            plugins_running[plugin['name']] = plugin_to_execute['hash']
            schedule.every(plugin['checkInterval']).minutes.do(lambda: execute_scrape(plugin_to_execute))
        
def state_check():
    schedule.every(0.3).minutes.do(register_plugins)
    while True:
        schedule.run_pending()
        time.sleep(5)

async def start_api():
    flask_api.run()

def start():
    api = Thread(target = flask_api.run)
    checker = Thread(target = state_check)
    api.start()
    checker.start()
    telebot.run()
    api.join()
    checker.join()

#state_check()
# api.run()
start()