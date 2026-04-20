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
    terList = []
    tmpDict = dict()
    nullList = [];
    for i in range(1970,2025):
        avg_year_temp = 0
        avg_year_rain = 0
        month_count = 0
        total_year_temp = 0
        total_year_rain = 0
        terTemp = dict()
        terRain = dict()
        terTempCount = dict()
        terRainCount = dict()
        maxNull = 0;
        maxNullMonth = 0;
        for(j) in range(1,13):
            nullCount = 0;
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
                        #territory data
                        if record[4] in terTempCount:
                            try:

                                terTempVal = terTemp[record[4]]
                                terTemp[record[4]] = terTempVal + float(record[5])
                                terTempCountVal = terTempCount[record[4]]
                                terTempCount[record[4]] = terTempCountVal + 1
                                
                            except ValueError:
                                pass
                        else:
                            try:
                                terTemp[record[4]] = float(record[5])
                                terTempCount[record[4]] = 1
                            except ValueError:
                                pass
                        if record[4] in terRainCount:
                            try:
                                terRainVal = terRain[record[4]]
                                terRain[record[4]] = terRainVal + float(record[15])
                                terRainCountVal = terRainCount[record[4]]
                                terRainCount[record[4]] = terRainCountVal + 1
                            except ValueError:
                                pass
                        else:
                            try:
                                terRain[record[4]] = float(record[15])
                                terRainCount[record[4]] = 1
                            except ValueError:
                                pass
                        #total data
                        try:
                            total_station_temp = total_station_temp + float(record[5])
                            
                            station_count_temp = station_count_temp + 1

                        except ValueError:
                            nullCount = nullCount + 1; #for counting null values
                        try:
                            total_station_rain = total_station_rain + float(record[15])
                            station_count_rain = station_count_rain + 1
                        except ValueError:
                            pass
                        
                    total_year_temp = total_year_temp + (total_station_temp / station_count_temp)
                    total_year_rain = total_year_rain + (total_station_rain / station_count_rain)
                    if(nullCount > maxNull):
                        maxNull = nullCount
                        maxNullMonth = j

                    # print(str(total_year_temp) + " | " +str(total_station_temp) + " | " + str(station_count_temp))
                
            except FileNotFoundError:
                print("File " + filename + " does not exist in folder")
        # print(str(nullCount) + " | " + str(maxNull) + " | " + str(maxNullMonth));
        avg_year_temp = total_year_temp / 12
        avg_year_rain = total_year_rain / 12
        # print(str(i) + " | " + str(avg_year_temp) + " | " + str(avg_year_rain))
        avg_temps_total.append(avg_year_temp)
        avg_rain_total.append(avg_year_rain)
        nullList.append((maxNull,maxNullMonth))
        
        # print("---------------------------------------------------")

        for key in terTempCount:

            tempCount = terTempCount[key]
            rainCount = terRainCount[key]
            temp = terTemp[key]
            rain = terRain[key]
            avgTemp = temp/tempCount
            avgRain = rain/rainCount
            tmpDict[key] = [avgTemp,avgRain]

        terList.append((i, tmpDict.copy()))
    return avg_temps_total, avg_rain_total,terList,nullList


def write_data(temp,rain,terData,nulls):
    with open("output.csv", 'w') as outfile:
        write = csv.writer(outfile)
        count = 0
        write.writerow(["year","avg temp","avg rain"])
        for year in range(1970,2025):
            write.writerow([year,temp[count],rain[count]])
            count = count + 1


    with open ("territory.csv", 'w') as terOut:
        terWrite = csv.writer(terOut)
        terWrite.writerow(["year","Territory/Province","avg temp","avg rain"])
        for i in range(len(terData)):
            terDataVals = terData[i][1]            
            year = terData[i][0]
            for key in terDataVals:
                ter = key
                temp = terDataVals[key][0]
                rain = terDataVals[key][1]
                # print(str(year) + " | " + str(ter) + " | " + str(temp) + " | " + str(rain))
                terWrite.writerow([year,ter,temp,rain])
    with open ("nulls.csv", 'w') as nullOut:
        nullWrite = csv.writer(nullOut)
        nullWrite.writerow(["year","Null count","Month"])
        count = 0
        for year in range(1970,2025):
            nullWrite.writerow([year,nulls[count][0],nulls[count][1]])
            count = count + 1

def main():
    data_files_test()
    avg_temp,avg_rain,terData,nulls = get_data()
    write_data(avg_temp,avg_rain,terData,nulls)
    print("Done")


main()