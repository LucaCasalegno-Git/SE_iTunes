from database.dao import DAO

soglia = 120
album = DAO.read_album(soglia)

print(album[0])

con = DAO.read_connesioni_album(soglia)
print(len(con))


