from models.question import QuestionCreate
from typing import List

def get_seed_questions() -> List[QuestionCreate]:
    """Get initial questions to seed the database"""
    return [
        # Level 1 - Music Questions
        QuestionCreate(
            question="Which band recorded 'Sweet Child O' Mine' in 1987?",
            options=["Guns N' Roses", "Bon Jovi", "Def Leppard", "Motley Crue"],
            correctAnswer=0,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="What was Madonna's first top 10 hit in the US?",
            options=["Like a Virgin", "Borderline", "Holiday", "Material Girl"],
            correctAnswer=1,
            difficulty="hard",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Who sang 'Take On Me'?",
            options=["Duran Duran", "A-ha", "New Order", "Depeche Mode"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which Prince album was released in 1984?",
            options=["1999", "Purple Rain", "Sign O' the Times", "Around the World in a Day"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Who sang 'Girls Just Want to Have Fun'?",
            options=["Pat Benatar", "Cyndi Lauper", "Blondie", "Joan Jett"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which band released 'Don't Stop Believin'' in 1981?",
            options=["Journey", "Foreigner", "REO Speedwagon", "Styx"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="What was Michael Jackson's best-selling album of the 80s?",
            options=["Off the Wall", "Thriller", "Bad", "Dangerous"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which duo sang 'Wake Me Up Before You Go-Go'?",
            options=["Wham!", "Tears for Fears", "Hall & Oates", "Pet Shop Boys"],
            correctAnswer=0,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="What instrument did Phil Collins play before becoming a lead singer?",
            options=["Guitar", "Keyboard", "Drums", "Bass"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which band performed 'Pour Some Sugar on Me'?",
            options=["Def Leppard", "Van Halen", "Whitesnake", "Poison"],
            correctAnswer=0,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Who sang 'Everybody Wants to Rule the World'?",
            options=["Duran Duran", "Tears for Fears", "The Human League", "Spandau Ballet"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which artist released 'Like a Prayer' in 1989?",
            options=["Madonna", "Whitney Houston", "Janet Jackson", "Cyndi Lauper"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="What was Bon Jovi's biggest hit of the 80s?",
            options=["Runaway", "Livin' on a Prayer", "You Give Love a Bad Name", "Wanted Dead or Alive"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Which band sang 'Come on Eileen'?",
            options=["Dexys Midnight Runners", "The Specials", "Madness", "The Beat"],
            correctAnswer=0,
            difficulty="hard",
            level=1,
            category="music"
        ),
        QuestionCreate(
            question="Who performed 'Total Eclipse of the Heart'?",
            options=["Pat Benatar", "Bonnie Tyler", "Heart", "Joan Jett"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="music"
        ),

        # Level 1 - Movies Questions
        QuestionCreate(
            question="Who directed 'Back to the Future' (1985)?",
            options=["Steven Spielberg", "Robert Zemeckis", "John Hughes", "George Lucas"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="In 'The Breakfast Club', how many students are in detention?",
            options=["4", "5", "6", "7"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which 1982 film featured the line 'E.T. phone home'?",
            options=["E.T. the Extra-Terrestrial", "Close Encounters", "Alien", "Blade Runner"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Who played the main character in 'Ferris Bueller's Day Off'?",
            options=["Matthew Broderick", "Anthony Michael Hall", "Emilio Estevez", "Andrew McCarthy"],
            correctAnswer=0,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which movie featured the song 'Eye of the Tiger'?",
            options=["Rocky III", "Top Gun", "Flashdance", "Footloose"],
            correctAnswer=0,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Who played the Terminator in the 1984 film?",
            options=["Sylvester Stallone", "Arnold Schwarzenegger", "Kurt Russell", "Bruce Willis"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="What was the highest-grossing film of 1982?",
            options=["E.T. the Extra-Terrestrial", "Tootsie", "Rocky III", "An Officer and a Gentleman"],
            correctAnswer=0,
            difficulty="hard",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which actor starred in 'Top Gun' (1986)?",
            options=["Tom Cruise", "Patrick Swayze", "Charlie Sheen", "Kevin Costner"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Who directed 'The Shining' (1980)?",
            options=["John Carpenter", "Stanley Kubrick", "David Lynch", "George A. Romero"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which film features the quote 'Nobody puts Baby in a corner'?",
            options=["Flashdance", "Footloose", "Dirty Dancing", "Fame"],
            correctAnswer=2,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="What year was 'Blade Runner' released?",
            options=["1981", "1982", "1983", "1984"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Who played Indiana Jones in 'Raiders of the Lost Ark'?",
            options=["Harrison Ford", "Tom Selleck", "Kurt Russell", "Michael Douglas"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which John Hughes film was released in 1985?",
            options=["Sixteen Candles", "The Breakfast Club", "Ferris Bueller's Day Off", "Pretty in Pink"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="What was the sequel to 'Alien' called?",
            options=["Alien II", "Aliens", "Alien: The Return", "Alien: Resurrection"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="movies"
        ),
        QuestionCreate(
            question="Which 1984 film starred Bill Murray as a paranormal investigator?",
            options=["Stripes", "Ghostbusters", "Scrooged", "Little Shop of Horrors"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="movies"
        ),

        # Level 1 - Fashion Questions
        QuestionCreate(
            question="What hairstyle was popular in the 80s, especially among women?",
            options=["Bob cut", "Big hair/Volume", "Pixie cut", "Straight hair"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What type of jeans were trendy in the 80s?",
            options=["Skinny jeans", "Acid-washed jeans", "Straight leg", "Bootcut"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which accessory was commonly worn by both men and women?",
            options=["Chokers", "Headbands", "Scrunchies", "All of the above"],
            correctAnswer=3,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What makeup trend was popular in the 80s?",
            options=["Natural look", "Bold, colorful eyeshadow", "Minimal makeup", "Matte lipstick"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What type of shoulder padding was fashionable in women's clothing?",
            options=["Small shoulder pads", "Huge shoulder pads", "No shoulder pads", "Rounded shoulder pads"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which footwear became a major trend in the 80s?",
            options=["High-top sneakers", "Ballet flats", "Combat boots", "Loafers"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What was a popular men's hairstyle in the 80s?",
            options=["Buzz cut", "Mullet", "Crew cut", "Side part"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which pattern was extremely popular on clothing in the 80s?",
            options=["Polka dots", "Stripes", "Neon colors and geometric patterns", "Floral prints"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What type of jewelry was trendy in the 80s?",
            options=["Delicate gold chains", "Chunky, statement jewelry", "Minimalist pieces", "Vintage brooches"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What type of jackets were trendy for both men and women?",
            options=["Leather jackets", "Denim jackets", "Bomber jackets", "All of the above"],
            correctAnswer=3,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which hair accessory was extremely popular among women?",
            options=["Hair clips", "Scrunchies", "Headbands", "Hair ribbons"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What was the popular trend for exercise wear?",
            options=["All black outfits", "Neon-colored spandex and leotards", "Loose-fitting clothes", "Cotton t-shirts"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which sunglasses style was iconic in the 80s?",
            options=["Aviators", "Cat-eye", "Oversized frames", "Round glasses"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="What brand popularized athletic wear as fashion?",
            options=["Nike", "Adidas", "Both Nike and Adidas", "Puma"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="fashion"
        ),
        QuestionCreate(
            question="Which material was popular for pants in the 80s?",
            options=["Cotton", "Spandex/Lycra", "Wool", "Linen"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="fashion"
        ),

        # Level 1 - General Questions
        QuestionCreate(
            question="Which gaming console was released by Nintendo in 1985?",
            options=["Game Boy", "NES", "Super Nintendo", "Nintendo 64"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What was the most popular dance of the 80s?",
            options=["The Robot", "Moonwalk", "Electric Slide", "All of the above"],
            correctAnswer=3,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which president served most of the 1980s?",
            options=["Jimmy Carter", "Ronald Reagan", "George H.W. Bush", "Gerald Ford"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="MTV launched in what year?",
            options=["1980", "1981", "1982", "1983"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which event happened in 1989?",
            options=["Chernobyl disaster", "Berlin Wall fell", "Live Aid concert", "Challenger explosion"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What was the first music video played on MTV?",
            options=["Video Killed the Radio Star", "Money for Nothing", "Girls Just Want to Have Fun", "Take On Me"],
            correctAnswer=0,
            difficulty="hard",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which home computer was popular in the early 80s?",
            options=["Apple II", "Commodore 64", "IBM PC", "All of the above"],
            correctAnswer=3,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What was the name of the U.S. space program in the 80s?",
            options=["Apollo", "Mercury", "Space Shuttle", "Gemini"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which arcade game was released in 1980?",
            options=["Pac-Man", "Donkey Kong", "Frogger", "Centipede"],
            correctAnswer=0,
            difficulty="easy",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What major nuclear accident occurred in 1986?",
            options=["Three Mile Island", "Fukushima", "Chernobyl", "Windscale"],
            correctAnswer=2,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which toy became extremely popular in the mid-80s?",
            options=["Cabbage Patch Kids", "Transformers", "My Little Pony", "All of the above"],
            correctAnswer=3,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which technology was introduced to consumers in the 80s?",
            options=["VHS", "CD players", "Personal computers", "All of the above"],
            correctAnswer=3,
            difficulty="easy",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What was the popular TV show 'Dallas' famous for?",
            options=["A cooking show", "A soap opera", "A game show", "A news program"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="Which fast food chain introduced the Happy Meal in 1979?",
            options=["Burger King", "McDonald's", "Wendy's", "KFC"],
            correctAnswer=1,
            difficulty="easy",
            level=1,
            category="general"
        ),
        QuestionCreate(
            question="What was CNN's launch year?",
            options=["1979", "1980", "1981", "1982"],
            correctAnswer=1,
            difficulty="medium",
            level=1,
            category="general"
        ),
    ]