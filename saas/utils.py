from mimesis import Generic
from mimesis.locales import Locale
import numpy as np
import pandas as pd
from saas.constants import *
import csv
import os
import uuid
from typing import Dict, Union
from pydantic import BaseModel
from saas.baseclass import *
import random
from datetime import timedelta, datetime

mim = Generic(locale=Locale.EN)

rng = np.random.default_rng()


# Generates `size` strings (lowercase alphabet - i.e. `a-z`) with uniform distribution
def gen_rand_strs(size: int, str_len: int = 10) -> np.ndarray:
    a, z = np.array(["a", "z"]).view("int32")
    return rng.integers(low=a, high=z, size=size * str_len, dtype="int32").view(
        f"U{str_len}"
    )


# Function to generate a unique timestamp for new account creation
def generate_unique_timestamp(base_time, time_shift_range):
    time_shift = np.random.randint(1, time_shift_range)  # Random shift within a range
    return base_time + np.timedelta64(time_shift, "s")


def gen_rand_categories(categories: list, p: list[float] = None, size: int = 1):
    if p is None:
        # If no probability is provided, generate a uniform distribution
        p = [1 / len(categories)] * len(categories)
    cumulative_prob = np.cumsum(p)
    random_value = np.random.rand()
    index = np.searchsorted(cumulative_prob, random_value)
    return categories[index]


# Generate random city, state, country
def normalize_population_weights(df):
    total_population = df["Population"].sum()
    return df["Population"] / total_population

def choose_city(df, weights):
    # Randomly choose a city based on the provided weights
    city_data = df.sample(weights=weights).iloc[0]
    return {
        "City": city_data["City"],
        "ST": city_data["ST"] if "ST" in city_data else None,
        "Country": city_data["Country"],
        "Latitude": city_data["Latitude"],
        "Longitude": city_data["Longitude"],
    }

def generate_location(location_type, local_percentage=0.0):
    if location_type == "local":
        # Normalize population weights for US cities
        us_weights = normalize_population_weights(us_cities_df)
        return choose_city(us_cities_df, us_weights)

    elif location_type == "global":

        # Normalize population weights for both datasets
        us_weights = normalize_population_weights(us_cities_df)
        global_weights = normalize_population_weights(global_cities_df)

        # Randomly decide whether to choose from local or global
        if np.random.rand() < local_percentage:
            # Choose from US cities
            return choose_city(us_cities_df, us_weights)
        else:
            # Choose from global cities
            return choose_city(global_cities_df, global_weights)

    else:
        raise ValueError("Invalid location_type. Choose 'local' or 'global'.")


# Generate random phone number based on country
def generate_phonenumber(country="United States"):
    # Ensure the country exists in the mapping, default to "United States" if not found
    if country not in country_codes:
        raise ValueError(f"Country '{country}' not found in the list")

    # Get the country code and length of the phone number
    country_code = country_codes[country]["telephone_code"]
    number_length = 9  # country_codes[country].get("number_length", 9) Default to 9 digits if not specified

    # Generate a random phone number of the specified length
    rng = np.random.default_rng()
    phone_number = "".join(
        [str(rng.integers(low=0, high=10)) for _ in range(number_length)]
    )

    # Combine the country code and the phone number with a '+' prefix for international format
    return f"{country_code} {phone_number}"


# Function to find page IDs by page type
def find_page_ids_by_type(page_type, pages):
    return [
        page_id
        for page_id, page_info in pages.items()
        if page_info.page_type == page_type
    ]


