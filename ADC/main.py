import csv
import datetime
from ADC import ADC

file_handles = []
REF = 5.08 # Do ustawienia !!
RPI_ID = 0

try:
    ADC_modules: list[ADC] = [ADC(),ADC()] # Ustawić pinout

    # CONFIGURATION
    for ADC_ID, module in enumerate(ADC_modules):
        if (module.ADS1263_init_ADC1('ADS1263_38400SPS') == -1): # Możliwa zmiana DRATE
            print(f'Unable to init ADC_{ADC_ID}')
            exit()
        module.ADS1263_SetMode(1)

    # READING AND SAVING (10000 samples per file)
    while(1):
        FIELD_NAMES = ['time_stamp']+[f'CH{id}' for id in range(5)]
        date = datetime.datetime.now()
        file_handles = [open(f'readings/RPI_{RPI_ID}_ADC_{ADC_ID}_{date.isoformat()}.csv','w',newline='') for ADC_ID, _ in enumerate(ADC_modules)]

        for ADC_ID, module in enumerate(ADC_modules):
                csvfile = file_handles[ADC_ID]
                writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
                writer.writeheader()

        for _ in range(10000):
            for ADC_ID, module in enumerate(ADC_modules):
                    date = datetime.datetime.now()

                    csvfile = file_handles[ADC_ID]
                    writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)

                    channelList = [ch for ch in range(5)]
                    ADC_Value = ADC.ADS1263_GetAll()    # get ADC1 value

                    Voltage_Readings = {'time_stamp': date.isoformat()}

                    for i in channelList:
                        if(ADC_Value[i]>>31 ==1):
                            Voltage_Readings[f'CH{i}'] = (REF*2 - ADC_Value[i] * REF / 0x80000000)
                        else:
                            Voltage_Readings[f'CH{i}'] = (ADC_Value[i] * REF / 0x7fffffff)   # 32bit

                    writer.writerow(Voltage_Readings)

        for file in file_handles:
            file.close()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    for file in file_handles:
        file.close()

    for module in ADC_modules:
        module.ADS1263_Exit()

    exit()
