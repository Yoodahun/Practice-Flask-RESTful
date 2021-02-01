# Practice-Flask-RESTful

API Test framework의 설계 및 구현 연습을 위해 파이썬으로 만든 간단한 RESTful API 이며, 아래 강의를 보며 작성하였습니다.

https://www.udemy.com/course/rest-api-flask-and-python/

----

**URI** : https://practice-flask-restful-dh.herokuapp.com/

모든 request의 `Content-Type` 은 `application/json` 입니다.

----

## User

### POST `/register`

User 등록을 진행합니다.

**Request Body**

| KEY      | TYPE | DESCRIPTION | REMARKS  |      |
| -------- | ---- | ----------- | -------- | ---- |
| username | str  | 유저 이름   | required |      |
| Password | str  | 비밀번호    | required |      |
|          |      |             |          |      |

**Response Body**

| STATUS_CODE | KEY      | TYPE | VALUE                                     | DESCRIPTION   |
| ----------- | -------- | ---- | ----------------------------------------- | ------------- |
| 201         | message  | str  | User created successfully                 |               |
| 400         | message  | str  | A User with that useranme already exists. | username 중복 |
| 400         | message  | key  | username / password                       |               |
|             | username | str  | This field cannot be let blank.           | username 공란 |
|             | password | str  | This field cannot be let blank.           | password 공란 |

### POST `/login`

`/login` 에서 사용하는 정보는, 반드시 `/register` 를 통해 등록되어있어야 합니다.

**Request Body**

| KEY      | TYPE | DESCRIPTION | REMARKS  |
| -------- | ---- | ----------- | -------- |
| username | str  | 유저 이름   | required |
| password | str  | 비밀번호    | required |
|          |      |             |          |

**Response Body**

| STATUS_CODE | KEY           | TYPE | VALUE                                  | DESCRIPTION               |
| ----------- | ------------- | ---- | -------------------------------------- | ------------------------- |
| 200         | access_token  | str  | Access token that allows use end-point |                           |
|             | refresh_token | str  | refresh token                          |                           |
| 401         | message       | str  | Invalid credentials                    | 존재하지 않는 유저 데이터 |

또한 Authorization과 관련한 reponse들은 아래와 같습니다.

| STATUS_CODE | KEY         | TYPE | VALUE                                     | DESCRIPTION                         |
| ----------- | ----------- | ---- | ----------------------------------------- | ----------------------------------- |
| 401         | description | str  | The token has expired                     | 시간초과된 토큰을 전송했을 때.      |
|             | error       | str  | token_expired                             |                                     |
| 401         | description | str  | Request does not contain an access token. | JWT 토큰을 전송하지 않았을때.       |
|             | error       | str  | authorization_required                    |                                     |
| 401         | description | str  | Signature verificaation failed.           | 잘못된 토큰이 전송되었을 때.        |
|             | error       | str  | Invalid_token                             |                                     |
| 401         | description | str  | The token has been revoked                | JWT 토큰이나, 로그인된 적이 없을때. |
|             | error       | str  | Token_revoked                             |                                     |

### POST `/logout`

`/logout` 은 login이 되어있는 상태여야합니다.

`--header 'Authorization: Bearer {access_token}'`

**Response Body**

| STATUS_CODE | KEY     | TYPE | VALUE                   | DESCRIPTION               |
| ----------- | ------- | ---- | ----------------------- | ------------------------- |
| 200         | message | str  | Successfully logged out |                           |
| 401         |         |      |                         | Authorization comon error |

### POST `/refresh`

시간경과가 거의 다 된 토큰을 갱신합니다.

`--header 'Authorization: Bearer {access_token}'`

**Response Body**

| STATUS_CODE | KEY          | TYPE | VALUE        | DESCRIPTION               |
| ----------- | ------------ | ---- | ------------ | ------------------------- |
| 200         | access_token | str  | ACCESS_TOKEN |                           |
| 401         |              |      |              | Authorization comon error |

