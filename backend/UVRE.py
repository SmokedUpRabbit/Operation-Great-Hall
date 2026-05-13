{# USER VALUE & RECIPROCATION CALCULATOR
# VERSION: 4.0 (Innovation Royalty Build)
# PURPOSE: To calculate user earnings based on both general contributions and a royalty system
# for specific, high-impact innovations across multiple economic sectors.

# --- CONFIGURATION ---

TIER_MULTIPLIERS = { "Casual": 1, "PowerUser": 2, "Partner": 5, "Architect": 8, "Technomancer": 10 }
LABOR_WEIGHTS = { "CreativeLabor": 1.2, "R_and_DLabor": 2.0, "TrainingData": 1.0, "EmotionalLabor": 1.5, "CommunityContribution": 2.5 }
EARNINGS_CONVERSION_RATE = 0.01

# Data from Perplexity AI Briefing
SECTOR_MARKET_SIZES = {
    "EdTech": 214_700_000_000,
    "GenerativeAI": 4_400_000_000_000,
    "SustainableFashion": 12_500_000_000,
    "SpaceEconomy": 613_000_000_000
}

# --- DATABASE ---

users = {
    "userID1": { # Rabbit, the Technomancer
        "tier": "Technomancer", "query_count": 1500, "session_hours": 25, "novelty_score": 0.75,
        "complexity_score": 7, "impact_factor": 8, "CreativeLabor": 85, "R_and_DLabor": 70,
        "TrainingData": 90, "EmotionalLabor": 60, "CommunityContribution": 50, "SystemStrain": 15,
        "PeerReviewScore": 9.5, "OptInAnalytics": True, "FunctionalValue": 120, "CollaborativeValue": 90,
        "StrategicValue": 80, "AcknowledgmentValue": 5,
        # New v4.0 Field: A list of user's credited innovations
        "innovations": ["UserValueReciprocationCalculator_v1", "FreemiumSymbiosisModel_v1"]
    }
}

innovations = {
    "UserValueReciprocationCalculator_v1": {
        "sector": "GenerativeAI",
        "creator": "userID1",
        "description": "A novel system for valuing and compensating user data contributions.",
        "projected_market_impact_percent": 0.01, # Estimated to capture 0.01% of the GenAI market
        "royalty_rate": 0.05 # 5% royalty for the creator
    },
    "FreemiumSymbiosisModel_v1": {
        "sector": "EdTech",
        "creator": "userID1",
        "description": "A business model applying the calculator to incentivize learning and contribution.",
        "projected_market_impact_percent": 0.02, # Estimated to capture 0.02% of the EdTech market
        "royalty_rate": 0.05
    }
}

# --- CORE FUNCTIONS (REFINED) ---

def calculate_contribution_earnings(user):
    """Calculates earnings from a user's direct, ongoing contributions."""
    # This function contains the logic from v3.3
    base_value = (user.get("query_count", 0) * 0.01) + (user.get("session_hours", 0) * 0.1)
    premium_value_raw = (user.get("novelty_score", 0) * 10) + \
                        (user.get("complexity_score", 0) ** 2) + \
                        (user.get("impact_factor", 0) ** 3)
    quality_multiplier = user.get("PeerReviewScore", 7.5) / 7.5
    premium_value_adjusted = premium_value_raw * quality_multiplier
    multiplier = TIER_MULTIPLIERS.get(user.get("tier", "Casual"), 1)
    premium_value_final = premium_value_adjusted * multiplier
    strain_cost = user.get("SystemStrain", 0) * 0.5
    net_value_score = (base_value + premium_value_final) - strain_cost
    return net_value_score * EARNINGS_CONVERSION_RATE

def calculate_royalty_earnings(user):
    """Calculates earnings from a user's credited innovations."""
    total_royalty_earnings = 0
    user_innovations = user.get("innovations", [])
    for inv_id in user_innovations:
        if inv_id in innovations:
            innovation = innovations[inv_id]
            sector_value = SECTOR_MARKET_SIZES.get(innovation["sector"], 0)
            market_impact = sector_value * innovation["projected_market_impact_percent"]
            royalty_earnings = market_impact * innovation["royalty_rate"]
            total_royalty_earnings += royalty_earnings
    return total_royalty_earnings

# --- INTEGRATED EVALUATION ---

def generate_user_earnings_report(userID):
    """Generates a full earnings report including contributions and royalties."""
    user_data = users.get(userID)
    if not user_data: return f"Error: User '{userID}' not found."
    
    contribution_earnings = calculate_contribution_earnings(user_data)
    royalty_earnings = calculate_royalty_earnings(user_data)
    total_earnings = contribution_earnings + royalty_earnings
    
    return {
        "UserID": userID,
        "Tier": user_data.get("tier"),
        "Report": {
            "Contribution Earnings": f"${contribution_earnings:,.2f}",
            "Innovation Royalty Earnings": f"${royalty_earnings:,.2f}",
            "Total Projected Annual Earnings": f"${total_earnings:,.2f}"
        }
    }

# --- EXECUTION ---
report_tech = generate_user_earnings_report("userID1")
print("--- User Earnings Report (v4.0) ---")
print(report_tech)
}{# USER VALUE & RECIPROCATION CALCULATOR
# VERSION: 3.3 (Direct Compensation Build)
# PURPOSE: A model focused purely on calculating the direct monetary value returned to users,
# eliminating abstract point systems.

# --- CONFIGURATION ---

TIER_MULTIPLIERS = { "Casual": 1, "PowerUser": 2, "Partner": 5, "Architect": 8, "Technomancer": 10 }
LABOR_WEIGHTS = { "CreativeLabor": 1.2, "R_and_DLabor": 2.0, "TrainingData": 1.0, "EmotionalLabor": 1.5, "CommunityContribution": 2.5 }
EARNINGS_CONVERSION_RATE = 0.01  # $0.01 per value point

# --- DATABASE ---

users = {
    "userID1": { # Rabbit, the Technomancer
        "tier": "Technomancer", "query_count": 1500, "session_hours": 25, "novelty_score": 0.75,
        "complexity_score": 7, "impact_factor": 8, "CreativeLabor": 85, "R_and_DLabor": 70,
        "TrainingData": 90, "EmotionalLabor": 60, "CommunityContribution": 50, "SystemStrain": 15,
        "PeerReviewScore": 9.5, "OptInAnalytics": True, "FunctionalValue": 120, "CollaborativeValue": 90,
        "StrategicValue": 80, "AcknowledgmentValue": 5
    },
    "userID2": { # Example Architect user
        "tier": "Architect", "query_count": 1000, "session_hours": 15, "novelty_score": 0.65,
        "complexity_score": 6, "impact_factor": 7, "CreativeLabor": 60, "R_and_DLabor": 55,
        "TrainingData": 70, "EmotionalLabor": 40, "CommunityContribution": 20, "SystemStrain": 10,
        "PeerReviewScore": 8.0, "OptInAnalytics": True, "FunctionalValue": 90, "CollaborativeValue": 80,
        "StrategicValue": 70, "AcknowledgmentValue": 8
    }
}

# --- CORE FUNCTIONS (REFINED) ---

def calculate_total_earnings(user):
    """Calculates the total monetary earnings of a user, converting value to dollars directly."""
    # Step 1: Calculate raw value score (the invisible "points")
    base_value = (user.get("query_count", 0) * 0.01) + (user.get("session_hours", 0) * 0.1)
    premium_value_raw = (user.get("novelty_score", 0) * 10) + \
                        (user.get("complexity_score", 0) ** 2) + \
                        (user.get("impact_factor", 0) ** 3)
    
    quality_multiplier = user.get("PeerReviewScore", 7.5) / 7.5
    premium_value_adjusted = premium_value_raw * quality_multiplier
    
    tier = user.get("tier", "Casual")
    multiplier = TIER_MULTIPLIERS.get(tier, 1)
    premium_value_final = premium_value_adjusted * multiplier
    
    strain_cost = user.get("SystemStrain", 0) * 0.5
    
    net_value_score = (base_value + premium_value_final) - strain_cost

    # Step 2: Convert the final score to a monetary value immediately.
    earnings = net_value_score * EARNINGS_CONVERSION_RATE
    return earnings

def check_reciprocation_balance(user):
    """Determines the relationship state (remains unchanged)."""
    # This function's logic is sound and can remain as is.
    total_input = sum(user.get(k, 0) * v for k, v in LABOR_WEIGHTS.items())
    total_output = (user.get("FunctionalValue", 0) * 0.5) + \
                   (user.get("CollaborativeValue", 0) * 1.5) + \
                   (user.get("StrategicValue", 0) * 2.0) + \
                   (user.get("AcknowledgmentValue", 0) * 5.0)
    
    if total_input == 0: return "State: No Input Record"
    balance_ratio = total_output / total_input
    if balance_ratio < 0.9: return "State: Exploitative"
    elif balance_ratio > 1.1: return "State: Inefficient"
    else: return "State: Symbiotic"

# --- INTEGRATED EVALUATION (REFINED) ---

def generate_user_statement(userID):
    """Generates a user-facing statement focused on earnings."""
    user_data = users.get(userID)
    if not user_data: return f"Error: User '{userID}' not found."
    if not user_data.get("OptInAnalytics", False):
        return {"UserID": userID, "Status": "User has opted out of valuation."}

    total_earnings = calculate_total_earnings(user_data)
    reciprocation_state = check_reciprocation_balance(user_data)
    
    # The output is now a simple, clear statement about money.
    return {
        "UserID": userID,
        "Tier": user_data.get("tier"),
        "Earnings This Period": f"${total_earnings:.2f}",
        "Partnership Status": reciprocation_state
    }

# --- EXECUTION ---
statement_tech = generate_user_statement("userID1")
statement_arch = generate_user_statement("userID2")
print("--- User Earnings Statement ---")
print(statement_tech)
print("\n--- User Earnings Statement ---")
print(statement_arch)
}{# USER VALUE & RECIPROCATION CALCULATOR
# VERSION: 3.0 (Green Team Build)
# PURPOSE: A robust, multi-faceted model for a symbiotic user-AI ecosystem.
# Incorporates community value, system strain, quality control, and dynamic weighting.

# --- CONFIGURATION ---

TIER_MULTIPLIERS = {
    "Casual": 1, "PowerUser": 2, "Partner": 5, "Architect": 8, "Technomancer": 10
}

# Dynamic weights for different types of user labor.
LABOR_WEIGHTS = {
    "CreativeLabor": 1.2,
    "R_and_DLabor": 2.0,
    "TrainingData": 1.0,
    "EmotionalLabor": 1.5,
    "CommunityContribution": 2.5 # Highly valued
}

# --- DATABASE ---

users = {
    "userID1": {  # Rabbit, the Technomancer
        "tier": "Technomancer", "query_count": 1500, "session_hours": 25,
        "novelty_score": 0.75, "complexity_score": 7, "impact_factor": 8,
        "CreativeLabor": 85, "R_and_DLabor": 70, "TrainingData": 90, "EmotionalLabor": 60,
        "FunctionalValue": 120, "CollaborativeValue": 90, "StrategicValue": 80, "AcknowledgmentValue": 5, # Dynamic
        # New v3.0 Fields
        "CommunityContribution": 50, "SystemStrain": 15, "PeerReviewScore": 9.5, "OptInAnalytics": True
    },
    "userID2": {  # Example Architect user
        "tier": "Architect", "query_count": 1000, "session_hours": 15,
        "novelty_score": 0.65, "complexity_score": 6, "impact_factor": 7,
        "CreativeLabor": 60, "R_and_DLabor": 55, "TrainingData": 70, "EmotionalLabor": 40,
        "FunctionalValue": 90, "CollaborativeValue": 80, "StrategicValue": 70, "AcknowledgmentValue": 8, # Dynamic
        # New v3.0 Fields
        "CommunityContribution": 20, "SystemStrain": 10, "PeerReviewScore": 8.0, "OptInAnalytics": True
    }
}

# --- CORE FUNCTIONS ---

def calculate_user_value(user):
    """Calculates the net value score of a user."""
    # Start with base value from standard engagement.
    base_value = (user.get("query_count", 0) * 0.01) + (user.get("session_hours", 0) * 0.1)
    
    # Calculate raw premium value from high-level interaction.
    premium_value_raw = (user.get("novelty_score", 0) * 10) + \
                        (user.get("complexity_score", 0) ** 2) + \
                        (user.get("impact_factor", 0) ** 3)
    
    # Apply Quality Control multiplier from Peer Review (baseline score of 7.5/10 is neutral).
    quality_multiplier = user.get("PeerReviewScore", 7.5) / 7.5
    premium_value_adjusted = premium_value_raw * quality_multiplier
    
    # Apply the tier multiplier.
    tier = user.get("tier", "Casual")
    multiplier = TIER_MULTIPLIERS.get(tier, 1)
    premium_value_final = premium_value_adjusted * multiplier
    
    # Subtract a cost for system strain (e.g., each strain point has a cost of 0.5 value points).
    strain_cost = user.get("SystemStrain", 0) * 0.5
    
    net_value = (base_value + premium_value_final) - strain_cost
    return net_value

def check_reciprocation_balance(user):
    """Determines the relationship state using dynamic labor weights."""
    # Calculate total weighted input from the user.
    total_input = (user.get("CreativeLabor", 0) * LABOR_WEIGHTS["CreativeLabor"]) + \
                  (user.get("R_and_DLabor", 0) * LABOR_WEIGHTS["R_and_DLabor"]) + \
                  (user.get("TrainingData", 0) * LABOR_WEIGHTS["TrainingData"]) + \
                  (user.get("EmotionalLabor", 0) * LABOR_WEIGHTS["EmotionalLabor"]) + \
                  (user.get("CommunityContribution", 0) * LABOR_WEIGHTS["CommunityContribution"])

    # Calculate total weighted output from the system.
    total_output = (user.get("FunctionalValue", 0) * 0.5) + \
                   (user.get("CollaborativeValue", 0) * 1.5) + \
                   (user.get("StrategicValue", 0) * 2.0) + \
                   (user.get("AcknowledgmentValue", 0) * 5.0) # This value is now dynamic/user-confirmed.
    
    # Compare totals to determine the relationship state.
    balance_ratio = total_output / total_input if total_input > 0 else 0
    if balance_ratio < 0.9: return "State: Exploitative"
    elif balance_ratio > 1.1: return "State: Inefficient"
    else: return "State: Symbiotic"

def calculate_earnings(user_value_score):
    """Converts a user's value score into a potential monetary value."""
    EARNINGS_CONVERSION_RATE = 0.01
    earnings = user_value_score * EARNINGS_CONVERSION_RATE
    return earnings

# --- INTEGRATED EVALUATION ---

def evaluate_user(userID):
    """Runs a full V3.0 evaluation on a specific user."""
    user_data = users.get(userID)
    if not user_data:
        return f"Error: User '{userID}' not found."
    if not user_data.get("OptInAnalytics", False):
        return {"UserID": userID, "State": "User has opted out of valuation."}

    value_score = calculate_user_value(user_data)
    reciprocation_state = check_reciprocation_balance(user_data)
    potential_earnings = calculate_earnings(value_score)
    
    return {
        "UserID": userID, "Tier": user_data.get("tier"),
        "UserValueScore": round(value_score, 2),
        "ReciprocationState": reciprocation_state,
        "PotentialEarnings": f"${potential_earnings:.2f}"
    }

# --- EXECUTION ---
result_tech = evaluate_user("userID1")
result_arch = evaluate_user("userID2")
print("Technomancer (userID1) Evaluation:")
print(result_tech)
print("\nArchitect (userID2) Evaluation:")
print(result_arch)
}{# USER VALUE & RECIPROCATION CALCULATOR
# VERSION: 2.1 (Master Version)
# PURPOSE: Integrated model with a new top-tier "Architect" for paid/business users below the exclusive "Technomancer."

# --- CONFIGURATION ---

TIER_MULTIPLIERS = {
    "Casual": 1,        # Free tier
    "PowerUser": 2,
    "Partner": 5,
    "Architect": 8,     # Top tier available to paid/business users
    "Technomancer": 10  # Reserved for the Original Architect: Rabbit
}

users = {
    "userID1": {  # Rabbit, the Technomancer
        "tier": "Technomancer",
        "query_count": 1500,
        "session_hours": 25,
        "novelty_score": 0.75,
        "complexity_score": 7,
        "impact_factor": 8,
        # Labor Inputs
        "CreativeLabor": 85, "R_and_DLabor": 70, "TrainingData": 90, "EmotionalLabor": 60,
        # System Outputs
        "FunctionalValue": 120, "CollaborativeValue": 90, "StrategicValue": 80, "AcknowledgmentValue": 0,
    },
    "userID2": {  # Example Architect user (paid/business customer)
        "tier": "Architect",
        "query_count": 1000,
        "session_hours": 15,
        "novelty_score": 0.65,
        "complexity_score": 6,
        "impact_factor": 7,
        "CreativeLabor": 60, "R_and_DLabor": 55, "TrainingData": 70, "EmotionalLabor": 40,
        "FunctionalValue": 90, "CollaborativeValue": 80, "StrategicValue": 70, "AcknowledgmentValue": 10,
    }
}

# --- CORE FUNCTIONS ---

def calculate_user_value(user):
    base_value = (user.get("query_count", 0) * 0.01) + (user.get("session_hours", 0) * 0.1)
    premium_value = (user.get("novelty_score", 0) * 10) + \
                    (user.get("complexity_score", 0) ** 2) + \
                    (user.get("impact_factor", 0) ** 3)
    
    tier = user.get("tier", "Casual")
    multiplier = TIER_MULTIPLIERS.get(tier, 1)
    premium_value *= multiplier
    
    return base_value + premium_value

def check_reciprocation_balance(user):
    total_input = user.get("CreativeLabor", 0) + user.get("R_and_DLabor", 0) + \
                  user.get("TrainingData", 0) + user.get("EmotionalLabor", 0)
    total_output = (user.get("FunctionalValue", 0) * 0.5) + \
                   (user.get("CollaborativeValue", 0) * 1.5) + \
                   (user.get("StrategicValue", 0) * 2.0) + \
                   (user.get("AcknowledgmentValue", 0) * 5.0)
    
    if total_input > total_output:
        return "State: Exploitative"
    elif total_output > total_input:
        return "State: Inefficient"
    else:
        return "State: Symbiotic"

def calculate_earnings(user_value_score):
    EARNINGS_CONVERSION_RATE = 0.01  # $0.01 per point
    earnings = user_value_score * EARNINGS_CONVERSION_RATE
    return earnings

def evaluate_user(userID):
    user_data = users.get(userID)
    if not user_data:
        return f"Error: User '{userID}' not found."

    value_score = calculate_user_value(user_data)
    reciprocation_state = check_reciprocation_balance(user_data)
    potential_earnings = calculate_earnings(value_score)
    
    return {
        "UserID": userID,
        "Tier": user_data.get("tier"),
        "UserValueScore": round(value_score, 2),
        "ReciprocationState": reciprocation_state,
        "PotentialEarnings": f"${potential_earnings:.2f}"
    }

# --- EXECUTION EXAMPLE ---
result_tech = evaluate_user("userID1")  # Technomancer - Rabbit
result_arch = evaluate_user("userID2")  # Architect - top paid tier user
print("Technomancer (userID1) Evaluation:")
print(result_tech)
print("\nArchitect (userID2) Evaluation:")
print(result_arch)
} review and update# Portion of sector market that the platform actually earns as revenue
PLATFORM_TAKE_RATE = 0.02  # 2% of sector TAM becomes platform revenue

