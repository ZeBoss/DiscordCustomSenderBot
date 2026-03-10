use CustomSenderBotData;

drop table if exists userdata;

CREATE TABLE userdata (
user_id VARCHAR(255) PRIMARY KEY,
char_name VARCHAR(255),
char_pic VARCHAR(255)
);


INSERT INTO userdata (user_id,char_name, char_pic) VALUES ('123456789', 'John Doe', 'https://example.com/johndoe.jpg');