### GET `/user/{user_id}`

user데이터를 조회합니다.

**Path parameter**

- user_id : User의 id값

**Response Body**

| STATUS_CODE | KEY      | TYPE    | VALUE           | DESCRIPTION                                   |
| ----------- | -------- | ------- | --------------- | --------------------------------------------- |
| 200         | id       | Integer |                 | 유저의 고유 아이디                            |
|             | username | str     |                 | 유저의 이름                                   |
| 404         | message  | str     | User not found. | 해당 아이디값을 가진 유저가 존재하지 않을 때. |



### DELETE  `/user/{user_id}`

user데이터를 삭제합니다.

**Path parameter**

- user_id : User의 id값

**Response Body**

| STATUS_CODE | KEY     | TYPE | VALUE                      | DESCRIPTION                                   |
| ----------- | ------- | ---- | -------------------------- | --------------------------------------------- |
| 200         | message | str  | User deleted successfully. | 해당 유저 삭제에 성공하였을 때.               |
| 404         | message | str  | User not found.            | 해당 아이디값을 가진 유저가 존재하지 않을 때. |



## Store

상점 리스트와 각각의 상점들에 대한 정보를 제공합니다.

### GET `/stores`

모든 store와 store에 종속되어있는 item들을 조회합니다.

**Response Body**

| STATUS_CODE | KEY    | TYPE  | VALUE | DESCRIPTION    | REMARKS |
| ----------- | ------ | ----- | ----- | -------------- | ------- |
| 200         | stores | array |       | Array of store |         |
|             | items  | array |       | Array of item  |         |

### GET `/store/{store_name}`

하나의 store를 조회합니다.

**Response Body**

| STATUS_CODE | KEY     | TYPE    | VALUE           | DESCRIPTION                            |
| ----------- | ------- | ------- | --------------- | -------------------------------------- |
| 200         | id      | Integer |                 | item id                                |
|             | name    | str     |                 | item name                              |
|             | items   | array   |                 | Array of item                          |
| 404         | message | str     | Store not found | store_name으로 등록된 store가 없을 때. |

### POST `/store/{store_name}`

store를 등록합니다.

**Response Body**

| STATUS_CODE | KEY      | TYPE    | VALUE                                          | DESCRIPTION                                              |
| ----------- | -------- | ------- | ---------------------------------------------- | -------------------------------------------------------- |
| 201         | id       | Integer |                                                | item id                                                  |
|             | name     | str     |                                                | item name                                                |
|             | items    | array   |                                                | Array of item                                            |
| 400         | message  | str     | A Store with name {store_name} already exists. | store_name으로 이미 등록되어있는 store 데이터가 있을 때. |
| 500         | messsage | str     | An error occurred while creating the store     | DB 저장 중 issue가 있을 때.                              |

### DELETE `/store/{store_name}`

store를 삭제하였을 시, 해당 store_id를 가지고 있는 item들도 같이 삭제됩니다.

**Response Body**

| STATUS_CODE | KEY     | TYPE | VALUE                             | DESCRIPTION                                           |
| ----------- | ------- | ---- | --------------------------------- | ----------------------------------------------------- |
| 200         | message | str  | Store deleted.                    | 삭제에 성공하였을 때.                                 |
| 400         | message | str  | Store {store_name} is not exists. | store_name의 아이템이 존재하지 않아 삭제에 실패할 때. |


## Item

각각의 item이나 item 전체에 대한 정보를 제공합니다.

### GET `/items`

로그인했을 떄와 하지 않았을 때의 response가 다릅니다.

**Response Body**

if JWT token has sent

| STATUS_CODE | KEY   | TYPE  | VALUE | DESCRIPTION    |
| ----------- | ----- | ----- | ----- | -------------- |
| 200         | items | Array |       | Array of items |

if JWT token has not sent

