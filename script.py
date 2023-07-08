import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

from langchain.document_loaders.base import Document
from langchain.utilities import ApifyWrapper

os.environ["OPENAI_API_KEY"] = "your OpenAI API key"
os.environ["APIFY_API_TOKEN"] = "your Apify key"

# Instantiate Apify
apify = ApifyWrapper()

# Define the input for the crawler. See the "Input" section of the Website Content Crawler on https://console.apify.com/actors for configuration options.
crawl_input={"htmlTransformer": "extractus",
           "crawlerType": "cheerio",
           "startUrls": [{"url": "https://www.the-website-you-want-to-curl.com"}]
          }

loader = apify.call_actor(
    actor_id="apify/website-content-crawler",
    run_input=crawl_input,
    dataset_mapping_function=lambda item: Document(
        page_content=item["text"] or"", matadata={"source": item["url"]}
    ),
)

# Inspect the extracted docs
docs=loader.load()

docs

#need to chunk up the output here
#...

# Instantiate GPT-3.5 and define load_qa chain
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.3)
chain = load_qa_chain(chat, chain_type="stuff")

# Your main query to the language model - modify to you needs
q="""
Formulate a short 5-8 line email to the website owner pitching lead generation for his business. The email should 
make a reference to his work and give him a compliment."""

# The personalized email or paragraph you can be send
email=chain.run(input_documents=docs, question=q)
print(email)

