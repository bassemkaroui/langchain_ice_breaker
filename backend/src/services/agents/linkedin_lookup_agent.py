from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI

from ...schemas.user import CLIUser
from ..tools import get_profile_url_tavily

# from pydantic import SecretStr


load_dotenv()


def lookup(name: str) -> str:
    template = """given this person's full name : {name_of_person}, I want you to get
    me a link to their LinkedIn profile page. Your answer should contain only a URL
    with no fancy markdown formatting."""
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)
    # llm = ChatOllama(model="llama3.1:8b", temperature=0)
    tools_for_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url_tavily,
            description="useful for when you need to get a person's Linkedin page URL",
        )
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True
    )

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    user = CLIUser()
    linkedin_url = lookup(f"{user.full_name}")
    print(linkedin_url)
