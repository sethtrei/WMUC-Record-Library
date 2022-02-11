import discogs_client
import csv

token = ""
with open('token.txt') as f:
    token = f.readlines()
token = token[0]
print(token)
d = discogs_client.Client('WMUC.Library.Manager/0.1',
                          user_token=token)
me = d.identity()
print(me)

headings = ['Title', 'Artists', 'Location']
info = []
for item in me.collection_folders:
    if ("Record Library" in item.name):
        for entry in item.releases:
            if(entry.notes != None):
                add = False
                for note in entry.notes:
                    if ((note["field_id"] == 3 or note["field_id"] == 4) and note["value"] != ""):
                        add = True
                if (add):

                    artists = ""
                    for artist in entry.release.artists:
                        artists = artists + ", " + artist.name
                    artists = artists[2:]
                    artists = artists.strip()
                    loc = ""
                    for note in entry.notes:
                        if (note["field_id"] == 3 or note["field_id"] == 4):
                            loc = note["value"] + " " + loc
                    loc = loc.strip()
                    info.append(
                        {"Title": entry.release.title, "Artists": artists, "Location": loc})


print("Done!")

with open('data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headings)
    writer.writeheader()
    writer.writerows(info)
