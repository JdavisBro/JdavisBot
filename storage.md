# Storage

> storage.create( fileName )

| Args           |Default/Required| Type           | Description    |
|----------------|----------------|----------------|----------------|
| fileName       | Required       | String         |The filename to save|
| write          | "{}"           |JSON Seralizable|The variable to json.dump in the file| 
| path           | "settings/"    | String         |The path from root folder to file|

> storage.exists( fileName )

| Args           |Default/Required| Type           | Description    |
|----------------|----------------|----------------|----------------|
| fileName       | Required       | String         |The filename to check|
| path           | "settings/"    | String         |The path from root folder to file|

> storage.read( fileName )

| Args           |Default/Required| Type           | Description     | 
|----------------|----------------|----------------|----------------|
| fileName       | Required       | String         |The filename to read|
| path           | "settings/"    | String         |The path from root folder to file|
| key            | None           | List of String |List of keys to go down in a dictionary|
| default        | None           | Any            |The value to be returned if key cannot be found.|

> storage.write( fileName , write )

| Args           |Default/Required| Type           | Description     | 
|----------------|----------------|----------------|----------------|
| fileName       | Required       | String         |The filename to write|
| write          | Required       |JSON Seralizable|The variable to json.dump to the file|
| path           | "settings/"    | String         |The path from root folder to file|
| key            | None           | String         |Keys to go down in a dictionary|