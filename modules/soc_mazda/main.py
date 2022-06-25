#
#
#   $$\      $$\                           $$\                  $$$$$$\             $$$$$$\
#   $$$\    $$$ |                          $$ |                $$  __$$\           $$  __$$\
#   $$$$\  $$$$ | $$$$$$\  $$$$$$$$\  $$$$$$$ | $$$$$$\        $$ /  \__| $$$$$$\  $$ /  \__|
#   $$\$$\$$ $$ | \____$$\ \____$$  |$$  __$$ | \____$$\       \$$$$$$\  $$  __$$\ $$ |
#   $$ \$$$  $$ | $$$$$$$ |  $$$$ _/ $$ /  $$ | $$$$$$$ |       \____$$\ $$ /  $$ |$$ |
#   $$ |\$  /$$ |$$  __$$ | $$  _/   $$ |  $$ |$$  __$$ |      $$\   $$ |$$ |  $$ |$$ |  $$\
#   $$ | \_/ $$ |\$$$$$$$ |$$$$$$$$\ \$$$$$$$ |\$$$$$$$ |      \$$$$$$  |\$$$$$$  |\$$$$$$  |
#   \__|     \__| \_______|\________| \_______| \_______|       \______/  \______/  \______/
#
#
#

# SoC Module for Mazda
#
# Based on pymazda from bdr99
#
# Parameters:
#  1 - Chargepointnumber ('1' or '2')
#  2 - User ID (eMail address of Mazda user account
#  3 - Password for Mazda user account
#  4 - Region (North America = MNAO, Europe = MME, Japan = MJO)
#  5 - vin of vehicle for SoC check
#  6 - Log Level 'Debug', 'INFO', 'WARNING', 'ERROR' or 'CRITICAL', if not used then it is set to 'DEBUG'

import asyncio
import sys
import logging

#import pymazda
#from pymazda import *
pymazda = __import__('pymazda', fromlist=['pymazda'])

async def test() -> None:
    logger = logging.getLogger('SoCmodule')

    client = pymazda.Client(userID, password, region)
    logger.info("Login done!")

    # Get list of vehicles from the API (returns a list)
    vehicles = await client.get_vehicles()
    logger.info("Vehicles retrieved!")
    found_ev = 0
    if vehicles==[]:
        logger.error("No supported vehicle on the mazda account!")

    # Loop through the registered vehicles
    for vehicle in vehicles:
        # Get vehicle ID (you will need this in order to perform any other actions with the vehicle)
        vehicle_id = vehicle["id"]
        vehicle_vin = vehicle["vin"]

        if vehicle_vin == charge_vehicle_vin:
            logger.info("Vehicle vin found!")
            found_ev = 1
            # Get and output vehicle status
            status = await client.get_ev_vehicle_status(vehicle_id)
            soc = status["batteryLevelPercentage"]
            logger.info("Vehicle battery level = " + format(soc) + "%!")
            if int(chargepoint) == 1:
                f = open('/var/www/html/openWB/ramdisk/soc', 'w')
            else :
                f = open('/var/www/html/openWB/ramdisk/soc1', 'w')
            f.write(str(soc))
            f.close()
    if found_ev == 0:
        logger.info("Vehicle vin not found!")


    #testcode without vehicle
    soc = 37
    logger.info("Vehicle battery level = " + format(soc) + "%!")
    f=open('/var/www/html/openWB/ramdisk/soc.log', 'w')
    f.write(str(soc))
    f.close()

    # Close the session
    await client.close()

if __name__ == "__main__":
    #logfilename='example.log'
    # Setting Logfile in case no parameters are given
    logfilename='/var/www/html/openWB/ramdisk/mazdareply'
    #logging.basicConfig(filename=logfilename, level=logging.DEBUG)
    argnum = len(sys.argv)
    if argnum < 5: # not enough parameter
        if argnum < 1:
            logger = logging.getLogger('SoCmodule:mainparameter')
            logging.basicConfig(filename=logfilename, level=logging.DEBUG)
            logging.error("wrong number of arguments!")
            # need to exit here
        else:
            logfilename='/var/www/html/openWB/ramdisk/mazdareply'+chargepoint
            logger = logging.getLogger('SoCmodule:mainparameter')
            logging.basicConfig(filename=logfilename, level=logging.DEBUG)
            logging.error("wrong number of arguments!")
            # need to exit here
    if argnum > 4: # enough parameter, without log level
        chargepoint=str(sys.argv[1])
        userID=str(sys.argv[2])
        password=str(sys.argv[3])
        region=str(sys.argv[4])
        charge_vehicle_vin=str(sys.argv[5])
        # Logfile for final Module
        logfilename='/var/www/html/openWB/ramdisk/mazdareply'+chargepoint
        if argnum == 5:
            logging.basicConfig(filename=logfilename, level=logging.DEBUG)
        else: # enough parameter with log level
            level=str(sys.argv[5])
            if level=='DEBUG':
                loglevel=logging.DEBUG
            elif level=='INFO':
                loglevel=logging.INFO
            elif level=='WARNING':
                loglevel=logging.WARNING
            elif level=='ERROR':
                loglevel=logging.ERROR
            elif level=='CRITICAL':
                loglevel=logging.CRITICAL
            else:
                loglevel=logging.DEBUG
            logging.basicConfig(filename=logfilename, level=loglevel)

        loop = asyncio.get_event_loop()
        SoC = loop.run_until_complete(test())

