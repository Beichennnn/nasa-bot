# Azure OpenAI & NASA Horizons Tool Integration

## Overview

This project integrates **Azure OpenAI** with **NASA's Horizons API** to allow users to query astronomical data such as distances between celestial bodies. By using the **Azure OpenAI GPT-4 model**, we have enabled dynamic interactions that allow users to input natural language questions, which are then processed and responded like 10 year old to with precise data obtained from NASA's Horizons API.

## Features

- Query distances between celestial bodies like **Earth**, **Mars**, **Jupiter**, etc., on a specific date using natural language.
- Utilizes **NASA Horizons API** for precise astronomical data.
- Uses **Azure OpenAI GPT-4** to understand user questions, extract necessary parameters, and generate understandable answers as act like 10 year old.

## How It Works

1. **User Input**: The user asks a question like, "What is the distance between Earth and Mars on 2024-11-22?"
2. **Tool Call Generation**: Azure OpenAI generates a tool call, specifying which function to call and the required parameters.
3. **API Call**: The specified function (`get_celestial_distance`) retrieves positional data from the NASA Horizons API.
4. **Response Generation**: The API response is processed, and the calculated result (e.g., distance) is then used to create a meaningful response for the user.

## Requirements

- **Azure OpenAI SDK** (`openai`)
- **NumPy** for vector calculations
- **Requests** for handling API calls

## Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your Azure and NASA credentials:

   - Create a `.env` file or use environment variables to store your **Azure OpenAI** credentials (`AZURE_KEY`, `AZURE_ENDPOINT`).
   - No API key is needed for the **NASA Horizons API**.

## Running the Code

1. **Start the Python script**:

   ```
   python nasa_bot.py
   ```

2. **Interact with the assistant**:

   - Enter a question such as: "What is the distance between Jupiter and Saturn on 2024-06-15?"
   - The script will call the Horizons API, compute the distance, and return the answer in natural language.

## Example

### User Input

```
What is the distance between Earth and Mars on 2022-03-20?
```

### Output

```
The distance between Earth and Mars on 2022-03-20 is 78,340,000 km.
```

## Project Structure

- **nasa_tool.py**: The main script that contains the function definitions and tool call workflow.
- **requirements.txt**: List of required Python packages.

## Important Functions

- **get_celestial_distance(body_id, date)**: Fetches distance data for a given celestial body from the NASA Horizons API.
- **calculate_angle(pos1, pos2)**: Computes the angle between two celestial bodies using their vectors.

## Key Dependencies

- **Azure OpenAI SDK**: Used to interact with the GPT-4 model.
- **NumPy**: Required for vector and numerical calculations.
- **Requests**: Handles the HTTP requests to the NASA API.

## Troubleshooting

- **NoneType Errors**: Ensure that the API parameters are valid and that there is no mismatch in celestial body names or date formats.
- **Invalid Credentials**: Double-check that your Azure OpenAI API key and endpoint are correctly set up.
- **Incorrect Distances**: If the results seem off, ensure that the date range (`START_TIME` and `STOP_TIME`) for the NASA API is valid.

## Future Improvements

- Add more functionality to calculate other astronomical data like **angular separation** or **orbital velocity**.
- Implement a **GUI** for easier interaction.

