import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def convert_score_to_float(score_str):
    try:
        match = re.match(r'^\s*(\d+(\.\d+)?)/(\d+(\.\d+)?)\s*$', score_str)
        if match:
            numerator = float(match.group(1))
            denominator = float(match.group(3))
            return round(numerator / denominator, 2)
        else:
            return None
    except:
        return None

def get_reviews_for_movie(url, max_reviews=3):
    review_url = url.rstrip("/") + "/reviews"

    options = Options()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    driver.get(review_url)
    time.sleep(3)

    reviews = []

    review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.review-text-container")
    info_blocks = driver.find_elements(By.CSS_SELECTOR, "div.review-data")

    for i in range(min(len(review_blocks), len(info_blocks), max_reviews)):
        try:
            reviewer = info_blocks[i].find_element(By.CSS_SELECTOR, ".reviewer-name-and-publication").text.strip()
        except:
            reviewer = "N/A"

        try:
            raw_score = review_blocks[i].find_element(By.CSS_SELECTOR, ".original-score-and-url").text.strip()
            match = re.search(r"Original Score:\s*([^|]+)", raw_score)
            score_str = match.group(1).strip() if match else ""
        except:
            score_str = ""

        score_value = convert_score_to_float(score_str)

        # if there's not score 
        if score_value is None:
            continue

        try:
            text = review_blocks[i].find_element(By.CSS_SELECTOR, ".review-text").text.strip()
        except:
            text = "N/A"

        reviews.append({
            "movie": url.rstrip("/").split("/")[-1],
            "url": url,
            "reviewer": reviewer,
            "score": score_value,  
            "review": text
        })

    driver.quit()
    return reviews


def main():
    movie_urls = [
        "https://www.rottentomatoes.com/m/mission_impossible_the_final_reckoning",
        "https://www.rottentomatoes.com/m/lilo_and_stitch_2025",
        "https://www.rottentomatoes.com/m/friendship_2024",
        "https://www.rottentomatoes.com/m/jane_austen_wrecked_my_life",
        "https://www.rottentomatoes.com/m/the_last_rodeo",
        "https://www.rottentomatoes.com/m/the_surrender",
        "https://www.rottentomatoes.com/m/ran",
        "https://www.rottentomatoes.com/m/the_new_boy",
        "https://www.rottentomatoes.com/m/trail_of_vengeance_2025",
        "https://www.rottentomatoes.com/m/northern_lights_1982",
        "https://www.rottentomatoes.com/m/kapkapiii",
        "https://www.rottentomatoes.com/m/the_protector_2025",
        "https://www.rottentomatoes.com/m/narivetta",
        "https://www.rottentomatoes.com/m/wiz",
        "https://www.rottentomatoes.com/m/luiz_melodia_within_the_heart_of_brazil",
        "https://www.rottentomatoes.com/m/kikis_delivery_service",
        "https://www.rottentomatoes.com/m/the_metropolitan_opera_salome",
        "https://www.rottentomatoes.com/m/final_destination_bloodlines",
        "https://www.rottentomatoes.com/m/hurry_up_tomorrow",
        "https://www.rottentomatoes.com/m/deaf_president_now",
        "https://www.rottentomatoes.com/m/sister_midnight",
        "https://www.rottentomatoes.com/m/things_like_this",
        "https://www.rottentomatoes.com/m/bound_2023",
        "https://www.rottentomatoes.com/m/the_ruse",
        "https://www.rottentomatoes.com/m/the_severed_sun",
        "https://www.rottentomatoes.com/m/a_breed_apart",
        "https://www.rottentomatoes.com/m/desert_dawn",
        "https://www.rottentomatoes.com/m/here_now",
        "https://www.rottentomatoes.com/m/the_legend_of_ochi",
        "https://www.rottentomatoes.com/m/the_trouble_with_jessica",
        "https://www.rottentomatoes.com/m/a_tooth_fairy_tale",
        "https://www.rottentomatoes.com/m/stolen_time",
        "https://www.rottentomatoes.com/m/cheech_and_chongs_last_movie",
        "https://www.rottentomatoes.com/m/trail_of_vengeance_2025",
        "https://www.rottentomatoes.com/m/abbys_list_a_dogumentary",
        "https://www.rottentomatoes.com/m/warfare",
        "https://www.rottentomatoes.com/m/black_bag",
        "https://www.rottentomatoes.com/m/a_minecraft_movie",
        "https://www.rottentomatoes.com/m/disneys_snow_white",
        "https://www.rottentomatoes.com/m/drop_2025",
        "https://www.rottentomatoes.com/m/companion_2025",
        "https://www.rottentomatoes.com/m/novocaine_2025",
        "https://www.rottentomatoes.com/m/a_working_man",
        "https://www.rottentomatoes.com/m/the_brutalist",
        "https://www.rottentomatoes.com/m/final_destination",
        "https://www.rottentomatoes.com/m/the_order_2024",
        "https://www.rottentomatoes.com/m/the_ballad_of_wallis_island",
        "https://www.rottentomatoes.com/m/babygirl_2024",
        "https://www.rottentomatoes.com/m/captain_america_brave_new_world",
        "https://www.rottentomatoes.com/m/mickey_17",
        "https://www.rottentomatoes.com/m/conclave",
        "https://www.rottentomatoes.com/m/final_destination_5",
        "https://www.rottentomatoes.com/m/the_wedding_banquet",
        "https://www.rottentomatoes.com/m/the_assessment",
        "https://www.rottentomatoes.com/m/small_things_like_these",
        "https://www.rottentomatoes.com/m/heart_eyes"
    ]
        
    

    with open("../data/raw/filtered_reviews.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["movie", "url", "reviewer", "score", "review"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in movie_urls:
            print(f"Scraping: {url}")
            reviews = get_reviews_for_movie(url, max_reviews=10)
            for r in reviews:
                writer.writerow(r)
            time.sleep(1)

    print("Filtered reviews with numeric scores saved to filtered_reviews.csv")


if __name__ == "__main__":
    main()
