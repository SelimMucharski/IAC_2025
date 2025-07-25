from ADC import ADC
import datetime

REF = 2.5

try:
    ADC_modules: list[ADC] = [ADC()] # Ustawić pinout

    # CONFIGURATION
    for ADC_ID, module in enumerate(ADC_modules):
        if (module.ADS1263_init_ADC1('ADS1263_38400SPS') == -1): # Możliwa zmiana DRATE
            print(f'Unable to init ADC_{ADC_ID}')
            exit()
        module.ADS1263_SetMode(1)

    while(1):
        for ADC_ID, module in enumerate(ADC_modules):
                date = datetime.datetime.now()

                channelList = [ch for ch in range(5)]
                ADC_Value = ADC.ADS1263_GetAll()    # get ADC1 value

                Voltage_Readings = {'time_stamp': date.isoformat()}

                for i in channelList:
                    if(ADC_Value[i]>>31 ==1):
                        Voltage_Readings[f'CH{i}'] = (REF*2 - ADC_Value[i] * REF / 0x80000000)
                    else:
                        Voltage_Readings[f'CH{i}'] = (ADC_Value[i] * REF / 0x7fffffff)   # 32bit

                print(Voltage_Readings)


except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")

    for module in ADC_modules:
        module.ADS1263_Exit()

    exit()
