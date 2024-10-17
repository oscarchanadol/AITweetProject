# Social Media Post Generator

This Streamlit application uses OpenAI's language model to generate social media posts based on user input. It's designed to create engaging content for various platforms while considering the user's mood.

This is a project for my 3rd year FunWithAI GenEd class at KMITL University

## Features

- Generate posts for Twitter, Instagram, LinkedIn, and Facebook
- Customizable topics and mood settings
- Post history tracking
- Password protection for app access
- Environment variable management for API keys

## Requirements

- Python 3.7+
- Streamlit
- OpenAI API key
- Other dependencies listed in requirements.txt

## Installation

1. Clone this repository:
   
   ```
   git clone https://github.com/oscarchanadol/AITweetProject.git
   cd AITweetProject
   ```


2. Install the required packages:
   

   `pip install -r requirements.txt`
   


3. Set up your environment variables:
   - Create a .env file in the project root
   - Add your OpenAI API key:
     

    `OPENAI_API_KEY=your_api_key_here`
     


## Usage

1. Run the Streamlit app:
   

`streamlit run app.py`
   


2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`)

3. Enter the password to access the application

4. Use the interface to:
   - Enter a topic
   - Select a social media platform
   - Adjust the mood slider
   - Generate posts
   - View post history

## Deployment

This app is configured for deployment on Streamlit Cloud. To deploy:

1. Push your code to a GitHub repository

2. Connect your GitHub account to Streamlit Cloud

3. Create a new app in Streamlit Cloud, pointing to your repository

4. Set up the following secrets in Streamlit Cloud:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `password`: The password for accessing the app

## Security Note

Ensure that your .env file and Streamlit secrets are kept secure and not shared publicly. The app uses password protection, but additional security measures may be necessary depending on your use case.

## Contributing

Contributions to improve the app are welcome. Please feel free to submit a Pull Request.

## License

MIT
