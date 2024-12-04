import requests

from ..config import Config
from ..schemas.user import CLIUser

config = Config()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"  # noqa
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_key = config.proxycurl_api_key
        # headers = {"Authorization": f"Bearer {api_key.get_secret_value()}"}
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        params = {
            "linkedin_profile_url": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            headers={"Authorization": f"Bearer {api_key.get_secret_value()}"},
        )

    data = response.json()

    # clean data to minimize tokens
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    user = CLIUser()
    print(
        scrape_linkedin_profile(
            f"https://www.linkedin.com/in/{user.full_name}", mock=True
        )
    )