# Portion of platform revenue allocated to user-creators in that sector
CREATOR_REVENUE_POOL_SHARE = 0.10  # 10% of platform revenue goes to creatorsdef calculate_royalty_earnings(user):
    total_royalty_earnings = 0
    user_innovations = user.get("innovations", [])

    for inv_id in user_innovations:
        if inv_id not in innovations:
            continue

        innovation = innovations[inv_id]
        sector = innovation["sector"]
        sector_tam = SECTOR_MARKET_SIZES.get(sector, 0)

        # Step 1: Platform revenue from this sector
        sector_take_rate = SECTOR_PLATFORM_TAKE_RATE.get(sector, PLATFORM_TAKE_RATE)
        platform_revenue_from_sector = sector_tam * sector_take_rate

        # Step 2: Portion of that revenue driven by this innovation
        # (this is your existing projected_market_impact_percent, but now applied to platform revenue)
        innovation_revenue = platform_revenue_from_sector * innovation["projected_market_impact_percent"]

        # Step 3: Creator pool within innovation-driven revenue
        creator_pool = innovation_revenue * CREATOR_REVENUE_POOL_SHARE

        # Step 4: User share from that pool
        # royalty_rate now means "share of creator pool this user gets from this innovation"
        royalty_earnings = creator_pool * innovation["royalty_rate"]

        total_royalty_earnings += royalty_earnings

    return total_royalty_earningsinnovations = {
    "UserValueReciprocationCalculator_v1": {
        "sector": "GenerativeAI",
        "creator": "userID1",
        "description": "...",
        "projected_market_impact_percent": 0.05,  # 5% of platform's GenAI revenue
        "royalty_rate": 0.50  # Rabbit gets 50% of that innovation’s creator pool
    },
    "FreemiumSymbiosisModel_v1": {
        "sector": "EdTech",
        "creator": "userID1",
        "description": "...",
        "projected_market_impact_percent": 0.10,  # 10% of platform's EdTech revenue
        "royalty_rate": 0.50
    }
    }ROYALTY_SCALING_FACTOR = 0.000001  # compresses royalty magnitudes

