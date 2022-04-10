# notion-word-data

This is a python project to fetch a given word parts of speech, definitions, examples and synonyms using Google Dictionary, and automatically add it to a Notion database.


## Appendix

Notion limits the number of requests to 3 per second (see [Notion website](https://developers.notion.com/reference/request-limits) for more information).
Limits for property value sent to the Notion API (see [Notion website](https://developers.notion.com/reference/request-limits#limits-for-property-values) for more information):
| Property value type | Inner property | Size limit |
| - | - | - |
| [Rich text object](https://developers.notion.com/reference/rich-text) | `text.content` | 2000 characters |
| [Rich text object](https://developers.notion.com/reference/rich-text) | `text.link.url` | 1000 characters |
| [Rich text object](https://developers.notion.com/reference/rich-text) | `equation.expression` | 1000 characters |
| Any array of [rich text objects](https://developers.notion.com/reference/rich-text) | | 100 elements |
| Any URL | | 1000 characters |
| Any email | | 200 characters |
| Any phone number | | 200 characters |
| Any multi-select | | 100 options |
| Any relation | | 100 related pages |
| Any people | | 100 users |


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DATABASE_ID`
See [Notion website](https://developers.notion.com/docs/getting-started#step-1-create-an-integration) for more information.
1. Get the URL of your database of choice
2. Copy your database ID, which you can see in `https://www.notion.so/{workspace_name}/{database_id}?v={view_id}`

`TOKEN`
See [Notion website](https://developers.notion.com/docs/working-with-databases#adding-pages-to-a-database) for more information.
1. Create a Notion integration
2. Share your integration to your database of choice
3. Copy your "Internal Integration Token"


## Run Locally

Clone the project

```bash
  git clone https://github.com/MatthieuMezirard/notion-word-data.git
```

Go to the project directory

```bash
  cd notion-word-data
```

Install dependencies

```bash
  poetry install
```

Enter the words and their languages

```bash
  code WORDS.md
```

Run the main file

```bash
  python .\notion-word-data\app.py
```


## Running Tests

To run tests, run the following command

```bash
  poetry run pytest
```


## License

[MIT](https://choosealicense.com/licenses/mit/)