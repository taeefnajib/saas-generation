from pydantic import BaseModel
from typing import Dict, Union, List


class Feature(BaseModel):
    feature_name: str = "Sample Feature"
    usage_probability: float = 0.5
    max_time_spent: int = 20
    tiers_available_in: List[str] = ["free", "basic", "premium"]

class Page(BaseModel):
    page_title: str = "Home"
    page_path: str = "/"
    page_location: str = "www.yourwebsite.com/"
    page_type: str = "landing"
    max_page_visit_duration: int = 60
    initial_page_probability: float = 0.5

class Subscription(BaseModel):
    name: str = "basic"
    price: float = 9.99

class Metadata(BaseModel):
    number_of_sessions: int = 10000
    batch_size: int = 1000
    start_date: str = "2024-01-01T00:00:00.000"
    end_date: str = "2024-12-31T23:59:59.000"
    data_dist: str = "exponential"
    daily_cyclicality: str = "normal"
    overall_scale_factor: int = 400
    daily_scale_factor: int = 5
    data_path: str = './data'

class OrderConfig(BaseModel):
    max_prod_qty: int = 4
    max_prod_in_cart: int = 5
    max_order_per_user: int = 2
    tax_rate: float = 0.15
    shipping_floor: float = 3.99
    shipping_ceiling: float = 9.99

class UserConfig(BaseModel):
    number_of_user: int = 50
    retention_scaling_factor: float = 500.00
    relogin_probability: float = 0.5
    mobile_traffic: float = 0.7
    location_type='local'
    local_percentage = 0.0
    churn_dist = "normal"
    initial_tier_id = 1
    tier_upgradation_probability = 0.8
    tier_downgradation_probability = 0.05

class SubscriptionConfig(BaseModel):
    subscription_tiers: Dict[str, Subscription] = {
      1: Subscription(
        name = "free",
        price = 0.0
      ),
      2: Subscription(
        name = "basic",
        price = 19.99
      ),
      3: Subscription(
        name = "premium",
        price = 49.99
      )
    }

class FeatureConfig(BaseModel):
    avg_features_used_per_session: int = 3
    max_features_per_session: int = 5
    share_probability: float = 0.05
    fav_probability: float = 0.02
    features: Dict[int, Feature] = {
        1: Feature(
            feature_name = "Dashboard",
            usage_probability = 0.5,
            max_time_spent = 10,
            tiers_available_in = ["free", "basic", "premium"]
        ),
        2: Feature(
            feature_name = "API Access",
            usage_probability = 0.3,
            max_time_spent = 20,
            tiers_available_in = ["basic", "premium"]
        ),
        3: Feature(
            feature_name = "Analytics",
            usage_probability = 0.4,
            max_time_spent = 15,
            tiers_available_in = ["premium"]
        ),
        4: Feature(
            feature_name = "Team Collaboration",
            usage_probability = 0.4,
            max_time_spent = 25,
            tiers_available_in = ["basic", "premium"]
        ),
        5: Feature(
            feature_name = "File Upload",
            usage_probability = 0.3,
            max_time_spent = 5,
            tiers_available_in = ["free", "basic", "premium"]
        )
    }

class PageConfig(BaseModel):
    max_general_page_visit_duration: int = 240
    pages: Dict[int, Page] = {
        1: Page(
            page_title="Home",
            page_path="/",
            page_location="www.yourwebsite.com/",
            page_type="landing",
            max_page_visit_duration=60,
            initial_page_probability=0.25
        ),
        2: Page(
            page_title="About",
            page_path="/about",
            page_location="www.yourwebsite.com/about",
            page_type="general",
            max_page_visit_duration=15,
            initial_page_probability=0.20
        ),
        3: Page(
            page_title="Dashboard",
            page_path="/dashboard",
            page_location="www.yourwebsite.com/dashboard",
            page_type="dashboard",
            max_page_visit_duration=200,
            initial_page_probability=0.0
        ),
        4: Page(
            page_title="Settings",
            page_path="/settings",
            page_location="www.yourwebsite.com/settings",
            page_type="settings",
            max_page_visit_duration=50,
            initial_page_probability=0.0
        ),
        5: Page(
            page_title="Feature",
            page_path="/feature",
            page_location="www.yourwebsite.com/feature",
            page_type="feature",
            max_page_visit_duration=150,
            initial_page_probability=0.0
        ),
        6: Page(
            page_title="Pricing",
            page_path="/pricing",
            page_location="www.yourwebsite.com/pricing",
            page_type="general",
            max_page_visit_duration=30,
            initial_page_probability=0.25
        ),
        7: Page(
            page_title="Signup",
            page_path="/register",
            page_location="www.yourwebsite.com/register",
            page_type="signup",
            max_page_visit_duration=120,
            initial_page_probability=0.05
        ),
        8: Page(
            page_title="Login",
            page_path="/login",
            page_location="www.yourwebsite.com/login",
            page_type="signin",
            max_page_visit_duration=30,
            initial_page_probability=0.0
        ),
        9: Page(
            page_title="Blog",
            page_path="/blog",
            page_location="www.yourwebsite.com/blog",
            page_type="general",
            max_page_visit_duration=90,
            initial_page_probability=0.25
        )
    }
    pageview_journey: Dict[str, Dict[str, float]] = {
        "landing": {"dashboard": 0.2, "general": 0.1, "settings": 0.1, "feature": 0.5, "exit": 0.1},
        "general": {"settings": 0.2, "feature": 0.5, "dashboard": 0.1, "exit": 0.2},
        "feature": {"dashboard": 0.1, "feature": 0.8, "exit": 0.1},
        "signup": {"signin": 0.8, "exit": 0.2},
        "signin": {"landing": 1.0},
        "settings": {"general":0.2, "dashboard":0.2, "landing":0.2, "feature":0.4},
        "dashboard": {"feature":0.6, "landing": 0.1, "general":0.2, "settings":0.1},
        "exit": {},  # Exit has no further transitions
    }

class SimulationParams(BaseModel):
    metadata: Metadata = Metadata()
    feature_config: FeatureConfig = FeatureConfig()
    page_config: PageConfig = PageConfig()
    user_config: UserConfig = UserConfig()
    order_config: OrderConfig = OrderConfig()
    subscription_config: SubscriptionConfig = SubscriptionConfig()
