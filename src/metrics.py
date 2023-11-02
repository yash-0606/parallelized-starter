import sqlite3
import database
import os
script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "../data/2023-11-02.db")
def calculate_overall_customer_satisfaction(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT AVG(rating_received) FROM rides"

    cursor.execute(query)
    average_satisfaction = cursor.fetchone()[0]

    conn.close()
    return average_satisfaction

def calculate_driver_efficiency(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = """
    SELECT driver_id, AVG(reported_cost)
    FROM rides
    GROUP BY driver_id
    """
    cursor.execute(query)
    driver_efficiency_data = cursor.fetchall()
    for driver in driver_efficiency_data:
        driver_id, avg_reported_cost = driver

    conn.close()

def analyze_driver_efficiency(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = """
    SELECT drivers.id, drivers.rides, drivers.age, vehicle_type, reported_cost, trip_duration, traffic_condition
    FROM drivers
    LEFT JOIN rides ON drivers.id = rides.driver_id
    """
    cursor.execute(query)
    data = cursor.fetchall()

    driver_inefficiency = {}

    for row in data:
        driver_id, rides, age, vehicle_type, reported_cost, trip_duration, traffic_condition = row

        if driver_id not in driver_inefficiency:
            driver_inefficiency[driver_id] = {
                "HIGHCOST": 0,
                "SLOW": 0,
                "TRAFFIC": 0
            }


        if vehicle_type in ('2W', '3W', '4W', 'other') and reported_cost is not None:
            cost_per_km = reported_cost / trip_duration
            if (
                (vehicle_type == '2W' and cost_per_km > 2.7) or
                (vehicle_type == '3W' and cost_per_km > 3.6) or
                (vehicle_type == '4W' and cost_per_km > 15) or
                (vehicle_type == 'other' and cost_per_km > 8)
            ):
                driver_inefficiency[driver_id]["HIGHCOST"] += 1


        if trip_duration is not None and trip_duration > 0 and trip_duration < 20:
            driver_inefficiency[driver_id]["SLOW"] += 1

        if traffic_condition in ('POOR', 'VPOOR'):
            driver_inefficiency[driver_id]["TRAFFIC"] += 1

    for driver_id, inefficiency in driver_inefficiency.items():
        inefficiency_string = ",".join([reason for reason, count in inefficiency.items() if count > 0])
        if inefficiency_string:
            print(f"Driver {driver_id} inefficiency reasons: {inefficiency_string}")

    conn.close()

def calculate_driver_average_rating(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
    SELECT driver_id, AVG(rating_received) AS avg_rating
    FROM rides
    GROUP BY driver_id
    """

    cursor.execute(query)
    driver_ratings = cursor.fetchall()

    conn.close()


    average_ratings = {}

    for driver_id, avg_rating in driver_ratings:
        average_ratings[driver_id] = avg_rating

    return average_ratings


def calculate_driver_loyalty(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = """
    SELECT id, rides, age
    FROM drivers
    """
    cursor.execute(query)
    driver_data = cursor.fetchall()
    for driver in driver_data:
        driver_id, rides, age = driver
        inefficiency_reasons = []

        rides = int(rides)  # Convert 'rides' to an integer

        if rides < 200:
            inefficiency_reasons.append("LOWLOYALTY")
        elif 200 <= rides < 300:
            inefficiency_reasons.append("MEDIUMLOYALTY")
        elif 300 <= rides < 400:
            inefficiency_reasons.append("HIGHLOYALTY")
        elif 400 <= rides < 500:
            inefficiency_reasons.append("VERYHIGHLOYALTY")
        else:
            inefficiency_reasons.append("SUPERHIGHLOYALTY")

        inefficiency_string = ",".join(inefficiency_reasons)
        print(f"Driver {driver_id} loyalty: {inefficiency_string}")

    conn.close()


def calculate_paycheck(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
    SELECT driver_id, SUM(distance_travelled) AS total_distance, SUM(trip_duration) AS total_duration
    FROM rides
    GROUP BY driver_id
    """

    cursor.execute(query)
    paycheck_data = cursor.fetchall()

    for driver in paycheck_data:
        driver_id, total_distance, total_duration = driver

        base_fee = 50
        cost_per_km = 10
        cost_per_minute = 5

        total_payment = base_fee + total_distance * cost_per_km + total_duration * cost_per_minute

        database.insert_analysis_row(
            driver_id=driver_id,
            efficiency="",  
            inefficiencyReason="",  
            payout=0,  
            bonus=0, 
            total_payment=total_payment,
            database_path=db_path
        )

    conn.close()

def calculate_bonus(loyalty, performance, efficiency):

    bonus = 0


    if loyalty == 5:
        bonus += 0.30
    elif loyalty == 4:
        bonus += 0.20
    elif loyalty == 3:
        bonus += 0.15
    elif loyalty == 2:
        bonus += 0.025
    else:
        bonus += 0


    if performance >= 4.5:
        bonus += 0.20
    elif performance >= 3:
        bonus += 0.10
    else:
        bonus += 0

    if 'SLOW' in efficiency or 'HIGHCOST' in efficiency:
        bonus = 0
    elif 'TRAFFIC' in efficiency:
        bonus += 0.05
    else:
        bonus += 0.10

    return bonus

def calculate_bonus_for_drivers(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = "SELECT driver_id FROM driver_analyses"
    cursor.execute(query)
    driver_data = cursor.fetchall()

    for driver_id in driver_data:
        loyalty = calculate_driver_loyalty(driver_id)
        performance = calculate_driver_average_rating(driver_id)
        efficiency = calculate_driver_efficiency(driver_id)
        bonus = calculate_bonus(loyalty, performance, efficiency)


    conn.commit()
    conn.close()













print("Task 1: Calculate Overall Customer Satisfaction")
calculate_overall_customer_satisfaction(db_path)
print("\nTask 2: Calculate Driver Efficiency")
calculate_driver_efficiency(db_path)
analyze_driver_efficiency(db_path)
print("\nTask 3: Analyze Driver Efficiency")
calculate_driver_average_rating(db_path)
print("\nTask 4: Calculate Driver Performance")
calculate_driver_loyalty(db_path)
print("\nTask 5: Calculate Driver Loyalty")
calculate_paycheck(db_path)
print("\nTask 6: Calculate Driver Paycheck")
calculate_bonus_for_drivers(db_path)
print("\nTask 7: Calculate Driver Bonus")