# python-pipeline: Code for America model.earth Google Sheets->CSV generator
## What This Is
This project is a simple Python script that scrapes configured Google Sheets
docs using the Google Sheets API and writes the contents to CSV docs in this repo.
The script is run every 5 minutes or on code change by Github Actions.
## How You Can Use It
### Reading Data
All output CSV data is in `output/${sheet_name}.csv`. 
You can view the files in the [Github UI](https://github.com/modelearth/python-pipeline/blob/main/output/georgia_ev_automotive.csv)
or [raw](https://raw.githubusercontent.com/modelearth/python-pipeline/main/output/georgia_ev_automotive.csv)
depending on your needs.
### Adding New Sheets
Add a new entry to the YAML array in `app/config/sheets.yaml`. You will need Github
committer permissions in this repo to make that change.

Editing the file directly in the Github UI is the simplest way to make such a change,
but please note that YAML files are very sensitive to tabs and whitespace, so please
copy a previous entry and change the content to ensure proper formatting.

You can of course also make the changes via the `git` client.