| STATUS_CODE | KEY     | TYPE            | VALUE                             | DESCRIPTION                |
| ----------- | ------- | --------------- | --------------------------------- | -------------------------- |
| 200         | items   | Array of string |                                   | Array of item name         |
|             | message | str             | More data available if you log-in |                            |
| 401         |         |                 |                                   | Authorization common error |

### DELETE `/items`

데이터베이스의 모든 아이템들을 삭제합니다.

**Response Body**

| STATUS_CODE | KEY     | TYPE | VALUE                             | DESCRIPTION |
| ----------- | ------- | ---- | --------------------------------- | ----------- |
| 200         | message | str  | all item is successfully deleted. |             |

### GET `/item/{item_name}`

`/item/{item_name}` 은 login이 되어있는 상태여야합니다.

`--header 'Authorization: Bearer {access_token}'`

**Response Body**

| STATUS_CODE | KEY      | TYPE    | VALUE           | DESCRIPTION |
| ----------- | -------- | ------- | --------------- | ----------- |
| 200         | id       | Integer |                 | item id     |
|             | name     | str     |                 | item name   |
|             | price    | Float   |                 | item price  |
|             | store_id | Integer |                 | store id    |
| 404         | message  | str     | Item not found. |             |

### POST `/item/{item_name}`

`/item/{item_name}` 은 login이 되어있는 상태여야합니다.

`--header 'Authorization: Bearer {access_token}'`

**Request Body**

| KEY      | TYPE  | DESCRIPTION | REMARKS  |
| -------- | ----- | ----------- | -------- |
| price    | float | item price  | required |
| store_id | str   | store id    | required |

**Response Body**

| STATUS_CODE | KEY      | TYPE    | VALUE                                             | DESCRIPTION                                      |
| ----------- | -------- | ------- | ------------------------------------------------- | ------------------------------------------------ |
| 201         | id       | Integer |                                                   | item id                                          |
|             | name     | str     |                                                   | item name                                        |
|             | price    | Float   |                                                   | item price                                       |
|             | store_id | Integer |                                                   | store id                                         |
| 400         | message  | str     | An item with {item_name} already exists.          | 같은 이름을 가진 아이템이 이미 존재하고 있을 때. |
| 400         | message  | str     | There is no Store. You should be add store first. | store id가 DB에 존재하지 않을 때.                |
| 400         | message  | str     | An error occurred inserting the item              | item data를 DB에 저장 중 issue가 발생했을 때.    |
| 400         | message  | key     | price / store_id                                  |                                                  |
|             | price    | str     | This field cannot be let blank                    |                                                  |
|             | store_id | str     | Every item needs a store id.                      |                                                  |



### PUT `/item/{item_name}`

**Request Body**

| KEY      | TYPE  | DESCRIPTION | REMARKS  |
| -------- | ----- | ----------- | -------- |
| price    | float | item price  | required |
| store_id | str   | store id    | required |

**Response Body**

| STATUS_CODE | KEY      | TYPE    | VALUE | DESCRIPTION |
| ----------- | -------- | ------- | ----- | ----------- |
| 201         | id       | Integer |       | item id     |
|             | name     | str     |       | item name   |
|             | price    | Float   |       | item price  |
|             | store_id | Integer |       | store id    |



### DELETE `/item/{item_name}`

`/item/{item_name}` 은 login이 되어있는 상태여야합니다.

`--header 'Authorization: Bearer {access_token}'`

user_id가 1번이어야 합니다.

**Response Body**

| STATUS_CODE | KEY     | TYPE | VALUE                    | DESCRIPTION                                                  |
| ----------- | ------- | ---- | ------------------------ | ------------------------------------------------------------ |
| 200         | message | str  | Item deleted.            |                                                              |
| 401         | message | str  | Admin privilege required | 로그인 되어있는 user의 user_id가 1번이 아닐 때.              |
| 404         | message | str  | Item no found.           | 삭제하고자 하는 아이템을 데이터베이스에서 찾을 수 없었을 때. |



















