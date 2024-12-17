from flask import Flask, request, jsonify
import logging
from itertools import combinations

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def generate_scenarios(n):
    result = []
    for length in range(1, n):
        for combo in combinations(range(n), length):
            result.append(list(combo))
    return result

@app.route('/productionplan', methods=['POST'])
def production_plan():
    try:
        data = request.json
        load = data['load']
        fuels = data['fuels']
        powerplants = data['powerplants']

        for plant in powerplants:
            if plant['type'] == 'gasfired':
                plant['cost/MWh'] = fuels['gas(euro/MWh)'] / plant['efficiency'] + 0.3*fuels["co2(euro/ton)"]
            if plant['type'] == 'turbojet':
                plant['cost/MWh'] = fuels['kerosine(euro/MWh)'] / plant['efficiency']
            if plant['type'] == 'windturbine':
                plant['cost/MWh'] = 0
                plant['pmin'] *= fuels['wind(%)'] / 100
                plant['pmax'] *= fuels['wind(%)'] / 100
            plant['pmin'] = round(plant['pmin'],1)
            plant['pmax'] = round(plant['pmax'],1)
            
        # ordering powerplants per cost
        powerplants = sorted(powerplants, key=lambda p: p['cost/MWh'])
        
        # trying different scenarios using different combinations of powerplants switched on.
        scenarios = generate_scenarios(len(powerplants))
        min_cost = -1
        for s in scenarios:
            scenario_powerplants = [p for i, p in enumerate(powerplants) if i in s]
            if load>sum([p['pmax'] for p in scenario_powerplants]):
                continue
            total_cost = 0
            load_scenario = load - sum([p['pmin'] for p in scenario_powerplants])
            scenario_production_plan = []
            for plant in scenario_powerplants:
                power = max(plant['pmin'], min(plant['pmax'], load_scenario + plant['pmin']))
                load_scenario -= power - plant['pmin']
                total_cost += plant['cost/MWh'] * power
                scenario_production_plan.append({'name': plant['name'], 'p': power})
            # selecting best production_plan
            if load_scenario==0 and (total_cost < min_cost or min_cost==-1):
                min_cost = total_cost
                production_plan = scenario_production_plan + [{'name': plant['name'], 'p': 0} for i, plant in enumerate(powerplants) if i not in s]

        if min_cost==-1:
            return jsonify({"error": "Unable to meet the load with the given powerplants"}), 400

        return jsonify(production_plan)

    except Exception as e:
        logging.error("An error occurred: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8888)
