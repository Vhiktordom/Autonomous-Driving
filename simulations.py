
import numpy as np
from db_manager import get_db
import datetime

class DrivingSimulator:
    def __init__(self):
        self.db = get_db()
        self._create_tables()

    def _create_tables(self):
        with self.db:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS lane_change_simulations (
                    id INTEGER PRIMARY KEY,
                    time INTEGER,
                    car_speed REAL,
                    lead_car_speed REAL,
                    distance_to_lead_car REAL,
                    lane_change_event INTEGER
                )
            ''')
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS pedestrian_stop_simulations (
                    id INTEGER PRIMARY KEY,
                    time INTEGER,
                    car_speed REAL,
                    pedestrian_event INTEGER
                )
            ''')
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS obstacle_avoidance_simulations (
                    id INTEGER PRIMARY KEY,
                    time INTEGER,
                    car_speed REAL,
                    obstacle_event INTEGER
                )
            ''')

    def simulate_lane_change(self, scenario_duration=60):
        """Simulate a driving scenario where the car follows another vehicle and occasionally changes lanes."""
        time = np.arange(0, scenario_duration, 1)
        car_speed = np.random.normal(loc=30, scale=2, size=len(time))
        lead_car_speed = car_speed - np.random.normal(loc=0, scale=3, size=len(time))
        distance_to_lead_car = np.abs(np.random.normal(loc=10, scale=2, size=len(time)))
        lane_change_event = np.random.choice([0, 1], size=len(time), p=[0.9, 0.1])

        with self.db:
            self.db.executemany('''
                INSERT INTO lane_change_simulations 
                (time, car_speed, lead_car_speed, distance_to_lead_car, lane_change_event)
                VALUES (?, ?, ?, ?, ?)
            ''', zip(time, car_speed, lead_car_speed, distance_to_lead_car, lane_change_event))

    def simulate_pedestrian_stop(self, scenario_duration=60):
        """Simulate a driving scenario where the car stops for a pedestrian at a crosswalk."""
        time = np.arange(0, scenario_duration, 1)
        car_speed = np.random.normal(loc=30, scale=2, size=len(time))
        pedestrian_event = np.zeros(len(time))
        pedestrian_event[30] = 1
        car_speed[30:] = 0

        with self.db:
            self.db.executemany('''
                INSERT INTO pedestrian_stop_simulations 
                (time, car_speed, pedestrian_event)
                VALUES (?, ?, ?)
            ''', zip(time, car_speed, pedestrian_event))

    def simulate_obstacle_avoidance(self, scenario_duration=60):
        """Simulate a scenario where the car avoids an obstacle."""
        time = np.arange(0, scenario_duration, 1)
        car_speed = np.random.normal(loc=30, scale=2, size=len(time))
        obstacle_event = np.zeros(len(time))
        obstacle_event[45] = 1
        car_speed[45:] = np.maximum(car_speed[45:] - 10, 0)

        with self.db:
            self.db.executemany('''
                INSERT INTO obstacle_avoidance_simulations 
                (time, car_speed, obstacle_event)
                VALUES (?, ?, ?)
            ''', zip(time, car_speed, obstacle_event))

    def run_all_simulations(self, scenario_duration=60):
        self.simulate_lane_change(scenario_duration)
        self.simulate_pedestrian_stop(scenario_duration)
        self.simulate_obstacle_avoidance(scenario_duration)

    def query_lane_change_simulation(self, limit=10):
        cursor = self.db.execute('''
            SELECT * FROM lane_change_simulations
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def query_pedestrian_stop_simulation(self, limit=10):
        cursor = self.db.execute('''
            SELECT * FROM pedestrian_stop_simulations
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]

    def query_obstacle_avoidance_simulation(self, limit=10):
        cursor = self.db.execute('''
            SELECT * FROM obstacle_avoidance_simulations
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def query_all_simulations(self, limit=10):
        def make_serializable(obj):
            if isinstance(obj, (int, float)):
                return obj
            elif isinstance(obj, bytes):
                return obj.decode('utf-8')
            return str(obj)

        results = {
            'lane_change': self.query_lane_change_simulation(limit),
            'pedestrian_stop': self.query_pedestrian_stop_simulation(limit),
            'obstacle_avoidance': self.query_obstacle_avoidance_simulation(limit)
        }
        
        serializable_results = {}
        for scenario, data in results.items():
            serializable_results[scenario] = [
                {key: make_serializable(value) for key, value in row.items()}
                for row in data
            ]
        
        return serializable_results

    # def query_all_simulations(self, limit=10):
    #     # print(f"Lane Change {self.query_lane_change_simulation(limit)}")
    #     # print(f"pedestrian_stop {self.query_pedestrian_stop_simulation(limit)}")
    #     # print(f"obstacle_avoidance {self.query_obstacle_avoidance_simulation(limit)}")
    #     return {
    #         'lane_change': self.query_lane_change_simulation(limit),
    #         'pedestrian_stop': self.query_pedestrian_stop_simulation(limit),
    #         'obstacle_avoidance': self.query_obstacle_avoidance_simulation(limit)
    #     }