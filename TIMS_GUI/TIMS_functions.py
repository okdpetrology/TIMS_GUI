import pandas as pd
import os
import re
import copy


# Functions
def get_raw_tables(file_name):
    df = pd.read_csv(file_name, header=None, skip_blank_lines=False)
    # df = dat_dataframe
    # date_ind = list(df.loc[df[0] == 'Date'].index.values)
    baselines_ind = list(df.loc[df[0] == 'Baselines for this Block'].index.values)
    baselines_ind2 = list(
        df.loc[df[0] == 'Block "Function" "Mean Bf" "%SdErrB" "Mean Af" "%SdErrA" "No After" "No Before"'].index.values)
    individualRatios_ind = list(df.loc[df[0] == 'Individual Ratios for this Block:'].index.values)
    grandFunction_ind = list(
        df.loc[df[0] == 'Grand "Function" "Mean Bf" "%SdErrB" "Mean Af" "%SdErrA" "No After" "No Before"'].index.values)

    # print('Date: ', date_ind)
    #     print('Baselines: ', baselines_ind)
    #     print('Blocks: ',baselines_ind2)
    #     print('Individual Ratios: ',individualRatios_ind)
    #     print('Grand: ',grandFunction_ind)
    date_dict = {}
    # file_name = 'TEST1'
    for idx in range(len(df)):
        if 'Date' in str(df.iloc[idx][0]):
            unicode_line = str(df.iloc[idx][0])
            uni_list = unicode_line.split(':')
            # date_dict[file_name] = uni_list.pop().strip()

    ### Important grand, block, individual ratios stuff
    chopped_df = []
    chopped_df_dict = {}
    for i in range(len(grandFunction_ind)):

        df_crop1 = df[baselines_ind[i]:baselines_ind2[i]]
        df_crop1b = df[baselines_ind2[i]:individualRatios_ind[i]]
        df_crop2 = df[individualRatios_ind[i]:grandFunction_ind[i]]
        # print(i)
        try:
            df_crop3 = df[grandFunction_ind[i]:baselines_ind[i + 1]]
        except:
            final = grandFunction_ind[i] + 14
            df_crop3 = df[grandFunction_ind[i]:final]
            df_crop4 = df[(final + 1): (final + 8)]
            chopped_df_dict['Machine Parameters:'] = df_crop4
        chopped_df.append(df_crop1)
        chopped_df.append(df_crop1b)
        chopped_df.append(df_crop2)
        chopped_df.append(df_crop3)

        chopped_df_dict['Baselines:' + str(i + 1)] = df_crop1
        chopped_df_dict['Block:' + str(i + 1)] = df_crop1b
        chopped_df_dict['Individual Ratios:' + str(i + 1)] = df_crop2
        chopped_df_dict['Grand:' + str(i + 1)] = df_crop3

    # Making these tables look nice

    for idx in range(len(grandFunction_ind)):
        string = 'Block:' + str(idx + 1)
        df_block = grand_dataframe(chopped_df_dict[string], file_name, string)
        chopped_df_dict[string] = df_block

        string2 = 'Grand:' + str(idx + 1)
        df_block = grand_dataframe(chopped_df_dict[string2], file_name, string2)
        chopped_df_dict[string2] = df_block

        string3 = 'Individual Ratios:' + str(idx + 1)
        df_block = indiv_dataframe(chopped_df_dict[string3], file_name, string3)
        chopped_df_dict[string3] = df_block
    chopped_df_dict['Date'] = uni_list.pop().strip()
    # print(file_name, " : ", string2)
    return chopped_df_dict


def grand_dataframe(grand_df, file_name, df_name):
    # Works for Grand or Block
    df2 = grand_df[1:]
    df2_list = []
    header = ['File Name',
              'Dataframe Name',
              'Function',
              'Mean Bf',
              '%SdErrB',
              'Mean Af',
              '%SdErrA',
              'No After',
              'No Before']

    for idx in range(len(df2)):
        # if idx == 0:
        # continue

        string = str(df2.iloc[idx][0])
        new_string = re.split('"', string)
        new_str_list = new_string[1:]

        if len(new_str_list) <= 1:
            # print(new_str_list)
            continue

        new_str_list2 = new_str_list[1].split()
        new_str_list = [new_str_list[0]]
        new_str_list.extend(new_str_list2)
        new_str_list.insert(0, df_name)
        new_str_list.insert(0, file_name)
        df2_list.append(new_str_list)

    return pd.DataFrame(df2_list, columns=header)


def indiv_dataframe(indiv_dataframe, file_name, df_name):
    df3 = indiv_dataframe
    df3_list = []
    header = ['File Name', 'Dataframe Name', 'F0', 'FG', 'FH', 'FI', 'FK', 'FL', 'FM', 'FN', 'FO', 'FP', 'FQ', 'FR',
              'FS']
    for idx in range(len(df3)):
        if idx <= 1:
            continue
        string = str(df3.iloc[idx][0])
        new_string = re.split('  ', string)
        # print(new_string)
        if len(new_string) <= 1:
            continue
        new_string.insert(0, df_name)
        new_string.insert(0, file_name)
        df3_list.append(new_string)

    return pd.DataFrame(df3_list, columns=header)


def multi_file_get_tables(list_filenames):
    dict_of_multifiles = {}
    for file in list_filenames:
        dict_of_multifiles[file] = get_raw_tables(file)

    return dict_of_multifiles