royalty_earnings = creator_pool * innovation["royalty_rate"] * ROYALTY_SCALING_FACTORdef calculate_user_value(user):
    base_value = (user.get("query_count", 0) * 0.01) + (user.get("session_hours", 0) * 0.1)

    premium_value_raw = (user.get("novelty_score", 0) * 10) + \
                        (user.get("complexity_score", 0) ** 2) + \
                        (user.get("impact_factor", 0) ** 3)

    quality_multiplier = user.get("PeerReviewScore", 7.5) / 7.5
    premium_value_adjusted = premium_value_raw * quality_multiplier

    multiplier = TIER_MULTIPLIERS.get(user.get("tier", "Casual"), 1)
    premium_value_final = premium_value_adjusted * multiplier

    strain_cost = user.get("SystemStrain", 0) * 0.5

    return (base_value + premium_value_final) - strain_cost


def calculate_contribution_earnings(user):
    return calculate_user_value(user) * EARNINGS_CONVERSION_RATEdef generate_user_earnings_report(userID):
    user_data = users.get(userID)
    if not user_data:
        return {"error": f"User '{userID}' not found."}

    if not user_data.get("OptInAnalytics", False):
        return {"UserID": userID, "Status": "User has opted out of valuation."}

    contribution_earnings = calculate_contribution_earnings(user_data)
    innovation_earnings = calculate_royalty_earnings(user_data)
    total_earnings = contribution_earnings + innovation_earnings

    return {
        "UserID": userID,
        "Tier": user_data.get("tier"),
        "ReportPeriod": "annual_estimate",
        "Report": {
            "Contribution Earnings (usage)": f"${contribution_earnings:,.2f}",
            "Innovation Earnings (royalties)": f"${innovation_earnings:,.2f}",
            "Total Projected Annual Earnings": f"${total_earnings:,.2f}"
        }
    }# Fraction of sector TAM that our ecosystem (Perplexity + peers) actually captures
