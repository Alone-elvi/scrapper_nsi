"""
SQL tables definition
"""

BIO_ACTIVE_TABLE = "bio_active"


CREATE_STATUS_TABLE = """
    CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT
    );
"""

CREATE_MANUFACTURER_TABLE = """
    CREATE TABLE IF NOT EXISTS manufacturer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL, -- Make title required
    address TEXT, -- Optional
    inn TEXT, -- Optional
    ogrn TEXT, -- Optional
    phone TEXT, -- Optional
    email TEXT, -- Optional
    site TEXT, -- Optional
    director TEXT, -- Optional
    manager TEXT, -- Optional
    okpo TEXT, -- Optional
    okved TEXT, -- Optional
    okfs TEXT, -- Optional
    okopf TEXT, -- Optional
    okato TEXT, -- Optional
    oktmo TEXT -- Optional
);
"""


INSERT_MANUFACTURER_TABLE = """
    INSERT OR IGNORE 
    INTO manufacturer (
        title, 
        address, 
        inn, 
        ogrn, 
        phone, 
        email, 
        site, 
        director, 
        manager, 
        okpo, 
        okved, 
        okfs, 
        okopf, 
        okato, 
        oktmo
        );
    """

FILL_STATUS_TABLE = """
INSERT OR IGNORE INTO status (title) 
VALUES 
    ('подписан и действует'), 
    ('приостановлен'), 
    ('аннулирован / отозван'), 
    ('удален из-за технической ошибки при оформлении'), 
    ('удален в связи с переоформлением');
"""

