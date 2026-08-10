const fs = require("fs");
const path = require("path");

function loadKnowledgeBase() {
    const filePath = path.join(
        __dirname,
        "knowledge",
        "incidents.json"
    );

    return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function analyzeIncident(description) {

    if (!description || !description.trim()) {
        return {
            status: "error",
            message: "Please provide an incident description."
        };
    }

    const knowledgeBase = loadKnowledgeBase();
    const text = description.toLowerCase();

    let bestMatch = null;
    let highestScore = 0;

    knowledgeBase.forEach(issue => {

        let score = 0;

        issue.keywords.forEach(keyword => {

            if (text.includes(keyword.toLowerCase())) {
                score++;
            }

        });

        if (score > highestScore) {
            highestScore = score;
            bestMatch = issue;
        }
    });

    if (!bestMatch) {
        return {
            status: "not_found",
            message: "No matching ITSM issue was found.",
            recommendation:
                "Collect more information such as error message, affected service, category and recent changes."
        };
    }

    return {
        status: "success",
        category: bestMatch.category,
        priority: bestMatch.priority,
        root_cause: bestMatch.root_cause,
        troubleshooting_steps: bestMatch.troubleshooting_steps,
        recommended_action: bestMatch.recommended_action
    };
}

module.exports = {
    analyzeIncident
};
