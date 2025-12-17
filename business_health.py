# business_health.py

def get_update_suggestions(business: dict):
    suggestions = []

    if not business.get("website"):
        suggestions.append("Add a website to improve trust")

    if not business.get("phone_number"):
        suggestions.append("Add a phone number so customers can contact you")

    if not business.get("address"):
        suggestions.append("Add a complete address")

    if business.get("reviews_count", 0) < 5:
        suggestions.append("Get more reviews to rank higher")

    if business.get("reviews_average", 0) < 4:
        suggestions.append("Improve service quality to increase rating")

    if not business.get("subcategory"):
        suggestions.append("Add a subcategory for better visibility")

    return suggestions
if __name__ == "__main__":
    sample_business = {
        "name": "Sample Cafe",
        "address": "123 Main St",
        "phone_number": "",
        "website": "",
        "reviews_count": 3,
        "reviews_average": 3.5,
        "category": "Cafe",
        "subcategory": ""
    }

    suggestions = get_update_suggestions(sample_business)
    print("Update Suggestions:")
    for s in suggestions:
        print(f"- {s}")