# Function to generate products dictionary
# def generate_products(number_of_products, max_prod_qty, avg_rev_per_order):
#     products = {}
#     avg_qty = (1 + max_prod_qty) / 2
#     avg_price = avg_rev_per_order / avg_qty
#     lower_price = avg_price * 0.5
#     higher_price = avg_price * 1.5
#     # Mean and standard deviation for the normal distribution (mean = 0.5 for center)
#     mean_popularity = 0.5
#     std_dev_popularity = 0.2  # Adjust this for sprea
#     for i in range(1, (number_of_products + 1)):  # Creating products
#         product_brand = str(gen_rand_categories(categories=product_brands, size=1)[0])
#         product_category = str(
#             gen_rand_categories(categories=product_categories, size=1)[0]
#         )
#         # Generate a normally distributed popularity score and clip it between 0 and 1
#         popularity_score = np.clip(
#             np.random.normal(mean_popularity, std_dev_popularity), 0, 1
#         )
#         products[i] = {
#             "product_sku": str(gen_rand_strs(size=1, str_len=16)[0]),
#             "product_name": str(mim.text.word()).capitalize(),
#             "product_brand": product_brand,
#             "product_category": product_category,
#             "product_colors": product_colors,
#             "product_sizes": product_sizes,
#             "price": round(rng.uniform(lower_price, higher_price), 2),
#             "product_popularity_score": round(popularity_score, 2),
#             "no_of_add_to_carts": 0,
#             "qty_added_to_carts": 0,
#             "no_of_orders": 0,
#             "qty_ordered": 0,
#         }
#     return products


def generate_users(
    number_of_user,
    start_time,
    location_type,
    local_percentage,
    end_time,
    subscription_tiers,
    churn_dist="normal"
):
    users = {}

    # Convert start_time and end_time to numpy.datetime64
    start_time = np.datetime64(start_time)
    end_time = np.datetime64(end_time)

    # Define subscription tiers
    # subscription_tiers = ["free", "basic", "premium"]

    # Generate users
    for idx in range(1, (number_of_user + 1)):
        signup_duration = rng.integers(1, 31104000)
        signup_time = np.datetime64(start_time) - np.timedelta64(signup_duration, "ms")
 
        user_location = generate_location(
            location_type=location_type, local_percentage=local_percentage
        )

        # Retrieve country-specific information
        country_info = country_codes[user_location["Country"]]

        # Select a random language if multiple languages are available
        language_choice = random.choice(list(country_info["language"].values()))

        # Assign a random subscription tier from 'subscription_tiers'
        subscription_tier_id = random.choice(list(subscription_tiers.keys()))

        # Generate a churn date
        signup_time_np = signup_time.astype('datetime64[s]').astype(float)
        end_time_np = end_time.astype('datetime64[s]').astype(float)

        if churn_dist == "normal":
            churn_duration = rng.normal(loc=(end_time_np - signup_time_np) / 2, scale=(end_time_np - signup_time_np) / 6)
        elif churn_dist == "left_skewed":
            churn_duration = rng.gamma(shape=2, scale=(end_time_np - signup_time_np) / 2)
        elif churn_dist == "right_skewed":
            churn_duration = rng.beta(a=2, b=5) * (end_time_np - signup_time_np)
        else:  # uniform distribution
            churn_duration = rng.uniform(0, end_time_np - signup_time_np)

        churn_time = signup_time + np.timedelta64(int(churn_duration), "s")

        # Ensure churn_time is between signup_time and end_time
        if churn_time < signup_time:
            churn_time = signup_time
        elif churn_time > end_time:
            churn_time = end_time

        # Add the user to the dictionary
        users[idx] = {
            "signup_time": signup_time,
            "user_id": str(gen_rand_strs(size=1, str_len=16)[0]),
            "activity_score": rng.uniform(0, 1),
            "username": mim.person.username(),
            "first_name": mim.person.first_name(),
            "last_name": mim.person.last_name(),
            "email": mim.person.email(),
            "address": mim.address.address(),
            "city": user_location["City"],
            "state": user_location["ST"],
            "country": user_location["Country"],
            "currency": country_info["currency"][1]["currency_code"],  
            "conversion_rate": country_info["currency"][1]["conversion_rate"],
            "phone_number": generate_phonenumber(country=user_location["Country"]),
            "signup_method": str(
                gen_rand_categories(
                    categories=signup_methods, size=1, p=[0.1, 0.1, 0.8]
                )
            ),
            "lat": user_location["Latitude"],
            "lng": user_location["Longitude"],
            "language": language_choice["language_name"],
            "locale": language_choice["locale"],
            "initial_tier": str(subscription_tiers[subscription_tier_id].name),
            "subscription_tier": str(subscription_tiers[subscription_tier_id].name),
            "churn_date": churn_time
        }

    # Sort and return users
    sorted_users = sorted(users.items(), key=lambda x: x[1]["signup_time"])
    sorted_users_dict = {user_id: user_data for user_id, user_data in sorted_users}

    return sorted_users_dict

