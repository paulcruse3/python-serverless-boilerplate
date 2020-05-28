# zeconomy-translation
A backend written assessment

## Development

### Installation

1. `brew install pyenv`
1. `pyenv install 3.7`
1. `pyenv global system 3.7`
1. `vim ~/.pyenv/version` # (remove: the option `system` from this file)
1. `vim ~/.bashrc` # (or equivalent: ~/.bash_profile, ~/.zshrc, etc)
1. `eval "$(pyenv init -)"` # (add: to your profile)
1. `brew install pipenv`
1. `pipenv install`
1. `nvm install` OR `nvm use` if version already installed (please use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating))
1. `npm install`.
1. `sls dynamodb install`
1. `npm start`

### API Samples

Review `openapi.yml` for full documentation, but below is a sample post and get for your local:

POST: http://localhost:9000/zeconomy-translation/v1/spanish
```javascript
//body
{
    "english2": "dog",
    "spanish": "perro"
}
```

GET: http://localhost:9000/zeconomy-translation/v1/english?word=hello
```javascript
// response
{
    "translation": "hola"
}
```

### Unit Testing

To properly unit test you must be follow this steps:

1. `pipenv shell`
1. `npm test`

### @TODO

1. Consolidate endpoints to one file to be more DRY; don't need both an english and spanish files
1. Make translation direction as part of the request to all for extensibility
1. Modify data model to allow for multiple translations tied to one word (graph database, neptune, neo4j may be more appropriate engine)
1. Add unit test to mock db interactions