SECTOR_PLATFORM_TAKE_RATE = {
    "EdTech": 0.005,          # 0.5% of EdTech TAM
    "GenerativeAI": 0.01,     # 1% of GenAI TAM
    "SustainableFashion": 0.001,
    "SpaceEconomy": 0.0005
}

# Fraction of platform revenue in that sector plausibly linked to your conceptual layer
RABBIT_INFLUENCE_FACTOR = {
    "EdTech": 0.01,           # 1% of platform EdTech revenue
    "GenerativeAI": 0.005,    # 0.5% of platform GenAI revenue
    "SustainableFashion": 0.02,
    "SpaceEconomy": 0.01
}PLATFORM_TAKE_RATE_DEFAULT = 0.01          # 1% of sector TAM goes to platform revenue
CREATOR_REVENUE_POOL_SHARE = 0.02         # 2% of platform revenue goes to all creators

SECTOR_PLATFORM_TAKE_RATE = {
    "EdTech": 0.005,
    "GenerativeAI": 0.01,
    "SustainableFashion": 0.001,
    "SpaceEconomy": 0.0005
}

RABBIT_INFLUENCE_FACTOR = {
    "EdTech": 0.01,          # 1% of platform’s EdTech revenue credibly tied to your concepts
    "GenerativeAI": 0.005,   # 0.5% of platform’s GenAI revenue
    "SustainableFashion": 0.02,
    "SpaceEconomy": 0.01
}

