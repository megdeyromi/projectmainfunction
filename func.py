import io
import json
import cohere

from fdk import response

def handler(ctx, data: io.BytesIO=None):
    print("Entering Python handler", flush=True)

    # Read JSON data from the file
    try:
        with open('/path/to/projects.json', 'r') as file:  # Update the path to the JSON file
            projects = json.load(file)["projects"]
    except Exception as e:
        print(f"Failed to read JSON file: {str(e)}", flush=True)
        return response.Response(
            ctx, 
            response_data=json.dumps({"error": "Failed to read JSON file"}),
            headers={"Content-Type": "application/json"}
        )

    # Filter projects with ITD cost greater than 100
    filtered_projects = [project for project in projects if project["ITD cost"] > 100]

    # Prepare a string representation of the filtered projects
    project_descriptions = "\n\n".join(
        f"Project Name: {project['name']}\n"
        f"ITD Cost: {project['ITD cost']}\n"
        f"Status: {project['status']}\n"
        f"Owner: {project['owner']}\n"
        f"Department: {project['department']}"
        for project in filtered_projects
    )

    # Initialize Cohere client
    cohere_api_key = "TX8xfSGQm7btpYjQBrf3qYHyo7M9gAXtGrp2kJtT"  # Replace with your Cohere API key
    co = cohere.Client(cohere_api_key)

    # Use Cohere to generate insights or summaries
    try:
        cohere_response = co.generate(
            model='command-r-plus',  # Use the latest model available
            prompt=f"Show me projects whose ITD cost is more than 100:\n\n{project_descriptions}",
            max_tokens=200  # Adjust the number of tokens as needed
        )
    except Exception as e:
        print(f"Failed to generate response from Cohere: {str(e)}", flush=True)
        return response.Response(
            ctx, 
            response_data=json.dumps({"error": "Failed to generate response from Cohere"}),
            headers={"Content-Type": "application/json"}
        )

    generated_text = cohere_response.generations[0].text

    print("Generated response:\n", generated_text, flush=True)
    print("Exiting Python handler", flush=True)
    
    return response.Response(
        ctx, 
        response_data=json.dumps({"generated_response": generated_text}),
        headers={"Content-Type": "application/json"}
    )
