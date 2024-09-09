from flask import jsonify, request

def init_app(app, simulator):
    @app.route('/simulate', methods=['POST'])
    def run_simulation():
        scenario_duration = request.json.get('scenario_duration', 60)
        simulator.run_all_simulations(scenario_duration)
        return jsonify({"message": "Simulations completed and stored in database"}), 200

    @app.route('/query/lane_change', methods=['GET'])
    def query_lane_change():
        limit = request.args.get('limit', default=10, type=int)
        results = simulator.query_lane_change_simulation(limit)
        return jsonify([dict(row) for row in results]), 200

    @app.route('/query/pedestrian_stop', methods=['GET'])
    def query_pedestrian_stop():
        limit = request.args.get('limit', default=10, type=int)
        results = simulator.query_pedestrian_stop_simulation(limit)
        return jsonify([dict(row) for row in results]), 200

    @app.route('/query/obstacle_avoidance', methods=['GET'])
    def query_obstacle_avoidance():
        limit = request.args.get('limit', default=10, type=int)
        results = simulator.query_obstacle_avoidance_simulation(limit)
        return jsonify([dict(row) for row in results]), 200

    @app.route('/query/all', methods=['GET'])
    def query_all_simulations():
        limit = request.args.get('limit', default=10, type=int)
        results = simulator.query_all_simulations(limit)
        return jsonify({k: [dict(row) for row in v] for k, v in results.items()}), 200