# from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from pydantic import HttpUrl

from ..integrations.linkedin import scrape_linkedin_profile
from ..integrations.twitter import scrape_user_tweets
from ..schemas.user import CLIUser
from ..utils import Summary, summary_parser
from .agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from .agents.twitter_lookup_agent import lookup as twitter_lookup_agent


def ice_break_with(name: str, mock: bool = False) -> tuple[Summary, HttpUrl]:
    linkedin_user_url = linkedin_lookup_agent(name=name)
    print(f"debug: {linkedin_user_url}")

    linkedin_data = scrape_linkedin_profile(linkedin_user_url, mock=mock)

    twitter_username = twitter_lookup_agent(name=name)
    print(f"debug: {twitter_username}")
    tweets = scrape_user_tweets(username=twitter_username, mock=mock)

    summary_template = """
    given the following LinkedIn information about a person and its tweets:
    Linkedin: {linkedin_information}
    Tweets: {twitter_posts}

    I want you to create:
    1. a short summary
    2. two interesting facts about them

    Use both information from Twitter and LinkedIn.

    {format_instructions}
    """

    # summary_prompt_template = PromptTemplate.from_template(
    #     template=summary_template, input_variables=["information"]
    # )
    summary_prompt_template = PromptTemplate(
        template=summary_template,
        input_variables=["linkedin_information", "twitter_posts"],
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)
    # llm = ChatOllama(model="llama3.2:3b", temperature=0)
    # llm = ChatOllama(model="llama3.1:8b", temperature=0)

    # chain = summary_prompt_template | llm | StrOutputParser()
    chain = summary_prompt_template | llm | summary_parser

    result: Summary = chain.invoke(
        input={"linkedin_information": linkedin_data, "twitter_posts": tweets}
    )
    return result, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":

    user = CLIUser(full_name="Eden Marco Udemy")
    result = ice_break_with(user.full_name, mock=True)
    print(result)
