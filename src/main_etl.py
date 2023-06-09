#----------------IMPORTS-----------------
import requests
from bs4 import BeautifulSoup

from s3_load import s3_loader

import re
import json
import sys
import uuid

from dotenv import load_dotenv
import logging
import logging.config
import os

import pymongo
import sqlite3

import pandas as pd

"""Logger conf
"""
logging.config.fileConfig("../config/logging.conf")

""".ENV Load
"""

load_dotenv()

#----------------MAIN FUNCTION-----------------

def gw2_etl(url):

    #----------------EXTRACT-----------------

    def log_scrape(url):

        HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}

        try:
            response = requests.get(url=url, headers=HEADERS)
            logging.info(f'{url}: {response.status_code}')
        except IndexError as ie:
            logging.critical(f'{url} could not be reached. Error: ( {ie} )')

        soup = BeautifulSoup(response.content, 'html.parser')

        data = soup.find_all('script')[8]
        dataString = data.text.rstrip()

        logData = re.findall(r'{.*}', dataString)

        global bossName
        try:
            urlLines = url.split('/')
            if len(urlLines) < 5:
                bossName = urlLines[3]
            elif len(urlLines) == 5:
                bossName = urlLines[4]
        except Exception as e:
            return 'Error' + str(e)
        
        global jsonFile
        for line in logData:
            jsonFile = line

        logging.info('Extraction done!')        
        return jsonFile
    
    #---------------TRANSFORM----------------

    def store_data(jsonFile):

        global data
        data = json.loads(jsonFile)

        bossTag = bossName.split('_')
        global nameTag
        nameTag = bossTag[1]

        # Target boss
        target = []
        if nameTag == 'twinlargos' or nameTag == 'twins':
            target.append('Twin Largos')
        else:
            target.append(data['targets'][0]['name'])
        
        #-----------Set global variables for data loading-----------
        global stats_dict, player_group,player_acc,player_names,player_classes, \
            player_dps1,player_dps2,player_dps3,player_dps4,player_dps5,player_dps6, \
                ice_phase_dps,fire_phase_dps,storm_phase_dps,abomination_phase_dps, \
                    full_fight_dps_list, \
                        from100_to75_dps,from75_to50_dps,from50_to25_dps,from25_to0_dps, \
                            from100_to10_dps,from10_to0_dps, \
                                pre_breakbar1_dps,pre_breakbar2_dps,pre_breakbar3_dps, \
                                    main_fight_dps,dhuum_fight_dps,ritual_dps, \
                                        burn1_dps,burn2_dps,burn3_dps, \
                                            nikare1_dps,kenut1_dps,nikare2_dps,kenut2_dps,nikare3_dps,kenut3_dps, \
                                                qadimP1_dps,qadimP2_dps,qadimP3_dps

        #-----------Players Data-----------
        player_group = []
        player_acc = []
        player_names = []
        player_classes = []

        #-----------DPS Data-----------
        player_dps1 = []
        player_dps2 = []
        player_dps3 = []
        player_dps4 = []
        player_dps5 = []
        player_dps6 = []

        ice_phase_dps = []
        fire_phase_dps = []
        storm_phase_dps = []
        abomination_phase_dps = []

        full_fight_dps_list = []

        from100_to75_dps = []
        from75_to50_dps = []
        from50_to25_dps = []
        from25_to0_dps = []

        from100_to10_dps = []
        from10_to0_dps = []

        pre_breakbar1_dps = []
        pre_breakbar2_dps = []
        pre_breakbar3_dps = []

        main_fight_dps = []
        dhuum_fight_dps = []
        ritual_dps = []

        burn1_dps = []
        burn2_dps = []
        burn3_dps = []

        nikare1_dps = []
        kenut1_dps = []

        nikare2_dps = []
        kenut2_dps = []

        nikare3_dps = []
        kenut3_dps = []

        qadimP1_dps = []
        qadimP2_dps = []
        qadimP3_dps = []

        #-----------Data Sorting-----------

        for player in data['players']:
            player_group.append(player['group'])
            player_acc.append(player['acc'])
            player_names.append(player['name'])
            player_classes.append(player['profession'])
        
        try:
            #-----------Wing-1-----------
            if nameTag == 'vg':

                # Phase_1
                phase1 = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2 = data['phases'][6]['dpsStats']

                phase2_time_raw = data['phases'][6]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3 = data['phases'][12]['dpsStats']

                phase3_time_raw = data['phases'][12]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3
                    }
                }

            elif nameTag == 'gors':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))
                
                # Phase_2
                phase2_dps = data['phases'][4]['dpsStats']

                phase2_time_raw = data['phases'][4]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][7]['dpsStats']

                phase3_time_raw = data['phases'][7]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3
                    }
                }

            elif nameTag == 'sab':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2_dps = data['phases'][3]['dpsStats']

                phase2_time_raw = data['phases'][3]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][6]['dpsStats']

                phase3_time_raw = data['phases'][6]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                # Phase_4
                try:
                    phase4_dps = data['phases'][9]['dpsStats']

                    phase4_time_raw = data['phases'][9]['duration']
                    phase4_time = round(phase4_time_raw/1000,1)
                except IndexError:
                    phase4_dps = data['phases'][8]['dpsStats']

                    phase4_time_raw = data['phases'][8]['duration']
                    phase4_time = round(phase4_time_raw/1000,1)

                for dps in phase4_dps:
                    dps4_raw = dps[0]
                    player_dps4.append(round(dps4_raw/phase4_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3,
                        'phase_4_dps': player_dps4
                    }
                }

            #-----------Wing-2-----------
            elif nameTag == 'sloth':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2_dps = data['phases'][3]['dpsStats']

                phase2_time_raw = data['phases'][3]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][5]['dpsStats']

                phase3_time_raw = data['phases'][5]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                # Phase_4
                phase4_dps = data['phases'][7]['dpsStats']

                
                phase4_time_raw = data['phases'][7]['duration']
                phase4_time = round(phase4_time_raw/1000,1)

                for dps in phase4_dps:
                    dps4_raw = dps[0]
                    player_dps4.append(round(dps4_raw/phase4_time,2))

                # Phase_5
                phase5_dps = data['phases'][9]['dpsStats']

                phase5_time_raw = data['phases'][9]['duration']
                phase5_time = round(phase5_time_raw/1000,1)

                for dps in phase5_dps:
                    dps5_raw = dps[0]
                    player_dps5.append(round(dps5_raw/phase5_time,2))

                # Phase_6
                phase6_dps = data['phases'][11]['dpsStats']

                phase6_time_raw = data['phases'][11]['duration']
                phase6_time = round(phase6_time_raw/1000,1)

                for dps in phase6_dps:
                    dps6_raw = dps[0]
                    player_dps6.append(round(dps6_raw/phase6_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3,
                        'phase_4_dps': player_dps4,
                        'phase_5_dps': player_dps5,
                        'phase_6_dps': player_dps6
                    }
                }

            elif nameTag == 'matt':

                # Ice_phase
                ice_phase = data['phases'][1]['dpsStats']

                ice_phase_time_raw = data['phases'][1]['duration']
                ice_phase_time = round(ice_phase_time_raw/1000,1)

                for dps in ice_phase:
                    dps_ice_raw = dps[0]
                    ice_phase_dps.append(round(dps_ice_raw/ice_phase_time,2))

                # Fire_phase
                fire_phase = data['phases'][3]['dpsStats']

                fire_phase_time_raw = data['phases'][3]['duration']
                fire_phase_time = round(fire_phase_time_raw/1000,1)

                for dps in fire_phase:
                    dps_fire_raw = dps[0]
                    fire_phase_dps.append(round(dps_fire_raw/fire_phase_time,2))

                # Storm_phase
                storm_phase = data['phases'][5]['dpsStats']

                storm_phase_time_raw = data['phases'][5]['duration']
                storm_phase_time = round(storm_phase_time_raw/1000,1)

                for dps in storm_phase:
                    dps_storm_raw = dps[0]
                    storm_phase_dps.append(round(dps_storm_raw/storm_phase_time,2))

                # Abomination_phase
                abomination_phase = data['phases'][6]['dpsStats']

                abomination_phase_time_raw = data['phases'][6]['duration']
                abomination_phase_time = round(abomination_phase_time_raw/1000,1)

                for dps in abomination_phase:
                    dps_abom_raw = dps[0]
                    abomination_phase_dps.append(round(dps_abom_raw/abomination_phase_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'ice_phase_dps': ice_phase_dps,
                        'fire_phase_dps': fire_phase_dps,
                        'storm_phase_dps': storm_phase_dps,
                        'abomination_phase_dps': abomination_phase_dps
                    }
                }

            #-----------Wing-3-----------
            elif nameTag == 'kc':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))
                
                # Phase_2
                phase2_dps = data['phases'][5]['dpsStats']

                phase2_time_raw = data['phases'][5]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][9]['dpsStats']

                phase3_time_raw = data['phases'][9]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3
                    }
                }

            elif nameTag == 'xera':

                    # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))
                
                # Phase_2
                phase2_dps = data['phases'][4]['dpsStats']

                phase2_time_raw = data['phases'][4]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2
                    }
                }

            #-----------Wing-4-----------
            elif nameTag == 'cairn':
                full_fight_dps_list = []

                # Full_fight
                full_fight_dps = data['phases'][0]['dpsStats']

                full_fight_time_raw = data['phases'][0]['duration']
                full_fight_time = round(full_fight_time_raw/1000,1)

                for dps in full_fight_dps:
                    full_fight_raw = dps[0]
                    full_fight_dps_list.append(round(full_fight_raw/full_fight_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'full_fight_dps': full_fight_dps_list
                    }
                }

            elif nameTag == 'mo':

                # 100-75
                from100_to75 = data['phases'][1]['dpsStats']

                from100_to75_time_raw = data['phases'][1]['duration']
                from100_to75_time = round(from100_to75_time_raw/1000,1)

                for dps in from100_to75:
                    dps1_raw = dps[0]
                    from100_to75_dps.append(round(dps1_raw/from100_to75_time,2))

                # 75-50
                from75_to50 = data['phases'][2]['dpsStats']

                from75_to50_time_raw = data['phases'][2]['duration']
                from75_to50_time = round(from75_to50_time_raw/1000,1)

                for dps in from75_to50:
                    dps2_raw = dps[0]
                    from75_to50_dps.append(round(dps2_raw/from75_to50_time,2))

                # 50-25
                from50_to25 = data['phases'][3]['dpsStats']

                from50_to25_time_raw = data['phases'][3]['duration']
                from50_to25_time = round(from50_to25_time_raw/1000,1)

                for dps in from50_to25:
                    dps3_raw = dps[0]
                    from50_to25_dps.append(round(dps3_raw/from50_to25_time,2))

                # 25-0
                from25_to0 = data['phases'][4]['dpsStats']

                from25_to0_time_raw = data['phases'][4]['duration']
                from25_to0_time = round(from25_to0_time_raw/1000,1)

                for dps in from25_to0:
                    dps4_raw = dps[0]
                    from25_to0_dps.append(round(dps4_raw/from25_to0_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        '100 - 75%': from100_to75_dps,
                        '75 - 50%': from75_to50_dps,
                        '50 - 25%': from50_to25_dps,
                        '25 - 0%': from25_to0_dps
                    }
                }

            elif nameTag == 'sam':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))
                
                # Phase_2
                phase2_dps = data['phases'][6]['dpsStats']

                phase2_time_raw = data['phases'][6]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][11]['dpsStats']

                phase3_time_raw = data['phases'][11]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3
                    }
                }

            elif nameTag == 'dei':

                # 100-10
                from100_to10 = data['phases'][1]['dpsStats']

                from100_to10_time_raw = data['phases'][1]['duration']
                from100_to10_time = round(from100_to10_time_raw/1000,1)

                for dps in from100_to10:
                    dps1_raw = dps[0]
                    from100_to10_dps.append(round(dps1_raw/from100_to10_time,2))

                # 10-0
                try:
                    from10_to0 = data['phases'][17]['dpsStats']
                except:
                    try:
                        from10_to0 = data['phases'][15]['dpsStats']
                    except:
                        from10_to0 = data['phases'][12]['dpsStats']

                try:
                    from10_to0_time_raw = data['phases'][17]['duration']
                    from10_to0_time = round(from10_to0_time_raw/1000,1)
                except:
                    try:
                        from10_to0_time_raw = data['phases'][15]['duration']
                        from10_to0_time = round(from10_to0_time_raw/1000,1)
                    except:
                        from10_to0_time_raw = data['phases'][12]['duration']
                        from10_to0_time = round(from10_to0_time_raw/1000,1)

                for dps in from10_to0:
                    dps2_raw = dps[0]
                    from10_to0_dps.append(round(dps2_raw/from10_to0_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        '100 - 10%': from100_to10_dps,
                        '10 - 0%': from10_to0_dps
                    }
                }

            #-----------Wing-5-----------
            elif nameTag == 'sh':

                # Pre_breakbar1
                pre_breakbar1 = data['phases'][1]['dpsStats']

                pre_breakbar1_time_raw = data['phases'][1]['duration']
                pre_breakbar1_time = round(pre_breakbar1_time_raw/1000,1)

                for dps in pre_breakbar1:
                    breakbar1_raw = dps[0]
                    pre_breakbar1_dps.append(round(breakbar1_raw/pre_breakbar1_time,2))

                # Pre_breakbar2
                pre_breakbar2 = data['phases'][3]['dpsStats']

                pre_breakbar2_time_raw = data['phases'][3]['duration']
                pre_breakbar2_time = round(pre_breakbar2_time_raw/1000,1)

                for dps in pre_breakbar2:
                    breakbar2_raw = dps[0]
                    pre_breakbar2_dps.append(round(breakbar2_raw/pre_breakbar2_time,2))
                    
                # Pre_breakbar3
                pre_breakbar3 = data['phases'][5]['dpsStats']

                pre_breakbar3_time_raw = data['phases'][5]['duration']
                pre_breakbar3_time = round(pre_breakbar3_time_raw/1000,1)

                for dps in pre_breakbar3:
                    breakbar3_raw = dps[0]
                    pre_breakbar3_dps.append(round(breakbar3_raw/pre_breakbar3_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'Pre-breakbar1_dps': pre_breakbar1_dps,
                        'Pre-breakbar2_dps': pre_breakbar2_dps,
                        'Pre-breakbar3_dps': pre_breakbar3_dps
                    }
                }

            elif nameTag == 'dhuum':

                # Main_fight
                main_fight = data['phases'][2]['dpsStats']

                main_fight_time_raw = data['phases'][2]['duration']
                main_fight_time = round(main_fight_time_raw/1000,1)

                for dps in main_fight:
                    main_raw = dps[0]
                    main_fight_dps.append(round(main_raw/main_fight_time,2))

                # Dhuum_fight
                dhuum_fight = data['phases'][3]['dpsStats']

                dhuum_fight_time_raw = data['phases'][3]['duration']
                dhuum_fight_time = round(dhuum_fight_time_raw/1000,1)

                for dps in dhuum_fight:
                    dhuum_raw = dps[0]
                    dhuum_fight_dps.append(round(dhuum_raw/dhuum_fight_time,2))
                    
                # Ritual
                try:
                    ritual = data['phases'][10]['dpsStats']

                    ritual_time_raw = data['phases'][10]['duration']
                    ritual_time = round(ritual_time_raw/1000,1)
                except:
                    ritual = data['phases'][8]['dpsStats']

                    ritual_time_raw = data['phases'][8]['duration']
                    ritual_time = round(ritual_time_raw/1000,1)

                for dps in ritual:
                    ritual_raw = dps[0]
                    ritual_dps.append(round(ritual_raw/ritual_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'Main_fight_dps': main_fight_dps,
                        'Dhuum_fight_dps': dhuum_fight_dps,
                        'Ritual_dps': ritual_dps
                    }
                }

            #-----------Wing-6-----------
            elif nameTag == 'ca':

                # Burn1
                burn1 = data['phases'][2]['dpsStats']

                burn1_time_raw = data['phases'][2]['duration']
                burn1_time = round(burn1_time_raw/1000,1)

                for dps in burn1:
                    burn1_raw = dps[0]
                    burn1_dps.append(round(burn1_raw/burn1_time,2))

                # Burn2
                burn2 = data['phases'][4]['dpsStats']

                burn2_time_raw = data['phases'][4]['duration']
                burn2_time = round(burn2_time_raw/1000,1)

                for dps in burn2:
                    burn2_raw = dps[0]
                    burn2_dps.append(round(burn2_raw/burn2_time,2))
                    
                # Burn3
                burn3 = data['phases'][6]['dpsStats']

                burn3_time_raw = data['phases'][6]['duration']
                burn3_time = round(burn3_time_raw/1000,1)

                for dps in burn3:
                    burn3_raw = dps[0]
                    burn3_dps.append(round(burn3_raw/burn3_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'Burn_1_dps': burn1_dps,
                        'Burn_2_dps': burn2_dps,
                        'Burn_3_dps': burn3_dps
                    }
                }
            
            elif nameTag == 'twinlargos' or nameTag == 'twins':

                # Nikare1
                nikare1 = data['phases'][1]['dpsStats']

                nikare1_time_raw = data['phases'][1]['duration']
                nikare1_time = round(nikare1_time_raw/1000,1)

                for dps in nikare1:
                    nikare1_raw = dps[0]
                    nikare1_dps.append(round(nikare1_raw/nikare1_time,2))

                # Kenut1
                kenut1 = data['phases'][2]['dpsStats']

                kenut1_time_raw = data['phases'][2]['duration']
                kenut1_time = round(kenut1_time_raw/1000,1)

                for dps in kenut1:
                    kenut1_raw = dps[0]
                    kenut1_dps.append(round(kenut1_raw/kenut1_time,2))

                # Nikare2
                nikare2 = data['phases'][3]['dpsStats']

                nikare2_time_raw = data['phases'][3]['duration']
                nikare2_time = round(nikare2_time_raw/1000,1)

                for dps in nikare2:
                    nikare2_raw = dps[0]
                    nikare2_dps.append(round(nikare2_raw/nikare2_time,2))
                
                # Kenut2
                kenut2 = data['phases'][4]['dpsStats']

                kenut2_time_raw = data['phases'][4]['duration']
                kenut2_time = round(kenut2_time_raw/1000,1)

                for dps in kenut2:
                    kenut2_raw = dps[0]
                    kenut2_dps.append(round(kenut2_raw/kenut2_time,2))
                    
                # Nikare3
                nikare3 = data['phases'][7]['dpsStats']

                nikare3_time_raw = data['phases'][7]['duration']
                nikare3_time = round(nikare3_time_raw/1000,1)

                for dps in nikare3:
                    nikare3_raw = dps[0]
                    nikare3_dps.append(round(nikare3_raw/nikare3_time,2))
                
                # Kenut3
                kenut3 = data['phases'][8]['dpsStats']

                kenut3_time_raw = data['phases'][8]['duration']
                kenut3_time = round(kenut3_time_raw/1000,1)

                for dps in kenut3:
                    kenut3_raw = dps[0]
                    kenut3_dps.append(round(kenut3_raw/kenut3_time,2))
                
                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'Nikare_1_dps': nikare1_dps,
                        'Kenut_1_dps': kenut1_dps,
                        'Nikare_2_dps': nikare2_dps,
                        'Kenut_2_dps': kenut2_dps,
                        'Nikare_3_dps': nikare3_dps,
                        'Kenut_3_dps': kenut3_dps
                    }
                }

            elif nameTag == 'qadim':

                # QadimP1
                qadimP1 = data['phases'][4]['dpsStats']

                qadimP1_time_raw = data['phases'][4]['duration']
                qadimP1_time = round(qadimP1_time_raw/1000,1)

                for dps in qadimP1:
                    qadimp1_raw = dps[0]
                    qadimP1_dps.append(round(qadimp1_raw/qadimP1_time,2))

                # QadimP2
                qadimP2 = data['phases'][8]['dpsStats']

                qadimP2_time_raw = data['phases'][8]['duration']
                qadimP2_time = round(qadimP2_time_raw/1000,1)

                for dps in qadimP2:
                    qadimp2_raw = dps[0]
                    qadimP2_dps.append(round(qadimp2_raw/qadimP2_time,2))
                    
                # QadimP3
                qadimP3 = data['phases'][11]['dpsStats']

                qadimP3_time_raw = data['phases'][11]['duration']
                qadimP3_time = round(qadimP3_time_raw/1000,1)

                for dps in qadimP3:
                    qadimp3_raw = dps[0]
                    qadimP3_dps.append(round(qadimp3_raw/qadimP3_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'Qadim_P1_dps': qadimP1_dps,
                        'Qadim_P2_dps': qadimP2_dps,
                        'Qadim_P3_dps': qadimP3_dps
                    }
                } 

            #-----------Wing-7-----------
            elif nameTag == 'adina':

                # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2_dps = data['phases'][3]['dpsStats']

                phase2_time_raw = data['phases'][3]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3_dps = data['phases'][5]['dpsStats']

                phase3_time_raw = data['phases'][5]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                # Phase_4
                phase4_dps = data['phases'][7]['dpsStats']

                phase4_time_raw = data['phases'][7]['duration']
                phase4_time = round(phase4_time_raw/1000,1)

                for dps in phase4_dps:
                    dps4_raw = dps[0]
                    player_dps4.append(round(dps4_raw/phase4_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3,
                        'phase_4_dps': player_dps4
                    }
                }

            elif nameTag == 'sabir':

                # Phase_1
                phase1 = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2 = data['phases'][3]['dpsStats']

                phase2_time_raw = data['phases'][3]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                phase3 = data['phases'][5]['dpsStats']

                phase3_time_raw = data['phases'][5]['duration']
                phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3
                    }
                }

            elif nameTag == 'prlqadim' or nameTag == 'qpeer':

                    # Phase_1
                phase1_dps = data['phases'][1]['dpsStats']

                phase1_time_raw = data['phases'][1]['duration']
                phase1_time = round(phase1_time_raw/1000,1)

                for dps in phase1_dps:
                    dps1_raw = dps[0]
                    player_dps1.append(round(dps1_raw/phase1_time,2))

                # Phase_2
                phase2_dps = data['phases'][3]['dpsStats']

                phase2_time_raw = data['phases'][3]['duration']
                phase2_time = round(phase2_time_raw/1000,1)

                for dps in phase2_dps:
                    dps2_raw = dps[0]
                    player_dps2.append(round(dps2_raw/phase2_time,2))

                # Phase_3
                try:
                    phase3_dps = data['phases'][5]['dpsStats']

                    phase3_time_raw = data['phases'][5]['duration']
                    phase3_time = round(phase3_time_raw/1000,1)
                except:
                    phase3_dps = data['phases'][6]['dpsStats']

                    phase3_time_raw = data['phases'][6]['duration']
                    phase3_time = round(phase3_time_raw/1000,1)

                for dps in phase3_dps:
                    dps3_raw = dps[0]
                    player_dps3.append(round(dps3_raw/phase3_time,2))

                # Phase_4
                try:
                    phase4_dps = data['phases'][7]['dpsStats']

                    
                    phase4_time_raw = data['phases'][7]['duration']
                    phase4_time = round(phase4_time_raw/1000,1)
                except :
                    phase4_dps = data['phases'][9]['dpsStats']

                    
                    phase4_time_raw = data['phases'][9]['duration']
                    phase4_time = round(phase4_time_raw/1000,1)

                for dps in phase4_dps:
                    dps4_raw = dps[0]
                    player_dps4.append(round(dps4_raw/phase4_time,2))

                # Phase_5
                try:
                    phase5_dps = data['phases'][9]['dpsStats']

                    phase5_time_raw = data['phases'][9]['duration']
                    phase5_time = round(phase5_time_raw/1000,1)
                except IndexError:
                    try:
                        phase5_dps = data['phases'][10]['dpsStats']

                        phase5_time_raw = data['phases'][10]['duration']
                        phase5_time = round(phase5_time_raw/1000,1)
                    except:
                        phase5_dps = data['phases'][11]['dpsStats']

                        phase5_time_raw = data['phases'][11]['duration']
                        phase5_time = round(phase5_time_raw/1000,1)

                for dps in phase5_dps:
                    dps5_raw = dps[0]
                    player_dps5.append(round(dps5_raw/phase5_time,2))

                # Phase_6
                try:
                    phase6_dps = data['phases'][11]['dpsStats']

                    phase6_time_raw = data['phases'][11]['duration']
                    phase6_time = round(phase6_time_raw/1000,1)
                except IndexError:
                    try:
                        phase6_dps = data['phases'][12]['dpsStats']

                        phase6_time_raw = data['phases'][12]['duration']
                        phase6_time = round(phase6_time_raw/1000,1)
                    except:
                        phase6_dps = data['phases'][13]['dpsStats']

                        phase6_time_raw = data['phases'][13]['duration']
                        phase6_time = round(phase6_time_raw/1000,1)

                for dps in phase6_dps:
                    dps6_raw = dps[0]
                    player_dps6.append(round(dps6_raw/phase6_time,2))

                stats_dict = {
                    'boss': target,
                    'players':{
                        'group': player_group,
                        'account': player_acc,
                        'names': player_names,
                        'profession': player_classes,
                        'phase_1_dps': player_dps1,
                        'phase_2_dps': player_dps2,
                        'phase_3_dps': player_dps3,
                        'phase_4_dps': player_dps4,
                        'phase_5_dps': player_dps5,
                        'phase_6_dps': player_dps6
                    }
                }

        except Exception as e:
            logging.warning('Error' + str(e))
            pass
        
        logging.info('Transformation done!')
        return stats_dict

        #-----------------LOAD-------------------

    def db_load(json_data):
        logging.info('-'*10)

        #-----------SQLite conn-----------
        logging.info('SQLite conn starting...')

        try:
            conn = sqlite3.connect(os.getenv('DB_DIR'))
            cur = conn.cursor()
        except Exception as e:
            logging.warning(f'Connection could not be done: {str(e)}')
            sys.exit()
        
        #-----------UUID data insert----------
        """
        Trial phase:
            Not yet working, maybe needs blob datatype since SQLite does not accept UUID as datatype
        """
        #uuid_token = uuid.uuid4()

        #cur.execute(f"INSERT INTO encounters(encounter_id,encounter_date) VALUES({uuid_token},{data['encounterStart']})")
        #cur.execute('''INSERT INTO encounters(encounter_id,encounter_date) VALUES(?,?)''',(uuid_token, data['encounterStart']))

        # Encounter date - data insert
        """Encounter Date

        Insert of encounter date on table encounters -> related to ?
        """

        #cur.execute(f"INSERT INTO _ VALUES _")
        
        #-----------DPS data insert-----------
        try:
            if nameTag == 'vg':
                boss_id = 1

                for (dps1,dps2,dps3,acc) in zip(player_dps1,player_dps2,player_dps3,player_acc):
                    cur.execute(
                        f"INSERT INTO vg_dps(phase1_dps,phase2_dps,phase3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'gors':
                boss_id = 2
                
                for (dps1,dps2,dps3,acc) in zip(player_dps1,player_dps2,player_dps3,player_acc):
                    cur.execute(
                        f"INSERT INTO gors_dps(phase1_dps,phase2_dps,phase3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'sab':
                boss_id = 3
                
                for (dps1,dps2,dps3,dps4,acc) in zip(player_dps1,player_dps2,player_dps3,player_dps4,player_acc):
                    cur.execute(
                        f"INSERT INTO sab_dps(phase1_dps,phase2_dps,phase3_dps,phase4_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},'{acc}')"
                    )
            elif nameTag == 'sloth':
                boss_id = 4

                for (dps1,dps2,dps3,dps4,dps5,dps6,acc) in zip(player_dps1,player_dps2,player_dps3,player_dps4,player_dps5,player_dps6,player_acc):
                    cur.execute(
                        f"INSERT INTO sloth_dps(phase1_dps,phase2_dps,phase3_dps,phase4_dps,phase5_dps,phase6_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},{dps5},{dps6},'{acc}')"
                    )
            elif nameTag == 'matt':
                boss_id = 5

                for (dps1,dps2,dps3,dps4,acc) in zip(ice_phase_dps,fire_phase_dps,storm_phase_dps,abomination_phase_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO matt_dps(ice_dps,fire_dps,storm_dps,abomination_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},'{acc}')"
                    )
            elif nameTag == 'kc':
                boss_id = 6

                for (dps1,dps2,dps3,acc) in zip(player_dps1,player_dps2,player_dps3,player_acc):
                    cur.execute(
                        f"INSERT INTO kc_dps(phase1_dps,phase2_dps,phase3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'xera':
                boss_id = 7

                for (dps1,dps2,acc) in zip(player_dps1,player_dps2,player_acc):
                    cur.execute(
                        f"INSERT INTO xera_dps(phase1_dps,phase2_dps,FK_player_id) VALUES({dps1},{dps2},'{acc}')"
                    )
            elif nameTag == 'cairn':
                boss_id = 8

                for (dps1,acc) in zip(full_fight_dps_list,player_acc):
                    cur.execute(
                        f"INSERT INTO cairn_dps(full_fight_dps,FK_player_id) VALUES({dps1},'{acc}')"
                    )
            elif nameTag == 'mo':
                boss_id = 9

                for (dps1,dps2,dps3,dps4,acc) in zip(from100_to75_dps,from75_to50_dps,from50_to25_dps,from25_to0_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO mo_dps(_100to75,_75to50,_50to25,_25to0,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},'{acc}')"
                    )
            elif nameTag == 'sam':
                boss_id = 10

                for (dps1,dps2,dps3,acc) in zip(player_dps1,player_dps2,player_dps3,player_acc):
                    cur.execute(
                        f"INSERT INTO sam_dps(phase1_dps,phase2_dps,phase3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'dei':
                boss_id = 11

                for (dps1,dps2,acc) in zip(from100_to10_dps,from10_to0_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO dei_dps(_100to10,_10to0,FK_player_id) VALUES({dps1},{dps2},'{acc}')"
                    )
            elif nameTag == 'sh':
                boss_id = 12

                for (dps1,dps2,dps3,acc) in zip(pre_breakbar1_dps,pre_breakbar2_dps,pre_breakbar3_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO sh_dps(prebreakbar1_dps,prebreakbar2_dps,prebreakbar3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'dhuum':
                boss_id = 13

                for (dps1,dps2,dps3,acc) in zip(main_fight_dps,dhuum_fight_dps,ritual_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO dhuum_dps(main_fight_dps,dhuum_fight_dps,ritual_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'ca':
                boss_id = 14

                for (dps1,dps2,dps3,acc) in zip(burn1_dps,burn2_dps,burn3_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO ca_dps(burn1_dps,burn2_dps,burn3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'twinlargos' or nameTag == 'twins':
                boss_id = 15

                for (dps1,dps2,dps3,dps4,dps5,dps6,acc) in zip(nikare1_dps,kenut1_dps,nikare2_dps,kenut2_dps,nikare3_dps,kenut3_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO twinlargos_dps(nikare1_dps,kenut1_dps,nikare2_dps,kenut2_dps,nikare3_dps,kenut3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},{dps5},{dps6},'{acc}')"
                    )
            elif nameTag == 'qadim':
                boss_id = 16

                for (dps1,dps2,dps3,acc) in zip(qadimP1_dps,qadimP2_dps,qadimP3_dps,player_acc):
                    cur.execute(
                        f"INSERT INTO qadim1_dps(qadim_p1_dps,qadim_p2_dps,qadim_p3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'adina':
                boss_id = 17

                for (dps1,dps2,dps3,dps4,acc) in zip(player_dps1,player_dps2,player_dps3,player_dps4,player_acc):
                    cur.execute(
                        f"INSERT INTO adina_dps(phase1_dps,phase2_dps,phase3_dps,phase4_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},'{acc}')"
                    )
            elif nameTag == 'sabir':
                boss_id = 18

                for (dps1,dps2,dps3,acc) in zip(player_dps1,player_dps2,player_dps3,player_acc):
                    cur.execute(
                        f"INSERT INTO sabir_dps(phase1_dps,phase2_dps,phase3_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},'{acc}')"
                    )
            elif nameTag == 'prlqadim' or nameTag == 'qpeer':
                boss_id = 19

                for (dps1,dps2,dps3,dps4,dps5,dps6,acc) in zip(player_dps1,player_dps2,player_dps3,player_dps4,player_dps5,player_dps6,player_acc):
                    cur.execute(
                        f"INSERT INTO prlqadim_dps(phase1_dps,phase2_dps,phase3_dps,phase4_dps,phase5_dps,phase6_dps,FK_player_id) VALUES({dps1},{dps2},{dps3},{dps4},{dps5},{dps6},'{acc}')"
                    )
        except Exception as e:
            logging.warning(f"Failed to insert dps data: {str(e)}")
        
        #-----------Players name, profession and account data insert-----------
        for (name,acc,profession) in zip(player_names,player_acc,player_classes):

            professions_dict = {
            "Guardian": 1,"Dragonhunter": 2,"Firebrand": 3,"Willbender": 4,
            "Revenant": 5,"Herald": 6,"Renegade": 7,"Vindicator": 8,
            "Warrior": 9,"Berserker": 10,"Spellbreaker": 11,"Bladesworn": 12,
            "Engineer": 13,"Scrapper": 14,"Holosmith": 15,"Mechanist": 16,
            "Ranger": 17,"Druid": 18,"Soulbeast": 19,"Untamed": 20,
            "Thief": 21,"Daredevil": 22,"Deadeye": 23,"Specter": 24,
            "Elementalist": 25,"Tempest": 26,"Weaver": 27,"Catalyst": 28,
            "Mesmer": 29,"Chronomancer": 30,"Mirage": 31,"Virtuoso": 32,
            "Necromancer": 33,"Reaper": 34,"Scourge": 35,"Harbinger": 36
            }

            class_id = professions_dict[profession]
            
            cur.execute(
                f'INSERT INTO player_info(account,name,boss_id,profession_id) VALUES("{acc}","{name}",{boss_id},{class_id})'
            )
            conn.commit()

        logging.info(f'{nameTag} dps data inserted.')

        uuid_tag = uuid.uuid4()

        sqlite_df = pd.read_sql_query(f"SELECT * FROM {nameTag}_dps;",conn)
        sqlite_df.to_csv(f'./tmp/{nameTag}_dps.csv',index=False)
        csv_name = f'{uuid_tag}-{nameTag}_dps.csv'

        s3_loader(f'./tmp/{nameTag}_dps.csv','gw2-srs-bucket',csv_name)

        logging.info('CSV uploaded.')

        logging.info('Player data inserted!')

        logging.info('-'*10)

        #-----------MongoDB conn-----------
        logging.info('MongoDB conn starting...')

        try:
           client = pymongo.MongoClient(os.getenv('MONGO_DB'))
        except Exception as e:
           logging.warning(f'Connection could not be done: {str(e)}')
           sys.exit()

        db = client['gw2_srs_stats']
        collection = db['encounters']

        collection.insert_one(json_data)
        logging.info('MongoDB load done!')
    
    db_load(store_data(log_scrape(url)))