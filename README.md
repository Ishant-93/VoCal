# VoCal - Voice-Activated Calculator

VoCal is a voice-activated calculator built with Streamlit that allows users to perform mathematical calculations using voice commands. It supports basic arithmetic operations and parentheses, making it easy to perform both simple and complex calculations hands-free.

## Features

- Voice input for mathematical expressions
- Supports basic arithmetic operations (addition, subtraction, multiplication, division)
- Parentheses support for complex expressions
- Text-to-speech output of results
- Adjustable recording duration and speech rate
- Detailed instructions and examples
- Interactive web interface

## Supported Operations

1. **Addition**: add, plus, sum, edition, addition, adding, summarize, summarizing, summation
2. **Subtraction**: minus, subtract, subtraction, difference, takeaway
3. **Multiplication**: multiply, multiplication, multiplying, multiplied, into, times, product
4. **Division**: divide, division, divided, by, quotient
5. **Parentheses Keywords**:
   - Opening: open parenthesis, start bracket, bracket open, parenthesis open
   - Closing: close parenthesis, end bracket, bracket close, parenthesis close

## Installation

### Prerequisites

Make sure you have Python 3.8 or later installed on your system.

### System Dependencies

The application requires several system-level packages. These are listed in `packages.txt`:
```bash
portaudio19-dev
python3-all-dev
python3-setuptools
python3-wheel
python3-pip
libespeak1
espeak
alsa-utils
libasound2-dev
ffmpeg
libsndfile1
```

On Ubuntu/Debian, you can install these manually using:
```bash
sudo apt-get update
sudo apt-get install -y $(cat packages.txt)
```

### Python Dependencies

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Clone this repository:
```bash
git clone [your-repository-url]
cd vocal-calculator
```

2. Run the Streamlit application:
```bash
streamlit run vocal.py
```

3. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. Navigate to the "Calculator" tab
2. Adjust the Speech Rate and Recording Duration sliders if needed
3. Click the "Record" button
4. Speak your mathematical expression clearly
5. Wait for the result to be displayed and spoken

### Example Expressions

- "What is 5 plus 3?"
- "Multiply 12 by 3"
- "Open bracket 10 plus 8 close bracket multiply by 5"
- "What is 15 divided by 3?"

## Deployment

### Deploying to Streamlit Cloud

1. Create a Streamlit Cloud account at https://streamlit.io
2. Connect your GitHub repository
3. Deploy your app through the Streamlit Cloud interface
4. The `packages.txt` and `requirements.txt` files will automatically handle dependencies

### Local Deployment

1. Ensure all system dependencies are installed
2. Install Python dependencies
3. Run the Streamlit application

## Troubleshooting

1. **Audio Device Issues**
   - Check if your microphone is properly connected
   - Adjust the device index in `vocal.py` if needed:
     ```python
     sd.default.device = 2  # Change this number based on your system
     ```

2. **Dependencies Issues**
   - Make sure all system packages are installed
   - Check if virtual environment is activated (if using one)
   - Verify Python package versions match those in requirements.txt

## File Structure
```
vocal-calculator/
├── vocal.py            # Main application file
├── requirements.txt    # Python package dependencies
├── packages.txt       # System-level dependencies
└── README.md         # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
