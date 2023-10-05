import json, re, sys, subprocess
from os.path import exists

DATA_DICT = {
    'APOLLO_KEY':'',
    'APOLLO_GRAPH_REF':'',
    'VARIANT_NAME':'current',
    'GRAPH_ID':'',
    'ROUTING_URL':'',
    'GOOGLE_PROJECT': '',
    'SUBGRAPH1_SUBGRAPH_NAME':'authors',
    'SUBGRAPH2_SUBGRAPH_NAME':'books',
    'SUBGRAPH3_SUBGRAPH_NAME':'awards',
    'SUBGRAPH1_ROUTING_URL': 'http://subgraph1:3200',
    'SUBGRAPH2_ROUTING_URL': 'http://subgraph2:3200',
    'SUBGRAPH3_ROUTING_URL': 'http://subgraph3:3200',
    'GATEWAY_CONNECTION_URL': '',
    'ROUTER_CONNECTION_URL': ''
}

DOT_RE = re.compile('(.+)=(.*)' )
GOOGLE_RE = re.compile('(<CHANGE_ME>)')

# prompt should not include trailing ":"
def ask_input(prompt, default):
    if default != "":
        result = input(prompt + " (%s): " % default)
        if result == "":
            result = default
    else:
        result = input(prompt + ": ")

    return result

def replace_re(m, filename):
    key = m.group(1)
    value = DATA_DICT.get(key, '')
    if key in ['ROUTING_URL', 'SUBGRAPH_NAME']:
        if 'subgraph1' in filename:
            value = DATA_DICT.get('SUBGRAPH1_' + key, '')
        if 'subgraph2' in filename:
            value = DATA_DICT.get('SUBGRAPH2_' + key, '')
        if 'subgraph3' in filename:
            value = DATA_DICT.get('SUBGRAPH3_' + key, '')
    return "%s=%s" % (key, value)

# replace contents of the dot file
def replace_dot(filename):
    file_contents = open(filename).read()
    file_contents = DOT_RE.sub(lambda m: replace_re(m, filename), file_contents)
    open(filename, 'w').write(file_contents)

def replace_google_yaml(filename):
    project = DATA_DICT.get("GOOGLE_PROJECT")
    if project is None:
        return
    file_contents = open("%s.tmpl" % filename).read()
    file_contents = GOOGLE_RE.sub(project, file_contents)
    open(filename, 'w').write(file_contents)

def parse_url(output_line):
    return re.search("https://\S+", output_line).group()

if __name__ == "__main__":

    print("---------------------------")
    print("SE Demo Setup")
    print("---------------------------")
    print("Press Control-C to exit.\n")

    if not exists("gateway/.env") or not exists("gateway/cloudbuild.yaml.tmpl"):
        print("ERROR: dependencies are missing, run 'make install-deps'.")
        sys.exit(1)

    try:
        data = json.loads(open('.config').read())
        for k, v in data.items():
            DATA_DICT[k] = v
    except:
        pass
    else:
        print("Press enter to accept any default/existing values in parenthesis.")


    DATA_DICT['APOLLO_KEY'] = ask_input("Enter your Apollo Studio Graph API Key", DATA_DICT.get('APOLLO_KEY', ''))
    DATA_DICT['GRAPH_ID'] = ask_input("Enter the Graph ID, it is found in Studio under settings", DATA_DICT.get('GRAPH_ID', ''))
    DATA_DICT['VARIANT_NAME'] = ask_input("Enter the Graph Variant to publish to", DATA_DICT.get('VARIANT_NAME', ''))
    DATA_DICT['GOOGLE_PROJECT'] = ask_input("Enter your Google Cloud Project ID", DATA_DICT.get('GOOGLE_PROJECT', ''))
    DATA_DICT['APOLLO_GRAPH_REF'] = "%s@%s" % (DATA_DICT['GRAPH_ID'], DATA_DICT['VARIANT_NAME'])

    print("\nSubgraph Names\nIf you customize your demo, you can change these.  Or keep the defaults.\n")
    DATA_DICT['SUBGRAPH1_SUBGRAPH_NAME'] = ask_input("Subgraph 1 Name", DATA_DICT.get('SUBGRAPH1_SUBGRAPH_NAME', ''))
    DATA_DICT['SUBGRAPH2_SUBGRAPH_NAME'] = ask_input("Subgraph 2 Name", DATA_DICT.get('SUBGRAPH2_SUBGRAPH_NAME', ''))
    DATA_DICT['SUBGRAPH3_SUBGRAPH_NAME'] = ask_input("Subgraph 3 Name", DATA_DICT.get('SUBGRAPH3_SUBGRAPH_NAME', ''))

    if ask_input("\nDo you want to automatically fetch deployment (router/subgraphs/gateway) URLs? If you haven't deployed yet, enter N.", 'Y/n') == "Y":
        services = subprocess.run(["gcloud", "run", "services", "list"], stdout=subprocess.PIPE)
        deployed = False
        outputs = services.stdout.decode('utf-8').split("\n")

        for line in outputs:
            if "subgraph" in line:
                subgraph = re.search("subgraph\d*", line).group()
                subgraph_url = parse_url(line)
                DATA_DICT[subgraph.upper() + "_ROUTING_URL"] = subgraph_url

            if "gateway" in line:
                gateway_url = parse_url(line)
                DATA_DICT["GATEWAY_CONNECTION_URL"] = gateway_url
                deployed = True

            if "router" in line:
                router_url = parse_url(line)
                DATA_DICT["ROUTER_CONNECTION_URL"] = router_url
                deployed = True

        if deployed:
            print("\nSubgraph URLs\nAutomatically found and configured. Enter to skip, or add value to override.\n")
        else:
            print("\nSubgraph URLs\nLooks like you haven't deploy your project yet, make sure to run \"make publish\" and re-run \"make setup\" after deploying.\n")
        
    DATA_DICT['SUBGRAPH1_ROUTING_URL'] = ask_input("Subgraph 1 URL", DATA_DICT.get('SUBGRAPH1_ROUTING_URL', ''))
    DATA_DICT['SUBGRAPH2_ROUTING_URL'] = ask_input("Subgraph 2 URL", DATA_DICT.get('SUBGRAPH2_ROUTING_URL', ''))
    DATA_DICT['SUBGRAPH3_ROUTING_URL'] = ask_input("Subgraph 3 URL", DATA_DICT.get('SUBGRAPH3_ROUTING_URL', ''))

    # If a gateway service exists, we allow it to be overriden
    if DATA_DICT["GATEWAY_CONNECTION_URL"]:
        DATA_DICT['GATEWAY_CONNECTION_URL'] = ask_input("Gateway URL", DATA_DICT.get('GATEWAY_CONNECTION_URL', ''))
    
    DATA_DICT['ROUTER_CONNECTION_URL'] = ask_input("Router URL", DATA_DICT.get('ROUTER_CONNECTION_URL', ''))

    open(".config", "w").write(json.dumps(DATA_DICT, indent=2))

    # Now change files
    replace_dot('subgraph1/.env')
    replace_dot('subgraph2/.env')
    replace_dot('subgraph3/.env')
    replace_dot('client/.env')
    replace_dot('router/.env')
    replace_dot('gateway/.env')

    replace_google_yaml('subgraph1/cloudbuild.yaml')
    replace_google_yaml('subgraph2/cloudbuild.yaml')
    replace_google_yaml('subgraph3/cloudbuild.yaml')
    replace_google_yaml('client/cloudbuild.yaml')
    replace_google_yaml('router/cloudbuild.yaml')
    replace_google_yaml('gateway/cloudbuild.yaml')

