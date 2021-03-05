import csv
import git
import json

def iterate_file_versions(repo_path, filepath, ref='master'):
  repo = git.Repo(repo_path, odbt=git.GitDB)
  commits = list(repo.iter_commits(ref, paths=filepath))
  for commit in commits:
    blob = [b for b in commit.tree.blobs if b.name == filepath][0]
    yield commit.committed_datetime, commit.hexsha, blob.data_stream.read()

def write_csv(): 
  with open('cities.csv', 'w', newline='') as csvfile:
    city_data = ['geo_id', 'city', 'population', 'cases']
    fieldnames = city_data + ['date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    it = iterate_file_versions(".", "cases_by_city.json", 'master')
    for i, (when, hash, data) in enumerate(it):
      cities = json.loads(data)
      for city in cities:
        filtered_city = {k: city[k] for k in city_data}
        filtered_city['date'] = when
        writer.writerow(filtered_city)

