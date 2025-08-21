import json
import re
import sys
import requests
from bs4 import BeautifulSoup
from game_library import get_titles, get_title_names
import os
from dotenv import load_dotenv
from typing import Dict, Any, List, Tuple, Optional

def fetch_scores(game: str) -> Tuple[str, Any, Any]:
    # Sanitize game name for URL
    game_url_name: str = re.sub(r'[^a-z0-9\s-]', '', game.lower()).replace(' ', '-')
    print(f"Fetching scores for: {game} ({game_url_name})")
    
    headers: Dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        game_url: str = f"https://www.metacritic.com/game/{game_url_name}/"
        print(f"Attempting direct URL: {game_url}")
        
        resp: requests.Response = requests.get(game_url, headers=headers, timeout=15)
        
        game_url_name, game_url, page_soup = metacritic_search_page(game, game_url_name, game_url, headers, resp)
        
        # extract the metascore hero section
        score_section = page_soup.find('div', class_='c-productHero_scoreInfo')
        
        metascore: Any = extract_metascore(game, game_url_name, score_section)
        userscore: Any = extract_userscore(game, game_url_name, score_section)
        
        print(f"Found scores for {game}: Metascore = {metascore}, Userscore = {userscore}")
        return game_url, metascore, userscore

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching scores for {game}: {e}")
        return game_url, 'tbd', 'tbd'
    except Exception as e:
        print(f"An error occurred while processing {game}: {e}")
        return game_url, 'tbd', 'tbd'

def extract_userscore(game: str, game_url_name: str, score_section: Any) -> Any:
    user_score_section = score_section.find('div', attrs={'data-testid': 'user-score-info'})
    userscore: Any = 'tbd'
    if user_score_section:
        user_score_span = user_score_section.find('span', attrs={'data-v-e408cafe': True})
        if user_score_span:
            user_score = user_score_span.get_text(strip=True)
            if user_score != 'tbd':
                try:
                    userscore = float(user_score)
                except (ValueError, AttributeError):
                    print(f"Could not parse user score from element for {game}")
            else:
                userscore = user_score
    else:
        print(f"Could not find user score section for {game}")
        with open(f"{game_url_name}_page.html", "w", encoding="utf-8") as f:
            f.write(score_section.prettify() )
        raise Exception(f"Could not find user score section for {game}")
    return userscore

def extract_metascore(game: str, game_url_name: str, score_section: Any) -> Any:
    metascore_span = score_section.find('span', attrs={'data-v-e408cafe': True})
    metascore: Any = 'tbd'
    if metascore_span:
        try:
            metascore = metascore_span.get_text(strip=True)
            if metascore != 'tbd':
                metascore = int(metascore)
        except (ValueError, AttributeError):
            print(f"Could not parse metascore from element for {game}")
    else:
        print(f"Could not find metascore section for {game}")
        with open(f"{game_url_name}_page.html", "w", encoding="utf-8") as f:
            f.write(score_section.prettify() )
        raise Exception(f"Could not find metascore section for {game}")
    return metascore

def metacritic_search_page(
    game: str,
    game_url_name: str,
    game_url: str,
    headers: Dict[str, str],
    resp: requests.Response
) -> Tuple[str, str, BeautifulSoup]:
    if resp.status_code == 404:
        print(f"No game found for '{game}' at direct URL, trying search...")
        search_url: str = f"https://www.metacritic.com/search/{game_url_name}"
        print(f"Searching for game at: {search_url}")
        search_resp: requests.Response = requests.get(search_url, headers=headers, timeout=5)
        if search_resp.status_code != 200:
            print(f"Failed to fetch {search_url}: HTTP {resp.status_code}")
            raise Exception(f"Failed to fetch search results for {game}: HTTP {search_resp.status_code}")
        else: 
            search_page: str = search_resp.text
            search_soup_page: BeautifulSoup = BeautifulSoup(search_page, "html.parser")
            results_sections = search_soup_page.find('div', class_='c-pageSiteSearch-results')
            if results_sections:
                first_item = results_sections.find('a', class_='c-pageSiteSearch-results-item')
                if first_item:
                    game_url_name = first_item['href'].split('/')[-2]
                    print(f"Found game URL name: {game_url_name}")
                    game_url = f"https://www.metacritic.com/game/{game_url_name}"
                    print(f"Fetching game page at: {game_url}")
                    resp = requests.get(game_url, headers=headers, timeout=5)
                else:
                    print(f"No results found for {game} in search page.")
                    with open(f"{game_url_name}_search_page.html", "w", encoding="utf-8") as f:
                        f.write(results_sections.prettify() )
                    raise Exception(f"No results found for {game} in search page.")
            else:
                print(f"No results found for {game} in search page.")
                with open(f"{game_url_name}_search_page.html", "w", encoding="utf-8") as f:
                    f.write(search_soup_page.prettify() )
                raise Exception(f"No results found for {game} in search page.")
    resp.raise_for_status()
    page: str = resp.text
    page_soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    return game_url_name, game_url, page_soup

def score_exists(game: str, metacritics_scores: Any, refresh_tbd: bool = False) -> bool:
    if not metacritics_scores:
        return False
    for entry in metacritics_scores:
        result: bool = 'name' in entry and entry['name'] == game
        if refresh_tbd:
            result = result and entry['metascore_category'] is not None and entry['userscore_category'] is not None
        if result:            
            print(f"Game '{game}' already exists in metacritic_scores.")
            return True
    return False

