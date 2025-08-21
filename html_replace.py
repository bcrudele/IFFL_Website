import os
import re
import json


def personalize_html_snippet(snippet: str, player_key: str) -> str:
    return snippet.replace("AidanN", player_key)

def html_replacer():
    with open("playerdata.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Map JSON keys to actual HTML filenames
    player_file_map = {
        "AidanN": "aidan_newett",
        "AnthonyW": "anthony_woodcock",
        "BrandonB": "brandon_bagneschi",
        "BrandonC": "brandon_crudele",
        "ChandlerR": "chandler_rogaskie",
        "CodyC": "cody_christensen",
        "ColinY": "colin_young",
        "DavidD": "david_delatorre",
        "DeanR": "dean_rizzo",
        "DylanG": "dylan_gunter",
        "GrahamH": "graham_holmes",
        "HunterS": "hunter_schiefelbein",
        "JacobW": "jacob_weber",
        "JamesL": "james_lundell",
        "JaredP": "jared_petrin",
        "JimmyD": "jimmy_doles",
        "JustinM": "justin_massillo",
        "KarlK": "karl_koleczek",
        "MikeyD": "mikey_duval",
        "RyanK": "ryan_konecki",
        "SamA": "sam_andrade",
        "SeanM": "sean_mau",
        "TeddyB": "teddy_bittman",
        "TommyL": "tommy_lykowski",
        "TonyM": "tony_mitchell",
        "TylerW": "tyler_wibbeler",
        "MattM": "matt_miedema"
    }

    script = '''
    <script>
        function initializeView() {
        document.getElementById('career-tile').style.display = 'block';
        document.getElementById('season-tile').style.display = 'block';
        document.getElementById('goalie-tile').style.display = 'none';
        document.getElementById('training-tile').style.display = 'none';
        document.getElementById('skater-stats').style.display = 'block';
        document.getElementById('goalie-stats').style.display = 'none';
        }

        function toggleTiles() {
        const career = document.getElementById('career-tile');
        const season = document.getElementById('season-tile');
        const goalie = document.getElementById('goalie-tile');
        const training = document.getElementById('training-tile');
        const skaterStats = document.getElementById('skater-stats');
        const goalieStats = document.getElementById('goalie-stats');
        const toggleBtn = document.getElementById('toggle-btn');

        const isSkaterMode = career.style.display !== 'none';

        career.style.display = isSkaterMode ? 'none' : 'block';
        season.style.display = isSkaterMode ? 'none' : 'block';
        goalie.style.display = isSkaterMode ? 'block' : 'none';
        training.style.display = isSkaterMode ? 'block' : 'none';

        skaterStats.style.display = isSkaterMode ? 'none' : 'block';
        goalieStats.style.display = isSkaterMode ? 'block' : 'none';

        toggleBtn.textContent = isSkaterMode ? 'Skater Mode' : 'Goalie Mode';
        }
    </script>
    '''

    for player_key, file_stub in player_file_map.items():
        html_path = f'pages/players/{file_stub}.html'

        # The exact <body> tag to match
        target_body_opening = r'<body\s+style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 40px; max-width: 900px; margin: auto; color: black;">'

        # ========== ACHIEVEMENT DIVS ==========
        career_scorer = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🎯 Career Scorer</h4>
        <p style="margin: 4px 0; color: #555;">25 career goals (<td id="AidanN_career_skater_G">8</td>/25)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 32%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        playmaker = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🧠 The Playmaker</h4>
        <p style="margin: 4px 0; color: #555;">15 career assists (<td id="AidanN_career_skater_A">12</td>/15)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 80%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        hat_trick = '''
        <div>
        <h4 style="margin: 0;">🎩 Hat Trick Hero</h4>
        <p style="margin: 4px 0; color: #555;">3 career hat tricks (<td id="AidanN_career_skater_HT">2</td>/3)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 66%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        # More achievement divs (e.g. duelist, big_apples, save_surge, etc.) can be defined similarly.
        duelist_2025 = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">⚔️ 2025 Duelist</h4>
        <p style="margin: 4px 0; color: #555;">Win 3 rival matchups (<td id="AidanN_2025_achievements_2025_DUELIST">0</td>/3)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        big_apples_2025 = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🍎 2025 Big Apples</h4>
        <p style="margin: 4px 0; color: #555;">Hit 10 assists (<td id="AidanN_2025_achievements_2025_BIGAPPLES">1</td>/10)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 10%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        hot_hand_2025 = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🔥 2025 Hot Hand</h4>
        <p style="margin: 4px 0; color: #555;">Points in 3 consecutive games (<td id="AidanN_2025_achievements_2025_HOTHAND">0</td>/3)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''
        brick_by_brick = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🧱 Brick by Brick</h4>
        <p style="margin: 4px 0; color: #555;">Make 30+ saves in a single game (<td id="AidanN_career_achievements_BRICKBYBRICK">0</td>/5)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 40%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        under_siege = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">⛑️ Under Siege</h4>
        <p style="margin: 4px 0; color: #555;">Face 500 shots (<td id="AidanN_career_goalie_SA">215</td>/500)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 43%; background: linear-gradient(90deg, #c0c0c0, #dcdcdc); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        wall_of_steel = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🛡️ Wall of Steel</h4>
        <p style="margin: 4px 0; color: #555;">Hold an opponent to 3 goals or fewer (<td id="AidanN_career_achievements_WALLOFSTEEL">0</td>/6)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #ffd700, #f9a602); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''
        training_duelist = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">⚔️ 2025 Duelist</h4>
        <p style="margin: 4px 0; color: #555;">Win 3 rival matchups (<td id="AidanN_2025_achievements_2025_DUELIST">0</td>/3)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        fortress = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🏰 2025 Fortress</h4>
        <p style="margin: 4px 0; color: #555;">0.800+ SV% in 3 games (<td id="AidanN_2025_achievements_2025_FORTRESS">0</td>/3)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        save_surge = '''
        <div style="margin-bottom: 20px;">
        <h4 style="margin: 0;">🌊 2025 Save Surge</h4>
        <p style="margin: 4px 0; color: #555;">Make 100 saves (<td id="AidanN_2025_achievements_2025_SAVESURGE">0</td>/100)</p>
        <div style="background: #eee; border-radius: 8px;">
            <div style="width: 1%; background: linear-gradient(90deg, #cd7f32, #b87333); height: 16px; border-radius: 8px;"></div>
        </div>
        </div>
        '''

        from generate_achievement import generate_achievement_html  
        # career_scorer      = personalize_html_snippet(career_scorer, player_key)
        # playmaker          = personalize_html_snippet(playmaker, player_key)
        # hat_trick          = personalize_html_snippet(hat_trick, player_key)
        # brick_by_brick     = personalize_html_snippet(brick_by_brick, player_key)
        # under_siege        = personalize_html_snippet(under_siege, player_key)
        # wall_of_steel      = personalize_html_snippet(wall_of_steel, player_key)

        career_scorer      = generate_achievement_html(player_key, "CAREERSCORER", data[player_key])
        playmaker          = generate_achievement_html(player_key, "PLAYMAKER", data[player_key])
        hat_trick          = generate_achievement_html(player_key, "HATTRICK", data[player_key])
        brick_by_brick     = generate_achievement_html(player_key, "BRICKBYBRICK", data[player_key])
        under_siege        = generate_achievement_html(player_key, "UNDERSIEGE", data[player_key])
        wall_of_steel      = generate_achievement_html(player_key, "WALLOFSTEEL", data[player_key])

        training_duelist = generate_achievement_html(player_key, "DUELIST", data[player_key])
        fortress = generate_achievement_html(player_key, "FORTRESS", data[player_key])
        save_surge = generate_achievement_html(player_key, "SAVESURGE", data[player_key])
        duelist_2025 = generate_achievement_html(player_key, "DUELIST", data[player_key])
        big_apples_2025 = generate_achievement_html(player_key, "BIGAPPLES", data[player_key])
        hot_hand_2025 = generate_achievement_html(player_key, "HOTHAND", data[player_key])


        # ========== BODY CONSTRUCTION ==========
        new_body_content = f'''
        <body
        style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 40px; max-width: 900px; margin: auto; color: black;">
        <div id="tile-container"
            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px;">

            <!-- CAREER TILE -->
            <div id="career-tile"
            style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; color: #e53935;">📈 Career</h3>
            {career_scorer}
            {playmaker}
            {hat_trick}
            <br>
            <button onclick="toggleTiles()"
                style="padding: 10px 20px; font-size: 16px; border-radius: 8px; background-color: #cfcfcf; color: rgb(0, 0, 0); border: none; cursor: pointer;">
                Goalie Mode
            </button>
            </div>

            <!-- SEASON TILE -->
            <div id="season-tile"
            style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; color: #8e24aa;">🚀 Season</h3>
            {duelist_2025}
            {big_apples_2025}
            {hot_hand_2025}
            </div>

            <!-- GOALIE TILE -->
            <div id="goalie-tile"
            style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; color: #1565c0;">🧤 Career</h3>
            {brick_by_brick}
            {under_siege}
            {wall_of_steel}
            <button onclick="toggleTiles()"
                style="padding: 10px 20px; font-size: 16px; border-radius: 8px; background-color: #cfcfcf; color: rgb(0, 0, 0); border: none; cursor: pointer;">
                Skater Mode
            </button>
            </div>

            <!-- TRAINING TILE -->
            <div id="training-tile"
            style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin-top: 0; color: #8e24aa;">🚀 Season</h3>
            {training_duelist}
            {fortress}
            {save_surge}
            </div>

        </div>
        </body>
        '''


        # ========== REPLACEMENT ==========
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            pattern = rf'{target_body_opening}[\s\S]*?</body>'
            match = re.search(pattern, content)

            if match:
                updated_content = content[:match.start()] + new_body_content.strip() + content[match.end():]
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                # print(content)
                print(f"Target <body> content successfully replaced in {html_path}.")
            else:
                print("❌Target <body> tag not found in the file.")
        else:
            print(f"❌File not found: {html_path}")
