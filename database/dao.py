from database.DB_connect import DBConnect
from model.album import Album


class DAO:
    @staticmethod
    def read_album(soglia):
        conn = DBConnect.get_connection()
        album = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, a.artist_id, sum(t.milliseconds/60000) as durata 
                    from album a, track t
                    where a.id = t.album_id 
                    group by a.id, a.title 
                    having durata >= %s """

        cursor.execute(query, (soglia,))

        for row in cursor:
            album.append(Album(**row))

        cursor.close()
        conn.close()
        return album

    @staticmethod
    def read_connesioni_album(soglia):

        conn = DBConnect.get_connection()
        connessioni = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct t.album_id as album1 , t1.album_id as album2
                    from playlist_track pt, playlist_track pt1, track t, track t1
                    where pt.playlist_id = pt1.playlist_id 
                    and t.album_id < t1.album_id 
                    and t.id = pt.track_id 
                    and t1.id= pt1.track_id	
                    and t.album_id != t1.album_id
                    and t.album_id in (select a.id
                                        from album a, track t2
                                        where a.id = t2.album_id
                                        group by a.id
                                        having sum(t2.milliseconds/60000) >= %s)
                    and t1.album_id in  (select a1.id
                                        from album a1, track t3
                                        where a1.id = t3.album_id
                                        group by a1.id
                                        having sum(t3.milliseconds/60000) >= %s)"""

        cursor.execute(query, (soglia,soglia))

        for row in cursor:
            connessioni.append((row['album1'], row['album2']))

        cursor.close()
        conn.close()
        return connessioni

