from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/productionplan', methods=['POST'])
def production_plan():
    try:
        data = request.json
        load = data['load']
        fuels = data['fuels']
        powerplants = data['powerplants']

        # Initialize the production plan
        production_plan = []
        
        for plant in powerplants:
            if plant['type'] == 'gasfired':
                plant['cost/MWh'] = fuels['gas(euro/MWh)'] / plant['efficiency'] + 0.3*fuels["co2(euro/ton)"]
            if plant['type'] == 'turbojet':
                plant['cost/MWh'] = fuels['kerosine(euro/MWh)'] / plant['efficiency']
            if plant['type'] == 'windturbine':
                plant['cost/MWh'] = 0
                plant['pmin'] *= fuels['wind(%)'] / 100
                plant['pmax'] *= fuels['wind(%)'] / 100
            load -= round(plant['pmin'],1)

        if load<0:
            return jsonify({"error": "the powerplants minimum capacities is bigger than the load"}), 400

        plants = sorted(powerplants, key=lambda p: p['cost/MWh'])
        for plant in plants:
            if load > 0:
                production_plan.append({
                    'name': plant['name'],
                    'p': round(min(plant['pmax'], load + plant['pmin']),1)
                })
                load -= round(plant['pmax'] - plant['pmin'],1)
            else:
                production_plan.append({
                'name': plant['name'],
                'p': round(plant['pmin'],1)
            })

        # Ensure that the load is met
        if load > 0:
            return jsonify({"error": "Unable to meet the load with the given powerplants"}), 400

        return jsonify(production_plan)

    except Exception as e:
        logging.error("An error occurred: %s", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8888)
