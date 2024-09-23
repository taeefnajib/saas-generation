import random
import logging
import numpy as np
from saas.utils import *
from saas.baseclass import *
from saas.constants import *
from datetime import datetime


def run_saas_batch(params: SimulationParams, original_users, features, batch_size):
    # Empty all the dictionary
    (
        users,
        pageviews,
        logins,
        new_accounts,
        social_shares,
        favorites,
        tier_upgradations, 
        visits,
        feature_consumptions
    ) = ({}, {}, {}, {}, {}, {}, {}, {}, {})
    users.update(original_users)

    session_step = 1
    starting_page_ids = list(params.page_config.pages.keys())
    starting_page_probabilities = [
        params.page_config.pages[page_id].initial_page_probability
        for page_id in starting_page_ids
    ]

    while session_step <= batch_size:
        logging.info("[[Session Started]]")
        
        # Set the date and time
        event_date_start, event_date_end = gen_random_date(
            params.metadata.start_date,
            params.metadata.end_date,
            params.metadata.data_dist,
            params.metadata.overall_scale_factor,
        )
        random_timestamp = gen_random_time(
            event_date_start,
            event_date_end,
            params.metadata.daily_cyclicality,
            params.metadata.daily_scale_factor,
        )

        is_tier_upgraded = gen_rand_categories(
                    categories=[True, False],
                    size=1,
                    p=[
                        (params.user_config.tier_upgradation_probability*2),
                        (1.0 - (params.user_config.tier_upgradation_probability*2)),
                    ],
                )
        is_tier_downgraded = gen_rand_categories(
                    categories=[True, False],
                    size=1,
                    p=[
                        (params.user_config.tier_downgradation_probability*2),
                        (1.0 - (params.user_config.tier_downgradation_probability*2)),
                    ],
                )

        event_step = 1  # Track session steps
        # # Initialize empty lists for cart products and amounts
        # cart_product = []
        # cart_amount = []
        # cart_qty = []
        # cart_id = []
        # order_per_user = 0
        starting_page_id = gen_rand_categories(
            categories=starting_page_ids, p=starting_page_probabilities
        )
        current_page_type = params.page_config.pages[starting_page_id].page_type
        selected_feature_id = ""
        has_account = gen_rand_categories(
            categories=[True, False],
            size=1,
            p=[
                params.user_config.relogin_probability,
                (1.0 - params.user_config.relogin_probability),
            ],
        )

        if has_account:
            user_ids = [
                user_id for user_id, user_data in users.items()
                if (user_data["churn_date"] > random_timestamp and user_data["activity_score"] > 0.0)
            ]
            activity_scores = []
            for _user_id in user_ids:
                activity_scores.append(users[_user_id]["activity_score"])

            total_score = sum(activity_scores)
            activity_scores = [score / total_score for score in activity_scores]
            selected_user_id = rng.choice(np.array(user_ids), size=1, p=activity_scores)[0]
  
            user_id = users[selected_user_id]["user_id"]
            current_user_id = selected_user_id

        else:
            signup_method = str(
                gen_rand_categories(
                    categories=signup_methods, size=1, p=[0.1, 0.1, 0.8]
                )
            )

            # Generate a churn date
            signup_time_np = random_timestamp.astype('datetime64[s]').astype(float)
            end_time_np = np.datetime64(params.metadata.end_date).astype(float)

            churn_duration = rng.normal(loc=(end_time_np - signup_time_np) / 2, scale=(end_time_np - signup_time_np) / 6)
            
            churn_time = random_timestamp + np.timedelta64(int(churn_duration), "s")

            new_user_id = gen_rand_strs(size=1, str_len=16)[0]
            next_key = max(users.keys()) + 1
            
            users[next_key] = {
                "signup_time": random_timestamp,
                "user_id": str(new_user_id),
                "activity_score": 0.0,  # rng.uniform(0, 0.01) if you want to add some guest purchase
                "signup_method": signup_method,
                "churn_date": churn_time
            }

            user_id = users[next_key]["user_id"]
            current_user_id = max(users.keys()) - 1

        # Convert params.metadata.end_date to np.datetime64 if it's a string
        if isinstance(params.metadata.end_date, str):
            params.metadata.end_date = np.datetime64(params.metadata.end_date)

        # Ensure users[current_user_id]['signup_time'] is a np.datetime64 object
        if isinstance(users[current_user_id]["signup_time"], str):
            users[current_user_id]["signup_time"] = np.datetime64(
                users[current_user_id]["signup_time"]
            )

        # Check and adjust signup time if needed
        if users[current_user_id]["signup_time"] >= params.metadata.end_date:
            users[current_user_id]["signup_time"] = (
                params.metadata.end_date - np.timedelta64(24, "h")
            )
        # Set the date and time after the user signup time
        if users[current_user_id]["signup_time"] > np.datetime64(params.metadata.start_date):
            event_date_start, event_date_end = gen_random_date(
                users[current_user_id]["signup_time"],
                params.metadata.end_date,
                params.metadata.data_dist,
                params.metadata.overall_scale_factor,
            )
            random_timestamp = gen_random_time(
                event_date_start,
                event_date_end,
                params.metadata.daily_cyclicality,
                params.metadata.daily_scale_factor,
            )

        device_type = rng.choice(
            np.array(device_types),
            size=1,
            p=[
                (1 - params.user_config.mobile_traffic),
                params.user_config.mobile_traffic,
            ],
        )[0]

        # Get random OS and Screen Size based on device type
        random_os = rng.choice(np.array(tech_specs[device_type]["OS"]))
        random_screen_size = rng.choice(
            np.array(tech_specs[device_type]["Screen Size"])
        )
        # Add a new visit to visits table
        kg = max(visits.keys()) + 1 if visits else 1
        visits[kg] = {
            "visit_time": str(random_timestamp),
            "user_id": str(user_id),
            "ip_address": mim.internet.ip_v4(),
            "mac_address": mim.internet.mac_address(),
            "device_type": device_type,
            "os": random_os,
            "screen_size": random_screen_size,
        }

        is_loggedin = False

        referral_pagename = "start"

        # Session starts for user
        while event_step < 20:
            # Initialize max_key when pageviews is empty or keep it outside the loop if needed
            if not pageviews:
                max_key_pageviews = 0  # or 1 depending on the starting index convention
            else:
                max_key_pageviews = max(
                    pageviews.keys()
                )  # Only calculate once if pageviews is already populated

            # login and signup checking
            if event_step > 1:
                if is_loggedin == False:
                    current_page_type = "signin" if has_account else "signup"


            # Find all page IDs of the current page type
            page_ids = find_page_ids_by_type(
                current_page_type, params.page_config.pages
            )

            # Randomly choose one page ID if there are multiple
            try:
                current_page_id = rng.choice(np.array(page_ids), size=1)[0]
                try:
                    max_specific_page_visit_duration = params.page_config.pages[
                        current_page_id
                    ].max_page_visit_duration
                    page_visit_duration = rng.integers(
                        1, max_specific_page_visit_duration
                    )
                except KeyError:
                    # In case page_activity or current_page_id doesn't exist
                    page_visit_duration = rng.integers(
                        1, params.page_config.max_general_page_visit_duration
                    )
                
            except:
                page_visit_duration = rng.integers(
                    1, params.page_config.max_general_page_visit_duration
                )
                logging.info("User exited the journey.")


            if current_page_type == "feature":  # On "ProductDetails" page

                # Get the current user's subscription tier as a string
                try:
                    current_tier = str(users[current_user_id]["subscription_tier"])
                except:
                    break


                # Filter feature_ids based on tiers_available_in
                available_feature_ids = [
                    feature_id for feature_id in params.feature_config.features.keys()
                    if current_tier in params.feature_config.features[feature_id].tiers_available_in
                ]

                # If no features are available for the current tier, skip further logic
                if not available_feature_ids:
                    print(f"No available features for subscription tier: {current_tier}")
                    return

                # Extract the feature ids and their corresponding popularity scores for the available features
                feature_popularity_scores = [
                    params.feature_config.features[feature_id].usage_probability
                    for feature_id in available_feature_ids
                ]

                # Normalize the feature popularity scores to make sure they sum up to 1
                total_score = sum(feature_popularity_scores)
                feature_popularity_scores = [
                    score / total_score for score in feature_popularity_scores
                ]

                # Randomly select a feature ID based on popularity scores
                selected_feature_id = rng.choice(
                    np.array(available_feature_ids), size=1, p=feature_popularity_scores
                )[0]

                # Add the selected feature's max_time_spent to page_visit_duration
                # feature_consumption_time = np.random.random_integers(1, params.feature_config.features[selected_feature_id].max_time_spent)
                max_time = params.feature_config.features[selected_feature_id].max_time_spent
                feature_consumption_time = int(np.random.beta(5, 2) * (max_time - 1)) + 1
                page_visit_duration += feature_consumption_time

                # Add a new feature consumption to feature_consumptions table
                ks= max(feature_consumptions.keys()) + 1 if feature_consumptions else 1
                feature_consumptions[ks] = {
                    "consumption_timestamp": random_timestamp,
                    "user_id": str(user_id),
                    "feature_id": selected_feature_id,
                    "feature_name": str(params.feature_config.features[selected_feature_id].feature_name),
                    "consumption_time": str(feature_consumption_time)
                }

                # Populate share table
                is_shared = gen_rand_categories(
                    categories=[True, False],
                    size=1,
                    p=[
                        params.feature_config.share_probability,
                        (1 - params.feature_config.share_probability),
                    ],
                )
                if is_shared:
                    l = max(social_shares.keys()) + 1 if social_shares else 1
                    social_shares[l] = {
                        "share_time": str(random_timestamp),
                        "user_id": user_id,
                        "share_method": gen_rand_categories(
                            categories=social_share_platforms, size=1
                        ),
                        "content_type": "feature",
                        "feature_name": params.feature_config.features[selected_feature_id].feature_name,
                    }

                # Populate favorite table
                is_fav = gen_rand_categories(
                    categories=[True, False],
                    size=1,
                    p=[
                        params.feature_config.fav_probability,
                        (1 - params.feature_config.fav_probability),
                    ],
                )
                if is_fav:
                    l = max(favorites.keys()) + 1 if favorites else 1
                    favorites[l] = {
                        "fav_time": str(random_timestamp),
                        "user_id": user_id,
                        "feature_name": params.feature_config.features[selected_feature_id].feature_name,
                    }
                    

                
            if current_page_type == "signin":
                # This will populate login table
                login_time = str(random_timestamp)  # Record the login time

                is_loggedin = True
                logging.info(f"User '{user_id}' logged in at {login_time}")

                # Record the login in the logins dictionary
                j = max(logins.keys()) + 1 if logins else 1
                logins[j] = {"login_time": login_time, "user_id": str(user_id)}
                j += 1

            if current_page_type == "signup":
                # This will populate the users table
                # Add a new account to new_account table
                if not has_account:
                    user_location = generate_location(
                        location_type=params.user_config.location_type,
                        local_percentage=params.user_config.local_percentage,
                    )
                    k = max(new_accounts.keys()) + 1 if new_accounts else 1

                    # Retrieve country-specific information
                    country_info = country_codes[user_location["Country"]]

                    # Select a random language if multiple languages are available
                    language_choice = random.choice(
                        list(country_info["language"].values())
                    )

                    signup_time = random_timestamp
                    end_time = params.metadata.end_date

                    # Assign a random subscription tier from 'subscription_tiers'
                    subscription_tier_id = params.user_config.initial_tier_id

                    # Generate a churn date
                    signup_time_np = signup_time.astype('datetime64[s]').astype(float)
                    end_time_np = end_time.astype('datetime64[s]').astype(float)

                    if params.user_config.churn_dist == "normal":
                        time_difference = end_time_np - signup_time_np
                        if time_difference < 0:
                            time_difference = 0
                        scale = max(time_difference / 6, 1) 
                        churn_duration = rng.normal(loc=(time_difference) / 2, scale=scale)
                    elif params.user_config.churn_dist == "left_skewed":
                        churn_duration = rng.gamma(shape=2, scale=(end_time_np - signup_time_np) / 2)
                    elif params.user_config.churn_dist == "right_skewed":
                        churn_duration = rng.beta(a=2, b=5) * (end_time_np - signup_time_np)
                    else:  # uniform distribution
                        churn_duration = rng.uniform(0, end_time_np - signup_time_np)

                    churn_time = signup_time + np.timedelta64(int(churn_duration), "s")

                    new_accounts[k] = {
                        "signup_time": random_timestamp,
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
                        "initial_tier": str(params.subscription_config.subscription_tiers[int(subscription_tier_id)].name),
                        "subscription_tier": str(params.subscription_config.subscription_tiers[subscription_tier_id].name),
                        "churn_date": churn_time
                    }

                    users[next_key] = new_accounts[k]
                    # current_number_of_new_users += 1
                    # logging.info(f"Newly created user id: {user_id}")
                    has_account = True

                else:
                    current_page_type = "signin"
                    continue

            if current_page_type == "exit":  # Exit condition
                logging.info("[[Session Ends]]")
                break

            if current_page_type != "exit":
                # This will populate pageviews table
                # Enter order data to orders
                # When adding new data to pageviews
                max_key_pageviews += 1  # Increment max_key instead of recalculating
                pageviews[max_key_pageviews] = {
                    "pageview_time": str(random_timestamp),
                    "user_id": str(user_id),
                    "page_type": str(current_page_type),
                    "pageview_duration": str(page_visit_duration),
                    "page_name": params.page_config.pages[current_page_id].page_title,
                    "page_location": (
                        params.page_config.pages[current_page_id].page_location
                        if selected_feature_id == ""
                        else params.page_config.pages[current_page_id].page_location
                        + "/"
                        + str(selected_feature_id)
                    ),
                    "page_path": (
                        params.page_config.pages[current_page_id].page_path
                        if selected_feature_id == ""
                        else params.page_config.pages[current_page_id].page_path
                        + "/"
                        + str(selected_feature_id)
                    ),
                    "referral_pagename": referral_pagename,
                }
                # current_number_of_pageviews += 1
                referral_pagename = params.page_config.pages[current_page_id].page_title

                previous_tier = users[current_user_id]["subscription_tier"]

                previous_tier_id = None
                for tier_id, subscription in params.subscription_config.subscription_tiers.items():
                    if subscription.name == previous_tier:
                        previous_tier_id = tier_id
                        break

                if previous_tier_id is None:
                    raise ValueError(f"Subscription tier '{previous_tier}' not found in the subscription tiers configuration.")
                

                if is_tier_upgraded:
            
                    # Check if there is a higher tier available
                    current_tier_id = previous_tier_id
                    max_tier_id = max(params.subscription_config.subscription_tiers.keys())
                 
                    # Check if user_id exists in tier_upgradations
                    user_upgradations = [entry for entry in tier_upgradations.values() if entry['user_id'] == str(user_id)]
                   
                    # user_upgradations = [entry for entry in tier_upgradations.values() if entry['user_id'] == str(user_id)]
                    # Get the maximum upgradation_time for the user_id, if upgradations exist
                    if user_upgradations:
                        max_previous_upgradation_time = max(entry['upgradation_time'] for entry in user_upgradations)
                    else:
                        max_previous_upgradation_time = None

                    # # Proceed with upgrade only if current tier is not max and if no previous upgradations exist
                    # # or the last upgradation_time is less than the current random_timestamp
                    # Get the maximum upgradation_time for the user_id, if upgradations exist
                    if user_upgradations:
                        max_previous_upgradation_time = max(entry['upgradation_time'] for entry in user_upgradations)
                    else:
                        max_previous_upgradation_time = None

                    # Convert random_timestamp and max_previous_upgradation_time to datetime objects for comparison
                    random_timestamp_dt = datetime.fromisoformat(str(random_timestamp))

                    if max_previous_upgradation_time:
                        max_previous_upgradation_time_dt = datetime.fromisoformat(str(max_previous_upgradation_time))
                    else:
                        max_previous_upgradation_time_dt = None

                    # Proceed with upgrade only if current tier is not max and if no previous upgradations exist
                    # or the date of random_timestamp is greater than the date of max_previous_upgradation_time
                    if (current_tier_id < max_tier_id) and (
                        max_previous_upgradation_time_dt is None or random_timestamp_dt.date() > max_previous_upgradation_time_dt.date()
                    ):
                        high_range = max_tier_id-current_tier_id
                        if high_range <= 1:
                            random_upgradation_step = 1
                        else:
                            random_upgradation_step = rng.integers(1,(max_tier_id-current_tier_id))
                        # Upgrade to the next tier
                        upgraded_tier_id = current_tier_id + random_upgradation_step
                        upgraded_tier = str(params.subscription_config.subscription_tiers[upgraded_tier_id].name)
                        users[current_user_id]["subscription_tier"] = upgraded_tier
                        kg = max(tier_upgradations.keys()) + 1 if tier_upgradations.keys() else 1
                        tier_upgradations[kg] = {
                            "upgradation_time": random_timestamp,
                            "user_id": users[current_user_id]['user_id'],
                            "previous_tier": previous_tier,
                            "upgraded_tier": upgraded_tier,
                        }
                        # print(f"User: {users[current_user_id]['user_id']}, Previous Tier: {previous_tier}, Upgraded Tier: {upgraded_tier}")
                        is_tier_upgraded = False
                else:
                    if is_tier_downgraded:
                        # Check if there is a lower tier available
                        current_tier_id = previous_tier_id
                        min_tier_id = min(params.subscription_config.subscription_tiers.keys())
                        
                        # Check if user_id exists in tier_upgradations
                        user_upgradations = [entry for entry in tier_upgradations.values() if entry['user_id'] == str(user_id)]
                        
                        # Get the maximum upgradation_time for the user_id, if upgradations exist
                        if user_upgradations:
                            max_previous_upgradation_time = max(entry['upgradation_time'] for entry in user_upgradations)
                        else:
                            max_previous_upgradation_time = None

                        # Convert random_timestamp and max_previous_upgradation_time to datetime objects for comparison
                        random_timestamp_dt = datetime.fromisoformat(str(random_timestamp))

                        if max_previous_upgradation_time:
                            max_previous_upgradation_time_dt = datetime.fromisoformat(str(max_previous_upgradation_time))
                        else:
                            max_previous_upgradation_time_dt = None

                        # Proceed with downgrade only if current tier is not min and if no previous upgradations exist
                        # or the date of random_timestamp is greater than the date of max_previous_upgradation_time
                        if (current_tier_id > min_tier_id) and (
                            max_previous_upgradation_time_dt is None or random_timestamp_dt.date() > max_previous_upgradation_time_dt.date()
                        ):
                            high_range = current_tier_id-min_tier_id
                            if high_range <= 1:
                                random_downgradation_step = 1
                            else:
                                random_downgradation_step = rng.integers(1,high_range)
                            # Downgrade to the previous tier
                            upgraded_tier_id = current_tier_id - random_downgradation_step
                            upgraded_tier = str(params.subscription_config.subscription_tiers[upgraded_tier_id].name)
                            users[current_user_id]["subscription_tier"] = upgraded_tier

                            # Add the downgrade to tier_upgradations
                            kg = max(tier_upgradations.keys()) + 1 if tier_upgradations.keys() else 1
                            tier_upgradations[kg] = {
                                "upgradation_time": random_timestamp,
                                "user_id": users[current_user_id]['user_id'],
                                "previous_tier": previous_tier,
                                "upgraded_tier": upgraded_tier,
                            }

                            is_tier_downgraded = False
                        
            else:  # Exit condition
                logging.info("[[Session Ends]]")
                break

            selected_feature_id = ""

            # Add the page visit duration to the event time
            random_timestamp += np.timedelta64(page_visit_duration, "s")

            next_page_choices = list(
                params.page_config.pageview_journey[current_page_type].keys()
            )
            next_page_probabilities = list(
                params.page_config.pageview_journey[current_page_type].values()
            )
            current_page_type = rng.choice(
                np.array(next_page_choices), size=1, p=next_page_probabilities
            )[0]

            event_step += 1

        session_step += 1
    
      

    return (
        pageviews,
        logins,
        new_accounts,
        social_shares,
        favorites,
        visits,
        users,
        features,
        tier_upgradations,
        feature_consumptions
    )
