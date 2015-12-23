import pandas as pd
import statsmodels.api as sm
import sys
import json
import os
import re
import glob


def calculate_coef(product, statistics_files):
    data_list = []
    for statistics_file in statistics_files:
        data_list.append(pd.read_csv(statistics_file))

    headers = []
    results = []
    for data in data_list:
        headers = []
        for column in data:
            if column != 'Loading Avg':
                headers.append(column)
        Y = data['Loading Avg']
        X = data[headers]
        X = sm.add_constant(X)
        try:
            model11 = sm.OLS(Y, X).fit()
            results.append(model11.params)
        except:
            print (statistics_file + "\nCSV format is wrong. CSV file can only contain numbers")
            print (input('\nPress ENTER to continue'))
            sys.exit(0)

    with open(product['config'], 'r') as config_file:
        try:
            config = json.load(config_file)
        except ValueError:
            print ("\nConfig format is wrong. Please check your config.json. All the key and value should be \"quoted\"")
            print (input('\nPress ENTER to continue'))
            sys.exit(0)

    coef = {
        "local_display_rf": results[config['coef']["local_display_rf"] - 1]['Local Decode(TotalCH*Resolution*FPS)'],
        "local_display_b": results[config['coef']["local_display_b"] - 1]['Local Decode(Total Bit Rate)'],
        "smart_guard_rf": results[config['coef']["smart_guard_rf"] - 1]['Smart Guard(General Motion)(Total DecodeResolution*FPS)'],
        "smart_guard_b": results[config['coef']["smart_guard_b"] - 1]['Smart Guard(General Motion)(Total Decode Bit Rate)'],
        "smart_guard_p": results[config['coef']["smart_guard_p"] - 1]['Smart Guard(General Motion)(Total DecodeResolution*FPS)(Pure)'],
        "ivs_rf": results[config['coef']["ivs_rf"] - 1]['IVS Channel(Resolution*FPS)'],
        "ivs_b": results[config['coef']["ivs_b"] - 1]['IVS Channel(Bit Rate)'],
        "ivs_p": results[config['coef']["ivs_p"] - 1]['IVS Channel(Resolution*FPS)(Pure)'],
        "live_view": results[config['coef']["live_view"] - 1]['Live View Connection(Server Total UpLoad Bit Rate)'],
        "record": results[config['coef']["record"] - 1]['Always Record(Total Record Bit Rate)'],
        "metadata": results[config['coef']["metadata"] - 1]['Metadata'],
        "edge_event": results[config['coef']["edge_event"] - 1]['Edge Event']
    }
    return {config['video_format']: coef}


def generate_product_spec():
    product_names = os.listdir('products/')
    products = {}
    product_list = []

    for name in product_names:
        products[name] = {'config': "", 'data': []}

        for dir_path in glob.glob('products/' + name + '/*'):
            if not os.path.isdir(dir_path):
                continue

            products[name]['config'] = os.path.join(dir_path, 'config.json')
            for file_path in glob.glob(dir_path + '/*.csv'):
                products[name]['data'].append(file_path)

    for name in products:
        print ('Processing:', name)
        product = products[name]

        with open(os.path.join('products', name, name + '.json'), 'r', encoding='utf-8') as outfile:
            template = json.load(outfile)

        if len(product['data']) == 0:
            print ('No data')
        else:
            template["cpu_loading_factors"] = calculate_coef(product, product['data'])

        product_list.append(str(json.dumps(template, indent=4, ensure_ascii=False)))

    product_spec = "var PRODUCT_SPECS = [" + ", ".join(product_list) + '];'
    print ('Done!')
    return product_spec


def generate_camera_spec():
    with open('cameras/camera_spec.txt', 'r', encoding='utf-8') as spec:
        camera_spec = spec.read()
    return camera_spec


def generate_client_product_spec():
    with open('client_pc/client_pc_spec.txt', 'r', encoding='utf-8') as spec:
        client_product_spec = spec.read()
    return client_product_spec


print ('Generating')

product_spec = generate_product_spec()
camera_spec = generate_camera_spec()
client_product_spec = generate_client_product_spec()

with open('product_spec.js', 'w', encoding='utf-8') as spec:
    spec.write(product_spec + '\n\n' + camera_spec + '\n\n' + client_product_spec)
