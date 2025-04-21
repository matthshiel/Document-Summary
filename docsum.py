import requests
from urllib.parse import urlparse
import base64
import textract
from pypdf import PdfReader
import os

def is_url(input_string):
    """Check if the input string is a valid URL."""
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def llm_image(image_path=None, image_url=None):
    """
    Process an image using the LLM. Supports both local image paths and image URLs.
    """
    if not image_path and not image_url:
        raise ValueError("Either image_path or image_url must be provided.")

    if image_path:
        print("Processing local image path:", image_path)
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        image_content = f"data:image;base64,{encoded_image}"
    elif image_url:
        print("Processing image URL:", image_url)
        image_content = image_url

    try:
        print("Sending request to LLM...")
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this image: {image_content}",
                }
            ],
            model="llama3-8b-8192",
        )
        print("Received response from LLM.")
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("Error during LLM request:", e)
        return None

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF file using PyPDF2."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def llm(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {

                # Any time I'm using an LLM,
                # I always provide an instruction about how long
                # the output should be
                "role": "user",

                # Any time I'm using an LLM,
                # I always provide an instruction about how long
                # the output should be
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

def split_text(text, max_chunk_size=1000):
    '''
    Takes a string as input and returns a list of strings
    that are all smaller than max_chunk_size.

    >>> split_text('abcdefg', max_chunk_size=2)
    ['ab', 'cd', 'ef', 'g']
    >>> split_text('this is an example', max_chunk_size=3)
    ['thi', ' is', ' an', ' ex', 'amp', 'le']

    This is the simplest possible way to split text.
    Much more sophisticated possibilities.
    Other more complex algorithms will:
    1) try not to split words/sentences/paragraphs
    2) provide overlaps between the chunks
    '''
    accumulator = []
    while len(text) > 0:
        accumulator.append(text[:max_chunk_size])
        text = text[max_chunk_size:]
    return accumulator

def summarize_text(text, max_recursion_depth=5, current_depth=0):
    '''
    Our current problem: we cannot summarize large documents.
    Our solution: recursive summarization.
    Other solutions exist, no one knows what the best one is.
    We use recursive sum. because it is easy and illustrates good CS concepts.

    Two step process:
    1) Split the document into chunks that are the size of the context window.
       Summarize those chunks using the LLM.
       This gives us a sequence of smaller documents that we will append together to 
        create a new document that contains the same information as the original doc
        but is smaller.
    2) Call summarize_text on this new smaller document.
    '''
    """
    if current_depth > max_recursion_depth:
        print("Maximum recursion depth reached. Returning partial summary.")
        return text[:1000]  # Return the first 1000 characters as a fallback.
    """
    prompt = f'''
    Summarize the following text in 1-3 sentences.

    {text}
    '''
    try:
        output = llm(prompt)
        return output.split('\n')[-1]
    except groq.APIStatusError:
        chunks = split_text(text, 10000)
        print('len(chunks)=', len(chunks))
        accumulator = []

        if len(chunks) == 1:
            print("Only one chunk, returning summarized text.")
            return llm(f"Summarize the following text in 1-3 sentences:\n\n{chunks[0]}")

        for i, chunk in enumerate(chunks):
            print('i=', i)
            # Recursively summarize each chunk
            summary = summarize_text(chunk, max_recursion_depth, current_depth + 1)
            accumulator.append(summary)
        summarized_text = ' '.join(accumulator)
        summarized_text = summarize_text(summarized_text)
        # print('summarized_text=', summarized_text)
        return summarized_text

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='docsum',
        description='summarize the input document',
    )
    parser.add_argument('filename')
    args = parser.parse_args()

    from dotenv import load_dotenv
    load_dotenv()

    import os
    from groq import Groq
    import groq
    from bs4 import BeautifulSoup
    from charset_normalizer import detect

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    def read_file_with_encoding(file_path):
        """Read a file with automatic encoding detection."""
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            detected = detect(raw_data)
            encoding = detected['encoding']
            if not encoding:
                raise ValueError("Unable to detect file encoding.")
            return raw_data.decode(encoding)
        print(args.filename)

    file_path = args.filename.replace("\\", "/")  
    if is_url(args.filename) and args.filename.lower().endswith('.jpg'):
        # Handle image URL input ending with .jpg
        print("Processing image URL:", args.filename)
        text = llm_image(image_url=args.filename)

    elif is_url(args.filename):
        response = requests.get(args.filename)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, features="lxml")
        main_content = soup.find('main')
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            print("No <main> tag found in the HTML. Using entire text.")
            text = soup.get_text(separator=' ', strip=True)

    elif args.filename.lower().endswith('.pdf'):
        print(file_path)
        text = extract_text_from_pdf(file_path)
        print(text)

    elif args.filename.lower().endswith('.html'):
        print("Processing HTML file from the web:", file_path)
        with open(file_path, 'r', encoding='utf-8') as html_file:
            html = html_file.read()
        soup = BeautifulSoup(html, features="lxml")
        meta_tags = soup.find_all('meta')
        if meta_tags:
            text = ' '.join(tag.get('content', '').strip() for tag in meta_tags if tag.get('content'))
        else:
            print("No <meta> tags with 'content' attribute found in the HTML file. Using entire text.")
            text = soup.get_text(separator=' ', strip=True)

    else:
        # Handle file input with encoding detection
        text = read_file_with_encoding(file_path)

    print(summarize_text(text))