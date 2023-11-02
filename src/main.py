import os
import sqlite3
import database
import metrics


script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, "../data/2023-11-02.db")


def calculate_and_insert_bonuses(database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    driver_ids = database.get_drivers(cursor)

    for driver_id in driver_ids:
        loyalty = metrics.calculate_driver_loyalty(database_path, driver_id)
        rating = metrics.calculate_driver_average_rating(database_path, driver_id)
        efficiency = metrics.calculate_driver_efficiency(database_path, driver_id)

        bonus = metrics.calculate_bonus(loyalty, rating, efficiency)

        database.insert_analysis_row(
            driver_id=driver_id,
            efficiency=efficiency,
            inefficiencyReason="",
            payout=0,
            bonus=bonus,
            total_payment=0,
        )

    conn.close()
if __name__ == '__main__':

    print("Task 1: Calculate Overall Customer Satisfaction")
    metrics.calculate_overall_customer_satisfaction(db_path)

    print("\nTask 2: Calculate Driver Efficiency")
    metrics.calculate_driver_efficiency(db_path)


    print("\nTask 3: Analyze Driver Efficiency")
    metrics.analyze_driver_efficiency(db_path)


    print("\nTask 4: Calculate Driver Performance")
    metrics.calculate_driver_loyalty(db_path)

  
    print("\nTask 5: Calculate Driver Loyalty")
    metrics.calculate_paycheck(db_path)

    
    print("\nTask 6: Calculate Driver Paycheck")
    calculate_and_insert_bonuses(db_path)

   
    print("\nTask 7: Calculate Driver Bonus")

    

    print("All tasks completed.")