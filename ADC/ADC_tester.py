from ADS1263 import ADS1263
import datetime
from time import sleep

REF = 2.5

try:
    module = ADS1263()

    # CONFIGURATION
    if (module.ADS1263_init_ADC1() == -1): # Możliwa zmiana DRATE
        print(f'Unable to init ADC module')
        exit()

    module.ADS1263_SetMode(1)

    while(1):
        date = datetime.datetime.now()

        channelList = [ch for ch in range(2)]
        ADC_Value = module.ADS1263_GetAll(channelList)    # get ADC1 value

        Voltage_Readings = {'time_stamp': date.isoformat()}

        for i in channelList:
            if(ADC_Value[i]>>31 ==1):
                Voltage_Readings[f'CH{i}'] = (REF*2 - ADC_Value[i] * REF / 0x80000000)
            else:
                Voltage_Readings[f'CH{i}'] = (ADC_Value[i] * REF / 0x7fffffff)   # 32bit

        print(Voltage_Readings)
        module.ADS1263_WaitDRDY()


except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")

    module.ADS1263_Exit()

    exit()
