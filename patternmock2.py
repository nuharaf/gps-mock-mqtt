# this script do what patternmock do but using hbmqtt client library
import logging
import asyncio
import time
import sys
import random
import json
from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2


async def main(loop):
    # starting point
    lons = [round(110.15 + (x*0.03), 2) for x in range(10)]
    lats = [round(-7.75 - (x*0.015), 2) for x in range(10)]
    latslons = [[m, n] for m in lats for n in lons]
    # radius = 500,point = 100
    paths = [[0, 0.004491576420597607], [-0.00028202841753038795, 0.004482713320516494], [-0.000562943797729746, 0.00445615899888065], [-0.0008416374959173631, 0.0044120182534679595], [-0.0011170096353773965, 0.004350465287637668], [-0.0013879734480701851, 0.004271743022829213], [-0.0016534595636096127, 0.004176162139862121], [-0.0019124202295797796, 0.004064099852820576], [-0.002163833446535356, 0.003935998420361553], [-0.002406707001366657, 0.0037923634003217232], [-0.002640082383111567, 0.003633761654511397], [-0.002863038565760383, 0.0034608191115696883], [-0.0030746956431245945, 0.0032742182967099086], [-0.003274218301424424, 0.003074695638104146], [-0.003460819115890429, 0.002863038560537505], [-0.0036337616583689883, 0.0026400823778020472], [-0.00379236340366738, 0.0024067069960947473], [-0.0039359984231684565, 0.002163833441429618], [-0.004064099855084471, 0.001912420224768758], [-0.0041761621416010804, 0.0016534595592175025], [-0.004271743024082621, 0.0013879734442125927], [-0.0043504652884644186, 0.0011170096321574154], [-0.004412018253943965, 0.0008416374934220519], [-0.004456158999095738, 0.0005629437960271501], [-0.0044827133205708, 0.0002820284166672096], [-0.004491576420597607, -8.250892021464997e-19], [-0.0044827133205708, -0.0002820284166672113], [-0.0044561589990957376, -0.0005629437960271517], [-0.004412018253943965, -0.0008416374934220534], [-0.004350465288464419, -0.0011170096321574132], [-0.00427174302408262, -0.0013879734442125943], [-0.00417616214160108, -0.0016534595592175045], [-0.00406409985508447, -0.0019124202247687598], [-0.003935998423168457, -0.0021638334414296164], [-0.003792363403667381, -0.002406706996094745], [-0.0036337616583689875, -0.002640082377802049], [-0.003460819115890428, -0.0028630385605375058], [-0.003274218301424421, -0.0030746956381041486], [-0.003074695643124592, -0.0032742182967099116], [-0.002863038565760383, -0.003460819111569688], [-0.0026400823831115644, -0.0036337616545113987], [-0.002406707001366654, -0.0037923634003217254], [-0.0021638334465353525, -0.003935998420361555], [-0.0019124202295797762, -0.004064099852820578], [-0.001653459563609613, -0.004176162139862121], [-0.0013879734480701834, -0.004271743022829213], [-0.0011170096353773928, -0.004350465287637669], [-0.0008416374959173635, -0.0044120182534679595], [-0.0005629437977297445, -0.004456158998880651], [-0.0002820284175303882, -0.004482713320516494],
             [5.500594697878427e-19, -0.004491576420597607], [0.0002820284175303893, -0.004482713320516494], [0.0005629437977297455, -0.00445615899888065], [0.0008416374959173626, -0.0044120182534679595], [0.001117009635377396, -0.004350465287637668], [0.0013879734480701843, -0.004271743022829213], [0.0016534595636096138, -0.004176162139862121], [0.0019124202295797788, -0.004064099852820576], [0.002163833446535352, -0.003935998420361555], [0.002406707001366657, -0.0037923634003217237], [0.0026400823831115665, -0.003633761654511397], [0.0028630385657603835, -0.0034608191115696875], [0.003074695643124594, -0.00327421829670991], [0.0032742183014244208, -0.003074695638104149], [0.0034608191158904274, -0.002863038560537507], [0.0036337616583689875, -0.002640082377802048], [0.00379236340366738, -0.0024067069960947477], [0.003935998423168457, -0.0021638334414296172], [0.004064099855084468, -0.001912420224768762], [0.00417616214160108, -0.0016534595592175038], [0.004271743024082621, -0.0013879734442125923], [0.0043504652884644186, -0.0011170096321574151], [0.004412018253943965, -0.0008416374934220532], [0.004456158999095738, -0.0005629437960271497], [0.0044827133205708, -0.00028202841666721216], [0.004491576420597607, 2.750297340488332e-19], [0.0044827133205708, 0.0002820284166672127], [0.0044561589990957376, 0.0005629437960271513], [0.004412018253943965, 0.0008416374934220538], [0.0043504652884644186, 0.0011170096321574147], [0.00427174302408262, 0.001387973444212594], [0.00417616214160108, 0.0016534595592175056], [0.004064099855084469, 0.001912420224768762], [0.003935998423168458, 0.0021638334414296155], [0.00379236340366738, 0.0024067069960947464], [0.0036337616583689875, 0.002640082377802049], [0.0034608191158904274, 0.002863038560537507], [0.003274218301424421, 0.003074695638104149], [0.003074695643124593, 0.0032742182967099103], [0.002863038565760383, 0.003460819111569688], [0.0026400823831115665, 0.003633761654511397], [0.002406707001366655, 0.003792363400321725], [0.0021638334465353525, 0.003935998420361555], [0.0019124202295797781, 0.004064099852820577], [0.001653459563609613, 0.004176162139862121], [0.0013879734480701838, 0.004271743022829213], [0.001117009635377394, 0.004350465287637668], [0.0008416374959173628, 0.0044120182534679595], [0.0005629437977297442, 0.004456158998880651], [0.00028202841753038844, 0.004482713320516494], [0, 0.004491576420597607]]
    # starting point offset
    states = [int(random.uniform(0, len(paths))) for x in range(len(latslons))]
    # clientid
    clientid = [
        f'{sys.argv[2]}.{x}{y}' for x in 'abcdefghij' for y in 'QRSTUVWXYZ'][:int(sys.argv[3])]

    Clients = [MQTTClient(client_id = cid,config=dict(keep_alive=2)) for cid in clientid]
    task = [loop.create_task(c.connect(sys.argv[1])) for c in Clients]
    a = await asyncio.gather(*task)
    print("Client conencted" ,len(a))
    while True:
        
        msgs = [dict(lat=latlon[0] + offset[0], lon=latlon[1] + offset[1], time=int(time.time()))
                for latlon, offset in zip(latslons, [paths[state] for state in states])]
        states = [1 if state >= 100 else state + 1 for state in states]
        task = [c.publish("gps",json.dumps(msg).encode())for c,msg in zip(Clients,msgs)]
        a = await asyncio.gather(*task)
        print("message published" ,len(a))
        await asyncio.sleep(1000)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.run_forever()
