import sqlite3

from typing import List
from pathlib import Path

class GeoPackage():
    def __init__(self, gpPath: Path) -> None:
        self.path = gpPath

        with sqlite3.connect(gpPath) as conn:
            cursor = conn.cursor()

            cursor.execute('''SELECT * FROM sqlite_master
                            WHERE name in ('gpkg_contents', 'gpkg_spatial_ref_sys')
                            ''')
            tables = cursor.fetchall()
            
            if tables == []:
                cursor.execute('''PRAGMA application_id = 1196444487
                                ''')
                cursor.execute('''PRAGMA user_version = 10200
                                ''')
                cursor.execute('''CREATE TABLE gpkg_contents (table_name TEXT NOT NULL PRIMARY KEY,
                                data_type TEXT NOT NULL,
                                identifier TEXT UNIQUE,
                                description TEXT DEFAULT '',
                                last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
                                min_x DOUBLE,
                                min_y DOUBLE,
                                max_x DOUBLE,
                                max_y DOUBLE,
                                srs_id INTEGER,
                                CONSTRAINT fk_gc_r_srs_id FOREIGN KEY (srs_id) REFERENCES gpkg_spatial_ref_sys(srs_id)
                                )''')
                cursor.execute('''CREATE TABLE gpkg_spatial_ref_sys ( 
                                srs_name TEXT NOT NULL, 
                                srs_id INTEGER NOT NULL PRIMARY KEY, 
                                organization TEXT NOT NULL, 
                                organization_coordsys_id INTEGER NOT NULL, 
                                definition  TEXT NOT NULL, 
                                description TEXT 
                                )''')
                cursor.execute('''INSERT INTO gpkg_spatial_ref_sys (
                                srs_name, srs_id, organization, organization_coordsys_id, definition)
                                VALUES ('Undefined cartesian SRS', -1, 'NONE', -1, 'undefined')
                                ''')
                cursor.execute('''INSERT INTO gpkg_spatial_ref_sys (
                                srs_name, srs_id, organization, organization_coordsys_id, definition)
                                VALUES ('Undefined geographic SRS', 0, 'NONE', 0, 'undefined')
                                ''')
                cursor.execute('''INSERT INTO gpkg_spatial_ref_sys (
                                srs_name, srs_id, organization, organization_coordsys_id, definition)
                                VALUES ('WGS 84 geodetic', 4326, 'EPSG', 4326, 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]')
                                ''')
                
    def get_content(self) -> List:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()

            cursor.execute('''SELECT * FROM gpkg_contents''')
            db_content = cursor.fetchall()
            return db_content