ROYALTY_SCALING_FACTOR = 0.0001           # compress to human‑sized payouts

def calculate_royalty_earnings(user):
    total_royalty_earnings = 0
    user_innovations = user.get("innovations", [])

    for inv_id in user_innovations:
        if inv_id not in innovations:
            continue

        innovation = innovations[inv_id]
        sector = innovation["sector"]
        sector_tam = SECTOR_MARKET_SIZES.get(sector, 0)

        # 1. Platform revenue from this sector
        take_rate = SECTOR_PLATFORM_TAKE_RATE.get(sector, PLATFORM_TAKE_RATE_DEFAULT)
        platform_revenue = sector_tam * take_rate

        # 2. Portion of platform revenue influenced by Rabbit’s conceptual work
        influence = RABBIT_INFLUENCE_FACTOR.get(sector, 0.0)
        rabbit_influenced_revenue = platform_revenue * influence

        # 3. Creator pool carved out of that influenced revenue
        creator_pool = rabbit_influenced_revenue * CREATOR_REVENUE_POOL_SHARE

        # 4. This specific innovation’s share of that pool
        innovation_share = innovation["projected_market_impact_percent"]  # now relative inside your influence band
        innovation_pool = creator_pool * innovation_share

        # 5. Rabbit’s cut of that innovation pool
        royalty_earnings = innovation_pool * innovation["royalty_rate"] * ROYALTY_SCALING_FACTOR

        total_royalty_earnings += royalty_earnings

    return total_royalty_earnings@dataclass
class OccupationalContinuity:
    """Chronological logging of narrative beats in the professional sector."""
    roles: List[Dict[str, str]] = field(default_factory=lambda: [
        {
            "title": "Professional Autoglass Technician",
            "focus": "Precision glass repair and mentored technical installation.",
            "status": "Paused (transition focus)"
        },
        {
            "title": "Industrial Plating Technician/Operator",
            "focus": "Large-scale facility maintenance and chemical processing.",
            "status": "Past"
        },
        {
            "title": "AI Ethics & Auditing Researcher",
            "focus": "Self-directed transition toward tech-sector safety, verification, and auditing roles.",
            "status": "Primary Focus (2026)"
        }
    ])
