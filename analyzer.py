import json
import os


def load_knowledge_base():
    """
    Load incident troubleshooting rules from the JSON knowledge base.
    """

    file_path = os.path.join(
        os.path.dirname(__file__),
        "knowledge",
        "incidents.json"
    )

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def analyze_incident(description):
    """
    Analyze an incident description and return
    the most relevant troubleshooting recommendation.
    """

    if not description or not description.strip():
        return {
            "status": "error",
            "message": "Please provide an incident description."
        }

    description = description.lower()
    knowledge_base = load_knowledge_base()

    best_match = None
    highest_score = 0

    for issue in knowledge_base:

        score = 0

        for keyword in issue["keywords"]:
            if keyword.lower() in description:
                score += 1

        if score > highest_score:
            highest_score = score
            best_match = issue

    if best_match is None:
        return {
            "status": "not_found",
            "message": "No matching ITSM issue was found.",
            "recommendation": "Collect more information such as error message, affected service, category and recent changes."
        }

    return {
        "status": "success",
        "category": best_match["category"],
        "priority": best_match["priority"],
        "root_cause": best_match["root_cause"],
        "troubleshooting_steps": best_match["troubleshooting_steps"],
        "recommended_action": best_match["recommended_action"]
    }


if __name__ == "__main__":

    print("\nServiceNow ITSM Incident Debugger")
    print("----------------------------------")

    incident = input("Enter incident description: ")

    result = analyze_incident(incident)

    print("\nAnalysis Result")
    print("---------------")

    if result["status"] == "success":

        print(f"Category: {result['category']}")
        print(f"Priority: {result['priority']}")

        print("\nPossible Root Causes:")
        for cause in result["root_cause"]:
            print(f"- {cause}")

        print("\nTroubleshooting Steps:")
        for step in result["troubleshooting_steps"]:
            print(f"- {step}")

        print("\nRecommended Action:")
        print(result["recommended_action"])

    else:

        print(result["message"])

        if "recommendation" in result:
            print("\nRecommendation:")
            print(result["recommendation"])
