<div align="center">


  # ably_backend

</div>

에이블리 주니어 백엔드 사전 과제

<br><br>

## 목차

- [개발 기간](#--개발-기간--)  
- [프로젝트 설명 및 분석](#-프로젝트)
- [API 사용법](#API) 
  <br><br>

<h2> ⌛ 개발 기간  </h2> 

 2022/09/03  ~ 2022/09/07
 <br><br>
  </div> 


# 💻 프로젝트

  ### 프로젝트 설명 및 분석

  - 회원 가입 및 비밀번호 재설정이 가능한 API 개발

    - 전화 번호 인증

      - 전화번호 인증을 통해 4자리 인증 코드를 받는다. (유효 시간: 180초)
      - 전화번호는 010 + 8자리 숫자만 가능 (예: 01012345678)
      - 새로 발급 요청을 하면 새로운 인증 코드를 발급 받는다.
      - redis로 인증 코드 관리 {"phone_number": " auth_code"}

    - 회원가입

      - 이메일 (이메일 형식인지 유효성 확인, 중복 불가)
      - 닉네임 (중복 불가)
      - 비밀번호 (8자리 이상, 소문자 1개 이상, 숫자 1개 이상 조합으로 유효성 확인)
      - 이름
      - 전화번호 (010 + 8자리 숫자인지 유효성 확인, 중복 불가)
      - 전화번호 인증 필수. 인증 코드 유효성을 확인해 일치하지 않으면 회원 가입 불가

    - 로그인

      - 식별 가능한 모든 정보로 로그인 가능
      - ModelBackend을 사용해 이메일/닉네임/전화번호로 로그인 가능 (로그아웃 필수)

    - 로그아웃

    - 내 정보 보기

      - LoginRequiredMixin을 사용해 로그인을 해야 내 정보를 볼 수 있다.

    - 비밀번호 변경

      - 전화번호 인증 필수. 인증 코드 유효성을 확인해 일치하지 않으면 비밀 번호 변경 불가

      

- 테스트 코드 작성 (12개)

  - Test Data Setup (슈퍼 유저, 유저, 로그인 context)
  - 관리자 계정 생성
  - 일반 계정 생성
  - 전화번호 인증 / error (잘못된 전화번호로 요청)
  - 회원 가입 / error (인증 코드 없이 요청)
  - 일반 계정 로그인 / error (비밀번호 틀림)
  - 내 정보 보기 / error (로그인을 하지 않고 요청)
  - 비밀번호 변경 / error (인증 코드 없이 요청)

<br>

  ### 실행 방법

```
#AWS EC2 배포
http://3.39.69.117/swagger/

#로컬에서 실행하기
cd ably_backend
docker-compose up
http://{ip-address}/swagger/
```

<br>

### 아키텍처 다이어그램

<img src="https://user-images.githubusercontent.com/44389424/188778792-365babf4-2308-4ca4-b1e4-9a70f261368a.png"/>

<br>
<br>

### ERD

- tb_user: 회원 정보



<img src="https://user-images.githubusercontent.com/44389424/188778795-8cb41f2e-de6a-493a-bd38-a6dfa231f9be.JPG"/>

<br>
<br>

## API

API 사용법을 안내합니다.

<br>

  ### API 명세서

| METHOD | URI                                         | 기능                |
| ------ | ------------------------------------------- | ------------------- |
| POST   | /api/v1/auth/                               | 전화 번호 인증      |
| POST   | /api/v1/register/                           | 회원 가입           |
| POST   | /api/v1/login/                              | 로그인              |
| GET    | /api/v1/logout/                             | 로그아웃            |
| GET    | /api/v1/user/<int: user_id>/                | 유저 정보 상세 조회 |
| POST   | /api/v1/user/<int: user_id>/change-password | 비밀 번호 변경      |

<br>

### 전화번호 인증

전화번호 인증을 통해 인증 코드를 발급받고 인증 제한 시간은 180초입니다. 전화번호를  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/v1/auth/ HTTP/1.1
Host: 127.0.0.1:8000
```



##### Parameter

| Name         | Type     | Description            | Required |
| :----------- | :------- | :--------------------- | :------- |
| phone_number | `String` | 전화 번호, 01012345678 | O        |



#### Response

| Name      | Type     | Description                |
| :-------- | :------- | :------------------------- |
| 인증 코드 | `String` | 인증 코드, 제한 시간 180초 |



#### Result

##### Response:성공

```json
{
    "인증 코드": "1234"
}
```

##### Response:실패

```json
{
    "msg": "유효하지 않은 휴대전화 번호입니다."
}
```

<br>

### 회원가입 

회원가입을 합니다. 이메일, 패스워드, 유저네임, 이름, 전화번호를 `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/v1/register/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter

| Name         | Type     | Description                            | Required |
| :----------- | :------- | :------------------------------------- | :------- |
| email        | `String` | 이메일                                 | O        |
| user_name    | `String` | 유저 네임                              | O        |
| password     | `String` | 패스워드, 소문자, 숫자 포함 8자리 이상 | O        |
| name         | `String` | 이름                                   | O        |
| phone_number | `String` | 전화번호                               | O        |
| my_auth_code | `String` | 인증 코드                              | O        |




#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
  "message": "회원가입이 완료되었습니다."
}
```

##### Response:실패

```json
{
  "message": "회원가입을 실패했습니다."
}
```

<br>

### 로그인 

로그인을 합니다. 이메일 / 유저네임 / 전화번호와 password를  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/v1/login/ HTTP/1.1
Host: 127.0.0.1:8000
```



##### Parameter

| Name      | Type     | Description                                | Required |
| :-------- | :------- | :----------------------------------------- | :------- |
| user_name | `String` | 이메일 / 유저네임 / 전화번호로 로그인 가능 | O        |
| password  | `String` | 패스워드                                   | O        |



#### Response

| Name   | Type     | Description |
| :----- | :------- | :---------- |
| result | `String` | 결과 메세지 |

#### Result

##### Response:성공

```json
{
    "msg": "user_name님이 로그인하셨습니다."
}
```

##### Response:실패

```json
{
    "msg": "아이디 또는 비밀번호를 확인해주세요."
}
```

<br>

### 로그아웃

로그아웃을 합니다. 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다.



#### Request

##### URL

```http
GET /api/v1/logout/ HTTP/1.1
Host: 127.0.0.1:8000
```



#### Response

| Name   | Type     | Description |
| :----- | :------- | :---------- |
| result | `String` | 결과 메세지 |

#### Result

##### Response:성공

```json
{
    "msg": "로그아웃했습니다"
}
```

<br>

### 유저 상세 정보 조회

로그인이 되어 있는 상태에서 유저 상세 정보를 조회합니다. user_id를  `GET`으로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
GET /api/v1/user/<int:user_id>/ HTTP/1.1
Host: 127.0.0.1:8000
```



##### Parameter:path

| Name    | Type     | Description | Required |
| :------ | :------- | :---------- | :------- |
| user_id | `String` | 유저 id:pk  | O        |



#### Response

| Name   | Type     | Description |
| :----- | :------- | :---------- |
| result | `String` | 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "id": 1, 
    "email": "test@ably.com", 
    "user_name": "test", 
    "name": "test", 
    "phone_number": "01087654321"
}
```

##### Response:실패

```json
{
    "msg": "Error: Not Found"
}
```

<br>

### 비밀 번호 변경

전화번호 인증을 통해 인증 코드를 발급받습니다. 변경할 비밀번호, 전화번호, 인증 코드를  `POST`로 요청하고, 성공 시 응답 바디에 `JSON` 객체로 성공 메세지를 받습니다. 실패 시 에러 코드를  받습니다.



#### Request

##### URL

```http
POST /api/v1/user/<int:user_id>/change-password/ HTTP/1.1
Host: 127.0.0.1:8000
```

##### Parameter:path

| Name    | Type     | Description | Required |
| :------ | :------- | :---------- | :------- |
| user_id | `String` | 유저 id:pk  | O        |

##### Parameter

| Name         | Type     | Description     | Required |
| :----------- | :------- | :-------------- | :------- |
| password     | `String` | 변경할 비밀번호 | O        |
| phone_number | `String` | 전화번호        | O        |
| my_auth_code | `String` | 인증 코드       | O        |



#### Response

| Name   | Type     | Description      |
| :----- | :------- | :--------------- |
| result | `String` | 등록 결과 메세지 |



#### Result

##### Response:성공

```json
{
    "msg": "{user.email}님의 비밀번호를 변경했습니다."
}
```

##### Response:실패

```json
{
    "msg": "전화번호 인증이 필수입니다.",
}
```

<br>
