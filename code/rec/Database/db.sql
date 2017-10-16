create database cloudcompiler;


CREATE TABLE users(
	email VARCHAR(100) UNIQUE KEY NOT NULL,
    username VARCHAR(15) PRIMARY KEY,
    password VARCHAR(20) NOT NULL,
    isEmailVerified VARCHAR(1) NOT NULL DEFAULT 0,
    isAccountActive VARCHAR(1) NOT NULL DEFAULT 1,
    dateCreated TIMESTAMP NOT NULL DEFAULT NOW(),
    activation_key VARCHAR(64) NOT NULL
);

CREATE TABLE forgotPassword(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(100) NOT NULL,
    password_key VARCHAR(64) NOT NULL,
    timeRequested TIMESTAMP NOT NULL DEFAULT NOW(),
    isLinkActive VARCHAR(1) NOT NULL DEFAULT 1,
    timeChanged TIMESTAMP,
    isPasswordChanged VARCHAR(1) NOT NULL DEFAULT 0,
    
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO users (email,username,password) VALUES('harshmehta87.1997.hm@gmail.com','hgmehta','12345');
SELECT * FROM users;
SELECT * FROM forgotPassword;
DELETE FROM `cloudcompiler`.`users` WHERE `username`='harshmehta';

-- UPDATE forgotPassword SET isLinkActive = '0', isPasswordChanged = '1', timeChanged = '2017-10-07 17:49:41.312178' WHERE email = 'harsh_m@hotmail.com' AND password_key = '7ad05a93993e860da600d797e627e833155b3219af223e7a346eeeb738fcfc23';