# dict by model Tier (Fast, Medium, High)
Model_Names = {
    "Fast": {
        "gpt": "gpt-5-nano",
        "gemini": "gemini-2.0-flash-lite"
    },
    "Medium": {
        "gpt": "gpt-5-mini",
        "gemini": "gemini-3-flash-preview"
    },
    "High": {
        "gpt": "gpt-5.2",
        "gemini": "gemini-3-pro-preview"
    }
}

# function to get the model names for a given tier
def get_model_names(tier):
    return Model_Names[tier]

def get_tier_keys():
    return list(Model_Names.keys())

