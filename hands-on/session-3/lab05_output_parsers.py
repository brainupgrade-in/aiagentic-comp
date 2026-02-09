"""
Lab 05: Output Parsers
=======================
Goal: Get structured data (JSON, Python objects) from LLM responses.

What you'll learn:
- StrOutputParser — extract plain text
- JsonOutputParser — parse JSON from the response
- PydanticOutputParser — validate into typed Python objects
- Why structured output matters for real applications
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: StrOutputParser (you already know this)
# ============================================================
# Extracts the plain text content from the AIMessage.

print("--- StrOutputParser ---")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise. One sentence only."),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "What is JSON?"})

print(f"Result: {result}")
print(f"Type: {type(result)}")  # str
print()

# ============================================================
# Step 2: JsonOutputParser — get a dictionary back
# ============================================================
# When your app needs structured data, not free text.
# The key: tell the LLM to respond in JSON format via the prompt.

print("--- JsonOutputParser ---")

json_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant.
Always respond in valid JSON format with these exact keys:
"name", "category", "description" (one sentence)."""),
    ("human", "Describe the technology: {tech}"),
])

json_chain = json_prompt | llm | JsonOutputParser()

result = json_chain.invoke({"tech": "Docker"})
print(f"Result: {result}")
print(f"Type: {type(result)}")  # dict
print(f"Name: {result.get('name', 'N/A')}")
print(f"Category: {result.get('category', 'N/A')}")
print()

# ============================================================
# Step 3: PydanticOutputParser — validated Python objects
# ============================================================
# Pydantic ensures the LLM output matches your exact schema.
# If a field is missing or wrong type, you get a clear error.

print("--- PydanticOutputParser ---")


# Define the structure you want
class BookInfo(BaseModel):
    title: str = Field(description="The book title")
    author: str = Field(description="The author's name")
    year: int = Field(description="Year of publication")
    genre: str = Field(description="The book's genre")


# Create the parser from the Pydantic model
parser = PydanticOutputParser(pydantic_object=BookInfo)

pydantic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a book expert. Respond with accurate book information.\n{format_instructions}"),
    ("human", "Tell me about the book: {book}"),
])

pydantic_chain = pydantic_prompt | llm | parser

# The parser generates format instructions automatically
result = pydantic_chain.invoke({
    "book": "To Kill a Mockingbird",
    "format_instructions": parser.get_format_instructions(),
})

print(f"Result: {result}")
print(f"Type: {type(result)}")  # BookInfo
print(f"Title: {result.title}")
print(f"Author: {result.author}")
print(f"Year: {result.year}")
print(f"Genre: {result.genre}")
print()

# ============================================================
# Step 4: See the format instructions
# ============================================================
# The parser auto-generates instructions that tell the LLM
# exactly what JSON format to produce.

print("--- Format Instructions (auto-generated) ---")
print(parser.get_format_instructions()[:300])
print("...")
print()

# ============================================================
# TODO 1: Create a JSON chain for movie info
# ============================================================
# Build a chain that takes a movie name and returns JSON with:
# "title", "director", "year", "genre"

# TODO: Build the chain using JsonOutputParser
# movie_prompt = ChatPromptTemplate.from_messages([...])
# movie_chain = movie_prompt | llm | JsonOutputParser()
# result = movie_chain.invoke({"movie": "Inception"})
# print(f"Movie: {result}")

# ============================================================
# TODO 2: Create a Pydantic model for a recipe
# ============================================================
# Define a Recipe model with: name (str), ingredients (str),
# prep_time_minutes (int), difficulty (str)
# Build a chain that returns a validated Recipe object.

# class Recipe(BaseModel):
#     name: str = Field(description="...")
#     ...
#
# recipe_parser = PydanticOutputParser(pydantic_object=Recipe)
# ...

# ============================================================
# TODO 3: Error handling — what happens with bad output?
# ============================================================
# Sometimes the LLM doesn't follow instructions perfectly.
# Wrap your chain.invoke() in a try/except to handle parse errors.

# try:
#     result = pydantic_chain.invoke({...})
# except Exception as e:
#     print(f"Parse error: {e}")
#     print("The LLM didn't return the expected format. Try again!")

print("=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- StrOutputParser → plain text (str)")
print("- JsonOutputParser → dictionary (dict)")
print("- PydanticOutputParser → validated Python object")
print("- format_instructions tell the LLM what structure to produce")
print("- Always handle potential parse errors in production code")