def combine_all_df(data_dict):
    grand_list = []
    block_list = []
    indiv_list = []
    # date_list = []
    for key in data_dict:
        # print(key)
        for value in data_dict[key]:
            if 'Grand' in value:
                grand_list.append(data_dict[key][value])
            if 'Block' in value:
                block_list.append(data_dict[key][value])
            if 'Individual' in value:
                indiv_list.append(data_dict[key][value])
    #             if 'Date' in value:
    #                 date_list.append(data_dict[key][value])

    for i in range(len(grand_list)):
        if i == 0:
            grand_df = grand_list[i]
        else:
            grand_df = grand_df.append(grand_list[i])

    for i in range(len(block_list)):
        if i == 0:
            block_df = block_list[i]
        else:
            block_df = block_df.append(block_list[i])

    for i in range(len(indiv_list)):
        if i == 0:
            indiv_df = indiv_list[i]
        else:
            indiv_df = indiv_df.append(indiv_list[i])

    #     for i in range(len(date_list)):
    #         if i == 0:
    #             date_df = date_list[i]
    #         else:
    #             date_df = date_df.append(date_list[i])

    mega_dict = {}
    mega_dict['Grand'] = grand_df
    mega_dict['Block'] = block_df
    mega_dict['Individual Ratios'] = indiv_df
    # mega_dict['Block'] = block_df

    return mega_dict


def format_grand12(data_dict):
    big_dict = {}

    file_list = list(data_dict.keys())

    for file in file_list:
        test_z_dict = {}
        # print(file)
        #         for i in range(13):
        #             if str(13-i) in data_dict[file].keys():
        #                 string = 'Grand:' + str(i)
        #                 test_z = data_dict[file][string]
        #             else:
        #                 continue
        try:
            test_z = data_dict[file]['Grand:12']  ##Technically, hardcoded right now
        except:
            print(file, ': Probably aborted during run.')
            continue
        # Define new Grand: 12 df based on file name

        for idx in range(len(test_z)):
            str1 = test_z.loc[idx]['Function']
            # print('DEBUG: ', file,' ', str1 )
            str2 = str1 + ' Mean Af'
            str3 = str1 + ' %SdErrA'
            test_z_dict[str2] = test_z.loc[idx]['Mean Af']
            # print('DEBUG: ', file,' ', test_z.loc[0]['Mean Af'])
            test_z_dict[str3] = test_z.loc[idx]['%SdErrA']

        new_name = file.split('/')
        name = new_name.pop()
        big_dict[name] = test_z_dict
    df_1 = pd.DataFrame(big_dict)
    df_flip = pd.DataFrame.transpose(df_1)
    columns = list(df_flip.columns)

    for col in columns:
        df_flip[col] = pd.to_numeric(df_flip[col])

    return df_flip


def format_machine(data_dict):
    big_dict = {}
    file_list = list(data_dict.keys())

    for file in file_list:

        # print(file)
        test_z = data_dict[file]['Machine Parameters:']
        # Define new Machine Parameters df based on file name

        test_dict = {}

        test_dict['Date'] = data_dict[file]['Date']
        uni_list2 = []
        for row in range(len(test_z)):
            # print(row)
            unicode_line = str(test_z.iloc[row][0])
            unicode_line = unicode_line.translate({ord(c): None for c in '""'})
            uni_list = unicode_line.split()
            # print(uni_list)

            if uni_list[0] == 'Source':
                uni_list2 = uni_list
                unicode_line = str(test_z.iloc[(row + 1)][0])
                unicode_line = unicode_line.translate({ord(c): None for c in '""'})
                uni_list3 = unicode_line.split()
                for val in range(len(uni_list2)):
                    test_dict[uni_list2[val]] = uni_list3[val]

            for idx in range(len(uni_list)):

                if ':' in uni_list[idx]:
                    # print(uni_list[idx])

                    filter = uni_list[idx].split(':')
                    # print('filter= ', filter)
                    if len(filter) == 3:
                        continue
                    if filter[0] == 'HT':
                        test_dict[uni_list[idx]] = None
                        continue
                    test_dict[uni_list[idx]] = uni_list[(idx + 1)]
        if '/' in file:
            new_name = file.split('/')
            name = new_name.pop()
        else:
            name = file
        big_dict[name] = test_dict

    df_1 = pd.DataFrame(big_dict)
    df_flip = pd.DataFrame.transpose(df_1)
    #     columns = list(df_flip.columns)

    #     for col in columns:
    #         df_flip[col] = pd.to_numeric(df_flip[col])

    return df_flip


def mega_format(data_files):
    mega_dict = {}
    data_dict = multi_file_get_tables(data_files)
    df_combine = combine_all_df(data_dict)

    df_a = format_grand12(data_dict)
    df_b = format_machine(data_dict)
    result = pd.concat([df_a, df_b], axis=1)
    col_name = "Date"
    first_col = result.pop(col_name)
    result.insert(0, col_name, first_col)

    mega_dict['Combine'] = df_combine
    mega_dict['Important'] = result
    return mega_dict


def files_process_toEXCEL(processed_dict, path, excel_name='TIMS_mega_output.xlsx'):
    with pd.ExcelWriter(os.path.join(path, excel_name)) as writer:
        processed_dict['Important'].to_excel(writer, sheet_name='Output', index=True)
        processed_dict['Combine']['Grand'].to_excel(writer, sheet_name='Grand', index=False)
        processed_dict['Combine']['Block'].to_excel(writer, sheet_name='Block', index=False)
        processed_dict['Combine']['Individual Ratios'].to_excel(writer, sheet_name='Individual Ratios', index=False)