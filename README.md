# Azure OpenAI & NASA Horizons Tool Integration

## Overview

This project integrates **Azure OpenAI** with **NASA's Horizons API** to allow users to query astronomical data such as distances between celestial bodies. By using the **Azure OpenAI GPT-4 model**, I have enabled dynamic interactions that allow users to input natural language questions, which are then processed and responded like 10 year old to with precise data obtained from NASA's Horizons API.

## How It Works

1. **User Input**: The user asks a question like, "What is the distance between Earth and Mars on 2024-11-22?"
2. **Tool Call Generation**: Azure OpenAI generates a tool call, specifying which function to call and the required parameters.
3. **API Call**: The specified function (`get_celestial_distance`) retrieves positional data from the NASA Horizons API.
4. **Response Generation**: The API response is processed, and the calculated result (e.g., distance) is then used to create a understandable answers as act like 10 year old for the user.

## Example

### User Input

```
What is the distance between Earth and Mars on 2024-03-20?
```

### Output

```
Wow! That's like super far! I can't even imagine walking that much, and my mom complains when I tell her school is far. That's more than 60 million kilometers. Can you even believe that? And to think my teacher told me Pluto was far away. I wonder how long it would take if we could fly there like in the movies.
```

## Project Structure

- **nasa_tool.py**: The main script that contains the function definitions and tool call workflow.
- **requirements.txt**: List of required Python packages.

## Key Dependencies

- **Azure OpenAI SDK**: Used to interact with the GPT-4 model.
- **NumPy**: Required for vector and numerical calculations.
- **Requests**: Handles the HTTP requests to the NASA API.

## Troubleshooting 

- **Invalid Credentials**: Double-check that your Azure OpenAI API key and endpoint are correctly set up.
- **Incorrect Distances**: If the results seem off, ensure that the date range (`START_TIME` and `STOP_TIME`) for the NASA API is valid.

## Future Improvements

- Add more functionality to calculate other astronomical data like **angular separation** or **orbital velocity**.
- Implement a **GUI** for easier interaction.

