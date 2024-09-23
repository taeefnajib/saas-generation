from fastapi import FastAPI
import os
import time
import shutil
from saas.baseclass import SimulationParams
from saas.utils import *
from saas.saas import run_saas_batch

app = FastAPI()

@app.post("/simulations/saas")
def run_simulation(params: SimulationParams):
    
    start = time.time()

    # Create data directory if it doesn't exist, otherwise remove all files inside
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    else:
        # Remove all files inside the 'data' directory
        for filename in os.listdir(data_dir):
            file_path = os.path.join(data_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove file or symlink
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directory
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    
    # Create users dictionary using UserConfig
    original_users = generate_users(
        number_of_user=params.user_config.number_of_user,
        start_time=params.metadata.start_date,
        location_type=params.user_config.location_type,
        local_percentage=params.user_config.local_percentage,
        end_time=params.metadata.end_date,
        subscription_tiers = params.subscription_config.subscription_tiers,
        churn_dist=params.user_config.churn_dist
    )

    original_features = params.feature_config.features
    features = original_features

    # Run multiple batches
    batch_count = 0
    session_left = params.metadata.number_of_sessions
    batch_size = params.metadata.batch_size

    while session_left > 0:
        batch_count += 1
        if session_left <= batch_size:
            batch_size = session_left

        batch_start = time.time()
        (
            pageviews,
            logins,
            new_accounts,
            social_shares,
            favorites,
            visits,
            users,
            features,
            tier_upgradations,
            feature_consumptions,
        ) = run_saas_batch(params, original_users, features, batch_size)

        
        # Append data directly to CSV files
        generate_csv_from_data(pageviews, "pageviews.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(logins, "logins.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(new_accounts, "new_accounts.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(social_shares, "social_shares.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(favorites, "favorites.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(visits, "visits.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(features, "features.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(users, "users.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(tier_upgradations, "tier_upgradations.csv", data_path=params.metadata.data_path)
        generate_csv_from_data(feature_consumptions, "feature_consumptions.csv", data_path=params.metadata.data_path)

        # For payments, you might need to wait until the deduplicated users are processed
        payments = generate_payments(params, users, params.subscription_config.subscription_tiers, tier_upgradations)
        generate_csv_from_data(payments, 'payments.csv', data_path=params.metadata.data_path)

        batch_end = time.time()
        session_left -= batch_size

        print(f"Batch #{batch_count} processed in {batch_end - batch_start:.2f} seconds.")

    # Add id column to CSV files after all batch runs
    add_id_column_to_csv("pageviews.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("logins.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("new_accounts.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("social_shares.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("favorites.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("visits.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("features.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("users.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("tier_upgradations.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("feature_consumptions.csv", data_path=params.metadata.data_path)
    add_id_column_to_csv("payments.csv", data_path=params.metadata.data_path)

    end = time.time()
    print(f"CSV files are generated successfully in the '{params.metadata.data_path}' folder.")
    print(f"Simulation completed in {end - start:.2f} seconds.")

    return {"status": "Simulation completed", "execution_time": round(end - start, 2)}


# uvicorn main:app --reload
# {"metadata":{"number_of_sessions": 5000},"user_config":{"location_type":"global","local_percentage":0.85}}
# {"metadata":{"number_of_sessions": 5000, "data_path":"../saas_pipeline/saas_pipeline/data"},"user_config":{"location_type":"global","local_percentage":0.85}}
# {"number_of_sessions": 1000,"number_of_user": 50, "location_type":"global","local_percentage":0.85, "data_path":"../ecom_pipeline/ecom_pipeline/data"}
# Need to change tier based on tier_upgradation_probability and need to create payment based on subscription_tier and churn_date
# need to choose features based on tier