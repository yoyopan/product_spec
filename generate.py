import pandas as pd
import statsmodels.api as sm
import sys
import json
import glob

from pathlib import Path


def _calculate_coef(config_file, statistics_files):
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

    with open(config_file, 'r') as config_file:
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
        "ivs_rf": results[config['coef']["ivs_rf"] - 1]['IVS Channel(Resolution*FPS)'],
        "ivs_b": results[config['coef']["ivs_b"] - 1]['IVS Channel(Bit Rate)'],
        "live_view": results[config['coef']["live_view"] - 1]['Live View Connection(Server Total UpLoad Bit Rate)'],
        "record": results[config['coef']["record"] - 1]['Always Record(Total Record Bit Rate)'],
        "metadata": results[config['coef']["metadata"] - 1]['Metadata'],
        "edge_event": results[config['coef']["edge_event"] - 1]['Edge Event']
    }

    # if this product doesn't have ivs_p / smart_p
    # we set it as ivs_rf / smart_guard_rf (max loading)
    smart_guard_p = 'Smart Guard(General Motion)(Total DecodeResolution*FPS)(Pure)'
    ivs_p = 'IVS Channel(Resolution*FPS)(Pure)'
    if smart_guard_p in results[config['coef']["smart_guard_p"] - 1]:
        coef["smart_guard_p"] = results[config['coef']["smart_guard_p"] - 1][smart_guard_p]
    else:
        coef["smart_guard_p"] = coef['smart_guard_rf']

    if ivs_p in results[config['coef']["ivs_p"] - 1]:
        coef["ivs_p"] = results[config['coef']["ivs_p"] - 1][ivs_p]
    else:
        coef["ivs_p"] = coef['ivs_rf']

    return coef


def generate_product_spec():
    products = []
    base_dir = "products/"

    if len(sys.argv) > 1:
        base_dir += sys.argv[1]
    else:
        base_dir += "nuuo"

    for product_path in Path(base_dir).iterdir():
        product = _parse_product(product_path)
        products.append(json.dumps(product, indent=4, ensure_ascii=False))

    product_spec = "var PRODUCT_SPECS = [{}];".format(", ".join(products))
    print('Done!')
    return product_spec


def _parse_product(product_path):
    print("Processing: {} ...".format(product_path.name))

    config_file = product_path / (product_path.name + ".json")
    with config_file.open(encoding='utf-8') as outfile:
        product = json.load(outfile)
        product['cpu_loading_factors'] = _parse_cpu_loading_factors(product_path)

    return product


def _parse_cpu_loading_factors(product_path):
    cpu_loading_factors = {}
    if product_path.name == "Mainconsole IP+":
        for cpu_model_path in product_path.iterdir():
            if not cpu_model_path.is_dir():
                continue
            cpu_loading_factors[cpu_model_path.name] = {
                'IP Camera': _calculate_cpu_factors(cpu_model_path / "IP Camera"),
                'Analog Camera': _calculate_cpu_factors(cpu_model_path / "Analog Camera"),
            }
    else:
        cpu_loading_factors = {
            'IP Camera': _calculate_cpu_factors(product_path / "IP Camera"),
            'Analog Camera': _calculate_cpu_factors(product_path / "Analog Camera"),
        }
    return cpu_loading_factors


def _calculate_cpu_factors(base_dir):
    cpu_factors = {}
    if base_dir.exists():
        for data_dir in base_dir.iterdir():
            video_format = data_dir.name
            print("Processing {} ...".format(video_format))

            cpu_factors[video_format] = _calculate_coef(
               config_file=str(data_dir / "config.json"),
               statistics_files=sorted(map(str, data_dir.glob("*.csv"))),
            )
    return cpu_factors


def generate_camera_spec():
    with open('cameras/camera_spec.txt', 'r', encoding='utf-8') as spec:
        camera_spec = spec.read()
    return camera_spec


def generate_client_product_spec():
    with open('client_pc/client_pc_spec.txt', 'r', encoding='utf-8') as spec:
        client_product_spec = spec.read()
    return client_product_spec


print('Generating')
product_spec = generate_product_spec()
camera_spec = generate_camera_spec()
client_product_spec = generate_client_product_spec()

with open('product_specs.js', 'w', encoding='utf-8') as spec:
    spec.write(product_spec + '\n\n' + camera_spec + '\n\n' + client_product_spec)
