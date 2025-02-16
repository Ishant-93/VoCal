import sounddevice as sd
import soundfile as sf
import pyttsx3
import streamlit as st
import numpy as np
import spacy
from transformers import pipeline
import re

# Initialize Whisper Pipeline
pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")

# Initialize spaCy
nlp = spacy.load("en_core_web_sm")

class VoiceCalculator:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.all_operations = [
            "add", "plus", "sum", "edition", "addition", "adding", "summarize", "summarizing", "summation",
            "minus", "subtract", "subtraction", "difference", "takeaway",
            "multiply", "multiplication", "multiplying", "multiplied", "into", "times", "product",
            "divide", "division", "divided", "by", "quotient",
        ]

    def query_stt_api(self, filename):
        """Queries the local Whisper Speech-to-Text model."""
        try:
            transcription = pipe(filename)
            return {"text": transcription["text"]}
        except Exception as e:
            print(f"Error during local STT: {e}")
            return None

    def record_audio(self, duration=5):
        """Records audio from the microphone and saves it to a file."""
        sd.default.device = 2  # Adjust device index if needed
        device_info = sd.query_devices(sd.default.device, 'input')
        samplerate = int(device_info['default_samplerate'])
        channels = 2

        st.info(f"Recording for {duration} seconds... Speak clearly.")
        my_bar = st.progress(0)
        audio_data = []
        recording = sd.InputStream(samplerate=samplerate, channels=channels)
        recording.start()
        for i in range(duration * 10):
            chunk, overflowed = recording.read(samplerate // 10)
            audio_data.extend(chunk)
            my_bar.progress((i+1) / (duration * 10))
        recording.stop()
        recording.close()
        st.success("Recording finished.")

        audio_data = np.array(audio_data)
        if len(audio_data) > 0:
            output_filename = "recorded_audio.flac"
            sf.write(output_filename, audio_data, samplerate)
            return output_filename
        else:
            st.error("No audio recorded.")
            return None

    def calculations(self, operation, operands, document, text_input):
        """Performs calculations based on parsed operations and operands following BODMAS rule."""
        
        # Parentheses Keyword Replacement
        text_input = re.sub(r"(open parenthesis|start bracket|bracket open|parenthesis open|open bracket)", "(", text_input, flags=re.IGNORECASE)
        text_input = re.sub(r"(close parenthesis|end bracket|bracket close|parenthesis close|close bracket)", ")", text_input, flags=re.IGNORECASE)

        document = nlp(text_input)
        print(f"Processing text: {text_input}")  # Debug print

        # Parentheses Handling
        parentheses_level = 0
        start_index = -1
        end_index = -1

        for i, char in enumerate(text_input):
            if char == '(':
                if parentheses_level == 0:
                    start_index = i + 1
                parentheses_level += 1
            elif char == ')':
                parentheses_level -= 1
                if parentheses_level == 0 and start_index != -1:
                    end_index = i
                    break

        if start_index != -1 and end_index != -1:
            print(f"Found parentheses from {start_index} to {end_index}")  # Debug print
            parentheses_content = text_input[start_index:end_index].strip()
            print(f"Parentheses content: {parentheses_content}")  # Debug print
            
            # Process content inside parentheses
            parentheses_doc = nlp(parentheses_content)
            parentheses_operation = []
            parentheses_operands = []
            parentheses_result = self.calculations(parentheses_operation, parentheses_operands, parentheses_doc, parentheses_content)

            if parentheses_result is not None:
                # Replace the parentheses expression with its result
                modified_text_input = text_input[:start_index-1] + str(parentheses_result) + text_input[end_index+1:]
                print(f"Modified text after parentheses: {modified_text_input}")  # Debug print
                
                # Process the modified expression
                document = nlp(modified_text_input)
                operation = []
                operands = []
                return self.calculations(operation, operands, document, modified_text_input)

        # Extract numbers and operations
        numbers = []
        operations = []
        
        # Improved token processing
        for token in document:
            token_text = token.text.lower()
            if token_text in self.all_operations:
                operations.append(token_text)
            elif token.pos_ == "NUM" or token.text.replace('.', '').isdigit():
                try:
                    numbers.append(float(token.text))
                except ValueError:
                    st.error(f"Could not understand number: '{token.text}'")
                    return None
        
        print(f"Extracted numbers: {numbers}")  # Debug print
        print(f"Extracted operations: {operations}")  # Debug print

        if len(numbers) < 2 and len(operations) > 0:
            st.error("Not enough numbers for the operation.")
            return None
        elif len(numbers) == 1 and len(operations) == 0:
            return numbers[0]
        elif len(numbers) == 0:
            st.error("No numbers found in the expression.")
            return None

        # Process operations following BODMAS
        result = numbers[0]
        i = 0
        
        # First pass: Handle multiplication and division
        while i < len(operations):
            op = operations[i]
            if op in ["multiply", "multiplication", "multiplying", "multiplied", "into", "times", "product", 
                     "divide", "division", "divided", "by", "quotient"]:
                if i + 1 < len(numbers):
                    next_num = numbers[i + 1]
                    if op in ["multiply", "multiplication", "multiplying", "multiplied", "into", "times", "product"]:
                        result *= next_num
                    else:  # Division
                        if next_num == 0:
                            st.error("Division by zero error!")
                            return None
                        result /= next_num
                    numbers = [result] + numbers[i + 2:]
                    operations.pop(i)
                    continue
            i += 1

        # Second pass: Handle addition and subtraction
        for i, op in enumerate(operations):
            if i < len(numbers) - 1:
                if op in ["add", "plus", "sum", "edition", "addition", "adding", "summarize", "summarizing", "summation"]:
                    result += numbers[i + 1]
                elif op in ["minus", "subtract", "subtraction", "difference", "takeaway"]:
                    result -= numbers[i + 1]

        return result

    def speak_result(self, text, rate=120):
        """Speaks the given text using pyttsx3."""
        self.engine.setProperty("rate", rate)
        self.engine.say(text)
        self.engine.runAndWait()

def display_instructions():
    """Displays the usage instructions in the Streamlit interface."""
    
    # Main Operations Section
    st.header("Supported Operations and Keywords")
    
    with st.expander("1. Addition", expanded=False):
        st.markdown("""
        **Keywords:** add, plus, sum, edition, addition, adding, summarize, summarizing, summation
        
        **Examples:**
        - "What is 5 plus 3?"
        - "Add 10 and 20"
        - "Calculate the sum of 15 and 25"
        """)
    
    with st.expander("2. Subtraction", expanded=False):
        st.markdown("""
        **Keywords:** minus, subtract, subtraction, difference, takeaway
        
        **Examples:**
        - "What is 10 minus 5?"
        - "Subtract 3 from 15"
        - "Calculate the difference between 20 and 7"
        """)
    
    with st.expander("3. Multiplication", expanded=False):
        st.markdown("""
        **Keywords:** multiply, multiplication, multiplying, multiplied, into, times, product
        
        **Examples:**
        - "What is 6 times 4?"
        - "Multiply 12 by 3"
        - "Calculate the product of 5 and 8"
        """)
    
    with st.expander("4. Division", expanded=False):
        st.markdown("""
        **Keywords:** divide, division, divided, by, quotient
        
        **Examples:**
        - "What is 15 divided by 3?"
        - "Divide 20 by 4"
        - "Calculate the quotient of 100 and 5"
        """)
    
    with st.expander("5. Using Parentheses", expanded=False):
        st.markdown("""
        **Opening Keywords:** open parenthesis, start bracket, bracket open, parenthesis open
        **Closing Keywords:** close parenthesis, end bracket, bracket close, parenthesis close
        
        **Examples:**
        - "Calculate open parenthesis 10 plus 5 close parenthesis times 2"
        - "What is start bracket 20 minus 5 end bracket divided by 3"
        - "Multiply bracket open 8 plus 2 bracket close by 4"
        """)

    # Tips Section
    with st.expander("Tips for Best Results", expanded=False):
        st.markdown("""
        1. **Speak Clearly**: Enunciate your words clearly and maintain a steady pace
        2. **Use Keywords**: Stick to the supported keywords listed above for reliable operation
        3. **Complex Calculations**: For complex calculations involving parentheses, break down your speech into clear segments
        4. **Numbers**: Speak numbers clearly and naturally
        5. **Pause Timing**: Allow a brief pause after clicking the record button before speaking
        """)

def main():
    st.markdown(
        """
        <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        p {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("___VoCal___")
    st.write("Your Voice-Activated Calculator")
    
    # Add tabs for Instructions and Calculator
    tab1, tab2 = st.tabs(["Instructions", "Calculator"])
    
    with tab1:
        display_instructions()
    
    with tab2:
        voice_calculator = VoiceCalculator()
        
        st.write("Click 'Record' and speak a mathematical expression.")
        speech_rate = st.slider("Speech Rate", min_value=50, max_value=250, value=120)
        record_duration = st.slider("Recording Duration (seconds)", min_value=3, max_value=15, value=5)
        
        if st.button("Click to Record", type="primary"):
            audio_filename = voice_calculator.record_audio(duration=record_duration)
            if audio_filename:
                with st.spinner("Transcribing and Calculating..."):
                    stt_output = voice_calculator.query_stt_api(audio_filename)
                    if stt_output and 'text' in stt_output:
                        main_o = stt_output['text']
                        st.write(f"**Transcribed Text:** {main_o}")
                        doc = nlp(main_o)
                        operation = []
                        operands = []
                        result = voice_calculator.calculations(operation, operands, doc, main_o)
                        if result is not None:
                            result_str = f"{result:.2f}" if isinstance(result, float) else str(result)
                            st.success(f"**Result:** {result_str}")
                            voice_calculator.speak_result(f"The result is {result_str}", rate=speech_rate)
                        else:
                            st.error("Could not calculate the result. Please try again with a clearer expression.")
                    else:
                        st.error("Speech-to-Text failed. Please try again.")

if __name__ == "__main__":
    main()
