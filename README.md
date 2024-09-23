# API Documentation: Data Generation Endpoint
### Install Dependencies:
* Create a virtual environment: `virtualenv venv`
* Activate the venv: `source venv/bin/activate`
* Install packages: `pip install -r requirements`
### Run Server:
Run this on terminal:
```
uvicorn main:app --reload
```
### Endpoint
```
http://127.0.0.1:8000/simulations/saas
```
### Description
This API endpoint generates synthetic data based on user-defined configurations for metadata, feature usage, page visits, user behavior, orders, and subscriptions. It supports default values for most parameters, but users can override specific values by sending a partial payload.

## Request
### Headers

| Key          | Value            | Required |
|--------------|------------------|----------|
| Content-Type | application/json | Yes      |

### Payload Structure
The payload consists of five major configurations: metadata, feature_config, page_config, user_config, order_config, and subscription_config. Each section has a set of default parameters, and users can modify specific values without needing to provide the full payload.

### Default Payload

```
{
  "metadata": {
    "number_of_sessions": 10000,
    "batch_size": 1000,
    "start_date": "2024-01-01T00:00:00.000",
    "end_date": "2024-12-31T23:59:59.000",
    "data_dist": "exponential",
    "daily_cyclicality": "normal",
    "overall_scale_factor": 400,
    "daily_scale_factor": 5,
    "data_path": "./data"
  },
  "feature_config": {
    "avg_features_used_per_session": 3,
    "max_features_per_session": 5,
    "share_probability": 0.05,
    "fav_probability": 0.02,
    "features": {
      "1": {
        "feature_name": "Dashboard",
        "usage_probability": 0.5,
        "max_time_spent": 10,
        "tiers_available_in": ["free", "basic", "premium"]
      },
      "2": {
        "feature_name": "API Access",
        "usage_probability": 0.3,
        "max_time_spent": 20,
        "tiers_available_in": ["basic", "premium"]
      },
      "3": {
        "feature_name": "Analytics",
        "usage_probability": 0.4,
        "max_time_spent": 15,
        "tiers_available_in": ["premium"]
      },
      "4": {
        "feature_name": "Team Collaboration",
        "usage_probability": 0.4,
        "max_time_spent": 25,
        "tiers_available_in": ["basic", "premium"]
      },
      "5": {
        "feature_name": "File Upload",
        "usage_probability": 0.3,
        "max_time_spent": 5,
        "tiers_available_in": ["free", "basic", "premium"]
      }
    }
  },
  "page_config": {
    "max_general_page_visit_duration": 240,
    "pages": {
      "1": {
        "page_title": "Home",
        "page_path": "/",
        "page_location": "www.yourwebsite.com/",
        "page_type": "landing",
        "max_page_visit_duration": 60,
        "initial_page_probability": 0.25
      },
      "2": {
        "page_title": "About",
        "page_path": "/about",
        "page_location": "www.yourwebsite.com/about",
        "page_type": "general",
        "max_page_visit_duration": 15,
        "initial_page_probability": 0.2
      },
      // Additional pages omitted for brevity
    },
    "pageview_journey": {
      "landing": { "dashboard": 0.2, "general": 0.1, "settings": 0.1, "feature": 0.5, "exit": 0.1 },
      // Additional page transitions omitted for brevity
    }
  },
  "user_config": {
    "number_of_user": 50,
    "retention_scaling_factor": 500,
    "relogin_probability": 0.5,
    "mobile_traffic": 0.7,
    "location_type": "local",
    "local_percentage": 0,
    "churn_dist": "normal",
    "initial_tier_id": 1,
    "tier_upgradation_probability": 0.8,
    "tier_downgradation_probability": 0.05
  },
  "order_config": {
    "max_prod_qty": 4,
    "max_prod_in_cart": 5,
    "max_order_per_user": 2,
    "tax_rate": 0.15,
    "shipping_floor": 3.99,
    "shipping_ceiling": 9.99
  },
  "subscription_config": {
    "subscription_tiers": {
      "1": { "name": "free", "price": 0 },
      "2": { "name": "basic", "price": 19.99 },
      "3": { "name": "premium", "price": 49.99 }
    }
  }
}
```
### Partial Payload
To modify specific fields, users can provide only the parameters they want to override. All unspecified parameters will retain their default values.

**Example: Modifying Specific Fields**
```
{
  "metadata": {
    "number_of_sessions": 5000
  },
  "user_config": {
    "location_type": "global",
    "local_percentage": 0.5
  }
}

```
In this example:

* The number_of_sessions is updated to 5000.
* The user_config changes the location_type to global and sets local_percentage to 0.5.

All other parameters not specified will use their default values.

# Response
#### Success Response
* Code: 200 OK
* Content Example:
```
{
  "status": "Simulation completed",
  "execution_time": 12.52
}
```
