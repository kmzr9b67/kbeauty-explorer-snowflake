# kbeauty-explorer-snowflake

# ✨ K-Beauty Advisor

**K-Beauty Advisor** is an interactive web application that helps users build a personalized, multi-step skincare routine.

The app connects to a **Snowflake** cloud data warehouse and uses **SQLAlchemy ORM** to match products to user profiles.

## Features
- **Personalization:** Product selection based on age, skin type, and primary concerns.
- **Intelligent Search:** Advanced SQL queries using JOINs across multiple reference tables.
- **Dynamic UI:** Clean results presentation with a visual rating system (stars ⭐).
- **Performance Optimization:** Implemented Singleton pattern and connection caching.

## Tech Stack
- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend/ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database:** [Snowflake](https://www.snowflake.com/)
- **Language:** Python 3.11

## Project Structure
```text
.
├── k_beauty_app/
│   ├── database.py    
│   ├── models.py      
├── config.yaml        
├── app.py            
├── .streamlit/
│   └── secrets.toml   
└── README.md 
```      
## Local Setup (using Poetry)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/kmzr9b67/kbeauty-explorer-snowflake.git](https://github.com/kmzr9b67/kbeauty-explorer-snowflake.git)
   ```

   ```bash
   cd k-beauty-orm-manager
   ```
## How to Run the Application

This project uses **Poetry** for dependency management. To run the Streamlit dashboard, follow these steps:

   ### 1. Prerequisites
   Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed on your system.

   ### 2. Installation
   First, install all required dependencies (including Streamlit and SQLAlchemy):
   ```bash
   poetry install
   ```

   ### 3. To start the Streamlit server, use the following command:

   ```bash 
   poetry run streamlit run app.py
   ```