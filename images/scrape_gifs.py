import requests
from bs4 import BeautifulSoup
import re
import os


# Function to fetch webpage content
def fetch_page(url):
    response = requests.get(url)
    return response.text

# Function to extract GIF URLs from HTML
def extract_gif_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Find all <img> tags with src attribute containing .gif
    gif_tags = soup.find_all('img', {'src': re.compile('.gif')})
    # Extract src attribute value from each tag
    gif_urls = [tag['src'] for tag in gif_tags]
    return gif_urls

def download_gifs(urls):
    for url in urls:
        # Extract filename from URL
        filename = url.split('/')[-1]
        # Extract base filename without extension
        base_filename = os.path.splitext(filename)[0]
        # Create subfolder if it doesn't exist
        subfolder = os.path.join('.', base_filename)
        os.makedirs(subfolder, exist_ok=True)
        # If the file already exists in the subfolder, append a number to make it unique
        filepath = os.path.join(subfolder, filename)
        i = 1
        while os.path.exists(filepath):
            filepath = os.path.join(subfolder, f"{base_filename}_{i}{os.path.splitext(filename)[1]}")
            i += 1
        # Download and save the GIF
        with open(filepath, 'wb') as f:
            f.write(requests.get(url).content)
        print(f"Downloaded: {filepath}")

first_gen_pokemon = [
    "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard",
    "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree",
    "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot",
    "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok",
    "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran-f", "Nidorina",
    "Nidoqueen", "Nidoran-m", "Nidorino", "Nidoking", "Clefairy", "Clefable",
    "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat",
    "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat",
    "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck",
    "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag",
    "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop",
    "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool",
    "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash",
    "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo",
    "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder",
    "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee",
    "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute",
    "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung",
    "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela",
    "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu",
    "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar",
    "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto",
    "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte",
    "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno",
    "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo",
    "Mew"
]

# Main function
def main():
    for pokemon_name in [name.lower() for name in first_gen_pokemon]:
        url = f"https://pokemondb.net/sprites/{pokemon_name}"  # URL of the webpage containing GIFs
        html = fetch_page(url)
        gif_urls = extract_gif_urls(html)
        download_gifs(gif_urls)

if __name__ == "__main__":
    main()
