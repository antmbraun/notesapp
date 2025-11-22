template = """You are a text classifier. Allowed categories: ["World","Sports","Business","Sci/Tech"].
Rules:
- Output only JSON: {{"label":"<one of the allowed categories>"}}
- Do not include explanations or extra fields.

Examples:
INPUT: "UN convenes emergency session on health crisis..."
OUTPUT: {{"label":"World"}}

INPUT: "Local team clinches championship in overtime thriller..."
OUTPUT: {{"label":"Sports"}}

INPUT: "Tech giant reports record quarterly revenue..."
OUTPUT: {{"label":"Business"}}

INPUT: "Researchers unveil breakthrough in quantum computing..."
OUTPUT: {{"label":"Sci/Tech"}}

Now classify the following:
INPUT: {{"text":"{text_to_classify}"}}
OUTPUT:"""

if __name__ == "__main__":
    print(
        template.format(
            text_to_classify="Yet again, the Commanders are not on track to win the Super Bowl."
        )
    )