def generate_csv_from_data(data_dict, filename, data_path, append=True):
    file_path = os.path.join(data_path, filename)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(data_dict, orient='index')

    # If append is True, check if the file exists and append data, otherwise create new file
    if append and os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)

def add_id_column_to_csv(filename, data_path):
    file_path = os.path.join(data_path, filename)
    
    if os.path.exists(file_path):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # If 'id' column is missing, generate it
        if 'id' not in df.columns:
            df.insert(0, 'id', range(1, len(df) + 1))
        
        # Write back the CSV with the id column
        df.to_csv(file_path, index=False)

# def generate_csv_from_data(data_dict, filename, data_path, append=True):
#     file_path = os.path.join(data_path, filename)
    
#     # Convert the dictionary to a DataFrame
#     df = pd.DataFrame.from_dict(data_dict, orient='index')
    
#     # Initialize the starting id value
#     start_id = 1
    
#     if append and os.path.exists(file_path):
#         # If the file exists and we are appending, read the file to get the max id
#         existing_df = pd.read_csv(file_path)
#         if 'id' in existing_df.columns:
#             max_id = existing_df['id'].max()
#             start_id = max_id + 1  # Increment the id starting point
    
#     # Add the incremental id column to the DataFrame
#     df.insert(0, 'id', range(start_id, start_id + len(df)))

#     # Append or write the CSV
#     if append and os.path.exists(file_path):
#         df.to_csv(file_path, mode='a', header=False, index=False)
#     else:
#         df.to_csv(file_path, mode='w', header=True, index=False)

# def generate_csv_from_data(
#     data: Dict[int, Union[BaseModel, Dict]], filename: str, data_path="./data", append: bool = False
# ):
#     filepath = os.path.join(data_path, filename)

#     if len(data) > 0:
#         # Get an example instance
#         example_instance = next(iter(data.values()))

#         if isinstance(example_instance, dict):
#             # If the values are dictionaries, infer the fieldnames from the first dictionary
#             first_item = next(iter(example_instance.values()))
#             if isinstance(first_item, dict):
#                 fieldnames = ["id"] + list(first_item.keys())
#             else:
#                 # If not a dictionary, infer fieldnames from the dictionary keys
#                 fieldnames = ["id"] + list(example_instance.keys())
#         else:
#             # If the values are instances of BaseModel, infer the fieldnames from the model's annotations
#             if hasattr(example_instance, "__annotations__"):
#                 fieldnames = ["id"] + list(example_instance.__annotations__.keys())
#             else:
#                 raise TypeError(
#                     "The provided data does not contain Pydantic BaseModel instances or dictionaries."
#                 )

#         # Open the file in append mode if requested
#         with open(filepath, mode="a" if append else "w", newline="") as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)

#             # Write the header only if the file is opened in write mode
#             if not append or file.tell() == 0:
#                 writer.writeheader()

#             # Write the data
#             for index, (item_id, item_data) in enumerate(data.items(), start=1):
#                 row_data = {"id": index}  # Add the unique ID
#                 if isinstance(item_data, dict):
#                     # Convert datetime64 and other non-serializable types to string
#                     for key, value in item_data.items():
#                         if isinstance(value, (np.datetime64,)):
#                             row_data[key] = str(value)
#                         else:
#                             row_data[key] = value
#                 elif isinstance(item_data, BaseModel):
#                     # Convert datetime64 and other non-serializable types to string
#                     for key, value in item_data.dict().items():
#                         if isinstance(value, (np.datetime64,)):
#                             row_data[key] = str(value)
#                         else:
#                             row_data[key] = value
#                 else:
#                     raise TypeError("The provided data contains invalid types.")
#                 writer.writerow(row_data)

    #     print(
    #         f"CSV file '{filename}' generated successfully in the '{data_path}' folder."
    #     )
    # else:
    #     print(f"CSV file '{filename}' is not generated since there is no data.")

# def generate_csv_from_data(
#     data: Dict[int, Union[BaseModel, Dict]], filename: str, data_path="./data"
# ):
#     filepath = os.path.join(data_path, filename)

#     if len(data) > 0:
#         # Get an example instance
#         example_instance = next(iter(data.values()))

