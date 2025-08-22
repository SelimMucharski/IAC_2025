import csv
import datetime
import time

from ADS1263 import ADS1263

file_handles = []
REF = 2.5
RPI_ID = 1

try:
    module = ADS1263()

    # CONFIGURATION
    if (module.ADS1263_init_ADC1() == -1): # Możliwa zmiana DRATE
        print(f'Unable to init ADC')
        exit()

    module.ADS1263_SetMode(1)

    # READING AND SAVING (10000 samples per file)
    while(1):
        FIELD_NAMES = ['time_stamp']+[f'CH{id}' for id in range(5)]
        date = datetime.datetime.now()
        READING_ID = time.time()
        csvfile = open(f'readings/RPI_{RPI_ID}_{READING_ID}.csv','w',newline='')

        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        writer.writeheader()

        for _ in range(10000):
            date = datetime.datetime.now()

            writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)

            channelList = [ch for ch in range(5)]
            ADC_Value = module.ADS1263_GetAll(channelList)    # get ADC1 value

            Voltage_Readings = {'time_stamp': date.isoformat()}

            for i in channelList:
                if(ADC_Value[i]>>31 ==1):
                    Voltage_Readings[f'CH{i}'] = (REF*2 - ADC_Value[i] * REF / 0x80000000)
                else:
                    Voltage_Readings[f'CH{i}'] = (ADC_Value[i] * REF / 0x7fffffff)   # 32bit

            writer.writerow(Voltage_Readings)
            # print(Voltage_Readings['CH0'])
            module.ADS1263_WaitDRDY()

        csvfile.close()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")

    csvfile.close()
    module.ADS1263_Exit()
    exit()
