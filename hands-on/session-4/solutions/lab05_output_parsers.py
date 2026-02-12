"""
Lab 05: Output Parsers — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

llm = ChatOllama(model="llama3.2:1b")

# StrOutputParser
print("--- StrOutputParser ---")
prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise. One sentence only."),
    ("human", "{question}"),
])
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "What is JSON?"})
print(f"Result: {result}")
print(f"Type: {type(result)}")
print()

# JsonOutputParser
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
print(f"Type: {type(result)}")
print(f"Name: {result.get('name', 'N/A')}")
print()

# PydanticOutputParser
print("--- PydanticOutputParser ---")


class BookInfo(BaseModel):
    title: str = Field(description="The book title")
    author: str = Field(description="The author's name")
    year: int = Field(description="Year of publication")
    genre: str = Field(description="The book's genre")


parser = PydanticOutputParser(pydantic_object=BookInfo)
pydantic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a book expert. Respond with accurate book information.\n{format_instructions}"),
    ("human", "Tell me about the book: {book}"),
])
pydantic_chain = pydantic_prompt | llm | parser

result = pydantic_chain.invoke({
    "book": "To Kill a Mockingbird",
    "format_instructions": parser.get_format_instructions(),
})
print(f"Title: {result.title}")
print(f"Author: {result.author}")
print(f"Year: {result.year}")
print(f"Genre: {result.genre}")
print()

# TODO 1: Movie info with JSON
print("--- Movie JSON ---")
movie_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a movie database. Always respond in valid JSON with these exact keys:
"title", "director", "year", "genre". Nothing else."""),
    ("human", "Give me info about: {movie}"),
])
movie_chain = movie_prompt | llm | JsonOutputParser()
result = movie_chain.invoke({"movie": "Inception"})
print(f"Movie: {result}")
print()

# TODO 2: Recipe with Pydantic
print("--- Recipe (Pydantic) ---")


class Recipe(BaseModel):
    name: str = Field(description="Name of the recipe")
    ingredients: str = Field(description="Main ingredients, comma-separated")
    prep_time_minutes: int = Field(description="Preparation time in minutes")
    difficulty: str = Field(description="Easy, Medium, or Hard")


recipe_parser = PydanticOutputParser(pydantic_object=Recipe)
recipe_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a chef. Provide recipe information.\n{format_instructions}"),
    ("human", "Give me a recipe for: {dish}"),
])
recipe_chain = recipe_prompt | llm | recipe_parser

try:
    result = recipe_chain.invoke({
        "dish": "pasta carbonara",
        "format_instructions": recipe_parser.get_format_instructions(),
    })
    print(f"Name: {result.name}")
    print(f"Ingredients: {result.ingredients}")
    print(f"Prep time: {result.prep_time_minutes} min")
    print(f"Difficulty: {result.difficulty}")
except Exception as e:
    print(f"Parse error: {e}")
    print("The LLM didn't return the expected format. Try again!")

print("\n" + "=" * 50)
print("Lab 05 complete!")
