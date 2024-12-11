docker pull mysql:8.0
docker run --name mysql -e MYSQL_ROOT_PASSWORD=123456 -e MYSQL_DATABASE=users_db -d mysql:8.0
docker exec -it mysql mysql -uroot -p123456 -e "

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    favorite_color VARCHAR(50),
    password_hash VARCHAR(255)
);


CREATE TABLE post (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(80) NOT NULL,
    content TEXT NOT NULL,
    author VARCHAR(255) NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    slug VARCHAR(255)
);
"