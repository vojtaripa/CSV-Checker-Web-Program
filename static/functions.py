def create_driver_list(CSV_file, df_data,output, highlight):
            driver_list = df_data['name'].tolist()
            driver_list2 = []
            for i in driver_list:
                if i not in driver_list2:
                    driver_list2.append(i)
                else:
                    print('There are two users in your CSV file with the name'+ i)
                    output.append('There are two users in your CSV file with the name ' + i)
                    highlight.append(i)
            return driver_list2