def finalize_scores(previous_scores: Any, scores: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged_results: Dict[str, Dict[str, Any]] = {}
    result_dict: Dict[str, Dict[str, Any]] = {r['name']: r for r in scores}
    existing_scores: Dict[str, Dict[str, Any]] = {r['name']: r for r in previous_scores}
    for name, result in result_dict.items():
        if name in existing_scores:
            existing_scores[name].update(result)
            merged_results[name] = existing_scores[name]
        else:
            merged_results[name] = result
    for existing_name, existing_result in existing_scores.items():
        if existing_name not in merged_results:
            merged_results[existing_name] = existing_result
    updated_scores: List[Dict[str, Any]] = list(sorted(merged_results.values(), key=lambda x: x['name'].lower()))
    return updated_scores

def run(refresh_tbd: bool = False) -> None:
    env = os.getenv
    load_dotenv()
    PATHO: str = env('PATHO')

    games_dict: Dict[str, Any] = get_titles()
    games_count: int = len(games_dict)
    print(f"Found {games_count} games in the library.")

    previous_scores: Any
    metacritic_file_path: str = os.path.join(PATHO, "metacritic.json")
    if os.path.exists(metacritic_file_path):
        with open(metacritic_file_path, "r") as f:
            previous_scores = json.load(f)
            print(f"Loaded existing metacritic scores, found {len(previous_scores)} entries.")
    else:
        previous_scores = []

    scores: List[Dict[str, Any]] = []
    try:
        for i, game in enumerate(games_dict.keys(), start=1):
            print("--------")
            print(f"[{i}/{games_count}]")
            if score_exists(game, previous_scores, refresh_tbd):
                print(f"Skipping {game}, already processed.")
                continue

            game_url, metascore, userscore = fetch_scores(game)
            result: Dict[str, Any] = {
                "id": games_dict[game],
                "name": game,
                "url": game_url,
                "metascore": metascore,
                "userscore": userscore,
                "metascore_category": None,
                "userscore_category": None
            }

            if metascore != 'tbd' and metascore > 0:
                result.update({
                    "metascore_category": f"metascore_{(metascore // 10) * 10}s",
                })
            
            if userscore != 'tbd' and userscore > 0:    
                if userscore != 'tbd':
                    userscore_cat: int = int(userscore) * 10
                else:
                    userscore_cat = 'tbd'
                result.update({
                    "userscore_category": f"userscore_{userscore_cat}s"
                })
            
            scores.append(result)

    except Exception as e:
        print(f"Error processing game '{game}': {e}")        
        raise e
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting gracefully.")
    finally:       
        updated_scores: List[Dict[str, Any]] = finalize_scores(previous_scores, scores)
        print(f"Saving {len(updated_scores)} entries.")
        with open(metacritic_file_path, "w") as f:
            json.dump(updated_scores, f, indent=2)
        
        print("--------")
        print(f"Finished. Metacritic scores saved to {metacritic_file_path}")

def read_custom_categories() -> Any:
    env = os.getenv
    load_dotenv()
    HEROIC_CONFIG: Optional[str] = env('HEROIC_CONFIG')

    with open(HEROIC_CONFIG) as custom_categories:
        data: Any = json.load(custom_categories)
    
    with open("custom_categories.json", "w") as f:
        json.dump(data, f, indent=2)
    
    return data

def add_metacritic_categories() -> None:
    metacritic_categories: List[str] = [
        "metascore_0s", "metascore_10s", "metascore_20s", "metascore_30s", "metascore_40s", 
        "metascore_50s", "metascore_60s", "metascore_70s", "metascore_80s", "metascore_90s", "metascore_100s",
        "userscore_0s",  "userscore_10s", "userscore_20s", "userscore_30s", "userscore_40s", 
        "userscore_50s", "userscore_60s", "userscore_70s", "userscore_80s", "userscore_90s", "userscore_100s"
    ]
    
    env = os.getenv
    load_dotenv()
    HEROIC_CONFIG: str = env('HEROIC_CONFIG')
    PATHO: str = env('PATHO')
    metacritic_file_path: str = os.path.join(PATHO, "metacritic.json")

    with open(HEROIC_CONFIG) as custom_categories:
        data: Dict[str, Any] = json.load(custom_categories)
    set_data=set(data['games']['customCategories'])

    for category in metacritic_categories:
        if category not in set_data:
            data['games']['customCategories'].update({category:[]})

    with open(metacritic_file_path) as metacritic_file:
        scores: List[Dict[str, Any]] = json.load(metacritic_file)
        
    for game_score_dictionary in scores:
        metascore_category_entry = game_score_dictionary.get('metascore_category')
        userscore_category_entry = game_score_dictionary.get('userscore_category')
        if metascore_category_entry is not None:
            #print(f"Adding {game_score_dictionary['name']} to category {metascore_category_entry}")
            data['games']['customCategories'][metascore_category_entry].append(game_score_dictionary['id'])
        if userscore_category_entry is not None:
            #print(f"Adding {game_score_dictionary['name']} to category {userscore_category_entry}")
            data['games']['customCategories'][userscore_category_entry].append(game_score_dictionary['id'])

    with open(HEROIC_CONFIG, 'w') as json_file:
        json.dump(data, json_file, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    env = os.getenv
    load_dotenv()
    METACRITIC_ENABLED: bool = True if env('METACRITIC_ENABLED', default='False') == 'True' else False
    METACRITIC_REFRESH: bool = True if env('METACRITIC_REFRESH', default='False') == 'True' else False
    print(f"METACRITIC_ENABLED: {METACRITIC_ENABLED}, METACRITIC_REFRESH: {METACRITIC_REFRESH}")
    if METACRITIC_ENABLED and METACRITIC_ENABLED in [True]:
        print("Retrieving Metacritic scores...")
        run(METACRITIC_REFRESH)
        print("Adding Metacritic categories to Heroic config...")
        add_metacritic_categories()
