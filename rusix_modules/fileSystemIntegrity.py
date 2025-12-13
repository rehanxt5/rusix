import os
try:
    import rusix_modules.config_db 
except ImportError:
    import config_db
# check if rusix_modules exists and all files are present
def rusix_modules_integrity():
    # wherther folder exists or not
    if not os.path.exists("rusix_modules"):
        return False
    # list of required files
    required_files = [
        "config_db.py",
        "fileSystemIntegrity.py",
    ]
    # check for each file
    for file in required_files:
        if not os.path.exists(os.path.join("rusix_modules", file)):
            return False
    return True

#  checking frontend integrity
def frontend_integrity():
    if not os.path.exists("frontend"):
        return False
    required_files = [
        "index.html",
        "styles.css",
        "app.js",
    ]
    for file in required_files:
        if not os.path.exists(os.path.join("frontend", file)):
            return False
    return True

#  checking assets integrity
def assets_integrity():
    if not os.path.exists("frontend/assets"):
        return False
    if not os.path.exists("frontend/assets/icons"):
        return False
    required_icon_files = [
        "add-white.svg",
        "add.svg",
        "home-white.svg",
        "home.svg",
        "library-white.svg",
        "library.svg",
        "liked-songs.svg",
        "music-control-next-white.svg",
        "music-control-next.svg",
        "music-control-pause-white.svg",
        "music-control-pause.svg",
        "music-control-play-white.svg",
        "music-control-play.svg",
        "music-control-prev-white.svg",
        "music-control-prev.svg",
        "music-control-repeat-white.svg",
        "music-control-repeat.svg",
        "music-control-shuffle-white.svg",
        "music-control-shuffle.svg",
        "search-white.svg",
        "search.svg",
        "temp-thumbnail.svg",
    ]
    for file in required_icon_files:
        if not os.path.exists(os.path.join("frontend/assets/icons", file)):
            return False
    return True
# User data integrity check
def user_data_integrity():
    if not os.path.exists("userData"):
        os.makedirs("userData")
    if not os.path.exists("userData/audio"):
        os.makedirs("userData/audio")
    if not os.path.exists("userData/thumbnails"):
        os.makedirs("userData/thumbnails")
    if not os.path.exists("userData/config.db"):
        config_db.create_config_db()

    