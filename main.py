import config
import gc
import json
from machine import Pin, I2C
from ina219 import INA219
from steppers import Stepper, Axis
from logging import ERROR
from microWebSrv import MicroWebSrv


# ina initialization
i2c = I2C(-1, Pin(config.device['ina_scl']), Pin(config.device['ina_sda']))
ina = INA219(config.device['shunt_ohms'], i2c, log_level=ERROR)
ina.configure()

# steppers initialization
m0 = Stepper(0, Pin(config.device['m1_dir']), Pin(config.device['m1_step']), Pin(config.device['m1_enable']), 500)
m1 = Stepper(1, Pin(config.device['m2_dir']), Pin(config.device['m2_step']), Pin(config.device['m2_enable']), 500)

# axis initialization
aperture = Axis(m0, ina, config.device['max_ma'])
focus = Axis(m1, ina, config.device['max_ma'])

# axis calibration
focus.calibration()
aperture.calibration()

# webserver functions

def _httpHandlerMemory(httpClient, httpResponse, routeArgs):
    print("In Memory HTTP variable route :")
    query = str(routeArgs['query'])

    if 'gc' in query or 'collect' in query:
        gc.collect()

    content = """\
        {}
        """.format(gc.mem_free())
    httpResponse.WriteResponseOk(headers=None,
                                contentType="text/html",
                                contentCharset="UTF-8",
                                content=content)



def _httpHandlerGetCalibration(httpClient, httpResponse, routeArgs):
    global focus, aperture

    mtype = routeArgs['mtype']

    if 'focus' in mtype:
        max_steps = focus.max_steps
        calibrated = focus.calibrated
    elif 'aperture' in mtype:
        max_steps = aperture.max_steps
        calibrated = aperture.calibrated

    data = {
        'mtype': mtype,
        'max_steps': max_steps,
        'calibrated': calibrated
    }

    httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=json.dumps(data))
    gc.collect()


def _httpHandlerSetCalibration(httpClient, httpResponse, routeArgs):
    global focus, aperture

    mtype = routeArgs['mtype']

    if 'focus' in mtype:
        max_steps = focus.calibration()
    elif 'aperture' in mtype:
        max_steps = aperture.calibration()

    data = {
        'mtype': mtype,
        'max_steps': max_steps
    }

    httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=json.dumps(data))
    gc.collect()

def _httpHandlerSetData(httpClient, httpResponse, routeArgs):
    global focus, aperture
    mtype = routeArgs['mtype']
    steps = int(routeArgs['steps'])
    clockwise = -1 if int(routeArgs['clockwise']) == 0 else 1
    status = 0

    if 'focus' in mtype:
        status = focus.move(clockwise * steps)
    elif 'aperture' in mtype:
        status = aperture.move(clockwise * steps)

    data = {
        'mtype': mtype,
        'steps': steps,
        'status': status,
        'clockwise': clockwise
    }

    httpResponse.WriteResponseOk(headers=None,
                                    contentType="text/html",
                                    contentCharset="UTF-8",
                                    content=json.dumps(data))
    gc.collect()

routeHandlers = [
    ("/move/<mtype>/<steps>/<clockwise>", "GET", _httpHandlerSetData),
    ("/calibration/<mtype>", "GET", _httpHandlerSetCalibration),
    ("/memory/<query>", "GET", _httpHandlerMemory)
]


mws = MicroWebSrv(routeHandlers=routeHandlers, webPath="www/")
mws.Start(threaded=True)
gc.collect()