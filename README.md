# Project-Prometheus
### In short
Calculate how much power each of a multitude of different [powerplants](https://en.wikipedia.org/wiki/Power_station) need to produce (a.k.a. the production-plan) when the [load](https://en.wikipedia.org/wiki/Load_profile) is given and taking into account the cost of the underlying energy sources (gas,  kerosine) and the Pmin and Pmax of each powerplant.

### More in detail

The load is the continuous demand of power. The total load at each moment in time is forecasted. For instance for Belgium you can see the load forecasted by the grid operator [here](https://www.elia.be/en/grid-data/load-and-load-forecasts).

At any moment in time, all available powerplants need to generate the power to exactly match the load.  The cost of generating power can be different for every powerplant and is dependent on external factors: The cost of producing power using a [turbojet](https://en.wikipedia.org/wiki/Gas_turbine#Industrial_gas_turbines_for_power_generation), that runs on kerosine, is higher compared to the cost of generating power using a gas-fired powerplant because of gas being cheaper compared to kerosine and because of the [thermal efficiency](https://en.wikipedia.org/wiki/Thermal_efficiency) of a gas-fired powerplant being around 50% (2 units of gas will generate 1 unit of electricity) while that of a turbojet is only around 30%.  The cost of generating power using windmills however is zero. Thus deciding which powerplants to activate is dependent on the [merit-order](https://en.wikipedia.org/wiki/Merit_order).

When deciding which powerplants in the merit-order to activate (a.k.a. [unit-commitment problem](https://en.wikipedia.org/wiki/Unit_commitment_problem_in_electrical_power_production)) the maximum amount of power each powerplant can produce (Pmax) obviously needs to be taken into account.  Additionally gas-fired powerplants generate a certain minimum amount of power when switched on, called the Pmin. 

#### Payload

The payload contains 3 types of data:
 - load: The load is the amount of energy (MWh) that need to be generated during one hour.
 - fuels: based on the cost of the fuels of each powerplant, the merit-order can be determined which is the starting point for deciding which powerplants should be switched on and how much power they will deliver.  Wind-turbine are either switched-on, and in that case generate a certain amount of energy depending on the % of wind, or can be switched off. 
   - gas(euro/MWh): the price of gas per MWh. Thus if gas is at 6 euro/MWh and if the efficiency of the powerplant is 50% (i.e. 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euro.
   - kerosine(euro/Mwh): the price of kerosine per MWh.
   - co2(euro/ton): the price of emission allowances (optionally to be taken into account).
   - wind(%): percentage of wind. Example: if there is on average 25% wind during an hour, a wind-turbine with a Pmax of 4 MW will generate 1MWh of energy.
 - powerplants: describes the powerplants at disposal to generate the demanded load. For each powerplant is specified:
   - name:
   - type: gasfired, turbojet or windturbine.
   - efficiency: the efficiency at which they convert a MWh of fuel into a MWh of electrical energy. Wind-turbines do not consume 'fuel' and thus are considered to generate power at zero price.
   - pmax: the maximum amount of power the powerplant can generate.
   - pmin: the minimum amount of power the powerplant generates when switched on.

Taken into account that a gas-fired powerplant also emits CO2, the cost of running the powerplant should also take into account the cost of the [emission allowances](https://en.wikipedia.org/wiki/Carbon_emission_trading).  Each MWh generated creates 0.3 ton of CO2. 

#### response

The response should be a json as in `example_response.json`, which is the expected answer for `example_payload.json`, specifying for each powerplant how much power each powerplant should deliver. The power produced by each powerplant has to be a multiple of 0.1 Mw and the sum of the power produced by all the powerplants together should equal the load.
