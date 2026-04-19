import csv
FILENAME_BASE = "Data/en_climate_summaries_All_"
def data_files_test():
    
    for i in range(1970,2024):
        for(j) in range(1,12):
            if(j < 10):
                j = "0" + str(j)
            filename = FILENAME_BASE + str(j) + "-" + str(i) + ".csv"
            try:
                file = open(filename)
                csv_reader = csv.reader(file)
                for record in csv_reader:
                    if(record[5] != "Tm"):
                        print("WARNING: FILE " + filename + " DOES NOT HAVE MEAN TEMP IN SPOT 5")
                    if(record[15] != "P"):
                        print("WARNING: FILE " + filename + " DOES NOT HAVE PRECIPITATION IN SPOT 15")
                    if(record[8] != "Tx"):
                        print("WARNING: FILE " + filename + " DOES NOT HAVE MAX TEMP IN SPOT 8")
                    if(record[10] != "Tn"):
                        print("WARNING: FILE " + filename + " DOES NOT HAVE MIN TEMP IN SPOT 10")
                    if(record[4] != "Prov_or_Ter"):
                        print("WARNING: FILE " + filename + " DOES NOT HAVE PROVINCE IN SPOT 4")
                    break
                file.close()
            except FileNotFoundError:
                print("File " + filename + " does not exist in folder")
    print("File test done")
    print("--------------------------------------------------------")

def get_data():
    avg_temps_total = []
    avg_rain_total = []
    count = 0
    terRainTotal = []
    terDict = []
    tmpDict = dict()
    for i in range(1970,2025):
        avg_year_temp = 0
        avg_year_rain = 0
        month_count = 0
        total_year_temp = 0
        total_year_rain = 0
        terTemp = dict()
        terRain = dict()
        terCount = dict()
        for(j) in range(1,13):
            # print(str(j) + "/" + str(i))
            month_count = month_count + 1
            if(j < 10):
                j = "0" + str(j)
            filename = FILENAME_BASE + str(j) + "-" + str(i) + ".csv"
            try:
                with open(filename) as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    station_count_temp = 0
                    station_count_rain = 0
                    total_station_temp = 0
                    total_station_rain = 0
                    
                    for record in csv_reader:

                        if record[4] in terCount:
                            try:
                                # print(record[4])
                                # print(terCount[record[4]])
                                # print(terTemp)
                                terTempVal = terTemp[record[4]]
                                terTemp[record[4]] = terTempVal + float(record[5])
                                terCountVal = terCount[record[4]]
                                terCount[record[4]] = terCountVal + 1
                                
                            except ValueError:
                                pass
                            try:
                                terRainVal = terRain[record[4]]
                                terRain[record[4]] = terRainVal + float(record[15])
                                terCountVal = terCount[record[4]]
                                terCount[record[4]] = terCountVal + 1
                            except ValueError:
                                pass
                        else:
                            try:
                                terTemp[record[4]] = float(record[5])
                                terCount[record[4]] = 1
                            except ValueError:
                                pass
                            try:
                                terRain[record[4]] = float(record[15])
                                terCount[record[4]] = 1
                            except ValueError:
                                pass


                        try:
                            total_station_temp = total_station_temp + float(record[5])
                        except ValueError:
                            station_count_temp = station_count_temp - 1
                        try:
                            total_station_rain = total_station_rain + float(record[15])
                        except ValueError:
                            station_count_rain = station_count_rain - 1
                        station_count_rain = station_count_rain + 1
                        station_count_temp = station_count_temp + 1
                    total_year_temp = total_year_temp + (total_station_temp / station_count_temp)
                    total_year_rain = total_station_rain / station_count_rain
                    # print(terCount)
                    # print(str(total_year_temp) + " | " +str(total_station_temp) + " | " + str(station_count_temp))
            except FileNotFoundError:
                print("File " + filename + " does not exist in folder")
        avg_year_temp = total_year_temp / 12
        avg_year_rain = total_year_rain / 12
        # print(str(i) + " | " + str(avg_year_temp) + " | " + str(avg_year_rain))
        avg_temps_total.append(avg_year_temp)
        avg_rain_total.append(avg_year_rain)
        for key in terCount:
            # print(i,key)
            count = terCount[key]
            temp = terTemp[key]
            rain = terRain[key]
            avgTemp = temp/count[0]
            avgRain = rain/count[1]
            tmpDict[key] = [avgTemp,avgRain]
        # print(i,tmpDict)
        terDict.append((i, tmpDict))
    # print(yearAvgTemp)
    return avg_temps_total, avg_rain_total,terDict


def write_data(temp,rain,terData):
    # with open("output.csv", 'w') as outfile:
    #     write = csv.writer(outfile)
    #     count = 0
    #     write.writerow(["year","avg temp","avg rain"])
    #     for year in range(1970,2025):
    #         write.writerow([year,temp[count],rain[count]])
    #         count = count + 1


    with open ("territory.csv", 'w') as terOut:
        terWrite = csv.writer(terOut)
        terWrite.writerow(["year","Territory/Province","avg temp","avg rain"])
        for i in range(len(terData)):
            terDataVals = terData[i][1]
            # print(type(terTempData))
            # print(terTempData)
            year = terData[i][0]
            for key in terDataVals:
                ter = key
                temp = terDataVals[key][0]
                rain = terDataVals[key][1]
                print(str(year) + " | " + str(ter) + " | " + str(temp) + " | " + str(rain))
                terWrite.writerow([year,ter,temp,rain])

def main():
    data_files_test()
    avg_temp,avg_rain,terData = get_data()
    write_data(avg_temp,avg_rain,terData)
    # print(avg_temp)
    # print(avg_rain)
    print("Done")


main()