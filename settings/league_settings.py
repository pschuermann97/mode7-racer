# Settings for the leagues that are playable in the game.

from race import Race
from league import League

from settings.track_settings import TrackCreator, STD_REQUIRED_LAPS

# ------------- creation of the different leagues in the game --------------------------

LEAGUE_1_RACES = [
    Race(
        race_track_creator = TrackCreator.create_track_2023,
        floor_tex_path = "gfx/event_horizon_track1.png",
        bg_tex_path = "gfx/event_horizon_bg.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time-attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = False
    ),
    Race(
        race_track_creator = TrackCreator.create_track_2023,
        floor_tex_path = "gfx/track_2023.png",
        bg_tex_path = "gfx/track_2023_bg_resized.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time-attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = True
    ),
    Race(
        race_track_creator = TrackCreator.create_track_2023_II,
        floor_tex_path = "gfx/track_2023_II.png",
        bg_tex_path = "gfx/track_2023_bg_resized.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time-attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = True
    ),
    Race(
        race_track_creator = TrackCreator.create_event_horizon_track2,
        floor_tex_path = "gfx/event_horizon_track2.png",
        bg_tex_path = "gfx/event_horizon_bg.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time_attack",
        init_player_pos_x = 26.26,
        init_player_pos_y = -98.86,
        init_player_angle = -111.565,
        is_foggy = False
    ),
    Race(
        race_track_creator = TrackCreator.create_monochrome_track,
        floor_tex_path = "gfx/monochrome_track.png",
        bg_tex_path = "gfx/monochrome_track_bg.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time_attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = True
    ),
    Race(
        race_track_creator = TrackCreator.create_track_2023,
        floor_tex_path = "gfx/track_2023_snow.png",
        bg_tex_path = "gfx/track_2023_snow_bg.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time-attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = False
    ),
    Race(
        race_track_creator = TrackCreator.create_monochrome_track,
        floor_tex_path = "gfx/black_hole_track1.png",
        bg_tex_path = "gfx/black_hole_track_bg.png",
        required_laps = STD_REQUIRED_LAPS,
        race_mode = "time_attack",
        init_player_pos_x = 25.55,
        init_player_pos_y = -119.78,
        init_player_angle = -111.565,
        is_foggy = False
    )
]
LEAGUE_1 = League(LEAGUE_1_RACES)

# special league that is not meant to be played 
# but serves as the track list to select from in single race
SINGLE_MODE_RACES = LEAGUE_1_RACES 

# ---------------------------- end of league creation --------------------------

LEAGUES = [LEAGUE_1]