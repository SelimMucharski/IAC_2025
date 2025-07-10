from ADC import ADC

try:
    ADC_modules: list[ADC] = [ADC(),ADC()]

    for module in ADC_modules:
        module.ADS1263_SetMode(1)

    for module in ADC_modules:
        module.ADS1263_Exit()

except IOError as e:
    print(e)

except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")

    for module in ADC_modules:
        module.ADS1263_Exit()

    exit()