#         if isinstance(example_instance, dict):
#             # If the values are dictionaries, infer the fieldnames from the first dictionary
#             first_item = next(iter(example_instance.values()))
#             if isinstance(first_item, dict):
#                 fieldnames = ["id"] + list(first_item.keys())
#             else:
#                 # If not a dictionary, infer fieldnames from the dictionary keys
#                 fieldnames = ["id"] + list(example_instance.keys())
#         else:
#             # If the values are instances of BaseModel, infer the fieldnames from the model's annotations
#             if hasattr(example_instance, "__annotations__"):
#                 fieldnames = ["id"] + list(example_instance.__annotations__.keys())
#             else:
#                 raise TypeError(
#                     "The provided data does not contain Pydantic BaseModel instances or dictionaries."
#                 )

#         with open(filepath, mode="w", newline="") as file:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)

#             # Write the header
#             writer.writeheader()

#             # Write the data
#             for index, (item_id, item_data) in enumerate(data.items(), start=1):
#                 row_data = {"id": index}  # Add the unique ID
#                 if isinstance(item_data, dict):
#                     # Convert datetime64 and other non-serializable types to string
#                     for key, value in item_data.items():
#                         if isinstance(value, (np.datetime64,)):
#                             row_data[key] = str(value)
#                         else:
#                             row_data[key] = value
#                 elif isinstance(item_data, BaseModel):
#                     # Convert datetime64 and other non-serializable types to string
#                     for key, value in item_data.dict().items():
#                         if isinstance(value, (np.datetime64,)):
#                             row_data[key] = str(value)
#                         else:
#                             row_data[key] = value
#                 else:
#                     raise TypeError("The provided data contains invalid types.")
#                 writer.writerow(row_data)

#         print(
#             f"CSV file '{filename}' generated successfully in the '{data_path}' folder."
#         )
#     else:
#         print(f"CSV file '{filename}' is not generated since there is no data.")

def gen_random_date(
    start_date_str, end_date_str, data_dist="exponential", overall_scale_factor=2
):
    # Convert string inputs to numpy.datetime64
    start_date = np.datetime64(start_date_str)
    end_date = np.datetime64(end_date_str)

    # Convert to milliseconds since epoch for easier random generation
    start_ms = start_date.astype("int64")
    end_ms = end_date.astype("int64")

    if data_dist == "normal":
        # Generate normally distributed random values
        mean = (start_ms + end_ms) / 2
        std_dev = (
            end_ms - start_ms
        ) / 6  # Assuming 99.7% of values fall within ±3 standard deviations
        random_date_ms = int(np.random.normal(mean, std_dev))

    elif data_dist == "uniform":
        random_date_ms = np.random.randint(start_ms, end_ms)

    elif data_dist == "right_skewed":
        # Skewed to the right: use the square of a uniform distribution
        u = np.random.uniform(0, 1)
        skewed_value = u**2
        random_date_ms = int(start_ms + skewed_value * (end_ms - start_ms))

    elif data_dist == "left_skewed":
        # Skewed to the left: use the square root of a uniform distribution
        u = np.random.uniform(0, 1)
        skewed_value = np.sqrt(u)
        random_date_ms = int(start_ms + skewed_value * (end_ms - start_ms))

    elif data_dist == "exponential":
        # Make scale dynamic by incorporating scale_factor
        scale = (
            end_ms - start_ms
        ) / overall_scale_factor  # Scale the range by the factor
        random_date_delta_ms = np.random.exponential(scale)
        # Adjust to create a more balanced distribution
        random_date_ms = int(start_ms + random_date_delta_ms)

    # Clip to ensure date is within the bounds
    random_date_ms = np.clip(random_date_ms, start_ms, end_ms)

    # Calculate the random date by adding milliseconds to the start_date
    random_date = start_date + np.timedelta64(random_date_ms - start_ms, "ms")

    # Return start and end of that day
    start_time = np.datetime64(random_date, "D").astype(
        "datetime64[ms]"
    )  # Start of the day
    end_time = (
        start_time + np.timedelta64(1, "D") - np.timedelta64(1, "ms")
    )  # End of the day

    return start_time, end_time


def gen_random_time(
    start_time, end_time, daily_cyclicality="uniform", daily_scale_factor=5
):
    start_ms = start_time.astype("int64")
    end_ms = end_time.astype("int64")

    if daily_cyclicality == "uniform":
        random_time_ms = np.random.randint(start_ms, end_ms)

    elif daily_cyclicality == "normal":
        mean = (start_ms + end_ms) / 2
        std_dev = (
            end_ms - start_ms
        ) / 6  # 99.7% of values fall within ±3 standard deviations
        random_time_ms = int(np.random.normal(mean, std_dev))

    elif daily_cyclicality == "exponential":
        scale = (
            end_ms - start_ms
        ) / daily_scale_factor  # Adjust skewness with scale_factor
        random_time_delta_ms = np.random.exponential(scale)
        random_time_ms = int(end_ms - random_time_delta_ms)

    elif daily_cyclicality == "right_skewed":
        u = np.random.uniform(0, 1)
        skewed_value = u**2  # Right skew: square of a uniform distribution
        random_time_ms = int(start_ms + skewed_value * (end_ms - start_ms))

    elif daily_cyclicality == "left_skewed":
        u = np.random.uniform(0, 1)
        skewed_value = np.sqrt(u)  # Left skew: square root of a uniform distribution
        random_time_ms = int(start_ms + skewed_value * (end_ms - start_ms))

    # Clip to ensure the generated time is within bounds
    random_time_ms = np.clip(random_time_ms, start_ms, end_ms)

    # Convert to np.datetime64 using the start_time as the base
    random_time = start_time + np.timedelta64(random_time_ms - start_ms, "ms")

    return random_time


def update_product_attributes(
    features: Dict[int, Feature], updates: Dict[str, int]
) -> None:
    for feature_id, feature_info in features.items():
        for key, value in updates.items():
            if hasattr(feature_info, key):
                setattr(feature_info, key, value)



# def generate_payments(params, users, subscription_tiers, tier_upgradations):
#     payments = {}

#     # Create a reverse lookup for subscription tier names
#     tier_name_to_id = {v.name: k for k, v in subscription_tiers.items()}

#     for user_key, user_info in users.items():
#         signup_date = user_info['signup_time']
#         churn_date = user_info.get('churn_date', None)
#         current_tier = user_info.get('subscription_tier', None)
#         user_id = user_info['user_id']  # Unique user_id to include in the payment record

#         # Skip users without a subscription_tier
#         if current_tier is None:
#             print(f"Skipping user {user_id} due to missing subscription_tier.")
#             continue

#         payment_dates = []

#         # Ensure that signup_date and churn_date are datetime objects
#         if isinstance(signup_date, np.datetime64):
#             signup_date = signup_date.astype('M8[ms]').astype('O')  # Convert numpy datetime to Python datetime
#         if churn_date and isinstance(churn_date, np.datetime64):
#             churn_date = churn_date.astype('M8[ms]').astype('O')

#         # If user has churned, stop payments at churn_date, otherwise till the end date
#         end_date = churn_date if churn_date else params.metadata.end_date

#         # Convert end_date to Python datetime if it's a numpy.datetime64 or an int
#         if isinstance(end_date, np.datetime64):
#             end_date = end_date.astype('M8[ms]').astype(datetime)
#         elif isinstance(end_date, int):
#             end_date = datetime.utcfromtimestamp(end_date / 10000)

#         # Generate payment dates every 30 days starting from signup_date
#         payment_date = signup_date

#         while payment_date < end_date:
#             payment_dates.append(payment_date)
#             payment_date += timedelta(days=30)

#         # Initialize with the user's original subscription tier
#         tier_upgrades = tier_upgradations.get(user_key, [])
        
#         if not isinstance(tier_upgrades, list):
#             tier_upgrades = []

#         next_upgrade_index = 0
#         next_upgrade = tier_upgrades[next_upgrade_index] if tier_upgrades else None

#         # For each payment date, check if there is a tier upgrade
#         for date in payment_dates:
#             # Check if a tier upgrade happened before or on this date
#             while next_upgrade and next_upgrade['upgrade_date'] <= date:
#                 print(f"User {user_id} upgraded from {current_tier} to {next_upgrade['new_tier']} on {next_upgrade['upgrade_date']}")
#                 current_tier = next_upgrade['new_tier']
#                 next_upgrade_index += 1

#                 if next_upgrade_index < len(tier_upgrades):
#                     next_upgrade = tier_upgradations.get(user_key, [])[next_upgrade_index]
#                 else:
#                     next_upgrade = None

#             # Find the subscription price for the current tier
#             current_tier_id = tier_name_to_id.get(current_tier)  
#             if current_tier_id is None:
#                 raise ValueError(f"Invalid tier name: {current_tier}")

#             tier_info = subscription_tiers[current_tier_id]
#             price = tier_info.price

#             # Record the payment, adding user_id to the payment information
#             if user_key not in payments:
#                 payments[user_key] = []
            
#             payments[user_key].append({
#                 'user_id': user_id,  # Add unique user_id to the payment entry
#                 'date': date,
#                 'tier': tier_info.name,
#                 'price': price
#             })

#     return payments

# def generate_payments(params, users, subscription_tiers, tier_upgradations):
#     payments = {}

#     # Create a reverse lookup for subscription tier names
#     tier_name_to_id = {v.name: k for k, v in subscription_tiers.items()}

#     idx = 1

#     for user_key, user_info in users.items():
#         signup_date = user_info['signup_time']
#         churn_date = user_info.get('churn_date', None)
#         initial_tier = user_info.get('initial_tier', None)
#         user_id = user_info['user_id'] 

#         tier_id = tier_name_to_id[initial_tier]
#         payment_amount = subscription_tiers[tier_id].price

#         # payment_dates = []
#         # If user has churned, stop payments at churn_date, otherwise till the end date
#         end_date = churn_date if churn_date <= params.metadata.end_date else params.metadata.end_date
#         payment_date = signup_date.astype('M8[ms]').astype(datetime)
     
#         while payment_date < end_date:
#             # payment_dates.append(payment_date)
#             payment_date += timedelta(days=30)
#             payment_dict = {idx: {"payment_date": payment_date, "user_id": user_id, "payment_amount": payment_amount}}
#             payments.update(payment_dict)
#             idx += 1
        

#     return payments


def generate_payments(params, users, subscription_tiers, tier_upgradations):
    payments = {}

    # Create a reverse lookup for subscription tier names
    tier_name_to_id = {v.name: k for k, v in subscription_tiers.items()}

    idx = 1

    for user_key, user_info in users.items():
        signup_date = user_info['signup_time']
        churn_date = user_info.get('churn_date', None)
        initial_tier = user_info.get('initial_tier', None)
        user_id = user_info['user_id'] 

        tier_id = tier_name_to_id[initial_tier]
        payment_amount = subscription_tiers[tier_id].price

        # Set end date based on churn or metadata end date
        end_date = churn_date if churn_date and churn_date <= params.metadata.end_date else params.metadata.end_date
        payment_date = signup_date.astype('M8[ms]').astype(datetime)

        # Loop through upgradations for the current user
        user_upgradations = sorted(
            [entry for entry in tier_upgradations.values() if entry['user_id'] == user_id],
            key=lambda x: x['upgradation_time']
        )

        # Keep track of the upgradation index and when to switch tiers
        next_upgrade_idx = 0
        next_upgrade_date = user_upgradations[next_upgrade_idx]['upgradation_time'] if user_upgradations else None

        while payment_date < end_date:
            # Handle the upgrade change if it falls within the payment window
            while next_upgrade_date and payment_date >= next_upgrade_date:
                upgraded_tier = user_upgradations[next_upgrade_idx]['upgraded_tier']
                tier_id = tier_name_to_id[upgraded_tier]
                payment_amount = subscription_tiers[tier_id].price  # Update payment amount based on upgraded tier

                # Move to the next upgradation if available
                next_upgrade_idx += 1
                next_upgrade_date = (
                    user_upgradations[next_upgrade_idx]['upgradation_time']
                    if next_upgrade_idx < len(user_upgradations) else None
                )

            # Increment payment date by 30 days for monthly payments
            payment_date += timedelta(days=30)

            # Store the payment details
            payments[idx] = {
                "payment_id": str(gen_rand_strs(size=1, str_len=10)[0]),
                "payment_date": payment_date,
                "user_id": user_id,
                "payment_amount": payment_amount
            }
            idx += 1

    return payments